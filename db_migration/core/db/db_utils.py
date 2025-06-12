from sqlalchemy import inspect, text
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError

from core.db.db_connect import get_db_engine

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
    inspector = inspect(engine)
    return inspector

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
        exist_indexes = inspector.get_indexes(table_name)
        for index in exist_indexes:
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

def get_indexes_info(db_type, db_name, table_name):
    inspector = get_db_inspector(db_type, db_name)
    processed_indexes = []

    try:
        exist_indexes = inspector.get_indexes(table_name)
        for index in exist_indexes:
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
    inspector = get_db_inspector(db_type, db_name)
    columns = get_column_info(db_type, db_name, table_name)

    try:
        pk_info = inspector.get_pk_constraint(table_name)
    except NoSuchTableError:
        raise ValueError(f"Table '{table_name}' does not exist.")
    
    pk_columns = pk_info.get("constrained_columns", [])

    ddl_parts = [f"CREATE TABLE `{table_name}` ("]
    col_def = []

    for col in columns:
        name = col["name"]
        col_type_obj = col["type"]
        mysql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if col["nullable"] else "" 
        default_val = ""
        col_def.append(f"`{name}` {mysql_type} {null_const} {default_val}".strip()) 
    if pk_columns:
        pk_list = ", ".join(f"`{c}`" for c in pk_columns)
        col_def.append(f"  PRIMARY KEY ({pk_list})")

    ddl_parts.append(",\n".join(col_def))
    ddl_parts.append(");")
    ddl_statement = "\n".join(ddl_parts)
    
    delete_tables(db_type, db_name, table_name)
    run_query(ddl_statement, db_type, db_name)
    
    return 
