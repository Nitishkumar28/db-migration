from fastapi import APIRouter
from fastapi import HTTPException
from core.data import ExportRequest
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

router = APIRouter()

@router.get("/")
def load_homepage():
    return {"result": "data"}

@router.get("/databases/{db_type}")
def fetch_databases(db_type):
    print("Fetch Databases")
    databases = get_databases(db_type)
    return {"result": [r[0] for r in databases]}

@router.get("/tables/{db_type}/{db_name}")
def fetch_table_names_from_db(db_type, db_name):
    table_names = get_table_names(db_type, db_name)
    return {"result": table_names}

@router.delete("/tables/{db_type}/{db_name}/{table_name}")
def remove_table(db_type, db_name, table_name):
    ack = delete_tables(db_type, db_name, table_name)
    if ack:
        return {"message": f"Table '{table_name}' deleted from {db_type}:{db_name}"}
    return {"message": f"Error occurred while deleting {table_name}"}

@router.delete("/tables/{db_type}/{db_name}")
def remove_tables(db_type, db_name):
    ack = delete_tables(db_type, db_name)
    if ack:
        return {"message": f"All tables deleted from {db_type}:{db_name}"}
    return {"message": f"Error occurred while deleting tables from {db_type}:{db_name}"}

@router.get("/indexes/{db_type}/{db_name}/{table_name}")
def fetch_indexes_for_table(db_type, db_name, table_name):
    indexes = get_indexes_info(db_type, db_name, table_name)
    return {"result": indexes}

@router.get("/schema/{db_type}/{db_name}/{table_name}")
def fetch_table_schema(db_type, db_name, table_name):
    schema = get_table_schema(db_type, db_name, table_name)
    return {"result": schema}

@router.get("/schema-ddl/{db_type}/{db_name}/{table_name}")
def fetch_table_ddl(db_type, db_name, table_name):
    table_ddl = get_table_ddl(db_type, db_name, table_name)
    return {"result": table_ddl}

@router.get("/triggers/{db_type}/{db_name}/{table_name}")
def fetch_triggers(db_type, db_name, table_name):
    trigger_data_for_table = get_triggers_for_table(db_type, db_name, table_name)
    return {"results": trigger_data_for_table}

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
    ack = export_tables(**args)
    print(ack)
    if ack:
        return {"results": True}
    return {"results": False}


@router.post("/export-triggers/")
def export_triggers_to_target(request: ExportRequest):
    result = export_triggers(
        {"db_type": request.source.db_type, 
         "db_name": request.source.db_name
        },
        {"db_type": request.target.db_type,
         "db_name": request.target.db_name
        },
    )
    if result["errors"]:
        raise HTTPException(status_code=500, detail=result)
    return {"exported_triggers": result["exported"]}
