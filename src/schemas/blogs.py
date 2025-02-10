import uuid
from pydantic import BaseModel, EmailStr

class BlogCreate(BaseModel):
    title: str
    content: str
    author_id: uuid.UUID

class BlogResponse(BlogCreate):
    id: uuid.UUID
