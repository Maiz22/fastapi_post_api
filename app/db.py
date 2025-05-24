from sqlmodel import create_engine, SQLModel
from .config.settings import SQL_ALCHEMY_DB_URL, DEBUG
import logging

# Need to be imported to register all models
from . import models

# Use uvicorns logging
logger = logging.getLogger("uvicorn")

logger.info("Connecting to database...")
if DEBUG is True:
    engine = create_engine(SQL_ALCHEMY_DB_URL, echo=True)
else:
    engine = create_engine(SQL_ALCHEMY_DB_URL, echo=False)
logger.info("Connection to database established.")


def create_db_and_tables() -> None:
    logger.info("Creating SQL database and tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("SQL database and tables created.")
