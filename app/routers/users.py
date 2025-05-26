from fastapi import APIRouter, status, HTTPException
from ..schemas import UsersCreate, UsersResponse
from ..crud.users import db_get_user_by_id, db_create_user


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersResponse)
def create_user(user: UsersCreate):
    created_user = db_create_user(user)
    return created_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UsersResponse)
def get_user(id: int):
    user = db_get_user_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found in the DB",
        )
    return user
