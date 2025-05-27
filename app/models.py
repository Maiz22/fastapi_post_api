from sqlmodel import Field, SQLModel
from datetime import datetime


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, default=datetime.now())


class Posts(SQLModel, table=True):
    __tablename__ = "posts"
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(nullable=False, default=True)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    user_id: int = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")


class Votes(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: int = Field(primary_key=True, foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(primary_key=True, foreign_key="posts.id", ondelete="CASCADE")
