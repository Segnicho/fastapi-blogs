import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from src.models.blogs import Blog
from src.schemas.blogs import BlogCreate

def get_blogs_service(session: Session):
    return session.exec(select(Blog)).all()

def create_blog_service(session: Session, blog_post: BlogCreate):
    blog = Blog(**blog_post.dict())
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

def update_blog_service(session: Session, blog_id: str, blog_data: BlogCreate):
    
    try:
        blog_uuid = uuid.UUID(blog_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    blog = session.get(Blog, blog_uuid)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog Not Found!")

    # Update the blog fields
    blog.title = blog_data.title
    blog.content = blog_data.content
    session.commit()
    session.refresh(blog)

    return blog
    
