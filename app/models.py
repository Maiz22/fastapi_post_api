from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(primary_key=True, nullable=False, default=None)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)


class Posts(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(primary_key=True, nullable=False, default=None)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(nullable=False, default=True)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    user_id: int = Field(nullable=False, foreign_key="users.id")


class Votes(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: int = Field(primary_key=True, foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(primary_key=True, foreign_key="posts.id", ondelete="CASCADE")
