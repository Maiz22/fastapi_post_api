from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status, HTTPException
from ..crud.comments import create_comment
from ..core.oauth2 import get_current_user
from ..schemas import CommentCreate, CommentResponse

if TYPE_CHECKING:
    from ..models import Users

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def set_comment(
    comment: CommentCreate, current_user: Users = Depends(get_current_user)
):
    comment = create_comment(
        post_id=comment.post_id, user_id=current_user.id, content=comment.content
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find post in DB.",
        )
    return comment
