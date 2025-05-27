from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from ..core.security import verify_password
from ..core.oauth2 import create_access_token
from ..crud.users import db_get_user_by_email
from ..schemas import Token


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Getting user credentials as form-data as predefined by OAuth2PasswordRequestForm.
    Looks up the user in the DB, verifies the password and creates an JWT.
    Returns the JWT.
    """
    user = db_get_user_by_email(email=user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return Token(access_token=access_token, token_type="bearer")
