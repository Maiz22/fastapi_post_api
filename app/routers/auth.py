from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from ..core.security import verify_password
from ..core.oauth2 import create_access_token
from ..crud.users import db_get_user_by_email
from ..services.throttling import is_locked_out, register_failed_attempt
from ..schemas import TokenCreate


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenCreate)
async def login(
    request: Request,
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if is_locked_out(username=user_credentials.username):
        raise HTTPException(
            status_code=429, detail="Too many login attempts. Try again later."
        )
    user = db_get_user_by_email(email=user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not verify_password(user_credentials.password, user.password):
        register_failed_attempt(username=user_credentials.username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return TokenCreate(access_token=access_token, token_type="bearer")
