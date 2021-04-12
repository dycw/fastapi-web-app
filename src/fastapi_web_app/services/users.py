from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt
from sqlalchemy import func
from sqlalchemy import select

from fastapi_web_app.data.db_session import create_async_session
from fastapi_web_app.data.user import User


async def user_count() -> int:
    sel = select(func.count(User.id))
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar()


async def create_account(name: str, email: str, password: str) -> User:
    user = User(
        name=name,
        email=email,
        hash_password=sha512_crypt.hash(password, rounds=172434),
    )
    async with create_async_session() as session:
        session.add(user)
        await session.commit()
    return user


async def login_user(email: str, password: str) -> Optional[User]:
    sel = select(User).filter(User.email == email)
    async with create_async_session() as session:
        user: Optional[User] = (await session.execute(sel)).scalar_one_or_none()
    if (user is not None) and sha512_crypt.verify(password, user.hash_password):
        return user
    else:
        return None


async def get_user_by_id(user_id: int) -> Optional[User]:
    sel = select(User).filter(User.id == user_id)
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    sel = select(User).filter(User.email == email)
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar_one_or_none()
