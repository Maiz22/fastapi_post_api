from sqlmodel import Session, select
from ..db import engine
from ..schemas import UsersCreate
from ..models import Users
from ..core import security


def db_get_user_by_id(id: int) -> Users | None:
    """
    Takes an id of type int and selects the coressponding
    user from the db.
    Returns user or None if no user could be found.
    """
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        user = session.exec(statement).first()
    return user


def db_get_user_by_email(email: str) -> Users | None:
    """
    Takes an email and selects a user from the DB that matches
    the email address.
    Returns User instance or None if no user was found.
    """
    with Session(engine) as session:
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()
    return user


def db_create_user(user: UsersCreate) -> Users:
    """
    Takes a user of schema type UsersCreate. Dumps the dictionary
    to the Users model and replaces the password with the hashed
    password. Adds the new_user to the DB, commits changes and refreshes the DB.
    Rerturns the User object.
    """
    new_user = Users(**user.model_dump())
    new_user.password = security.hash_password(user.password)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
