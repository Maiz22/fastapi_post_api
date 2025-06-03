from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from ..models import Comments
from ..db import engine


def create_comment(post_id: int, user_id: int, content: str) -> Comments:
    comment = Comments(post_id=post_id, user_id=user_id, content=content)
    try:
        with Session(engine) as session:
            session.add(comment)
            session.commit()
            session.refresh(comment)
    except IntegrityError:
        return None
    return comment
