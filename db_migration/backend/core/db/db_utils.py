import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError
import re

from core.db.db_connect import get_db_engine
from core.process import PostgresToMySQLDataTypeAdapter
from core.data import TriggerModel


def run_query(query, db_type, db_name=None):
    engine = get_db_engine(db_type, db_name)
    if engine is not None:
        try:
            with engine.begin() as conn:
                results = conn.execute(text(query))
                return results
        except Exception as e:
            print(f"Exception occurred while running query: {query}, {str(e)}")
    return None


def get_db_inspector(db_type, db_name):
    engine = get_db_engine(db_type, db_name)
    try:
        inspector = inspect(engine)
        return inspector
    except Exception as e:
        print(f"Error occurred while creating the inspector")
    return None


def get_databases(db_type):
    """
    ????? db_name ?????
    """
    if db_type == "postgresql":
        query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        results = run_query(query, "postgresql")
    elif db_type == "mysql":
        query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        results = run_query(query, "mysql")
    return results if results is not None else []


def get_table_names(db_type, db_name):
    inspector = get_db_inspector(db_type, db_name)
    try:
        table_names = inspector.get_table_names()
        return table_names
    except Exception as e:
        print(f"Error occurred while retrieving table names: {str(e)}")
        return None


def delete_tables(db_type, db_name, table_name=None):
    if table_name is None:
        table_names = get_table_names(db_type, db_name)
    else:
        table_names = [table_name]

    removed_tables = []

    for table_name in table_names:
        message = ""
        query = f"DROP TABLE IF EXISTS `{table_name}`;"
        result = run_query(query, db_type, db_name)

        if result is None:
            message = "table doesn't exist"

        removed_tables.append((table_name, message))

    return {"removed": removed_tables}


def get_column_info(db_type, db_name, table_name):
    inspector = get_db_inspector(db_type, db_name)
    processed_columns = []

    try:
        exist_columns = inspector.get_columns(table_name)
        for column in exist_columns:
            column_info = {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": column.get("default")
            }
            processed_columns.append(column_info)
        return processed_columns

    except NoSuchTableError:
        raise ValueError(f"Table '{table_name}' does not exist.")
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error accessing columns: {str(e)}")


def get_indexes_info(db_type, db_name, table_name):
    inspector = get_db_inspector(db_type, db_name)
    processed_indexes = []

    try:
        indexes = inspector.get_indexes(table_name)
        for index in indexes:
            index_info = {
                "name": index.get("name"),
                "column_names": index.get("column_names", []),
                "unique": index.get("unique", False),
            }
            processed_indexes.append(index_info)
        return processed_indexes

    except NoSuchTableError:
        raise ValueError(f"Table '{table_name}' does not exist.")
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error accessing columns: {str(e)}")


def get_table_schema(db_type, db_name, table_name):
    processed_columns = get_column_info(db_type, db_name, table_name)
    processed_indexes = get_indexes_info(db_type, db_name, table_name)
    return {
        "column_data": processed_columns,
        "Index_data": processed_indexes
    }


def get_table_ddl(db_type, db_name, table_name):
    columns = get_column_info(db_type, db_name, table_name)
    adapter = PostgresToMySQLDataTypeAdapter()

    table_ddl_create = [f"CREATE TABLE IF NOT EXISTS `{table_name}` ("]
    col_defs = []

    for column in columns:
        col_name = column["name"]
        col_type_obj = column["type"]
        sql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if column["nullable"] else "NOT NULL"
        default_val = ""
        col_defs.append(
            f"  `{col_name}` {sql_type} {null_const} {default_val}".strip())

    table_ddl_create.append(",\n".join(col_defs))
    table_ddl_create.append(");")
    return "\n".join(table_ddl_create)


def get_triggers_for_table(db_type, db_name, table_name):
    query = f"""
    SELECT
        trigger_name    AS name,
        action_timing   AS timing,
        event_manipulation AS event,
        action_statement   AS statement
    FROM {table_name}.triggers
    WHERE event_object_table = :tbl
    AND trigger_schema = 'public';
    """
    results = run_query(query, db_type, db_name)
    return [
        {
            "name": row.name,
            "timing": row.timing,
            "event": row.event,
            "statement": row.statement.strip()
        }
        for row in results
    ]


def load_data_to_table(db_type, db_name, table_name, df, if_exists="replace"):
    try:
        engine = get_db_engine(db_type, db_name)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        return True
    except Exception as e:
        print(f"Error occurred while loading data: {str(e)}")
        return False


