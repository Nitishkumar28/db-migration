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
    UUID as PG_UUID,
    VARCHAR as PG_VARCHAR,
    CHAR as PG_CHAR,
    TEXT as PG_TEXT,
    INTEGER as PG_INTEGER,
    SMALLINT as PG_SMALLINT,
    BIGINT as PG_BIGINT,
    NUMERIC as PG_NUMERIC,
    REAL as PG_REAL,
    DOUBLE_PRECISION as PG_DOUBLE_PRECISION,
    BYTEA as PG_BYTEA,
    JSON as PG_JSON,
    JSONB as PG_JSONB,
    TIMESTAMP as PG_TIMESTAMP,
    TIME as PG_TIME,
    DATE as PG_DATE,
    BOOLEAN as PG_BOOLEAN,
)

from sqlalchemy.types import (
    Integer as Generic_Integer,
    String as Generic_String,
    Numeric as Generic_Numeric,
    Date as Generic_Date,
    DateTime as Generic_DateTime,
    Boolean as Generic_Boolean,
    Float as Generic_Float,
    LargeBinary as Generic_LargeBinary,
    JSON as Generic_JSON,
    Time as Generic_Time,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class TableRequest(BaseModel):
    db_name: str
    tables: List[str]


@app.get("/")
def load_homepage():
    return FileResponse(os.path.join("static", "index.html"))


MYSQL_CONNECTION_STRING = 'mysql+pymysql://root:Nitish%40123@localhost:3306/demo'
POSTGRES_CONNECTION_STRING = 'postgresql+psycopg2://postgres:Nitish%40123@localhost:5432/postgres'

mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
postgres_engine = create_engine(POSTGRES_CONNECTION_STRING)

already_exported_tables = {}


class PostgresToMySQLDataTypeAdapter:

    def convert(self, column_type_obj) -> str:
        cls_name = column_type_obj.__class__.__name__.upper()

        # 1) UUID -> CHAR(36)
        if isinstance(column_type_obj, PG_UUID) or cls_name == "UUID":
            return "CHAR(36)"

        # 2) BIGINT
        if isinstance(column_type_obj, PG_BIGINT) or cls_name == "BIGINT":
            return "BIGINT"

        # 3) SMALLINT
        if isinstance(column_type_obj, PG_SMALLINT) or cls_name == "SMALLINT":
            return "SMALLINT"

        # 4) INTEGER -> INT
        if (isinstance(column_type_obj, PG_INTEGER) or isinstance(column_type_obj, Generic_Integer) or cls_name == "INTEGER"):
            return "INT"
        
        # 5) DOUBLE PRECISION -> DOUBLE
        if (isinstance(column_type_obj, PG_DOUBLE_PRECISION) or (isinstance(column_type_obj, Generic_Float) and getattr(column_type_obj, "precision", None) == 53) or cls_name in ("DOUBLE_PRECISION", "DOUBLE")):
            return "DOUBLE"

        # 6) REAL -> FLOAT
        if (isinstance(column_type_obj, PG_REAL) or (isinstance(column_type_obj, Generic_Float) and getattr(column_type_obj, "precision", None) == 24) or cls_name == "REAL" or (cls_name == "FLOAT" and getattr(column_type_obj, "precision", None) is None)):
            return "FLOAT"
        
        # 7) CHAR(length)
        if isinstance(column_type_obj, PG_CHAR) or cls_name.startswith("CHAR"):
            length = getattr(column_type_obj, "length", None) or 1
            return f"CHAR({length})"

        # 8) TEXT
        if isinstance(column_type_obj, PG_TEXT) or cls_name == "TEXT":
            return "TEXT"

        # 9) VARCHAR(length)
        if (isinstance(column_type_obj, PG_VARCHAR) or isinstance(column_type_obj, Generic_String) or cls_name.startswith("VARCHAR")):
            length = getattr(column_type_obj, "length", None) or 255
            return f"VARCHAR({length})"

        # 10) DATE
        if (isinstance(column_type_obj, PG_DATE) or isinstance(column_type_obj, Generic_Date) or cls_name == "DATE"):
            return "DATE"

        # 11) TIME
        if (isinstance(column_type_obj, PG_TIME) or isinstance(column_type_obj, Generic_Time) or cls_name == "TIME"):
            return "TIME"

        # 12) TIMESTAMP (both with & without time zone) -> DATETIME 
        if (isinstance(column_type_obj, PG_TIMESTAMP) or isinstance(column_type_obj, Generic_DateTime) or cls_name == "TIMESTAMP"):
            return "DATETIME"

        # 13) BOOLEAN
        if (isinstance(column_type_obj, PG_BOOLEAN) or isinstance(column_type_obj, Generic_Boolean) or cls_name == "BOOLEAN"):
            return "BOOLEAN"

        # 14) NUMERIC/DECIMAL -> DECIMAL
        if (isinstance(column_type_obj, PG_NUMERIC) or isinstance(column_type_obj, Generic_Numeric) or cls_name in ("NUMERIC", "DECIMAL")):
            precision = getattr(column_type_obj, "precision", None) or 10
            scale = getattr(column_type_obj, "scale", None) or 0
            return f"DECIMAL({precision},{scale})"

        # 15) BYTEA -> BLOB
        if (isinstance(column_type_obj, PG_BYTEA) or isinstance(column_type_obj, Generic_LargeBinary) or cls_name == "BYTEA"):
            return "BLOB"

        # 16) JSON/JSONB -> JSON
        if (isinstance(column_type_obj, PG_JSON) or isinstance(column_type_obj, PG_JSONB) or isinstance(column_type_obj, Generic_JSON) or cls_name in ("JSON", "JSONB")):
            return "JSON"

        # 17) Default fallback to TEXT
        return "TEXT"


def generate_mysql_create_table(conn, db_name: str, table_name: str, adapter: PostgresToMySQLDataTypeAdapter):
    db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
    pg_engine = create_engine(f"{db_base}/{db_name}")
    inspector = inspect(pg_engine)

    columns = inspector.get_columns(table_name)
    try:
        pk_info = inspector.get_pk_constraint(table_name)
        pk_columns = pk_info.get("constrained_columns", []) or []
    except Exception:
        pk_columns = []

    ddl_parts = [f"CREATE TABLE `{table_name}` ("]
    col_defs = []

    for col in columns:
        name = col["name"]
        col_type_obj = col["type"]
        mysql_type = adapter.convert(col_type_obj)
        nullable = "NULL" if col["nullable"] else "NOT NULL"
        default_val = ""
        col_defs.append(f"  `{name}` {mysql_type} {nullable} {default_val}".strip())

    if pk_columns:
        pk_list = ", ".join(f"`{c}`" for c in pk_columns)
        col_defs.append(f"  PRIMARY KEY ({pk_list})")

    ddl_parts.append(",\n".join(col_defs))
    ddl_parts.append(");")
    ddl_statement = "\n".join(ddl_parts)

    # Debug print
    print(f"===== DDL FOR TABLE {table_name} =====")
    print(ddl_statement)
    print("=====================================")

    conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
    conn.execute(text(ddl_statement))


@app.get("/databases")
def fetch_postgres_databases():
    with postgres_engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT datname FROM pg_database WHERE datistemplate = false;"
        )).fetchall()
        return {"databases": [r[0] for r in rows]}


