from typing import Optional

from fastapi_web_app.data.user import User


def user_count() -> int:
    return 73874


def create_account(name: str, email: str, password: str) -> User:
    return User(name, email, password)


def login_user(email: str, password: str) -> Optional[User]:
    if password == "abc":  # noqa: S105
        return User("derek", email, password)
    else:
        return None
