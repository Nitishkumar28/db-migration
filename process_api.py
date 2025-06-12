import pandas as pd
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, inspect, text
import os
from dotenv import load_dotenv
from functools import lru_cache

from typing import List, Optional

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



load_dotenv() 


POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")

MYSQL_USER     = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST     = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT     = os.getenv("MYSQL_PORT", "3306")




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




'''
@router.post("/export")
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

@router.get("/schema-ddl/{database_name}/{table_name}")
def fetch_table_ddl(database_name: str, table_name: str):
    try:
        table_ddl = generate_mysql_ddl(database_name, table_name)
        return {"ddl": table_ddl}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.get("/triggers/{database_name}/{table_name}", response_model=TriggerModel)
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


@router.post("/export-triggers")
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
'''