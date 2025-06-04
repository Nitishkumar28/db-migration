from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import os

app = FastAPI()

# handle frontend-backend communication (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files like HTML, JS, CSS, and Images
app.mount("/static", StaticFiles(directory="static"), name="static")

class TableRequest(BaseModel):
    db_name: str
    tables: List[str]

@app.get("/")
def load_homepage():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)

MYSQL_CONNECTION_STRING = 'mysql+pymysql://root:Nitish%40123@localhost:3306/demo'
POSTGRES_CONNECTION_STRING = 'postgresql+psycopg2://postgres:Nitish%40123@localhost:5432/postgres'

mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
postgres_engine = create_engine(POSTGRES_CONNECTION_STRING)

already_exported_tables = {}

class PostgresToMySQLDataTypeAdapter:
    def __init__(self):
        self.type_map = {
            "INTEGER": "INT",
            "BIGINT": "BIGINT",
            "SMALLINT": "SMALLINT",
            "VARCHAR": "VARCHAR(255)",
            "CHAR": "CHAR(10)",
            "TEXT": "TEXT",
            "DATE": "DATE",
            "BOOLEAN": "BOOLEAN",
            "TIMESTAMP": "DATETIME",
            "TIME": "TIME",
            "NUMERIC": "DECIMAL(10,2)",
            "DECIMAL": "DECIMAL(10,2)",
            "REAL": "FLOAT",
            "DOUBLE_PRECISION": "DOUBLE",
            "BYTEA": "BLOB",
            "JSON": "JSON",
            "JSONB": "JSON",
            "UUID": "CHAR(36)",
        }

    def convert(self, column_type_obj) -> str:
        type_name = column_type_obj.__class__.__name__.upper()
        if type_name not in self.type_map:
            print(f"[WARN] Unrecognized PostgreSQL type: {type_name}, defaulting to TEXT")
        return self.type_map.get(type_name, "TEXT")

@app.get("/databases")
def fetch_postgres_databases():
    with postgres_engine.connect() as conn:
        databases = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;")).fetchall()
        return {"databases": [row[0] for row in databases]}
    

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

    for tbl in request.tables:
        if tbl in already_exported_tables[request.db_name]:
            skipped.append(tbl)
        else:
            df = pd.read_sql_table(tbl, source_db)
            df.to_sql(tbl, mysql_engine, if_exists='replace', index=False)
            already_exported_tables[request.db_name].add(tbl)
            exported.append(tbl)

            indexes = inspector.get_indexes(tbl)
            with mysql_engine.connect() as mysql_conn:
                for idx in indexes:
                    index_name = idx.get("name")
                    columns = []
                    for col in idx.get("column_names", []):
                        col_type = df[col].dtype
                        if str(col_type) == 'object':
                            columns.append(f"{col}(255)")
                        else:
                            columns.append(f"{col}")
                    unique = "UNIQUE" if idx.get("unique", False) else ""
                    try:
                        mysql_conn.execute(text(f"CREATE {unique} INDEX `{index_name}` ON `{tbl}` ({', '.join(columns)});"))
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
                conn.execute(text(f"DROP TABLE IF EXISTS `{tbl}`"))
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
        for tbl in list(table_set):
            try:
                with mysql_engine.connect() as conn:
                    conn.execute(text(f"DROP TABLE IF EXISTS `{tbl}`"))
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
    return {
        "columns": inspector.get_columns(table_name),
        "indexes": inspector.get_indexes(table_name)
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
                "name": idx["name"],
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
        col_name = column['name']
        pg_type = str(column['type'])
        sql_type = adapter.convert(pg_type)
        nullable = "NULL" if column['nullable'] else "NOT NULL"
        default_val = f"DEFAULT {column['default']}" if column['default'] else ""

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