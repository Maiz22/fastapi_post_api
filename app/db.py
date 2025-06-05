from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import create_engine, SQLModel
from .config.settings import settings
import logging
import redis

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

# Need to be imported to register all models
from . import models

# Use uvicorns logging
logger = logging.getLogger("uvicorn")


def connect_to_postgres_db() -> Engine | None:
    logger.info("Create postgres DB engine...")
    if settings.is_dev is True:
        logger.info("Create non containerized development engine...")
        SQL_ALCHEMY_DB_URL = "postgresql://{}:{}@{}/{}".format(
            settings.db_user, settings.db_pw, settings.db_host, settings.db_name
        )
    else:
        logger.info("Create containerized engine...")
        SQL_ALCHEMY_DB_URL = f"postgresql://{settings.db_user}:{settings.db_pw}@db:5432/{settings.db_name}"
    logger.info("Engine created.")
    return create_engine(SQL_ALCHEMY_DB_URL, echo=settings.debug)


def connect_to_redis_db():
    if settings.is_dev is True:
        logger.warning("Unaible to connect to redis in dev mode")
        return
    logger.info("Creatin redis client...")
    try:
        client = redis.Redis(
            host="my-production-redis.example.com", port=6379, password="secret"
        )
    except Exception as e:
        logger.error("Unaible to create redis client.")
        return
    return client


redis_client = connect_to_redis_db()
engine = connect_to_postgres_db()


def create_db_and_tables() -> None:
    logger.info("Creating SQL database and tables...")
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.error("Unable to create DB and tables. Please check your DB engine.")
        return
    logger.info("SQL database and tables created.")
