from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import VotesResponse, VotesCreate
from ..core.oauth2 import get_current_user
from ..crud.votes import db_create_vote, db_delete_vote, db_get_vote

if TYPE_CHECKING:
    from ..models import Users


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def set_vote(vote: VotesCreate, current_user: Users = Depends(get_current_user)):
    if vote.vote_dir == 1:
        cur_vote = db_create_vote(user_id=current_user.id, post_id=vote.post_id)
        if cur_vote is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User can only upvote a post once.",
            )
        return {"message": f"Successfully voted on post {cur_vote.post_id}"}
    elif vote.vote_dir == 0:
        cur_vote = db_get_vote(user_id=current_user.id, post_id=vote.post_id)
        if cur_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist.",
            )
        db_delete_vote(cur_vote)
        return {"message": f"Succesfully deleted vote on post {cur_vote.post_id}."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote_dir value."
        )
