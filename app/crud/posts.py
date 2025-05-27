from sqlmodel import Session, select
from typing import List
from ..db import engine
from ..models import Posts
from ..schemas import PostsCreate, PostsUpdate


def db_get_all_posts() -> List[Posts]:
    """
    Extracts all elements from the Posts db.
    Returns a list of all Posts instances.
    """
    with Session(engine) as session:
        statement = select(Posts)
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


def db_create_post(post: PostsCreate) -> Posts:
    """
    Takes a post of schema type PostsCreate. Dumps the dictionary
    to the Posts model.Adds the new_post to the DB, commits changes and refreshes the DB.
    Rerturns the Posts object.
    """
    new_post = Posts(**post.model_dump())
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
