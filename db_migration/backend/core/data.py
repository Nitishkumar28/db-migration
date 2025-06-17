from pydantic import BaseModel
from typing import List

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
    source: Source
    target: Target
    table_names: List[str]



class DBInfo(BaseModel):
    host_name: str
    username: str
    password: str
    port: str
    db_name: str


class ConnectionRequest(BaseModel):
    source: DBInfo
    target: DBInfo