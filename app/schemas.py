from sqlmodel import SQLModel
from typing import Optional, List
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


class TokenCreate(SQLModel):
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


class PostsResponse(SQLModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = True
    created_at: datetime
    user_id: int
    votes_count: int
    comments: List


class PostsResponseCreate(SQLModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = True
    created_at: datetime
    user_id: int


class VotesBase(SQLModel):
    post_id: int


class VotesCreate(VotesBase):
    vote_dir: int


class VotesResponse(VotesBase):
    user_id: int


class BaseComment(SQLModel):
    content: str
    post_id: int


class CommentCreate(BaseComment):
    pass


class CommentResponse(BaseComment):
    id: int
    user_id: int
