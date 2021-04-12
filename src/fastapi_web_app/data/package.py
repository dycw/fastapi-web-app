import datetime as dt
from typing import Union

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import relation

from fastapi_web_app.data.modelbase import SqlAlchemyBase
from fastapi_web_app.data.release import Release


class Package(SqlAlchemyBase):
    __tablename__ = "packages"

    id: Union[Column, str] = Column(String, primary_key=True)
    created_date: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    last_updated: Union[Column, dt.datetime] = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    summary: Union[Column, str] = Column(String, nullable=False)
    description: Union[Column, str] = Column(String, nullable=True)
    home_page: Union[Column, str] = Column(String)
    docs_url: Union[Column, str] = Column(String)
    package_url: Union[Column, str] = Column(String)
    author_name: Union[Column, str] = Column(String)
    author_email: Union[Column, str] = Column(String, index=True)
    license: Union[Column, str] = Column(String, index=True)

    # releases relationship

    releases: list[Release] = relation(
        "Release",
        order_by=[
            Release.major_ver.desc(),
            Release.minor_ver.desc(),
            Release.build_ver.desc(),
        ],
        back_populates="package",
    )

    def __repr__(self) -> str:
        return f"<Package {self.id}>"
