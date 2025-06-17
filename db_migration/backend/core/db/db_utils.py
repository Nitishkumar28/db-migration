import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError
from sqlalchemy.engine import CursorResult
import re
import json

from core.db.db_connect import get_db_engine
from core.process import PostgresToMySQLDataTypeAdapter
from core.data import TriggerModel


def run_query(query, db_type, db_name=None):
    print("Run Query")
    engine = get_db_engine(db_type, db_name)
    if engine is not None:
        try:
            with engine.begin() as conn:
                results = conn.execute(text(query)) # check the value stored in results
                return results
        except Exception as e:
            print(f"Exception occurred while running query: {query}, {str(e)}")
    return []


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
    results = []
    if db_type == "postgresql":
        query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        results = run_query(query, "postgresql")
    elif db_type == "mysql":
        query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');" 
        results = run_query(query, "mysql")
    return results if results is not None else []


def get_table_names(db_type, db_name):
    inspector = get_db_inspector(db_type, db_name)
    print(inspector)
    print(db_type, db_name)
    table_names = []
    try:
        if inspector is not None:
            table_names = inspector.get_table_names()
    except Exception as e:
        print(f"Error occurred while retrieving table names: {str(e)}")
    return table_names


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
        if inspector is not None:
            exist_columns = inspector.get_columns(table_name)
            for column in exist_columns:
                column_info = {
                    "name": column["name"],
                    "type": column["type"], # Potential error each data type value is being casted to str and hence being mapped to TEXT 
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
        if inspector is not None:
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

def get_primary_keys(db_type, db_name, table_name):
    inspector = get_db_inspector(db_type, db_name)
    if inspector:
        return inspector.get_pk_constraint(table_name) or {}
    return {}

def get_table_ddl(db_type, db_name, table_name):
    columns = get_column_info(db_type, db_name, table_name)
    primary_keys_detail = get_primary_keys(db_type, db_name, table_name)
    adapter = PostgresToMySQLDataTypeAdapter()

    table_ddl_create = [f"CREATE TABLE IF NOT EXISTS `{table_name}` ("]
    col_defs = []

    for column in columns:
        col_name = column["name"]
        col_type_obj = column["type"] 
        sql_type = adapter.convert_data(col_type_obj)
        print("DDL - SQL TYPE")
        print(sql_type)
        null_const = "NULL" if column["nullable"] else "NOT NULL"
        default_val = ""
        col_defs.append(
            f"  `{col_name}` {sql_type} {null_const} {default_val}".strip())

    if primary_keys_detail and primary_keys_detail.get("constrained_columns"):
        cols = ", ".join(f"`{c}`" for c in primary_keys_detail["constrained_columns"])
        col_defs.append(f" PRIMARY KEY ({cols})")

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


def load_data_to_table(db_type, db_name, table_name, df, dtype_map, if_exists="replace"):
    try:
        engine = get_db_engine(db_type, db_name)
        print("Printing DF")
        for colname in df.columns:
            if df[colname].apply(lambda x: isinstance(x,dict)).any():
                print("Inside if")
                df[colname] = df[colname].apply(json.dumps)
        print(df)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, dtype=dtype_map)
        return True
    except Exception as e:
        print(f"Error occurred while loading data: {str(e)}")
        return False


def export_tables(source, target, table_names):
    skipped, exported = set(), set()
    print(source,target, table_names)

    for table_name in table_names:
        run_query(f"DROP TABLE IF EXISTS `{table_name}`;", target["db_type"], target["db_name"])
        # 1. Get data from "source" table
        get_records_query = f"SELECT * FROM {table_name};"
        data = run_query(get_records_query, source["db_type"], source["db_name"])
        if not data:
            skipped.add(table_name)
            continue

        # 2. Build "create table" query from source
        create_table_query = get_table_ddl(source["db_type"], source["db_name"], table_name)
        print("TABLE DDL")
        print(create_table_query)
        # 3. Execute "create table" query on target, if query failed to run, skip it
        ack = run_query(create_table_query, target["db_type"], target["db_name"]) # mySQL Table create
        print("ACK ")
        print(ack)
        if not ack: # check this
            skipped.add(table_name)
            continue

        
        # 4. get column names for the current table from source
        column_info = get_column_info(target["db_type"], target["db_name"], table_name)
        print("MYSQL -  COLUMN INFO")
        print(column_info)
        dtype_map = {
            column["name"]: column["type"]
            for column in column_info
        }
        column_names = [
            column["name"] 
            for column in column_info
            ]
        
        # 5. Create df for the data with its column names, then load data to target table
        df = pd.DataFrame(data, columns=column_names)
        load_data_to_table(target["db_type"], target["db_name"], table_name , df, dtype_map, if_exists="append")

        # 6. get indexes and run "create index" query
        indexes = get_indexes_info(source["db_type"], source["db_name"], table_name)

        for index in indexes:
            is_unique = "UNIQUE " if index["unique"] else ""
            modified_cols = []
            print("Index print")
            columns_with_dt = [(col['name'],col['type']) for col in column_info]
            for col_name, col_type in columns_with_dt:
                if col_name in index["column_names"]:
                    print(col_name, col_type)
                    if str(col_type).upper() in {"TEXT","BLOB"}:
                        modified_cols.append(f'{col_name}(100)')
                    else:
                        modified_cols.append(f'{col_name}')
            create_index_query = (
                    f"CREATE {is_unique}INDEX `{index["name"]}` "
                    f"ON `{table_name}` ({', '.join(modified_cols)});"
                )
            print(create_index_query)
            ack = run_query(create_index_query, target["db_type"], target["db_name"])
            if not ack:
                skipped.add(table_name)
                print(f"Error occurred while creating indexes for {table_name}!")
                continue
        exported.add(table_name)
    
    return exported, skipped


