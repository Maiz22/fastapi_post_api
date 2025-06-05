from ..db import redis_client
from ..config.settings import settings


def get_key(username: str) -> str:
    """
    Takes the username or emamil.
    Returns a redis key of a prefix and the username.
    """
    return f"login_attempts:{username}"


def is_locked_out(username: str) -> bool:
    """
    Takes a username. Gets the number of attempts from the redis
    db by username.
    Returns true if an entry exists and if the value is bigger
    or equal to the amount of attempts.
    """
    key = get_key(username)
    attempts = redis_client.get(key)
    return attempts is not None and int(attempts) >= settings.throttling_max_attempts


def register_failed_attempt(username: str):
    """
    Sets a new entry in the redis db or increments the number of
    attempts in the db if the key (username) already exists.
    Adds an expiration time after which an entry is deleted.
    """
    key = get_key(username)
    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.set(key, 1, ex=settings.throttling_lockout_time)
