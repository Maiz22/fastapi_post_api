from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session, select
from typing import List
from ..core import security
from ..schemas import UsersCreate, UsersResponse
from ..models import Users
from ..db import engine


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersResponse)
def create_user(user: UsersCreate):
    new_user = Users(**user.model_dump())
    new_user.password = security.hash_password(user.password)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UsersResponse)
def get_user(id: int):
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} not found in the DB",
            )
    return user
