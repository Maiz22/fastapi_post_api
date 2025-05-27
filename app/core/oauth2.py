from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from ..schemas import TokenData
from ..config.settings import SECRET_KEY, JWT_ALGORITHM
from ..crud.users import db_get_user_by_id
from ..models import Users
from ..schemas import Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Takes a token relevant data and an optional expiration date
    sets the expiration data or falls back to default 15 minutes.
    Adds the expiration date to the data, takes the SECRET_KEY and
    JWT_ALGORITHM to create the token.
    Returns the jwt.
    """
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db_get_user_by_id(id=token_data.id)
    if user is None:
        raise credentials_exception
    return user
