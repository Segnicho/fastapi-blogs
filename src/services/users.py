from sqlmodel import Session, select
from src.models.users import User
from src.schemas.users import UserCreate
from fastapi import HTTPException

def create_user(session: Session, user_data: UserCreate):
    print("Here", user_data)
    new_user = User(**user_data.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_users(session: Session):
    return session.exec(select(User)).all()

def delete_user(session: Session, user_id: str):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found!")
    
    session.delete(user)
    session.commit()
    return {"ok": True}