def export_tables(source, target, table_names):
    skipped, exported = set(), set()

    for table_name in table_names:
        # 1. Get data from "source" table
        get_records_query = f"SELECT * FROM {table_name};"
        data = run_query(get_records_query, source["db_type"], source["db_name"])
        if data is None:
            skipped.add(table_name)
            continue

        # 2. Build "create table" query from source
        create_table_query = get_table_ddl(source["db_type"], source["db_name"], table_name)
        # 3. Execute "create table" query on target, if query failed to run, skip it
        ack = run_query(create_table_query, target["db_type"], target["db_name"])
        if ack is None:
            skipped.add(table_name)
            continue
        
        # 4. get column names for the current table from source
        column_names = [
            column["name"] 
            for column in get_column_info(source["db_type"], source["db_name"], table_name)
            ]
        
        # 5. Create df for the data with its column names, then load data to target table
        df = pd.DataFrame(data, columns=column_names)
        load_data_to_table(target["db_type"], target["db_name"], df, if_exists="replace")

        # 6. get indexes and run "create index" query
        indexes = get_indexes_info(source["db_type"], source["db_name"], table_name)
        for index in indexes:
            create_index_query = (
                    f"CREATE {index["unique"]}INDEX `{index["index_name"]}` "
                    f"ON `{table_name}` ({', '.join(index["column_list"])});"
                )
            ack = run_query(create_index_query, target["db_type"], target["db_name"])
            if ack is None:
                skipped.add(table_name)
                print(f"Error occurred while creating indexes for {table_name}!")
                continue
        exported.add(table_name)
    
    return exported, skipped


def get_trigger_rows(pg_conn, table):
    sql = """
          SELECT trigger_name, action_timing, event_manipulation, action_statement
          FROM information_schema.triggers
          WHERE event_object_table = :tbl
            AND trigger_schema = 'public'; \
          """
    return pg_conn.execute(text(sql), {"tbl": table}).fetchall()


def drop_mysql_trigger(db_name, trigger_name):
    sql = f"DROP TRIGGER IF EXISTS `{trigger_name}`;"
    run_query(sql, 'mysql', db_name)


def build_json(alias, columns):
    pairs = ", ".join(f"'{col}', {alias}.{col}" for col in columns)
    return f"JSON_OBJECT({pairs})"


def trigger_body(pg_conn, name, event, columns):
    sql = text(
        """
        SELECT pg_get_functiondef(p.oid) AS def
        FROM pg_proc p
                 JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE p.proname = :func
          AND n.nspname = 'public';
        """
    )
    full_def = pg_conn.execute(sql, {'func': name}).scalar_one()
    patterns = {
        'INSERT': r"IF\s+TG_OP='INSERT' THEN(.*?)ELSIF",
        'UPDATE': r"ELSIF\s+TG_OP='UPDATE' THEN(.*?)ELSIF",
        'DELETE': r"ELSIF\s+TG_OP='DELETE' THEN(.*?)END IF",
    }
    body_match = re.search(patterns[event], full_def, re.S | re.I)
    if not body_match:
        raise ValueError(f"No body for event {event}")
    body = body_match.group(1)
    body = re.sub(r"RETURN[^;]*;", '', body, flags=re.I)
    body = re.sub(r"--.*?$", '', body, flags=re.M)
    
    body = body.replace('TG_OP', f"'{event}'")
    for alias in ['NEW', 'OLD']:
        body = re.sub(rf"to_jsonb\(\s*{alias}\s*\)",
                      f"JSON_OBJECT({', '.join(f'\'{each_col}\', {alias}.{each_col}' for each_col in columns)})",
                      body, flags=re.I)
    return body.strip().rstrip(';')


def create_mysql_trigger(mysql_conn, table, trigger_name, timing, event, body_sql):
    ddl = f"""
    CREATE TRIGGER `{trigger_name}` {timing} {event} ON `{table}` FOR EACH ROW
    BEGIN
      {body_sql};
    END;"""
    mysql_conn.execute(text(ddl))


def export_triggers(db_name, tables):
    exported = []
    errors = []
    pg_engine = get_db_engine('postgresql', db_name)
    my_engine = get_db_engine('mysql', db_name)
    inspector = inspect(pg_engine)
    
    with pg_engine.connect() as pg_conn, my_engine.connect() as my_conn:
        for table in tables:
            try:
                cols = [c['name'] for c in inspector.get_columns(table)]
                rows = fetch_trigger_rows(pg_conn, table)
                for name, timing, event, stmt in rows:
                    trig_name = f"{name}_{event.lower()}"
                    drop_mysql_trigger(my_conn, trig_name)
                    m = re.match(r"EXECUTE FUNCTION (\w+)\(\)", stmt, re.I)
                    if not m:
                        raise ValueError(f"Unsupported statement: {stmt}")
                    func = m.group(1)
                    body = extract_trigger_body(pg_conn, func, event, cols)
                    create_mysql_trigger(my_conn, table, trig_name, timing, event, body)
                    exported.append(trig_name)
            except Exception as e:
                errors.append({'table': table, 'error': str(e)})
    return exported, errors