def get_source_triggers(db_type, db_name, table_name):
    sql = f"""
    SELECT trigger_name, action_timing, event_manipulation, action_statement
      FROM information_schema.triggers
     WHERE event_object_table = '{table_name}'
       AND trigger_schema      = 'public';
    """
    return run_query(sql, db_type, db_name)


def fetch_function_definition(function_name, db_type, db_name):
    sql = f"""
    SELECT pg_get_functiondef(p.oid) AS definition
      FROM pg_proc p
      JOIN pg_namespace n ON p.pronamespace = n.oid
     WHERE p.proname = '{function_name}'
       AND n.nspname = 'public';
    """
    result = run_query(sql, db_type, db_name)
    if isinstance(result, CursorResult):
        rows = result.fetchall() or []
    elif isinstance(result, list):
        rows = result
    else:
        rows = []
    if not rows:
        raise ValueError(f"Function definition not found for {function_name}")
    return rows[0][0]


def trigger_body_definition(definition, event):
    patterns = {
        "INSERT": r"IF\s+TG_OP\s*=\s*'INSERT'\s+THEN(.*?)ELSIF",
        "UPDATE": r"ELSIF\s+TG_OP\s*=\s*'UPDATE'\s+THEN(.*?)ELSIF",
        "DELETE": r"ELSIF\s+TG_OP\s*=\s*'DELETE'\s+THEN(.*?)END IF",
    }
    pattern = patterns.get(event.upper())
    if not pattern:
        raise ValueError(f"Unsupported event type: {event}")
    match = re.search(pattern, definition, re.S | re.I)
    if not match:
        raise ValueError(f"Could not extract body for {event}")

    body = match.group(1)
    body = re.sub(r"\bRETURN\b[^\n;]*[;\n]?", "", body, flags=re.I)
    body = re.sub(r"--.*?$", "", body, flags=re.M).strip()
    return body.rstrip(';')


def trigger_body_to_sql(body_sql, column_names, event):
    def build_json(alias: str) -> str:
        pairs = ", ".join(f"'{col}', {alias}.{col}" for col in column_names)
        return f"JSON_OBJECT({pairs})"

    sql = body_sql.replace("TG_OP", f"'{event}'")
    sql = re.sub(r"\bto_jsonb\s*\(\s*NEW\s*\)", build_json("NEW"), sql, flags=re.I)
    sql = re.sub(r"\bto_jsonb\s*\(\s*OLD\s*\)", build_json("OLD"), sql, flags=re.I)
    return sql


def generate_mysql_trigger_ddl(trigger_name, timing, event, table_name, body_sql):
    return f"""
    CREATE TRIGGER `{trigger_name}`
    {timing.upper()} {event.upper()} ON `{table_name}`
    FOR EACH ROW
    BEGIN
        {body_sql};
    END;"""


def export_triggers(source: dict, target: dict) -> dict:
    pg_type, pg_name = source["db_type"], source["db_name"]
    mysql_type, mysql_name = target["db_type"], target["db_name"]
    exported, errors = [], []

    tables = get_table_names(pg_type, pg_name) or []

    for table in tables:
        try:
            col_info = get_column_info(pg_type, pg_name, table)
            cols = [c["name"] for c in col_info]

            result = get_source_triggers(pg_type, pg_name, table)
            if isinstance(result, CursorResult):
                rows = result.fetchall() or []
            else:
                rows = result if isinstance(result, list) else []

            for name, timing, event, statement in rows:
                event = event.upper()
                statement = statement.strip()
                match = re.match(r"EXECUTE FUNCTION ([\w_]+)\(\)", statement, re.I)
                if not match:
                    raise ValueError(f"Unsupported action: {statement}")
                func_name = match.group(1)

                definition = fetch_function_definition(func_name, pg_type, pg_name)
                body = trigger_body_definition(definition, event)
                body = trigger_body_to_sql(body, cols, event)
                trigger_name = f"{name}_{event.lower()}"

                run_query(f"DROP TRIGGER IF EXISTS `{trigger_name}`;", mysql_type, mysql_name)
                ddl = generate_mysql_trigger_ddl(trigger_name, timing, event, table, body)
                run_query(ddl, mysql_type, mysql_name)

                exported.append(trigger_name)
        except Exception as e:
            errors.append({"table": table, "error": str(e)})
    return {"exported": exported, "errors": errors}