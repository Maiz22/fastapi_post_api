from ..core.security import verify_password, hash_password
from ..models import Users


def authenticate_user(user: Users, password: str) -> bool:
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
