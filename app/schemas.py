from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class PostsBase(SQLModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostsCreate(PostsBase):
    pass


class PostsUpdate(PostsBase):
    pass


class PostsResponse(PostsBase):
    id: int
    created_at: datetime
