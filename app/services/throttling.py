import time


def is_locked_out(user_id: int) -> bool:
    pass
    # get locked_until from user_locked_db
    # locket_until = cache_get_user_locked(user_id)
    # if locket_until and locket_until > time.time():
    #    return False
    # return True


def register_failed_attempt(user_id: int) -> None:
    pass
    # save attempt in db with timestamp
    # get total number of attempts
    # if num attempts > 5:
    # add_user_to_locked_db
