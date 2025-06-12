from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import json
import os
import re
from dotenv import load_dotenv
from functools import lru_cache

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
    INTERVAL as PostGre_INTERVAL,
    ENUM as PostGre_ENUM,
    MONEY as PostGre_MONEY,
    OID as PostGre_OID,
    BIT as PostGre_BIT,
    ARRAY as PostGre_ARRAY,
    INT4RANGE as PostGre_INT4RANGE,
    INT4MULTIRANGE as PostGre_INT4MULTIRANGE,
    INT8RANGE as PostGre_INT8RANGE,
    INT8MULTIRANGE as PostGre_INT8MULTIRANGE,
    TSRANGE as PostGre_TSRANGE,
    TSTZRANGE as PostGre_TSTZRANGE,
    TSTZMULTIRANGE as PostGre_TSTZMULTIRANGE,
    DATERANGE as PostGre_DATERANGE,
    TSVECTOR as PostGre_TSVECTOR,
    TSQUERY as PostGre_TSQUERY,
    INET as PostGre_INET,
    CIDR as PostGre_CIDR,
    MACADDR as PostGre_MACADDR,
    MACADDR8 as PostGre_MACADDR8,
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

load_dotenv() 

class TableModel(BaseModel):
    db_name: str
    tables: List[str]


class TriggerModel(BaseModel):
    name: str
    timing: str
    event: str
    statement: str


POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")

MYSQL_USER     = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST     = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT     = os.getenv("MYSQL_PORT", "3306")


@app.get("/")
def load_homepage():
    return FileResponse(os.path.join("static", "index.html"))


@lru_cache(maxsize=None)
def db_engine(db_engine_type: str, database: Optional[str] = "postgres"):
    if db_engine_type == "mysql":
        if not database:
            raise ValueError("MySQL database name must be given")
        url = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{database}"
        )
    elif db_engine_type == "postgres":
        url = (
            f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{database}"
        )
    else:
        raise ValueError(f"DB engine '{db_engine_type}' not supported")
    return create_engine(url)


mysql_engine = None
postgres_engine = db_engine("postgres")
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
        
        # 9) ENUM -> VARCHAR(255)
        if isinstance(column_object_type, PostGre_ENUM) or data_class_name == "ENUM":
            return "VARCHAR(255)"

        # 10) VARCHAR(length)
        if (
            isinstance(column_object_type, PostGre_VARCHAR)
            or isinstance(column_object_type, Gen_String)
            or data_class_name.startswith("VARCHAR")
        ):
            length = getattr(column_object_type, "length", None) or 255
            return f"VARCHAR({length})"

        # 11) DATE
        if (
            isinstance(column_object_type, PostGre_DATE)
            or isinstance(column_object_type, Gen_Date)
            or data_class_name == "DATE"
        ):
            return "DATE"

        # 12) TIME
        if (
            isinstance(column_object_type, PostGre_TIME)
            or isinstance(column_object_type, Gen_Time)
            or data_class_name == "TIME"
        ):
            return "TIME"

        # 13) TIMESTAMP (both with & without time zone) -> DATETIME
        if (
            isinstance(column_object_type, PostGre_TIMESTAMP)
            or isinstance(column_object_type, Gen_DateTime)
            or data_class_name == "TIMESTAMP"
        ):
            return "DATETIME"

        # 14) BOOLEAN
        if (
            isinstance(column_object_type, PostGre_BOOLEAN)
            or isinstance(column_object_type, Gen_Boolean)
            or data_class_name == "BOOLEAN"
        ):
            return "BOOLEAN"

        # 15) NUMERIC/DECIMAL -> DECIMAL
        if (
            isinstance(column_object_type, PostGre_NUMERIC)
            or isinstance(column_object_type, Gen_Numeric)
            or data_class_name in ("NUMERIC", "DECIMAL")
        ):
            precision = getattr(column_object_type, "precision", None) or 10
            scale = getattr(column_object_type, "scale", None) or 0
            return f"DECIMAL({precision},{scale})"

        # 16) BYTEA -> BLOB
        if (
            isinstance(column_object_type, PostGre_BYTEA)
            or isinstance(column_object_type, Gen_LargeBinary)
            or data_class_name == "BYTEA"
        ):
            return "BLOB"

        # 17) JSON/JSONB -> JSON
        if (
            isinstance(column_object_type, PostGre_JSON)
            or isinstance(column_object_type, PostGre_JSONB)
            or isinstance(column_object_type, Gen_JSON)
            or data_class_name in ("JSON", "JSONB")
        ):
            return "JSON"

        # 18) ARRAY -> JSON
        if isinstance(column_object_type, PostGre_ARRAY) or data_class_name == "ARRAY":
            return "JSON"

        # 19) Range types -> JSON
        if (
            isinstance(column_object_type, (PostGre_INT4RANGE, PostGre_INT8RANGE,
                                            PostGre_TSRANGE, PostGre_TSTZRANGE,
                                            PostGre_DATERANGE))
            or data_class_name in ("INT4RANGE", "INT8RANGE", "TSRANGE", "TSTZRANGE", "DATERANGE")
        ):
            return "JSON"

        # 20) Multirange types -> JSON
        if (
            isinstance(column_object_type, (PostGre_INT4MULTIRANGE,
                                            PostGre_INT8MULTIRANGE,
                                            PostGre_TSTZMULTIRANGE))
            or data_class_name in ("INT4MULTIRANGE", "INT8MULTIRANGE", "TSTZMULTIRANGE")
        ):
            return "JSON"

        # 21) INET / CIDR -> VARCHAR(45)
        if (isinstance(column_object_type, (PostGre_INET, PostGre_CIDR))
            or data_class_name in ("INET", "CIDR")
        ):
            return "VARCHAR(45)"

        # 22) MACADDR -> VARBINARY(6)
        if (isinstance(column_object_type, (PostGre_MACADDR, PostGre_MACADDR8))
            or data_class_name in ("MACADDR", "MACADDR8")
        ):
            return "VARBINARY(6)"

        # 23) Full-text -> TEXT
        if (isinstance(column_object_type, (PostGre_TSVECTOR, PostGre_TSQUERY))
            or data_class_name in ("TSVECTOR", "TSQUERY")
        ):
            return "TEXT"

        # 24) BIT -> BIT
        if isinstance(column_object_type, PostGre_BIT) or data_class_name == "BIT":
            length = getattr(column_object_type, "length", None) or 1
            return f"BIT({length})"
       

        # 25) INTERVAL -> TIME
        if isinstance(column_object_type, PostGre_INTERVAL) or data_class_name == "INTERVAL":
            return "TIME"

        # 26) MONEY -> DECIMAL(19,4)
        if isinstance(column_object_type, PostGre_MONEY) or data_class_name == "MONEY":
            return "DECIMAL(19,4)"

        # 27) OID -> INT UNSIGNED
        if isinstance(column_object_type, PostGre_OID) or data_class_name == "OID":
            return "INT UNSIGNED"

        # 28) Default fallback to TEXT
        return "TEXT"


