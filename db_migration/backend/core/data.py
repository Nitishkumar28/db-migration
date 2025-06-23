from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TableModel(BaseModel):
    db_name: str
    tables: List[str]


class TriggerModel(BaseModel):
    name: str
    timing: str
    event: str
    statement: str


class Source(BaseModel):
    db_type: str
    db_name: str


class Target(BaseModel):
    db_type: str
    db_name: str


class ExportRequest(BaseModel):
    job_id: int
    source: Source
    target: Target


class DBInfo(BaseModel):
    host_name: str
    username: str
    password: str
    port: str
    db_name: str
    db_type: str


class MigrationHistoryItemSchema(BaseModel):
    job_id: int
    name: Optional[str] = None
    source_total_rows: Optional[int] = None
    target_total_rows: Optional[int] = None
    index_validation: Optional[str] = None
    primary_key_validation: Optional[str] = None
    foreign_key_validation: Optional[str] = None
    status: Optional[str] = "inprogress"
    duration: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True  


class MigrationHistorySchemaBrief(BaseModel):
    job_id: int
    source_db_type: Optional[str]
    target_db_type: Optional[str]
    source_db_name: Optional[str]
    target_db_name: Optional[str]
    status: Optional[str]
    started_by: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class MigrationHistorySchemaBriefInput(BaseModel):
    source_db_type: Optional[str]
    target_db_type: Optional[str]
    source_db_name: Optional[str]
    target_db_name: Optional[str]
    status: Optional[str]
    started_by: Optional[str]

    class Config:
        orm_mode = True

class MigrationHistoryUpdateSchema(BaseModel):
    source_db_type: Optional[str] = ""
    target_db_type: Optional[str] = ""
    source_db_name: Optional[str] = ""
    target_db_name: Optional[str] = ""
    status: Optional[str] = ""
    created_at: Optional[datetime] = datetime.now()
    completed_at: Optional[str] = ""
    total_migration_time: Optional[str] = ""
    started_by: Optional[str] = ""
    description: Optional[str] = ""
    tags: Optional[List[str]] = []
    items: Optional[List[MigrationHistoryItemSchema]] = []

class MigrationHistorySchema(BaseModel):
    job_id: int
    source_db_type: Optional[str]
    target_db_type: Optional[str]
    source_db_name: Optional[str]
    target_db_name: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    completed_at: Optional[str]
    total_migration_time: Optional[str]
    started_by: Optional[str]
    description: Optional[str]
    tags: Optional[str]
    items: List[MigrationHistoryItemSchema] = []

    class Config:
        orm_mode = True

class MigrationItemSchema(BaseModel):
    job_id: int
    source_db_type: str
    target_db_type: str
    source_db_name: str
    target_db_name: str
    started_by: str
    status: str


class TestModelSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
