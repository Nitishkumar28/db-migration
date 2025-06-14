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
