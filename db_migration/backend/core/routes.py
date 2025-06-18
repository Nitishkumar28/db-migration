from tabnanny import check
from fastapi import APIRouter
from fastapi import HTTPException
from core.data import DBInfo, ExportRequest, TriggerRequest
from core.db.db_utils import (
    get_databases,
    get_table_names,
    get_indexes_info,
    get_table_schema,
    get_table_ddl,
    get_triggers_for_table,
    export_tables,
    delete_tables,
    export_triggers
    )
from core.db.db_connect import get_db_engine

router = APIRouter()

@router.get("/")
def load_homepage():
    try:
        return {"result": "data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.post("/check-connection/")
def check_connection(request: DBInfo):
    try:
        args = {
            "host_name": request.host_name,
            "username": request.username,
            "password": request.password,
            "port": request.port,
            "db_name": request.db_name,
        }
        check_connection_res = get_db_engine(**args)
        return {"results": check_connection_res is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection check failed: {e}")


@router.get("/databases/{db_type}")
def fetch_databases(db_type):
    print("Fetch Databases")
    try:
        databases = get_databases(db_type)
        return {"result": [r[0] for r in databases]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching databases: {e}")

@router.get("/tables/{db_type}/{db_name}")
def fetch_table_names_from_db(db_type, db_name):
    try:
        table_names = get_table_names(db_type, db_name)
        return {"result": table_names}
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tables: {e}")


@router.delete("/tables/{db_type}/{db_name}/{table_name}")
def remove_table(db_type, db_name, table_name):
    try:
        ack = delete_tables(db_type, db_name, table_name)
        return {"message": ack}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting table '{table_name}': {e}")

@router.delete("/tables/{db_type}/{db_name}")
def remove_tables(db_type, db_name):
    try:
        ack = delete_tables(db_type, db_name)
        return {"message": ack}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting tables from {db_type}:{db_name}: {e}")

@router.get("/indexes/{db_type}/{db_name}/{table_name}")
def fetch_indexes_for_table(db_type, db_name, table_name):
    try:
        indexes = get_indexes_info(db_type, db_name, table_name)
        return {"result": indexes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching indexes: {e}")

@router.get("/schema/{db_type}/{db_name}/{table_name}")
def fetch_table_schema(db_type, db_name, table_name):
    try:
        schema = get_table_schema(db_type, db_name, table_name)
        return {"result": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schema: {e}")

@router.get("/schema-ddl/{db_type}/{db_name}/{table_name}")
def fetch_table_ddl(db_type, db_name, table_name):
    try:
        table_ddl = get_table_ddl(db_type, db_name, table_name)
        return {"result": table_ddl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching DDL: {e}")
    

@router.get("/triggers/{db_type}/{db_name}/{table_name}")
def fetch_triggers(db_type, db_name, table_name):
    try:
        trigger_data_for_table = get_triggers_for_table(db_type, db_name, table_name)
        return {"results": trigger_data_for_table}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching triggers: {e}")

@router.post("/export/")
def export_tables_to_target(request: ExportRequest):
    """
    Request Body:
    {
        "source": {
            "db_type": db_type,
            "db_name": db_name
        },
        "target": {
            "db_type": db_type,
            "db_name": db_name
        },
        "tables_names": [
            table1,
            table2,
            ...
        ]
    }
    """
    print(request, type(request))
    try:
        args = {
        "source": {
            "db_type": request.source.db_type,
            "db_name": request.source.db_name
        },
        "target": {
            "db_type": request.target.db_type,
            "db_name": request.target.db_name
        },
        "table_names": request.table_names
        }
        exported, skipped = export_tables(**args)
        if skipped:
            raise HTTPException(
                status_code=500,
                detail={"exported": list(exported), "skipped": list(skipped)}
            )
        return {"exported": list(exported)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting tables: {e}")


@router.post("/export-triggers/")
def export_triggers_to_target(request: TriggerRequest):
    try:
        result = export_triggers(
            {"db_type": request.source.db_type, 
            "db_name": request.source.db_name
            },
            {"db_type": request.target.db_type,
            "db_name": request.target.db_name
            },
        )
        if result["errors"]:
                raise HTTPException(status_code=500,detail=result)
        return {"exported_triggers": result["exported"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting triggers: {e}")
