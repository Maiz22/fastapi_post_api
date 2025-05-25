from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session, select
from ..db import engine
from ..schemas import UserLogin
from ..models import Users
from ..core.security import verify_password


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: UserLogin):
    with Session(engine) as session:
        statement = select(Users).where(user_credentials.email == Users.email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
            )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    # create token
    # return token
    return {"token": "example token"}
