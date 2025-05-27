from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas import UsersCreate, UsersResponse
from ..crud.users import db_get_user_by_id, db_create_user
from ..core.oauth2 import get_current_user

if TYPE_CHECKING:
    from ..models import Users


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersResponse)
async def create_user(user: UsersCreate):
    created_user = db_create_user(user)
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    return created_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UsersResponse)
async def get_user(id: int, user: Users = Depends(get_current_user)):
    user = db_get_user_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found in the DB",
        )
    return user
