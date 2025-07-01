from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from urllib.parse import quote_plus
import logging

from core.secret_manager import get_secret

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DBConnectionError(Exception):
    def __init__(self, db_type: str, original: Exception):
        super().__init__(f"{db_type} connection error: {original}")
        self.db_type = db_type
        self.original = original

class DBConfigError(Exception):
    pass

_mysql_engine = None
_postgresql_engine = None

def check_connection(db_engine):
    try:
        with db_engine.begin() as conn:
            conn.execute(text("SELECT 1"))
            return True
    except SQLAlchemyError as sae:
        print(f"SQLAlchemy Error, details: {str(sae)}")
    except Exception as e:
        print(f"Error occurred while checking the connection, details: {str(e)}")
    return False

def get_mysql_db_engine(db_name=None, check_connection_status=False, **kwargs):    
    global _mysql_engine

    try:
        if _mysql_engine is None or check_connection_status:
            db_host = kwargs.get("host_name", "") or get_secret("MYSQL_DB_HOST")
            db_port = kwargs.get("port", "") or get_secret("MYSQL_DB_PORT")
            db_user = kwargs.get("username", "") or get_secret("MYSQL_DB_USER")
            db_pass = kwargs.get("password", "") or get_secret("MYSQL_DB_PASS")

            if not all([db_host, db_port, db_user, db_pass]):
                    raise DBConfigError("MySQL credentials incomplete")

            db_user_encoded = quote_plus(db_user) 
            db_pass_encoded = quote_plus(db_pass)
            conn_url = f"mysql+pymysql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}"

            if db_name is not None:
                conn_url = f"mysql+pymysql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"

            logger.info("Creating MySQL engine for %s", db_name)
            _mysql_engine = create_engine(conn_url, pool_size=10)

            if not check_connection(_mysql_engine):
                _mysql_engine = None
                return None
            
        return _mysql_engine

    except OperationalError as oe:
        print(f"MySQL OperationalError: {oe}")
        _mysql_engine = None
        raise DBConnectionError("mysql", oe)
    except DBConfigError:
        raise
    except Exception as e:
        print(f"Unexpected error in get_mysql_db_engine: {e}")
        _mysql_engine = None
        raise DBConnectionError("mysql", e)

def get_postgresql_db_engine(db_name=None, check_connection_status=False, **kwargs):    
    global _postgresql_engine

    try:
        if db_name is None:
            db_name = "postgres"

        if _postgresql_engine is None or check_connection_status:
            db_host = kwargs.get("host_name", "") or get_secret("POSTGRES_DB_HOST")
            db_port = kwargs.get("port", "") or get_secret("POSTGRES_DB_PORT")
            db_user = kwargs.get("username", "") or get_secret("POSTGRES_DB_USER")
            db_pass = kwargs.get("password", "") or get_secret("POSTGRES_DB_PASS")

            if not all([db_host, db_port, db_user, db_pass]):
                raise DBConfigError("PostgreSQL credentials incomplete")
            

            db_user_encoded = quote_plus(db_user)
            db_pass_encoded = quote_plus(db_pass)
            conn_url = f'postgresql+psycopg2://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}'

            logger.info("Creating PostgreSQL engine for %s", db_name)
            _postgresql_engine = create_engine(conn_url, pool_size=10)

            if not check_connection(_postgresql_engine):
                _postgresql_engine = None
                return None
        
        
        return _postgresql_engine
    
    except OperationalError as oe:
        print(f"PostgreSQL OperationalError: {oe}")
        _postgresql_engine = None
        raise DBConnectionError("postgresql", oe)
    except DBConfigError:
        raise
    except Exception as e:
        print(f"Unexpected error in get_postgresql_db_engine: {e}")
        _postgresql_engine = None
        raise DBConnectionError("postgresql", e)

def get_db_engine(db_type, db_name=None, check_connection_status=False, **kwargs):
    _engine = None
    if db_type == "postgresql":
        _engine = get_postgresql_db_engine(db_name, check_connection_status, **kwargs)
    elif db_type == "mysql":
        _engine = get_mysql_db_engine(db_name, check_connection_status, **kwargs)
    else:
        raise DBConfigError(f"Unsupported db_type: {db_type!r}")
    return _engine