from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


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


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: int


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
    user_id: int


class VotesBase(SQLModel):
    user_id: int
    post_id: int
    vote_dir: int


class VoteCreate(VotesBase):
    pass


class VoteResponse(VotesBase):
    pass
