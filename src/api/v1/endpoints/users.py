from typing import Annotated
import uuid
from fastapi import Depends, APIRouter, HTTPException
from src.schemas.users import UserCreate, UserResponse
from src.core.database import  get_session
from sqlmodel import Session
from src.services.users import create_user as create_a_user,\
    get_users as get_all_users, delete_user as delete_a_user


SESSION_DEP = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_users(session: SESSION_DEP):
    return get_all_users(session)

@router.post("/", response_model=UserResponse)
def create_user( user: UserCreate, session: SESSION_DEP):
    return create_a_user(session, user)

@router.delete("/{used_id}")
def delete_user(user_id: str, session: SESSION_DEP):
    try:
        uuid_id = uuid.UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid id, uuid format")
    return delete_a_user(session, uuid_id)
