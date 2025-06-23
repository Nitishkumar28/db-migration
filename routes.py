from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import Session as _Session
from core.data import DBInfo, ExportRequest, CreateJobRequest
from core.db.db_connect import get_db_engine, get_postgresql_db_engine
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
from core.stats import collect_export_stats, get_most_recent_stats
from core.data import (
    DBInfo,
    ExportRequest,
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
        "job_id": int,
        "source": {
            "db_type": db_type,
            "db_name": db_name
        },
        "target": {
            "db_type": db_type,
            "db_name": db_name
        }
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


        start_time = time.time()
        job_id = request.job_id
        exported, skipped, durations = export_tables(**args)
        logger.info(f"=== Tables exported: {len(exported)}; skipped: {len(skipped)} ===\n")

        if skipped:
            raise HTTPException(
                status_code=500,
                detail={"exported": list(exported), "skipped": list(skipped)}
            )
        
        logger.info("=== Section: Export Triggers ===")

        result = export_triggers(**args)
        # result = export_triggers(
        #     args["source"],
        #     args["target"]
        # )

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
        total_time = (end_time - start_time)
        update_data = {
            "total_migration_time": total_time
        }
        update_migration_data(job_id, update_data, db)

        collect_export_stats(
            source={ "db_type": request.source.db_type, "db_name": request.source.db_name },
            target={ "db_type": request.target.db_type, "db_name": request.target.db_name },
            exported=exported,
            errors=result.get("errors", []),
            start_time=start_time,
            end_time=end_time,
            durations=durations
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
@router.get("/stats/{job_id}")
def stats_display(job_id, db: Session = Depends(get_db)):
    stats = get_most_recent_stats()
    for stat in stats:
        {
            "job_id": job_id,
            "name": stat["name"],
            "source_total_rows": stat["source_total_rows"],
            "target_total_rows": stat["target_total_rows"],
            "index_validation": stat["index_validation"],
            "primary_key_validation": stat["primary_key_validation"],
            "foreign_key_validation": stat["foreign_key_validation"],
            "status": stat["status"],
            "duration": stat["duration"]
        }
        create_history_item(stat, db)
    print("Stats updated")
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
def get_migration_items(item_obj: MigrationHistoryItemSchema, db: Session = Depends(get_db)):
    return create_history_item(item_obj, db)


# @router.delete("/migration-history-items/", status_code=204)
# def delete_migration():
#     # delete_history_item(id, db)
#     drop_table("history_item")
#     return "dropped"
