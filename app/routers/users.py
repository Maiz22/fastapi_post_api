from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session, select
from ..schemas import UsersCreate, UsersResponse
from ..models import Users
from ..db import engine


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersResponse)
def create_user(user: UsersCreate):
    new_user = Users(**user.model_dump())
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
