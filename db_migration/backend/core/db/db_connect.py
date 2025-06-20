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
    except Exception as e:
        print(f"Error occurred while checking the connection, details: {str(e)}")
    return False

def get_mysql_db_engine(db_name=None, check_connection_status=False, **kwargs):    
    global _mysql_engine

    if _mysql_engine is None or check_connection_status:
        db_host = kwargs.get("host_name", "") or get_secret("MYSQL_DB_HOST")
        db_port = kwargs.get("port", "") or get_secret("MYSQL_DB_PORT")
        db_user = kwargs.get("username", "") or get_secret("MYSQL_DB_USER")
        db_pass = kwargs.get("password", "") or get_secret("MYSQL_DB_PASS")
        db_user_encoded = quote_plus(db_user) 
        db_pass_encoded = quote_plus(db_pass)

        print(db_host,db_port,db_user,db_pass,db_user_encoded,db_pass_encoded,end="\n")
        conn_url = f"mysql+pymysql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}"

        if db_name is not None:
            conn_url = f"mysql+pymysql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"

        _mysql_engine = create_engine(conn_url, pool_size=10)

        if check_connection(_mysql_engine, db_type="mysql"):
            return _mysql_engine
        
    return _mysql_engine

def get_postgresql_db_engine(db_name=None, check_connection_status=False, **kwargs):    
    if db_name is None:
        db_name = "postgres"
    
    global _postgresql_engine

    print("postgre db variables:", _postgresql_engine, check_connection_status)

    if _postgresql_engine is None or check_connection_status:
        db_host = kwargs.get("host_name", "") or get_secret("POSTGRES_DB_HOST")
        db_port = kwargs.get("port", "") or get_secret("POSTGRES_DB_PORT")
        db_user = kwargs.get("username", "") or get_secret("POSTGRES_DB_USER")
        db_pass = kwargs.get("password", "") or get_secret("POSTGRES_DB_PASS")
        print("Inside Engine")
        print(db_host)
        print("Leaving db host")
        db_user_encoded = quote_plus(db_user)
        db_pass_encoded = quote_plus(db_pass)
        print(db_host,db_port,db_user,db_pass,db_user_encoded,db_pass_encoded)

        conn_url = f'postgresql+psycopg2://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}'

        _postgresql_engine = create_engine(conn_url, pool_size=10)

        if check_connection(_postgresql_engine, db_type="postgresql"):
            return _postgresql_engine
        
    return _postgresql_engine

def get_db_engine(db_type, db_name=None, check_connection_status=False, **kwargs):
    _engine = None
    if db_type == "postgresql":
        _engine = get_postgresql_db_engine(db_name, check_connection_status, **kwargs)
    elif db_type == "mysql":
        _engine = get_mysql_db_engine(db_name, check_connection_status, **kwargs)
    return _engine