from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class MigrationHistory(Base):
    __tablename__ = "migration_history"

    job_id = Column(Integer, primary_key=True, index=True)
    source_db_type = Column(String)
    target_db_type = Column(String)
    source_db_name = Column(String)
    target_db_name = Column(String)
    status = Column(String, default="running")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(String)
    total_migration_time = Column(String)
    started_by = Column(String)
    description = Column(String)
    tags = Column(String)

    items = relationship("MigrationItem", back_populates="history", cascade="all, delete-orphan")


class MigrationItem(Base):
    __tablename__ = "migration_item"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("migration_history.job_id"))
    name = Column(String)
    source_total_rows = Column(Integer)
    target_total_rows = Column(Integer)
    index_validation = Column(String)
    primary_key_validation = Column(String)
    foreign_key_validation = Column(String)
    status = Column(String, default="inprogress")
    duration = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    history = relationship("MigrationHistory", back_populates="items")


class TestModel(Base):
    __tablename__ = "test_model"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)