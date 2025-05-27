from sqlmodel import Field, SQLModel, ForeignKey, Relationship
from datetime import datetime


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, default=datetime.now())


class Posts(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(nullable=False, default=True)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)
    user_id: int = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")
