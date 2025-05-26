from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from ..db import engine
from ..schemas import UserLogin
from ..models import Users
from ..core.security import verify_password
from ..core.oauth2 import create_access_token


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Getting user credentials as form-data as predefined by OAuth2PasswordRequestForm.
    Looks up the user in the DB, verifies the password and creates an JWT.
    Returns the JWT.
    """
    with Session(engine) as session:
        statement = select(Users).where(user_credentials.username == Users.email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
            )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
