from __future__ import annotations
from typing import TYPE_CHECKING
from ..core.security import verify_password, hash_password
from ..models import Users

if TYPE_CHECKING:
    from fastapi import Request


def authenticate_user(user: Users, password: str) -> bool:
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
