from fastapi_web_app.data.user import User


def user_count() -> int:
    return 73874


def create_account(name: str, email: str, password: str) -> User:
    return User(name, email, password)
