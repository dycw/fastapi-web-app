import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from fastapi_web_app.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    email: str = Column(String, index=True, unique=True)
    hash_password: str = Column(String)
    created_date: dt.datetime = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    last_login: dt.datetime = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    profile_image_url: str = Column(String)
