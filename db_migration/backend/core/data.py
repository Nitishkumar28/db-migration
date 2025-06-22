from pydantic import BaseModel
from typing import List, Optional
<<<<<<< Updated upstream
=======
from datetime import datetime

>>>>>>> Stashed changes

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


<<<<<<< Updated upstream
class CreateJobRequest(BaseModel):
    source_db_type: str
    source_db_name: str
    target_db_type: str
    target_db_name: str

mockLogs = [
  { "time": "09:58:21 AM", "message": "✓ done" },
  { "time": "09:58:21 AM", "message": "✓ built in 2.97s" },
  { "time": "09:58:22 AM", "message": "==> Uploading build..." },
  { "time": "09:58:24 AM", "message": "==> Build uploaded in 2s" },
  { "time": "09:58:24 AM", "message": "==> Build successful 🎉" },
  { "time": "09:58:25 AM", "message": "==> Deploying..." },
  { "time": "09:58:25 AM", "message": "==> Installing dependencies..." },
  { "time": "09:58:30 AM", "message": "==> Dependencies installed" },
  { "time": "09:58:31 AM", "message": "==> Requesting Node version 20" },
  { "time": "09:58:31 AM", "message": "==> Using Node version 20.11.1 via env var" },
  { "time": "09:58:31 AM", "message": "==> Docs: https://render.com/docs/node-version" },
  { "time": "09:58:32 AM", "message": "==> Running 'node server.js'" },
  { "time": "09:58:33 AM", "message": "Listening on http://0.0.0.0:3000" },
  { "time": "09:58:35 AM", "message": "Your service is live 🎉" },
];
=======

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
>>>>>>> Stashed changes