@app.get("/tables/{database_name}")
def fetch_tables(database_name: str):
    db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
    full_conn = f"{db_base}/{database_name}"
    db_engine = create_engine(full_conn)
    inspector = inspect(db_engine)
    return {"tables": inspector.get_table_names()}


@app.post("/export")
def export_feature(request: TableRequest):
    db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
    source_db = create_engine(f"{db_base}/{request.db_name}")
    inspector = inspect(source_db)

    if request.db_name not in already_exported_tables:
        already_exported_tables[request.db_name] = set()

    skipped, exported = [], []
    adapter = PostgresToMySQLDataTypeAdapter()

    with mysql_engine.connect() as mysql_conn:
        for tbl in request.tables:
            if tbl in already_exported_tables[request.db_name]:
                skipped.append(tbl)
                continue

            generate_mysql_create_table(mysql_conn, request.db_name, tbl, adapter)
            df = pd.read_sql_table(tbl, source_db)

            for colname, dtype in df.dtypes.items():
                if dtype == object:
                    sample = df[colname].dropna()
                    if not sample.empty and isinstance(sample.iloc[0], dict):
                        df[colname] = df[colname].apply(lambda v: json.dumps(v) if isinstance(v, dict) else v)

            df.to_sql(tbl, mysql_engine, if_exists='append', index=False)

            already_exported_tables[request.db_name].add(tbl)
            exported.append(tbl)

            indexes = inspector.get_indexes(tbl)
            for idx in indexes:
                index_name = idx.get("name")
                cols = []
                for c in idx.get("column_names", []):
                    col_type = df[c].dtype
                    if str(col_type) == 'object':
                        cols.append(f"{c}(255)")
                    else:
                        cols.append(f"{c}")
                unique = "UNIQUE" if idx.get("unique", False) else ""
                try:
                    mysql_conn.execute(text(
                        f"CREATE {unique} INDEX `{index_name}` "
                        f"ON `{tbl}` ({', '.join(cols)});"
                    ))
                except Exception as e:
                    print(f"Index creation failed for {index_name} on {tbl}: {e}")

    return {
        "status": "partial" if skipped else "success",
        "exported_tables": exported,
        "skipped_tables": skipped
    }


