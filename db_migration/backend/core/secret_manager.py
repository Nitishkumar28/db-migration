import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key):
    value = os.environ.get(key, "")
    return value

def set_secret(key, value):
    if key is None:
        raise
    os.environ[key] = value

def set_db_secrets_for_db(db_type, details):
    if db_type == "postgresql":
        set_secret("POSTGRES_DB_HOST", details["host_name"])
        set_secret("POSTGRES_DB_PORT", details["port"])
        set_secret("POSTGRES_DB_USER", details["username"])
        set_secret("POSTGRES_DB_PASS", details["password"])
        print("✅ PostgreSQL environment set!")
    elif db_type == "mysql":
        set_secret("MYSQL_DB_HOST", details["host_name"])
        set_secret("MYSQL_DB_PORT", details["port"])
        set_secret("MYSQL_DB_USER", details["username"])
        set_secret("MYSQL_DB_PASS", details["password"])
        print("✅ MySQL environment set!")