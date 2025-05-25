from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


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


class UsersBase(SQLModel):
    email: EmailStr


class UsersCreate(UsersBase):
    password: str


class UsersUpdate(UsersBase):
    password: str


class UsersResponse(UsersBase):
    id: int


class UserLogin(UsersBase):
    password: str
