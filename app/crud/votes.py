from sqlmodel import Session
from ..db import engine
from ..models import Votes


def db_create_vote(user_id: int, post_id: int) -> Votes | None:
    vote = Votes(user_id=user_id, post_id=post_id)
    with Session(engine) as session:
        session.add(vote)
        session.commit()
        session.refresh()
    return vote
