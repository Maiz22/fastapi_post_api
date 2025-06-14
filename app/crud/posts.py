from __future__ import annotations
from typing import TYPE_CHECKING, Sequence, Tuple
from sqlmodel import Session, select, func
from typing import List
import logging
from ..db import engine
from ..models import Posts, Votes, Comments
from ..schemas import PostsCreate, PostsUpdate

if TYPE_CHECKING:
    from ..models import Users


logger = logging.getLogger("uvicorn")


def db_get_all_posts(limit: int, skip: int, search: str) -> List[Posts]:
    """
    Extracts all elements from the Posts db.
    Returns a list of all Posts instances.
    """
    with Session(engine) as session:
        statement = (
            select(Posts)
            .where(Posts.title.ilike(f"%{search}%"))
            .offset(skip)
            .limit(limit)
        )
        results = session.exec(statement)
        posts = results.all()
    return posts


def db_get_post_by_id(id: int) -> Posts | None:
    """
    Takes an id and selects the first element from the db that
    matches the id.
    Returns the corresponding post or None if no post is found.
    """
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == id)
        post = session.exec(statement).first()
    return post


def db_create_post(post: PostsCreate, user: Users) -> Posts:
    """
    Takes a post of schema type PostsCreate. Dumps the dictionary
    to the Posts model.Adds the new_post to the DB, commits changes and refreshes the DB.
    Rerturns the Posts object.
    """
    new_post = Posts(**post.model_dump())
    new_post.user_id = user.id
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


def db_delete_post(post: Posts) -> None:
    """
    Takes a post instance and delete it from db.
    """
    with Session(engine) as session:
        session.delete(post)
        session.commit()


def db_update_post(post: Posts, updated_post: PostsUpdate) -> Posts:
    """
    Take a Posts instance and a post of schmey PostsUpdate.
    Update the post with the data of updated_post and commit
    changes to the DB.
    Return the updated Posts instance.
    """
    updated_data = updated_post.model_dump(exclude_unset=True)
    with Session(engine) as session:
        for key, value in updated_data.items():
            setattr(post, key, value)
            session.add(post)
            session.commit()
            session.refresh(post)
    return post


def db_get_posts_with_votes(
    limit: int = 10, skip: int = 0, search: str = ""
) -> Sequence[Tuple[Posts, int, List[str]]]:
    """
    Performs a left join between posts, votes and comments on the
    posts_id column. Groups everything by posts_id and counts the
    votes per post.
    Returns a Sequence of tuples of Posts with the corresponding
    votes count as int and comments as list of strings.
    """
    with Session(engine) as session:
        statement = (
            select(
                Posts,
                func.count(Votes.post_id).label("votes_count"),
                func.JSON_ARRAYAGG(Comments.content).label("comments"),
            )
            .join(Votes, Posts.id == Votes.post_id, isouter=True)
            .join(Comments, Posts.id == Comments.post_id, isouter=True)
            .group_by(Posts.id)
            .where(Posts.title.ilike(f"%{search}%"))
            .offset(skip)
            .limit(limit)
        )
        votes_count_table = session.exec(statement).all()
    return votes_count_table


def db_get_post_by_id_join_votes_comments(id: int) -> Tuple[Posts, int, List[str]]:
    """
    Takes a post id, selects a post from the db and performs
    a left join between posts, votes and comments on the posts_id
    column. Groups everything by posts_id and counts the votes
    per post.
    Returns a Sequence of tuples of Posts with the corresponding
    votes count as int and comments as list of strings.
    """
    with Session(engine) as session:
        statement = (
            select(
                Posts,
                func.count(Votes.post_id).label("votes_count"),
                func.JSON_ARRAYAGG(Comments.content).label("comments"),
            )
            .join(Votes, Posts.id == Votes.post_id, isouter=True)
            .join(Comments, Posts.id == Comments.post_id, isouter=True)
            .where(Posts.id == id)
            .group_by(Posts.id)
        )
        try:
            post, votes, comments = session.exec(statement).first()
        except TypeError:
            return None, None, None
    return post, votes, comments
