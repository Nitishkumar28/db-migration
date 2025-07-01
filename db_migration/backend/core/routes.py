import stat
from fastapi import APIRouter, Depends, Response
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
import time

from core.db.db_utils import (
    get_databases,
    get_table_names,
    get_indexes_info,
    get_table_schema,
    get_table_ddl,
    get_triggers_for_table,
    export_tables,
    delete_tables,
    export_triggers,
    run_query
    )

from core.database import get_db
from core.stats import collect_combined_stats, validate_export_success
from core.data import (
    DBInfo,
    ExportRequest,
    StatRequest,
    MigrationHistorySchema,
    MigrationHistorySchemaBrief,
    MigrationHistorySchemaBriefInput,
    MigrationHistoryUpdateSchema,
    MigrationHistoryItemSchema,
    TestModelSchema
    )
from core.models import MigrationHistory, TestModel
from core.views import (
    create_initial_job,
    get_migration_for_jobid,
    get_full_history,
    get_full_history_brief,
    update_migration_data,
    get_full_history_items,
    create_history_item,
    delete_history_for_jobid,
    delete_history_item,

    drop_table
    )

from core.logging import logger, RUN_ID, get_next_log_counter
from datetime import datetime
from core.db.db_connect import get_db_engine
from core.secret_manager import set_db_secrets_for_db, get_secret

from core.schemas import SignUpRequest, LoginRequest, TokenRequest
from core.signup import register_user, authenticate_user
from core.authentication import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/")
def load_homepage():
    try:
        return {"result": "data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/test")
def get_data(db: Session = Depends(get_db)):
    return db.query(TestModel).all()

@router.post("/test")
def create_data(request: TestModelSchema, db: Session = Depends(get_db)):
    new_data = TestModel(**dict(request))
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.patch("/test")
def update_data(request: TestModelSchema, db: Session = Depends(get_db)):
    db_obj = db.query(TestModel).filter_by(id=request.id).first()

    if not db_obj:
        return None

    for field, value in request.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/test/{id}")
