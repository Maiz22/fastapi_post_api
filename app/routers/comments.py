from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..crud.comments import (
    db_create_comment,
    db_get_comment_by_id,
    db_delete_comment,
)
from ..core.oauth2 import get_current_user
from ..schemas import CommentCreate, CommentResponse

if TYPE_CHECKING:
    from ..models import Users

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate, current_user: Users = Depends(get_current_user)
):
    comment = db_create_comment(
        post_id=comment.post_id, user_id=current_user.id, content=comment.content
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find post in DB.",
        )
    return comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int, current_user: Users = Depends(get_current_user)):
    comment = db_get_comment_by_id(id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID: {id} was not found",
        )
    if current_user.id != comment.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perfrom requested action",
        )
    db_delete_comment(comment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
