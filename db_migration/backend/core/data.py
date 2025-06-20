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


class DBInfo(BaseModel):
    host_name: str
    username: str
    password: str
    port: str
    db_name: str
    db_type: str


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