def delete_data(id, db: Session = Depends(get_db)):
    db_obj = db.query(TestModel).filter_by(id=id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        print("deleted")
    return

        




@router.post("/check-connection/")
def check_connection(request: DBInfo):
    try:
        print(request)
        check_connection_stat = True
        args = {
            "host_name": request.host_name,
            "username": request.username,
            "password": request.password,
            "port": request.port,
            "db_name": request.db_name,
            "db_type": request.db_type,
            "check_connection_status": check_connection_stat
        }
        db_name = request.db_name
        if request.db_type != "postgresql" and db_name != "":
            run_query(f"CREATE DATABASE IF NOT EXISTS {db_name}", request.db_type, check_connection_status=check_connection_stat)
        check_connection_res = get_db_engine(**args)
        print("SUCESS")
        return {"results": check_connection_res is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection check failed: {e}")


@router.get("/databases/{db_type}")
def fetch_databases(db_type):
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
    logger.info("=== Section: Deleting Tables ===")
    try:
        ack = delete_tables(db_type, db_name, table_name)
        for tbl, msg in ack["removed"]:
            logger.info(f"Deleted table `{tbl}`{': ' + msg if msg else ''}")
        logger.info(f"=== Deleted {len(ack['removed'])} tables ===\n")
        return {"message": ack}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting table '{table_name}': {e}")

@router.delete("/tables/{db_type}/{db_name}")
def remove_tables(db_type, db_name):
    logger.info("=== Section: Deleting All Tables ===")
    try:
        ack = delete_tables(db_type, db_name)
        for tbl, msg in ack["removed"]:
            logger.info(f"Deleted table `{tbl}`{': ' + msg if msg else ''}")
        logger.info(f"=== Deleted {len(ack['removed'])} tables ===\n")
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


@router.post("/signup", response_model=TokenRequest)
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    token = register_user(data, db)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenRequest)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    token = authenticate_user(data, db)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,                 
        secure=False,                  
        samesite="none",                
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/" # cookies enabled for all paths
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/export/")
def export_feature(request: ExportRequest, db: Session = Depends(get_db)):
    """
    Request Body:
    {
        "job_id": int,
        "source": {
            "host_name":"",
            "username": "",
            "password": "",
            "port": "",
            "db_type": db_type,
            "db_name": db_name
        },
        "target": {
            "host_name": "",
            "username": "",
            "password": "",
            "port": "",
            "db_type": db_type,
            "db_name": db_name
        }
    }
    """
    logger.info("=== Section: Export Tables & Data ===")
    source_details = dict(request.source)
    target_details = dict(request.target)
    set_db_secrets_for_db(source_details["db_type"], source_details)
    set_db_secrets_for_db(target_details["db_type"], target_details)
    print("connection_details")
    print(source_details, target_details)
    try:
        start_time = time.time()
        job_id = request.job_id
        exported, skipped, durations = export_tables(source=source_details, target=target_details)
        logger.info(f"=== Tables exported: {len(exported)}; skipped: {len(skipped)} ===\n")

        if skipped:
            raise HTTPException(
                status_code=500,
                detail={"exported": list(exported), "skipped": list(skipped)}
            )
        
        logger.info("=== Section: Export Triggers ===")
        result = export_triggers(source=source_details, target=target_details)

        end_time = time.time()

        total_time = (end_time - start_time)
        update_data = {
            "total_migration_time": total_time
        }
        update_migration_data(job_id, update_data, db)


        logger.info(f"=== ✅ Triggers exported: {len(result.get('exported', []))}; errors: {len(result.get('errors', []))} ===\n")

        if result["errors"]:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Table export succeeded, but trigger export failed.",
                    "exported_tables": list(exported),
                    "exported_triggers": result.get("exported", []),
                    "trigger_errors": result["errors"]
                }
            )
        
        
        logger.info(f"API `/export/` succeeded: exported_tables={exported}, exported_triggers={result.get('exported', [])}")


        
        return {
            "message": "Tables and triggers exported successfully.",
            "exported_tables": list(exported),
            "exported_triggers": result.get("exported", []),
            "durations": durations
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error during `/export/`")
        raise HTTPException(status_code=500, detail=f"Error exporting tables: {e}")


@router.post("/get-stats/")
def stats_display(request: StatRequest, db: Session = Depends(get_db)):
    source_details = dict(request.source)
    target_details = dict(request.target)
    set_db_secrets_for_db(source_details["db_type"], source_details)
    set_db_secrets_for_db(target_details["db_type"], target_details)
    durations = request.durations
    stats = collect_combined_stats(source_details, target_details)
    print("HI STATS")
    for stat in stats:
        current_stat = {
            "job_id": request.job_id,
            "name": stat["table_name"],
            "source_total_rows": stat["source_rows"],
            "target_total_rows": stat["target_rows"],
            "index_validation": stat["index_count"],
            "primary_key_validation": stat["primary_key_count"],
            "foreign_key_validation": stat["foreign_key_count"],
            "trigger_count": stat["trigger_count"],
            "duration": durations.get(stat["table_name"], 0)
        }
        print("History Item Created!")
        create_history_item(current_stat, db)
    print("Stats Updated")
    return { "result": stats }


@router.post("/migration-history/create", response_model=MigrationHistorySchemaBrief)
def create_migration(history: MigrationHistorySchemaBriefInput, db: Session = Depends(get_db)):
    created_obj = create_initial_job(history, db)
    return created_obj

@router.patch("/migration-history/{job_id}", response_model=MigrationHistoryUpdateSchema)
def update_migration(job_id, history_update: MigrationHistoryUpdateSchema, db: Session = Depends(get_db)):
    result = update_migration_data(job_id, history_update, db)
    return result

@router.get("/migration-history/{job_id}")
def get_migration(job_id: int, db: Session = Depends(get_db)):
    data = get_migration_for_jobid(job_id, db)
    if data is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return data

@router.get("/migration-history/", response_model=List[MigrationHistorySchema])
def get_migrations(db: Session = Depends(get_db)):
    return get_full_history(db)

@router.get("/migration-history/brief/", response_model=List[MigrationHistorySchemaBrief])
def get_migrations_brief(db: Session = Depends(get_db)):
    return get_full_history_brief(db)


@router.delete("/migration-history/{job_id}", status_code=204)
def delete_migration(job_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(MigrationHistory).filter_by(job_id=job_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Migration job not found")

    db.delete(db_obj)
    db.commit()
    return

# History Items

@router.get("/migration-history-items/", response_model=List[MigrationHistoryItemSchema])
def get_migration_items(db: Session = Depends(get_db)):
    return get_full_history_items(db)


@router.post("/migration-history-items/create", response_model=MigrationHistoryItemSchema)
def post_migration_items(item_obj: MigrationHistoryItemSchema, db: Session = Depends(get_db)):
    return create_history_item(item_obj, db)


# @router.delete("/migration-history-items/", status_code=204)
# def delete_migration():
#     # delete_history_item(id, db)
#     drop_table("history_item")
#     return "dropped"

@router.post("/validate/")
def validate_stats_data(request: ExportRequest, db: Session = Depends(get_db)):
    job_id = request.job_id
    source_details = dict(request.source)
    target_details = dict(request.target)
    set_db_secrets_for_db(source_details["db_type"], source_details)
    set_db_secrets_for_db(target_details["db_type"], target_details)
    final_validation_result = validate_export_success(source_details, target_details)
    final_status = "completed" if final_validation_result else "failed"
    update_migration_data(job_id, {"status": final_status}, db)
    return final_status