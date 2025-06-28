from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.db.db_connect import get_db_engine

db_args = {
    "host_name": "",
    "username": "",
    "port": "",
    "password": "",
    "db_name": ""
}

# SQLALCHEMY_DATABASE_URL = get_db_engine(db_type="postgresql", db_name="db_migration", **db_args)

SQLALCHEMY_DATABASE_URL = "sqlite:///./migration.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
