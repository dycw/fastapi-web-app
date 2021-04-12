import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from fastapi_web_app.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, index=True, unique=True)
    hash_password = Column(String)
    created_date = Column(DateTime, default=dt.datetime.now, index=True)
    last_login = Column(DateTime, default=dt.datetime.now, index=True)
    profile_image_url = Column(String)
