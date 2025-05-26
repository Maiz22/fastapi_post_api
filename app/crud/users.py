from sqlmodel import Session, select
from ..db import engine
from ..models import Users


def get_user_by_id(id: int) -> Users | None:
    """
    Takes an id of type int and selects the coressponding
    user from the db.
    Returns user or None if no user could be found.
    """
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        user = session.exec(statement).first()
    return user
