from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.models import LoginUser

from core.authentication import (
    check_password_strength,
    generate_hash_salting,
    verify_password_checker,
    create_session_token,
)

def register_user(data, db: Session):
    if not check_password_strength(data.password):
        raise HTTPException(status_code=400,detail="Password must be atleast 8 chars, must start with uppercase and include digit a special symbol")
    
    if (db.query(LoginUser).filter((LoginUser.email == data.email) | (LoginUser.username == data.username)).first()):
        raise HTTPException(status_code=400, detail="Email or username already registered")

    user = LoginUser(
        first_name      = data.first_name,
        last_name       = data.last_name,
        email           = data.email,
        username        = data.username,
        hashed_password = generate_hash_salting(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return create_session_token(user.username)


def authenticate_user(data, db: Session):
    username_email, password = data.username_email, data.password

    user = (db.query(LoginUser).filter((LoginUser.username == username_email) | (LoginUser.email == username_email)).first())

    if not user or not verify_password_checker(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return create_session_token(user.username)