def generate_mysql_create_table(
    connection,
    database_name: str,
    table_name: str,
    adapter: PostgresToMySQLDataTypeAdapter,
):
    postgre_eng = db_engine("postgres", database_name)
    inspector = inspect(postgre_eng)

    columns = inspector.get_columns(table_name)
    try:
        pk_info = inspector.get_pk_constraint(table_name)
    except Exception:
        pk_info = {}
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
    engine = db_engine("postgres", database_name)
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}


@app.post("/export")
def export_button(request: TableModel):
    request_database = db_engine("postgres", request.db_name)
    inspector = inspect(request_database)

    if request.db_name not in already_exported_tables:
        already_exported_tables[request.db_name] = set()

    skipped, exported = [], []
    adapter = PostgresToMySQLDataTypeAdapter()

    with db_engine("mysql", request.db_name).connect() as mysql_conn:
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

            df.to_sql(each_tbl, mysql_conn, if_exists="append", index=False)

            already_exported_tables[request.db_name].add(each_tbl)
            exported.append(each_tbl)

            indexes = inspector.get_indexes(each_tbl)

            for index in indexes:
                index_name = index["name"]
                columns     = index["column_names"]
                unique   = "UNIQUE " if index.get("unique", False) else ""

                column_list = [f"`{col}`" for col in columns]

                create_idx_sql = (
                    f"CREATE {unique}INDEX `{index_name}` "
                    f"ON `{each_tbl}` ({', '.join(column_list)});"
                )

                mysql_conn.execute(text(create_idx_sql))

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
            with db_engine("mysql", request.db_name).connect() as mysql_conn:
                mysql_conn.execute(text(f"DROP TABLE IF EXISTS `{each_tbl}`;"))
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
        for tbl in list(table_set):
            with db_engine("mysql", dbname).connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS `{tbl}`;"))
                dropped.append(tbl)
    already_exported_tables.clear()
    return {"reset": True, "dropped_tables": dropped}


@app.get("/schema/{database_name}/{table_name}")
def fetch_table_schema(database_name: str, table_name: str):
    engine = db_engine("postgres", database_name)
    inspector = inspect(engine)

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
        engine = db_engine("postgres", database_name)
        inspector = inspect(engine)
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
    engine = db_engine("postgres", database_name)
    inspector = inspect(engine)
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


