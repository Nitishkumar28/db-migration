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
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 8 characters, start with an uppercase letter, "
                "include a digit and a special symbol"
            )
        )

    if db.query(LoginUser).filter(LoginUser.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = LoginUser(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=generate_hash_salting(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return create_session_token(user.email)


def authenticate_user(data, db: Session):
    user = db.query(LoginUser).filter(LoginUser.email == data.email).first()

    if not user or not verify_password_checker(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return create_session_token(user.email)