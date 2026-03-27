from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.user import User, UserCreate, UserRead, UserRole
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserRead], dependencies=[Depends(deps.get_current_active_superuser)])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.post("/", response_model=UserRead, dependencies=[Depends(deps.get_current_active_superuser)])
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == user_in.username)).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user
