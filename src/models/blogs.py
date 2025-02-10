from sqlmodel import SQLModel, Field
import uuid

class Blog(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    content: str
    author_id: uuid.UUID = Field(foreign_key="user.id") 