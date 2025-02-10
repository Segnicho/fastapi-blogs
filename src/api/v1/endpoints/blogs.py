from typing import Annotated
import uuid
from fastapi import Depends, APIRouter, HTTPException
from src.schemas.blogs import BlogCreate, BlogResponse
from src.core.database import  get_session
from sqlmodel import Session
from src.services.blogs import get_blogs_service, create_blog_service,\
    update_blog_service


SESSION_DEP = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/", response_model=BlogResponse)
def create_blog(blog: BlogCreate, session: SESSION_DEP):
    return create_blog_service(session, blog)

@router.get("/", response_model=list[BlogResponse])
def get_blogs(session: SESSION_DEP):
    return get_blogs_service(session)

@router.put("/{blog_id}")
def update_blog(blog_id: str, blog: BlogCreate, session: SESSION_DEP):
    return update_blog_service(session,blog_id,  blog)