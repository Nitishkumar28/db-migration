from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(String(6), primary_key=True, index=True)
    source_db_type = Column(String, nullable=False)
    source_db_name = Column(String, nullable=False)
    target_db_type = Column(String, nullable=False)
    target_db_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default='running')
    created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    started_by = Column(String, nullable=True)
    description = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)
    total_migration_time = Column(String, nullable=True)