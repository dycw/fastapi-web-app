import datetime as dt
from typing import Union

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from fastapi_web_app.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id: Union[Column, int] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Union[Column, str] = Column(String)
    email: Union[Column, str] = Column(String, index=True, unique=True)
    hash_password: Union[Column, str] = Column(String)
    created_date: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    last_login: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    profile_image_url: Union[Column, str] = Column(String)
