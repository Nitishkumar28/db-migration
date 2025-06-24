import time
from datetime import datetime
from core.db.db_utils import (
    get_table_names,
    run_query,
    get_indexes_info,
    get_primary_keys,
    get_foreign_keys,
    get_triggers_for_table
)
from sqlalchemy.engine import CursorResult

_last_export_metrics = []


def get_table_count(table_results):
    try:
        if isinstance(table_results, CursorResult):
            val = table_results.scalar()
            return int(val) if val is not None else 0
    except Exception:
        pass

    try:
        table_rows = list(table_results) if table_results is not None else []
        if not table_rows:
            return 0
        first_row = table_rows[0]
        if isinstance(first_row, (tuple, list)):
            return int(first_row[0])
        if hasattr(first_row, 'get'):
            return int(first_row.get('cnt', first_row.get(0, 0)) or 0)
    except Exception:
        pass

    return 0


def collect_source_stats(source):
    tables = get_table_names(source['db_type'], source['db_name'])
    metrics = []
    for sno, table in enumerate(tables, start=1):
        src_count = get_table_count(
            run_query(f"SELECT COUNT(*) AS cnt FROM {table};", source['db_type'], source['db_name'])
        )
        indexes = get_indexes_info(source['db_type'], source['db_name'], table)
        index_count = len(indexes or [])
        pk_info = get_primary_keys(source['db_type'], source['db_name'], table) or {}
        pk_cols = pk_info.get('constrained_columns', [])
        fk_count = len(get_foreign_keys(source['db_type'], source['db_name'], table))
        triggers = get_triggers_for_table(source['db_type'], source['db_name'], table)
        trigger_count = len(triggers)
        metrics.append({
            'sno': sno,
            'table_name': table,
            'source_rows': src_count,
            'index_count': index_count,
            'primary_key_count': len(pk_cols),
            'foreign_key_count': fk_count,
            'trigger_count': trigger_count
        })
    return metrics



def collect_target_stats(source, target):
    tables = get_table_names(source['db_type'], source['db_name'])
    metrics = []
    for sno, table in enumerate(tables, start=1):
        targ_count = get_table_count(
            run_query(f"SELECT COUNT(*) AS cnt FROM {table};", target['db_type'], target['db_name'])
        )
        indexes = get_indexes_info(target['db_type'], target['db_name'], table)
        index_count = len(indexes or [])
        pk_info = get_primary_keys(target['db_type'], target['db_name'], table) or {}
        pk_cols = pk_info.get('constrained_columns', [])
        fk_list = get_foreign_keys(target['db_type'], target['db_name'], table)
        fk_names = [fk.get('name') for fk in (fk_list or [])]
        foreign_key_count = len(fk_names)
        triggers = get_triggers_for_table(target['db_type'], target['db_name'], table)
        trigger_count = len(triggers or [])
        metrics.append({
            'sno': sno,
            'table_name': table,
            'target_rows': targ_count,
            'index_count': index_count,
            'primary_key_count': len(pk_cols),
            'foreign_key_count': foreign_key_count,
            'trigger_count': trigger_count
        })
    return metrics


def collect_export_durations(durations):
    timestamp = datetime.utcnow().isoformat()
    metrics = []
    for sno, (table, dur) in enumerate(durations.items(), start=1):
        metrics.append({
            'sno': sno,
            'table_name': table,
            'time_taken_seconds': dur,
            'timestamp': timestamp
        })
    return metrics


def collect_combined_stats(source, target):
    source_stats = collect_source_stats(source)
    target_stats = collect_target_stats(source, target)
    combined = []
    for src, targ in zip(source_stats, target_stats):
        combined.append({
            'sno': src['sno'],
            'table_name': src['table_name'],
            'source_rows': src['source_rows'],
            'target_rows': targ.get('target_rows', 0),
            'index_count': f"{src.get('index_count', 0)}/{targ.get('index_count',0)}",
            'primary_key_count': f"{src.get('primary_key_count', 0)}/{targ.get('primary_key_count',0)}",
            'foreign_key_count': f"{src.get('foreign_key_count', 0)}/{targ.get('foreign_key_count',0)}",
            'trigger_count': f"{src.get('trigger_count', 0)}/{targ.get('trigger_count',0)}"
        })
    return combined


