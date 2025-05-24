from __future__ import annotations
from typing import TYPE_CHECKING, List
from fastapi import APIRouter, Response, status, HTTPException
from sqlalchemy.exc import StatementError
from sqlmodel import Session, select
from ..db import engine
from ..models import Posts
from ..schemas import PostsCreate, PostsUpdate, PostsResponse


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostsResponse])
async def get_posts():
    with Session(engine) as session:
        statement = select(Posts)
        results = session.exec(statement)
        posts = results.all()
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostsResponse)
async def get_post(id: int):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == id)
        post = session.exec(statement).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {id} was not found",
            )
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def create_post(new_post: PostsCreate):
    new_post = Posts(**new_post.model_dump())
    try:
        with Session(engine) as session:
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
    except StatementError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == id)
        post = session.exec(statement).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {id} was not found",
            )
        session.delete(post)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def update_post(id: int, updated_post: PostsUpdate):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == id)
        post = session.exec(statement).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {id} was not found",
            )
        updated_data = updated_post.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post
