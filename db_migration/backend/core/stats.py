import time
from datetime import datetime
from core.db.db_utils import get_table_names, run_query
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


def collect_export_stats(source, target, exported, errors, start_time, end_time, durations):
    timestamp = datetime.utcnow()
    overall_duration = end_time - start_time
    metrics = []
    sno = 1

    tables = get_table_names(source['db_type'], source['db_name'])
    for table in tables:
        source_records = run_query(f"SELECT COUNT(*) AS cnt FROM {table};", source['db_type'], source['db_name'])
        source_records_count = get_table_count(source_records)

        try:
            target_records = run_query(f"SELECT COUNT(*) AS cnt FROM {table};", target['db_type'], target['db_name'])
            target_records_count = get_table_count(target_records)
        except Exception as e:
            target_records_count = 0
            print("Table does not exist")

        check_for_errors = any(error.get('table') == table for error in errors)
        status = 'success' if (table in exported and not check_for_errors) else 'failure'

        metrics.append({
            'sno': sno,
            'table_name': table,
            'source_rows': source_records_count,
            'target_rows': target_records_count,
            'time_taken_seconds': durations.get(table, overall_duration),
            'timestamp': timestamp.isoformat(),
            'status': status
        })
        sno += 1

    global _last_export_metrics
    _last_export_metrics = metrics


def get_most_recent_stats():
   return _last_export_metrics
        