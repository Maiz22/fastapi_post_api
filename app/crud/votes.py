from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError
from ..db import engine
from ..models import Votes
import logging


logger = logging.getLogger("uvicorn")


def db_get_vote(user_id: int, post_id: int) -> Votes | None:
    """
    Gets a vote by the two primary keys user_id and post_id.
    Returns vote if fount in DB or None if no vote was found.
    """
    with Session(engine) as session:
        statement = (
            select(Votes)
            .where(Votes.user_id == user_id)
            .where(Votes.post_id == post_id)
        )
        vote = session.exec(statement).first()
    return vote


def db_create_vote(user_id: int, post_id: int) -> Votes | None:
    """
    Creates a new vote instance and saves it in the DB. Raises
    an IntegrityError if the combitaion of user_id and post_id
    already exists in votes.
    Returns the vote if it is created.
    Returns None if vote already exists in DB.
    """
    vote = Votes(user_id=user_id, post_id=post_id)
    try:
        with Session(engine) as session:
            session.add(vote)
            session.commit()
            session.refresh(vote)
    except IntegrityError:
        logger.info(
            f"A vote for post {post_id} by user {user_id} already exists in db."
        )
        return None
    return vote


def db_delete_vote(vote: Votes) -> None:
    """
    Takes a vote instance and removes it from db.
    """
    with Session(engine) as session:
        session.delete(vote)
        session.commit()
