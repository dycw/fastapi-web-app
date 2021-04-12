import datetime as dt
from typing import Union

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relation

from fastapi_web_app.data.modelbase import SqlAlchemyBase


class Release(SqlAlchemyBase):
    __tablename__ = "releases"

    id: Union[Column, int] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    major_ver: Union[Column, int] = Column(BigInteger, index=True)
    minor_ver: Union[Column, int] = Column(BigInteger, index=True)
    build_ver: Union[Column, int] = Column(BigInteger, index=True)
    created_date: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    comment: Union[Column, str] = Column(String)
    url: Union[Column, str] = Column(String)
    size: Union[Column, int] = Column(BigInteger)

    # package relationship
    package_id: Union[Column, str] = Column(String, ForeignKey("packages.id"))
    package = relation("Package")

    @property
    def version_text(self) -> str:
        return f"{self.major_ver}.{self.minor_ver}.{self.build_ver}"
