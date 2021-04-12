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

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    major_ver: int = Column(BigInteger, index=True)
    minor_ver: int = Column(BigInteger, index=True)
    build_ver: int = Column(BigInteger, index=True)
    created_date: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    comment: str = Column(String)
    url: str = Column(String)
    size: int = Column(BigInteger)

    # package relationship
    package_id: str = Column(String, ForeignKey("packages.id"))
    package = relation("Package")

    @property
    def version_text(self) -> str:
        return f"{self.major_ver}.{self.minor_ver}.{self.build_ver}"
