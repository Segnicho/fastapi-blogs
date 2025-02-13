import jwt
import datetime
import uuid
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from src.models.users import User
from sqlmodel import Session, select
from src.core.database import get_session

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALOGORITHM
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pwd: str):
    return pwd_context.hash(pwd)

def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def create_jwt_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str):
    access_token = create_jwt_token({"sub": user_id}, ACCESS_TOKEN_EXPIRE_MINUTES)
    return access_token

def create_refresh_token(user_id: str):
    refresh_token = create_jwt_token({"sub": user_id}, REFRESH_TOKEN_EXPIRE_DAYS * 1440)
    return refresh_token
    
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
