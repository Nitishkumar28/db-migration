from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from core.models import MigrationHistory, MigrationItem
from core.data import MigrationHistorySchemaBrief, MigrationHistorySchema
from core.database import get_db, engine



import secrets

used_codes = set()

def generate_unique_code():
    while True:
        code = secrets.randbelow(900_000_000) + 100_000_000  # 9-digit
        if code not in used_codes:
            used_codes.add(code)
            return code
        

def create_initial_job(request_obj, db, started_by=None):
    if started_by is None:
        print("No user found")
        return None
    job_id = generate_unique_code()
    current_data = {"job_id": job_id, "started_by": started_by, **dict(request_obj)}
    print(current_data)
    history_obj = MigrationHistory(**current_data)
    db.add(history_obj)
    db.commit()
    db.refresh(history_obj)
    return history_obj


def get_migration_for_jobid(job_id, db, user):
    history = db.query(MigrationHistory).options(joinedload(MigrationHistory.items)).filter_by(job_id=job_id, started_by=user.id).first()
    return history


def get_full_history(db, user):
    return db.query(MigrationHistory).order_by(desc(MigrationHistory.created_at)).filter_by(started_by=user.id)

def get_full_history_brief(db, user):
    history_objs = db.query(MigrationHistory).order_by(desc(MigrationHistory.created_at)).filter_by(started_by=user.id)
    result = []
    for history in history_objs:
        curr = {
            "job_id": history.job_id,
            "source_db_type": history.source_db_type,
            "target_db_type": history.target_db_type,
            "source_db_name": history.source_db_name,
            "target_db_name": history.target_db_name,
            "started_by": history.started_by,
            "status": history.status,
            "created_at": history.created_at
        }
        result.append(MigrationHistorySchemaBrief(**curr))
    return result


def update_migration_data(job_id, data, db):
    db_obj = db.query(MigrationHistory).filter_by(job_id=job_id).first()

    if not db_obj:
        return None

    for field, value in data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_history_for_jobid(job_id, db):
    db_obj = db.query(MigrationHistory).filter_by(job_id=job_id).first()

    if not db_obj:
        print("migration object not found")
        return

    db.delete(db_obj)
    db.commit()
    return


def get_full_history_items(db):
    return db.query(MigrationItem).all()

def create_history_item(item_obj, db):
    history_obj = MigrationItem(**dict(item_obj))
    db.add(history_obj)
    db.commit()
    db.refresh(history_obj)
    return history_obj

def delete_history_item(id, db):
    db_obj = db.query(MigrationItem).filter_by(id=id).first()

    if not db_obj:
        print("migration object not found")
        return

    db.delete(db_obj)
    db.commit()
    return

def drop_table(which):
    if which == "history_item":
        MigrationItem.__table__.drop(engine)
    elif which == "history":
        MigrationHistory.__table__.drop(engine)