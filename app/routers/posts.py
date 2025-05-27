from __future__ import annotations
from typing import TYPE_CHECKING, List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from ..schemas import PostsCreate, PostsUpdate, PostsResponse
from ..core.oauth2 import get_current_user
from typing import Optional
from ..crud.posts import (
    db_get_all_posts,
    db_get_post_by_id,
    db_create_post,
    db_delete_post,
    db_update_post,
)

if TYPE_CHECKING:
    from ..models import Users

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostsResponse])
async def get_posts(
    user: Users = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = db_get_all_posts(limit=limit, skip=skip, search=search)
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostsResponse)
async def get_post(id: int, current_user: Users = Depends(get_current_user)):
    post = db_get_post_by_id(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def create_post(
    post: PostsCreate, current_user: Users = Depends(get_current_user)
):
    new_post = db_create_post(post, current_user)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: Users = Depends(get_current_user)):
    post = db_get_post_by_id(id)
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perfrom requested action",
        )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    db_delete_post(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostsResponse)
async def update_post(
    id: int, updated_post: PostsUpdate, current_user: Users = Depends(get_current_user)
):
    post = db_get_post_by_id(id)
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perfrom requested action",
        )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} was not found",
        )
    post = db_update_post(post, updated_post)
    return post
