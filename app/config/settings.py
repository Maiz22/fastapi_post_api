import os
from dotenv import load_dotenv


load_dotenv()


def require_env(env_name: str) -> str:
    """
    Checks if an env exists and returns it.
    Raises an Environment error if it does not exist.
    """
    env = os.getenv(env_name)
    if env is None or env.strip() == "":
        raise EnvironmentError(f"Missing environment variable {env}")
    return env


def get_bool_env(env_name: str) -> bool:
    """
    Transforms the env var to bool. Returns false when value
    is set to false, or no valid boolean has been set.
    """
    env = require_env(env_name)
    return env.strip().lower() in ("1", "true", "yes")


def get_int_env(env_name: str) -> int:
    """
    Transforms the str input to integer.
    Returns value error if env cannot be transformed.
    """
    env = require_env(env_name)
    return int(env)


DB_HOST = require_env(env_name="POSTGRES_HOST_ADDRESS")
DB_NAME = require_env(env_name="POSTGRES_DB_NAME")
DB_USER = require_env(env_name="POSTGRES_USERNAME")
DB_PW = require_env(env_name="POSTGRES_PW")
SQL_ALCHEMY_DB_URL = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PW, DB_HOST, DB_NAME)
DEBUG = get_bool_env(env_name="DEBUG")
SECRET_KEY = require_env(env_name="SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = require_env(env_name="ACCESS_TOKEN_EXPIRE_MINUTES")