@app.post("/remove")
def remove_from_mysql(request: TableRequest):
    removed_tables = []
    failed = []

    for tbl in request.tables:
        try:
            with mysql_engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS `{tbl}`;"))
            removed_tables.append(tbl)
            already_exported_tables.get(request.db_name, set()).discard(tbl)
        except Exception as ex:
            failed.append((tbl, str(ex)))

    if failed:
        raise HTTPException(status_code=500, detail={"removed": removed_tables, "errors": failed})
    return {"removed": removed_tables}


@app.post("/reset")
def reset_mysql():
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


@app.get("/schema/{db_name}/{table_name}")
def fetch_table_schema(db_name: str, table_name: str):
    db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
    db_conn = create_engine(f"{db_base}/{db_name}")
    inspector = inspect(db_conn)

    raw_columns = inspector.get_columns(table_name)
    processed_columns = []
    for col in raw_columns:
        processed_columns.append({
            "name": col["name"],
            "type": str(col["type"]),
            "nullable": col["nullable"],
            "default": col.get("default")
        })

    raw_indexes = inspector.get_indexes(table_name)
    processed_indexes = []
    for idx in raw_indexes:
        processed_indexes.append({
            "name": idx.get("name"),
            "column_names": idx.get("column_names", []),
            "unique": idx.get("unique", False)
        })

    return {
        "columns": processed_columns,
        "indexes": processed_indexes
    }


@app.get("/indexes/{db_name}/{table_name}")
def list_indexes(db_name: str, table_name: str):
    try:
        db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
        conn = create_engine(f"{db_base}/{db_name}")
        inspector = inspect(conn)
        raw_indexes = inspector.get_indexes(table_name)
        return {"indexes": [
            {
                "name": idx.get("name"),
                "columns": idx.get("column_names", []),
                "unique": idx.get("unique", False)
            } for idx in raw_indexes
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_mysql_ddl(db_name: str, table_name: str) -> str:
    db_base = POSTGRES_CONNECTION_STRING.rsplit('/', 1)[0]
    engine = create_engine(f"{db_base}/{db_name}")
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)

    ddl_parts = [f"CREATE TABLE `{table_name}` ("]
    col_defs = []
    adapter = PostgresToMySQLDataTypeAdapter()

    for column in columns:
        col_name     = column["name"]
        col_type_obj = column["type"]
        sql_type     = adapter.convert(col_type_obj)
        nullable     = "NULL" if column["nullable"] else "NOT NULL"
        default_val  = "" 
        col_defs.append(f"  `{col_name}` {sql_type} {nullable} {default_val}".strip())

    ddl_parts.append(",\n".join(col_defs))
    ddl_parts.append(");")
    return "\n".join(ddl_parts)


@app.get("/schema-ddl/{db_name}/{table_name}")
def fetch_table_ddl(db_name: str, table_name: str):
    try:
        ddl = generate_mysql_ddl(db_name, table_name)
        return {"ddl": ddl}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    