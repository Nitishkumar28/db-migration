import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.db.db_connect import get_db_engine
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "postgresql").lower()
DB_NAME = os.getenv("DB_NAME", "migration_db")
DB_HOST = os.getenv("POSTGRES_DB_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_DB_PORT", "5432")
DB_USER = os.getenv("POSTGRES_DB_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_DB_PASS", "")

# SQLALCHEMY_DATABASE_URL = get_db_engine(db_type="postgresql", db_name="db_migration", **db_args)

#SQLALCHEMY_DATABASE_URL = "sqlite:///./migration.db"

engine = get_db_engine(
    db_type=DB_TYPE,
    db_name=DB_NAME,
    host_name=DB_HOST,
    username=DB_USER,
    password=DB_PASS,
    port=DB_PORT,
    check_connection_status=True
)

if engine is None:
    raise RuntimeError(f"Unable to connect to Postgres at {DB_HOST}:{DB_PORT}/{DB_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
