from pathlib import Path
from dotenv import load_dotenv
import os, re
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import LoginUser

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def check_password_strength(password):
    password_condition = len(password) >= 8 and re.search(r"\d", password) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) and password[0].isupper()    
    return password_condition


def generate_hash_salting(password):
    password_salt = pwd_ctx.hash(password)
    return password_salt

def verify_password_checker(password, hashed_password):
    verify_password = pwd_ctx.verify(password, hashed_password)
    return verify_password


def create_session_token(token_target):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode = {"exp": expire, "sub": token_target}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_session_token(token):
    verify_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return verify_token.get("sub")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        username = verify_session_token(token)
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = db.query(LoginUser).filter(LoginUser.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
