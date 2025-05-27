import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """
    Settings class loading all of our env vars directly
    from the .env file if it exists (in dev).
    If there is  no .env file in production it will look
    in our OS.
    """

    db_host: str = Field(validation_alias="POSTGRES_HOST_ADDRESS")
    db_name: str = Field(validation_alias="POSTGRES_DB_NAME")
    db_user: str = Field(validation_alias="POSTGRES_USERNAME")
    db_pw: str = Field(validation_alias="POSTGRES_PW")
    debug: bool = Field(validation_alias="DEBUG")
    secret_key: str = Field(validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")

    class Config:
        env_file = "....env"


settings = Settings()
