from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt
from sqlalchemy import func
from sqlalchemy import select

from fastapi_web_app.data.db_session import create_async_session
from fastapi_web_app.data.db_session import create_session
from fastapi_web_app.data.user import User


async def user_count() -> int:
    sel = select(func.count(User.id))
    async with create_async_session() as session:
        result = await session.execute(sel)
        return result.scalar()


def create_account(name: str, email: str, password: str) -> User:
    session = create_session()
    try:
        user = User(
            name=name,
            email=email,
            hash_password=sha512_crypt.hash(password, rounds=172434),
        )
        session.add(user)
        session.commit()
        return user
    finally:
        session.close()


def login_user(email: str, password: str) -> Optional[User]:
    session = create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return user
        else:
            if sha512_crypt.verify(password, user.hash_password):
                return user
            else:
                return None
    finally:
        session.close()


async def get_user_by_id(user_id: int) -> Optional[User]:
    sel = select(User).filter(User.id == user_id)
    async with create_async_session() as session:
        return session.execute(sel).scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    sel = select(User).filter(User.email == email)
    async with create_async_session() as session:
        return session.execute(sel).scalar_one_or_none()
