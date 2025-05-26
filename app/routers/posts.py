from __future__ import annotations
from typing import TYPE_CHECKING, List
from fastapi import APIRouter, Response, status, HTTPException
from sqlalchemy.exc import StatementError
from sqlmodel import Session, select
from ..db import engine
from ..models import Posts
from ..schemas import PostsCreate, PostsUpdate, PostsResponse
from ..crud.posts import (
    db_get_all_posts,
    db_get_post_by_id,
    db_create_post,
    db_delete_post,
    db_update_post,
)


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostsResponse])
async def get_posts():
    posts = db_get_all_posts()
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostsResponse)
async def get_post(id: int):
    post = db_get_post_by_id()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def create_post(post: PostsCreate):
    new_post = db_create_post(post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = db_get_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    db_delete_post(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def update_post(id: int, updated_post: PostsUpdate):
    post = db_get_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    post = db_update_post(post, updated_post)
    return post
