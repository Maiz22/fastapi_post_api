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
    db_port: str = Field(validation_alias="POSTGRES_PORT")
    db_pw: str = Field(validation_alias="POSTGRES_PASSWORD")
    db_service_name: str = Field(validation_alias="POSTGRES_SERVICE_NAME")
    redis_service_name: str = Field(validation_alias="REDIS_SERVICE_NAME")
    redis_port: str = Field(validation_alias="REDIS_PORT")
    redis_pw: str = Field(validation_alias="REDIS_PASSWORD")
    debug: bool = Field(validation_alias="DEBUG")
    is_dev: bool = Field(validation_alias="DEV")
    secret_key: str = Field(validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")
    throttling_max_attempts: int = Field(validation_alias="MAX_LOGIN_ATTEMPTS")
    throttling_lockout_time: int = Field(validation_alias="LOGIN_LOCKOUT_TIME")

    class Config:
        env_file = "....env"


settings = Settings()