@app.get("/triggers/{database_name}/{table_name}", response_model=List[TriggerModel])
def fetch_triggers(database_name: str, table_name: str):
    engine = db_engine("postgres", database_name)

    sql = """
    SELECT
      trigger_name    AS name,
      action_timing   AS timing,
      event_manipulation AS event,
      action_statement   AS statement
    FROM information_schema.triggers
    WHERE event_object_table = :tbl
      AND trigger_schema = 'public';
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql), {"tbl": table_name}).fetchall()

    return [
        TriggerModel(
            name=row.name,
            timing=row.timing,
            event=row.event,
            statement=row.statement.strip(),
        )
        for row in rows
    ]


@app.post("/export-triggers")
def export_triggers(request: TableModel):
    pg_engine = db_engine("postgres", request.db_name)

    exported = []
    errors = []

    with db_engine("mysql", request.db_name).connect() as mysql_conn, pg_engine.connect() as pg_conn:
        pg_inspector = inspect(pg_engine)

        for each_table in request.tables:
            column_names = [c["name"] for c in pg_inspector.get_columns(each_table)]

            def build_json(alias: str) -> str:
                pairs = ", ".join(f"'{c}', {alias}.{c}" for c in column_names)
                return f"JSON_OBJECT({pairs})"
            

            rows = pg_conn.execute(
                text(
                    """
                SELECT trigger_name,
                       action_timing,
                       event_manipulation,
                       action_statement
                  FROM information_schema.triggers
                 WHERE event_object_table = :tbl
                   AND trigger_schema      = 'public';
                """
                ),
                {"tbl": each_table},
            ).fetchall()

            for row in rows:
                name = row.trigger_name
                timing = row.action_timing
                event = row.event_manipulation.upper()
                statement = row.action_statement.strip()

                try:
                    trigger_name = f"{name}_{event.lower()}"
                    mysql_conn.execute(
                        text(f"DROP TRIGGER IF EXISTS `{trigger_name}`;")
                    )

                    check = re.match(r"EXECUTE FUNCTION ([\w_]+)\(\)", statement, re.I)
                    if not check:
                        raise ValueError(f"Unsupported action: {statement}")
                    function_type = check.group(1)

                    defintion_state = pg_conn.execute(
                        text(
                            """
                        SELECT pg_get_functiondef(p.oid)
                          FROM pg_proc p
                          JOIN pg_namespace n ON p.pronamespace = n.oid
                         WHERE p.proname  = :func
                           AND n.nspname = 'public';
                        """
                        ),
                        {"func": function_type},
                    ).scalar_one()

                    patterns = {
                        "INSERT": r"IF\s+TG_OP\s*=\s*'INSERT'\s+THEN(.*?)ELSIF",
                        "UPDATE": r"ELSIF\s+TG_OP\s*=\s*'UPDATE'\s+THEN(.*?)ELSIF",
                        "DELETE": r"ELSIF\s+TG_OP\s*=\s*'DELETE'\s+THEN(.*?)END IF",
                    }
                    body_match = re.search(
                        patterns[event], defintion_state, re.S | re.I
                    )
                    if not body_match:
                        raise ValueError(f"Could not extract body for {event}")

                    body_sql = body_match.group(1)
                    body_sql = re.sub(
                        r"\bRETURN\b[^\n;]*[;\n]?", "", body_sql, flags=re.I
                    )
                    body_sql = re.sub(r"--.*?$", "", body_sql, flags=re.M)
                    body_sql = body_sql.replace("TG_OP", f"'{event}'")
                    body_sql = re.sub(
                        r"\bto_jsonb\s*\(\s*NEW\s*\)",
                        build_json("NEW"),
                        body_sql,
                        flags=re.I,
                    )
                    body_sql = re.sub(
                        r"\bto_jsonb\s*\(\s*OLD\s*\)",
                        build_json("OLD"),
                        body_sql,
                        flags=re.I,
                    )

                    body_sql = body_sql.strip().rstrip(";")
                    ddl = f"""
                    CREATE TRIGGER `{trigger_name}`
                    {timing} {event} ON `{each_table}`
                    FOR EACH ROW
                    BEGIN
                      {body_sql};
                    END;"""
                    mysql_conn.execute(text(ddl))
                    exported.append(trigger_name)

                except Exception as e:
                    errors.append({"trigger": name, "event": event, "error": str(e)})

    if errors:
        raise HTTPException(
            status_code=500, detail={"exported": exported, "errors": errors}
        )

    return {"exported_triggers": exported}

