from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import json
import os

# Better Type Detection
from sqlalchemy.dialects.postgresql import (
    UUID as PostGre_UUID,
    VARCHAR as PostGre_VARCHAR,
    CHAR as PostGre_CHAR,
    TEXT as PostGre_TEXT,
    INTEGER as PostGre_INTEGER,
    SMALLINT as PostGre_SMALLINT,
    BIGINT as PostGre_BIGINT,
    NUMERIC as PostGre_NUMERIC,
    REAL as PostGre_REAL,
    DOUBLE_PRECISION as PostGre_DOUBLE_PRECISION,
    BYTEA as PostGre_BYTEA,
    JSON as PostGre_JSON,
    JSONB as PostGre_JSONB,
    TIMESTAMP as PostGre_TIMESTAMP,
    TIME as PostGre_TIME,
    DATE as PostGre_DATE,
    BOOLEAN as PostGre_BOOLEAN,
)

from sqlalchemy.types import (
    Integer as Gen_Integer,
    String as Gen_String,
    Numeric as Gen_Numeric,
    Date as Gen_Date,
    DateTime as Gen_DateTime,
    Boolean as Gen_Boolean,
    Float as Gen_Float,
    LargeBinary as Gen_LargeBinary,
    JSON as Gen_JSON,
    Time as Gen_Time,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class TableModel(BaseModel):
    db_name: str
    tables: List[str]


@app.get("/")
def load_homepage():
    return FileResponse(os.path.join("static", "index.html"))


MYSQL_CONNECTION_STRING = "mysql+pymysql://root:Nitish%40123@localhost:3306/demo"
POSTGRES_CONNECTION_STRING = (
    "postgresql+psycopg2://postgres:Nitish%40123@localhost:5432/postgres"
)

mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
postgres_engine = create_engine(POSTGRES_CONNECTION_STRING)

already_exported_tables = {}


class PostgresToMySQLDataTypeAdapter:
    def convert_data(self, column_object_type) -> str:
        data_class_name = column_object_type.__class__.__name__.upper()

        # 1) UUID -> CHAR(36)
        if isinstance(column_object_type, PostGre_UUID) or data_class_name == "UUID":
            return "CHAR(36)"

        # 2) BIGINT
        if (
            isinstance(column_object_type, PostGre_BIGINT)
            or data_class_name == "BIGINT"
        ):
            return "BIGINT"

        # 3) SMALLINT
        if (
            isinstance(column_object_type, PostGre_SMALLINT)
            or data_class_name == "SMALLINT"
        ):
            return "SMALLINT"

        # 4) INTEGER -> INT
        if (
            isinstance(column_object_type, PostGre_INTEGER)
            or isinstance(column_object_type, Gen_Integer)
            or data_class_name == "INTEGER"
        ):
            return "INT"

        # 5) DOUBLE PRECISION -> DOUBLE
        if (
            isinstance(column_object_type, PostGre_DOUBLE_PRECISION)
            or (
                isinstance(column_object_type, Gen_Float)
                and getattr(column_object_type, "precision", None) == 53
            )
            or data_class_name in ("DOUBLE_PRECISION", "DOUBLE")
        ):
            return "DOUBLE"

        # 6) REAL -> FLOAT
        if (
            isinstance(column_object_type, PostGre_REAL)
            or (
                isinstance(column_object_type, Gen_Float)
                and getattr(column_object_type, "precision", None) == 24
            )
            or data_class_name == "REAL"
            or (
                data_class_name == "FLOAT"
                and getattr(column_object_type, "precision", None) is None
            )
        ):
            return "FLOAT"

        # 7) CHAR(length)
        if isinstance(column_object_type, PostGre_CHAR) or data_class_name.startswith(
            "CHAR"
        ):
            length = getattr(column_object_type, "length", None) or 1
            return f"CHAR({length})"

        # 8) TEXT
        if isinstance(column_object_type, PostGre_TEXT) or data_class_name == "TEXT":
            return "TEXT"

        # 9) VARCHAR(length)
        if (
            isinstance(column_object_type, PostGre_VARCHAR)
            or isinstance(column_object_type, Gen_String)
            or data_class_name.startswith("VARCHAR")
        ):
            length = getattr(column_object_type, "length", None) or 255
            return f"VARCHAR({length})"

        # 10) DATE
        if (
            isinstance(column_object_type, PostGre_DATE)
            or isinstance(column_object_type, Gen_Date)
            or data_class_name == "DATE"
        ):
            return "DATE"

        # 11) TIME
        if (
            isinstance(column_object_type, PostGre_TIME)
            or isinstance(column_object_type, Gen_Time)
            or data_class_name == "TIME"
        ):
            return "TIME"

        # 12) TIMESTAMP (both with & without time zone) -> DATETIME
        if (
            isinstance(column_object_type, PostGre_TIMESTAMP)
            or isinstance(column_object_type, Gen_DateTime)
            or data_class_name == "TIMESTAMP"
        ):
            return "DATETIME"

        # 13) BOOLEAN
        if (
            isinstance(column_object_type, PostGre_BOOLEAN)
            or isinstance(column_object_type, Gen_Boolean)
            or data_class_name == "BOOLEAN"
        ):
            return "BOOLEAN"

        # 14) NUMERIC/DECIMAL -> DECIMAL
        if (
            isinstance(column_object_type, PostGre_NUMERIC)
            or isinstance(column_object_type, Gen_Numeric)
            or data_class_name in ("NUMERIC", "DECIMAL")
        ):
            precision = getattr(column_object_type, "precision", None) or 10
            scale = getattr(column_object_type, "scale", None) or 0
            return f"DECIMAL({precision},{scale})"

        # 15) BYTEA -> BLOB
        if (
            isinstance(column_object_type, PostGre_BYTEA)
            or isinstance(column_object_type, Gen_LargeBinary)
            or data_class_name == "BYTEA"
        ):
            return "BLOB"

        # 16) JSON/JSONB -> JSON
        if (
            isinstance(column_object_type, PostGre_JSON)
            or isinstance(column_object_type, PostGre_JSONB)
            or isinstance(column_object_type, Gen_JSON)
            or data_class_name in ("JSON", "JSONB")
        ):
            return "JSON"

        # 17) Default fallback to TEXT
        return "TEXT"


def generate_mysql_create_table(
    connection, database_name: str, table_name: str, adapter: PostgresToMySQLDataTypeAdapter
):
    database = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
    postgre_eng = create_engine(f"{database}/{database_name}")
    inspector = inspect(postgre_eng)

    columns = inspector.get_columns(table_name)
    try:
        pk_info = inspector.get_pk_constraint(table_name)
        pk_columns = pk_info.get("constrained_columns", []) or []
    except Exception:
        pk_columns = []

    ddl_parts = [f"CREATE TABLE `{table_name}` ("]
    col_def = []

    for col in columns:
        name = col["name"]
        col_type_obj = col["type"]
        mysql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if col["nullable"] else "NOT NULL"
        default_val = ""
        col_def.append(f"  `{name}` {mysql_type} {null_const} {default_val}".strip())

    if pk_columns:
        pk_list = ", ".join(f"`{c}`" for c in pk_columns)
        col_def.append(f"  PRIMARY KEY ({pk_list})")

    ddl_parts.append(",\n".join(col_def))
    ddl_parts.append(");")
    ddl_statement = "\n".join(ddl_parts)

    # Debug print
    print(f"===== DDL FOR TABLE {table_name} =====")
    print(ddl_statement)
    print("=====================================")

    connection.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
    connection.execute(text(ddl_statement))


@app.get("/databases")
def fetch_postgres_databases():
    with postgres_engine.connect() as conn:
        rows = conn.execute(
            text("SELECT datname FROM pg_database WHERE datistemplate = false;")
        ).fetchall()
        return {"databases": [r[0] for r in rows]}


@app.get("/tables/{database_name}")
def fetch_tables(database_name: str):
    database_str = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
    conn_str = f"{database_str}/{database_name}"
    database_engine = create_engine(conn_str)
    inspector = inspect(database_engine)
    return {"tables": inspector.get_table_names()}


@app.post("/export")
def export_button(request: TableModel):
    database_str = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
    request_database = create_engine(f"{database_str}/{request.db_name}")
    inspector = inspect(request_database)

    if request.db_name not in already_exported_tables:
        already_exported_tables[request.db_name] = set()

    skipped, exported = [], []
    adapter = PostgresToMySQLDataTypeAdapter()

    with mysql_engine.connect() as mysql_conn:
        for each_tbl in request.tables:
            if each_tbl in already_exported_tables[request.db_name]:
                skipped.append(each_tbl)
                continue

            generate_mysql_create_table(mysql_conn, request.db_name, each_tbl, adapter)
            df = pd.read_sql_table(each_tbl, request_database)

            for colname, dtype in df.dtypes.items():
                if dtype == object:
                    sample = df[colname].dropna()
                    if not sample.empty and isinstance(sample.iloc[0], dict):
                        df[colname] = df[colname].apply(
                            lambda v: json.dumps(v) if isinstance(v, dict) else v
                        )

            df.to_sql(each_tbl, mysql_engine, if_exists="append", index=False)

            already_exported_tables[request.db_name].add(each_tbl)
            exported.append(each_tbl)

            indexes = inspector.get_indexes(each_tbl)
            for each_idx in indexes:
                index_name = each_idx.get("name")
                cols = []
                for c in each_idx.get("column_names", []):
                    col_type = df[c].dtype
                    if str(col_type) == "object":
                        cols.append(f"{c}(255)")
                    else:
                        cols.append(f"{c}")
                unique = "UNIQUE" if each_idx.get("unique", False) else ""
                try:
                    mysql_conn.execute(
                        text(
                            f"CREATE {unique} INDEX `{index_name}` "
                            f"ON `{each_tbl}` ({', '.join(cols)});"
                        )
                    )
                except Exception as e:
                    print(f"Index creation failed for {index_name} on {each_tbl}: {e}")

    return {
        "status": "partial" if skipped else "success",
        "exported_tables": exported,
        "skipped_tables": skipped,
    }


@app.post("/remove")
def remove_from_mysql(request: TableModel):
    removed_tables = []
    failed_tables = []

    for each_tbl in request.tables:
        try:
            with mysql_engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS `{each_tbl}`;"))
            removed_tables.append(each_tbl)
            already_exported_tables.get(request.db_name, set()).discard(each_tbl)
        except Exception as ex:
            failed_tables.append((each_tbl, str(ex)))

    if failed_tables:
        raise HTTPException(
            status_code=500, detail={"removed": removed_tables, "errors": failed_tables}
        )
    return {"removed": removed_tables}


@app.post("/reset")
def clear_mysql():
    dropped = []
    for dbname, table_set in list(already_exported_tables.items()):
        with mysql_engine.connect() as conn:
            for tbl in list(table_set):
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS `{tbl}`;"))
                    dropped.append(tbl)
                except Exception as e:
                    print(f"Failed to drop {tbl}: {e}")
    already_exported_tables.clear()
    return {"reset": True, "dropped_tables": dropped}


@app.get("/schema/{database_name}/{table_name}")
def fetch_table_schema(database_name: str, table_name: str):
    database_str = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
    database_connection = create_engine(f"{database_str}/{database_name}")
    inspector = inspect(database_connection)

    exist_columns = inspector.get_columns(table_name)
    processed_columns = []
    for each_col in exist_columns:
        processed_columns.append(
            {
                "name": each_col["name"],
                "type": str(each_col["type"]),
                "nullable": each_col["nullable"],
                "default": each_col.get("default"),
            }
        )

    exist_indexes = inspector.get_indexes(table_name)
    processed_indexes = []
    for idx in exist_indexes:
        processed_indexes.append(
            {
                "name": idx.get("name"),
                "column_names": idx.get("column_names", []),
                "unique": idx.get("unique", False),
            }
        )

    return {"columns": processed_columns, "indexes": processed_indexes}


@app.get("/indexes/{database_name}/{table_name}")
def list_indexes(database_name: str, table_name: str):
    try:
        database_str = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
        connection_str = create_engine(f"{database_str}/{database_name}")
        inspector = inspect(connection_str)
        exist_indexes = inspector.get_indexes(table_name)
        return {
            "indexes": [
                {
                    "name": each_idx.get("name"),
                    "columns": each_idx.get("column_names", []),
                    "unique": each_idx.get("unique", False),
                }
                for each_idx in exist_indexes
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_mysql_ddl(database_name: str, table_name: str) -> str:
    database_str = POSTGRES_CONNECTION_STRING.rsplit("/", 1)[0]
    database_engine = create_engine(f"{database_str}/{database_name}")
    inspector = inspect(database_engine)
    table_columns = inspector.get_columns(table_name)

    table_ddl_create = [f"CREATE TABLE `{table_name}` ("]
    col_defs = []
    adapter = PostgresToMySQLDataTypeAdapter()

    for column in table_columns:
        col_name = column["name"]
        col_type_obj = column["type"]
        sql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if column["nullable"] else "NOT NULL"
        default_val = ""
        col_defs.append(f"  `{col_name}` {sql_type} {null_const} {default_val}".strip())

    table_ddl_create.append(",\n".join(col_defs))
    table_ddl_create.append(");")
    return "\n".join(table_ddl_create)


@app.get("/schema-ddl/{database_name}/{table_name}")
def fetch_table_ddl(database_name: str, table_name: str):
    try:
        table_ddl = generate_mysql_ddl(database_name, table_name)
        return {"ddl": table_ddl}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
