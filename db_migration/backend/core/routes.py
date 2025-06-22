from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import Session as _Session
from core.data import DBInfo, ExportRequest, CreateJobRequest
from core.db.db_connect import get_db_engine, get_postgresql_db_engine
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

from core.stats import (
    collect_export_durations,
    collect_source_stats,
    collect_target_stats,
    collect_combined_stats,
    collect_index_names,
    collect_primary_key_names,
    collect_foreign_key_names,
    collect_trigger_names
)
from core.job import create_job_record
from core.logging import logger, RUN_ID, get_next_log_counter
from datetime import datetime
import time
from core.job import update_job_status, create_job_record
from core.models import Job

router = APIRouter()

def get_db():
    engine = get_postgresql_db_engine()
    if engine is None:
        raise HTTPException(500, "Could not connect to jobs database")
    with _Session(engine) as db:
        yield db


@router.get("/")
def load_homepage():
    try:
        return {"result": "data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    

@router.post("/check-connection/")
def check_connection(request: DBInfo):
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
    print(check_connection_res)
    if check_connection_res is not None:
        print("SUCESS")
        return {"results": True}
    return {"results": False}
    

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


@router.post("/jobs/create")
def create_job(request: CreateJobRequest, db: Session = Depends(get_db)):
    job = create_job_record(
        db,
        source_db_type=request.source_db_type,
        source_db_name=request.source_db_name,
        target_db_type=request.target_db_type,
        target_db_name=request.target_db_name
    )
    return {"result": True, "job_id": job.job_id}


@router.post("/export/")
def export_feature(request: ExportRequest, db: Session = Depends(get_db)):
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
    logger.info("=== Section: Export Tables & Data ===")
    job = create_job_record(
        db,
        source_db_type = request.source.db_type,
        source_db_name = request.source.db_name,
        target_db_type = request.target.db_type,
        target_db_name = request.target.db_name
    )
    start = datetime.utcnow()

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
        }


        exported, skipped, durations = export_tables(**args)
        logger.info(f"=== Tables exported: {len(exported)}; skipped: {len(skipped)} ===\n")

        if skipped:
            raise HTTPException(
                status_code=500,
                detail={"exported": list(exported), "skipped": list(skipped)}
            )
        
        logger.info("=== Section: Export Triggers ===")

        result = export_triggers(
            args["source"],
            args["target"]
        )

        timing = collect_combined_stats(
            {"db_type": request.source.db_type, "db_name": request.source.db_name},
            {"db_type": request.target.db_type, "db_name": request.target.db_name}
        )

        end = datetime.utcnow()
        total_secs = (end - start).total_seconds()
        update_job_status(
            db,
            job_id=job.job_id,
            status="completed",
            completed_at=end,
            total_migration_time=str(total_secs)
        )

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
            "timing": timing
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error during `/export/`")
        raise HTTPException(status_code=500, detail=f"Error exporting tables: {e}")


@router.get("/stats/source/{db_type}/{db_name}")
def stats_source(db_type, db_name):
    return {"result": collect_source_stats({"db_type": db_type, "db_name": db_name})}

@router.get("/stats/target/{src_db_type}/{src_db_name}/{targ_db_type}/{targ_db_name}")
def stats_target(src_db_type, src_db_name, targ_db_type, targ_db_name):
    return {"result": collect_target_stats(
        {"db_type": src_db_type, "db_name": src_db_name},
        {"db_type": targ_db_type, "db_name": targ_db_name}
    )}

@router.get("/stats/combined/{src_db_type}/{src_db_name}/{targ_db_type}/{targ_db_name}")
def stats_combined(src_db_type, src_db_name, targ_db_type, targ_db_name):
    return {"result": collect_combined_stats(
        {"db_type": src_db_type, "db_name": src_db_name},
        {"db_type": targ_db_type, "db_name": targ_db_name}
    )}

@router.get("/names/indexes/{db_type}/{db_name}")
def names_indexes(db_type, db_name):
    return {"result": collect_index_names({"db_type": db_type, "db_name": db_name})}

@router.get("/names/primary-keys/{db_type}/{db_name}")
def names_primary_keys(db_type, db_name):
    return {"result": collect_primary_key_names({"db_type": db_type, "db_name": db_name})}

@router.get("/names/foreign-keys/{db_type}/{db_name}")
def names_foreign_keys(db_type, db_name):
    return {"result": collect_foreign_key_names({"db_type": db_type, "db_name": db_name})}

@router.get("/names/triggers/{db_type}/{db_name}")
def names_triggers(db_type, db_name):
    return {"result": collect_trigger_names({"db_type": db_type, "db_name": db_name})}


@router.get("/stats/")
def stats_display():
    return {"result": collect_export_durations({})}


@router.get("/jobs/{job_id}/stats")
def get_job_stats(job_id, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    items = []
    if job.status == "completed":
        items = collect_combined_stats(
            {"db_type": job.source_db_type, "db_name": job.source_db_name},
            {"db_type": job.target_db_type, "db_name": job.target_db_name}
        )

    return {
        "job": {
            "job_id": job.job_id,
            "source_db_type": job.source_db_type,
            "source_db_name": job.source_db_name,
            "target_db_type": job.target_db_type,
            "target_db_name": job.target_db_name,
            "status": job.status,
            "created_at": job.created_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "total_migration_time": job.total_migration_time
        },
        "items": items
    }