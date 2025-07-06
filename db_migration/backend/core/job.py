import random
from datetime import datetime
from sqlalchemy.orm import Session
from core.db.db_connect import get_postgresql_db_engine
from core.models import Job


def generate_job_id():
    return f"{random.randint(100000, 999999):06d}"


def create_job_record(db,source_db_type,source_db_name,target_db_type,target_db_name):
    job_id = generate_job_id()
    now = datetime.utcnow()
    job = Job(
        job_id=job_id,
        source_db_type=source_db_type,
        source_db_name=source_db_name,
        target_db_type=target_db_type,
        target_db_name=target_db_name,
        status="in progress",
        created_at=now
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job_status(db,job_id,status,completed_at = None,total_migration_time = None):
    job = db.query(Job).filter(Job.job_id == job_id).one()
    job.status = status
    if completed_at:
        job.completed_at = completed_at
    if total_migration_time:
        job.total_migration_time = total_migration_time
    db.commit()
    db.refresh(job)
    return job