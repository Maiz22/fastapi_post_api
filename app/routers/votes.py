from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, status, Depends
from ..schemas import VoteResponse, VoteCreate
from ..core.oauth2 import get_current_user
from ..crud.votes import db_create_vote

if TYPE_CHECKING:
    from ..models import Users


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VoteResponse)
def set_vote(vote: VoteCreate, current_user: Users = Depends(get_current_user)):
    new_vote = db_create_vote(user_id=current_user.id, post_id=vote.post_id)
    return new_vote
