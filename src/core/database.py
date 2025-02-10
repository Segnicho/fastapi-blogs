from sqlmodel import SQLModel, create_engine, Session
import os
from src.core.config import settings

# Use the DATABASE_URL from .env
engine = create_engine(settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
        

def init_db():
    SQLModel.metadata.create_all(engine)