def collect_index_names(db):
    tables = get_table_names(db['db_type'], db['db_name'])
    result = []
    for table in tables:
        indexes = get_indexes_info(db['db_type'], db['db_name'], table) or []
        names = [idx.get('name') for idx in indexes]
        result.append({'table_name': table, 'index_names': names})
    return result



def collect_primary_key_names(db):
    tables = get_table_names(db['db_type'], db['db_name'])
    result = []
    for table in tables:
        pk_info = get_primary_keys(db['db_type'], db['db_name'], table) or {}
        cols = pk_info.get('constrained_columns', [])
        result.append({'table_name': table, 'primary_key_names': cols})
    return result



def collect_foreign_key_names(db):
    tables = get_table_names(db['db_type'], db['db_name'])
    result = []
    for table in tables:
        fks = get_foreign_keys(db['db_type'], db['db_name'], table) or []
        names = [fk.get('name') for fk in fks]
        result.append({'table_name': table, 'foreign_key_names': names})
    return result



def collect_trigger_names(db):
    tables = get_table_names(db['db_type'], db['db_name'])
    result = []
    for table in tables:
        triggers = get_triggers_for_table(db['db_type'], db['db_name'], table) or []
        names = [t.get('name') for t in triggers]
        result.append({'table_name': table, 'trigger_names': names})
    return result


# 1) Validator - Could have reused other functions to reduce extra/unneccesary calls -> look into it 

# Conditions for validation
# 1) Table names match
# 2) Row count match
# 3) Indexes count match
# 4) Primary keys count match
# 5) Foreign keys count match
# 6) Trigger count match

# Meeting all of the above conditions for now indictaes a complete sucess 

def validate_export_success(source, target):
    source_tables = get_table_names(source['db_type'], source['db_name'])
    target_tables = get_table_names(target['db_type'], target['db_name'])

    # 1. Table name match
    if set(source_tables) != set(target_tables):
        return False

    for table in source_tables:
        # 2. Row count match
        src_count = get_table_count(
            run_query(f"SELECT COUNT(*) AS cnt FROM {table};", source['db_type'], source['db_name'])
        )
        targ_count = get_table_count(
            run_query(f"SELECT COUNT(*) AS cnt FROM {table};", target['db_type'], target['db_name'])
        )
        if src_count != targ_count:
            return False

        # 3. Index count match
        src_indexes = get_indexes_info(source['db_type'], source['db_name'], table) or []
        targ_indexes = get_indexes_info(target['db_type'], target['db_name'], table) or []
        if len(src_indexes) != len(targ_indexes):
            return True

        # 4. Primary key match
        src_pk = get_primary_keys(source['db_type'], source['db_name'], table) or {}
        targ_pk = get_primary_keys(target['db_type'], target['db_name'], table) or {}
        if sorted(src_pk.get('constrained_columns', [])) != sorted(targ_pk.get('constrained_columns', [])):
            return False

        # 4. Foreign key match
        src_fk = get_foreign_keys(source['db_type'], source['db_name'], table) or []
        targ_fk = get_foreign_keys(target['db_type'], target['db_name'], table) or []
        src_fk_names = sorted([fk.get('name') for fk in src_fk])
        targ_fk_names = sorted([fk.get('name') for fk in targ_fk])
        if src_fk_names != targ_fk_names:
            return False

        # 5. Trigger match
        src_triggers = get_triggers_for_table(source['db_type'], source['db_name'], table) or []
        targ_triggers = get_triggers_for_table(target['db_type'], target['db_name'], table) or []
        src_trigger_names = sorted([
            str(name) for t in src_triggers for name in [t.get('name')] if name is not None
        ])
        targ_trigger_names = sorted([
            str(name) for t in targ_triggers for name in [t.get('name')] if name is not None
        ])
        if src_trigger_names != targ_trigger_names:
            return False
        
    
    return True


# 2) Test