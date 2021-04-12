from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt

from fastapi_web_app.data.db_session import create_session
from fastapi_web_app.data.user import User


def user_count() -> int:
    session = create_session()
    try:
        return session.query(User).count()
    finally:
        session.close()


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


def get_user_by_id(user_id: int) -> Optional[User]:
    session = create_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()


def get_user_by_email(email: str) -> Optional[User]:
    session = create_session()
    try:
        return session.query(User).filter(User.email == email).first()
    finally:
        session.close()
