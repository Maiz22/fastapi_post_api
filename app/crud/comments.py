from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models import Comments
from ..db import engine


def db_create_comment(post_id: int, user_id: int, content: str) -> Comments:
    comment = Comments(post_id=post_id, user_id=user_id, content=content)
    try:
        with Session(engine) as session:
            session.add(comment)
            session.commit()
            session.refresh(comment)
    except IntegrityError:
        return None
    return comment


def db_delete_comment(comment: Comments) -> None:
    with Session(engine) as session:
        session.delete(comment)
        session.commit()
    return


def db_get_comment_by_id(id: int) -> Comments:
    with Session(engine) as session:
        statement = select(Comments).where(Comments.id == id)
        comment = session.exec(statement).first()
    return comment
