from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from urllib.parse import quote_plus


from core.secret_manager import get_secret


_mysql_engine = None
_postgresql_engine = None

def check_connection(db_engine, db_type):
    try:
        with db_engine.begin() as conn:
            conn.execute(text("SELECT 1"))
            print(f"Successfully connected to {db_type}!")
            return True
    except SQLAlchemyError as sae:
        print(f"SQLAlchemy Error, details: {str(sae)}")
    except OperationalError as oe:
        print(f"Operational Error, details: {str(oe)}")
    except Exception as e:
        print(f"Error occurred while checking the connection, details: {str(e)}")
    return False

def get_mysql_db_engine(db_name=None):
    if db_name is None:
        raise ValueError("MySQL database name must be provided")
    
    global _mysql_engine
    
    if _mysql_engine is None:
        db_host = get_secret("MYSQL_DB_HOST")
        db_port = get_secret("MYSQL_DB_PORT")
        db_user = get_secret("MYSQL_DB_USER")
        db_pass = get_secret("MYSQL_DB_PASS")
        db_user_encoded = quote_plus(db_user)
        db_pass_encoded = quote_plus(db_pass)

        conn_url = f"mysql+pymysql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
        _mysql_engine = create_engine(conn_url, pool_size=10, pool_cycle=4800)

        if check_connection(_mysql_engine, type="mysql"):
            return _mysql_engine
        
    return _mysql_engine

def get_postgresql_db_engine(db_name=None):
    if db_name is None:
        db_name = "postgres"
    
    global _postgresql_engine

    if _postgresql_engine is None:
        db_host = get_secret("POSTGRES_DB_HOST")
        db_port = get_secret("POSTGRES_DB_PORT")
        db_user = get_secret("POSTGRES_DB_USER")
        db_pass = get_secret("POSTGRES_DB_PASS")
        db_user_encoded = quote_plus(db_user)
        db_pass_encoded = quote_plus(db_pass)

        conn_url = f'postgresql+psycopg2://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}'
        _postgresql_engine = create_engine(conn_url, pool_size=10, pool_cycle=4800)

        if check_connection(_postgresql_engine, type="postgresql"):
            return _postgresql_engine
        
    return _postgresql_engine

def get_db_engine(db_type, db_name=None):
    _engine = None
    if db_type == "postgresql":
        _engine = get_postgresql_db_engine(db_name)
    elif db_type == "mysql":
        _engine = get_postgresql_db_engine(db_name)
    return _engine