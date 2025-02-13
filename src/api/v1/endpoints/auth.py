import uuid
from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlmodel import Session, select
from src.core.database import get_session
from src.models.users import User
from src.schemas.users import UserCreate, TokenResponse
from src.core.auth import hash_password, verify_password, create_access_token
from src.core.config import settings


router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, session:Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(id=uuid.uuid4(), name=user_data.name, email=user_data.email, password=hash_password(user_data.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    token = create_access_token(str(new_user.id))
    return {"access_token": token, "token_type": "bearer"}



@router.post("/login", response_model=TokenResponse)
def login(user_data: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh")
def get_access_token(refresh_token: str, session: Session=Depends(get_session)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALOGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        access_token = create_access_token(str(user.id))
        return {"access_token": access_token, "refresh_token": refresh_token,"token_type": "bearer"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
