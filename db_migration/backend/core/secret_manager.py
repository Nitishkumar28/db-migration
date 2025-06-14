import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key):
    value = os.environ.get(key, None)
    return value

def set_secret(key, value):
    if key is None:
        raise
    os.environ[key] = value