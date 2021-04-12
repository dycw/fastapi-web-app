import datetime as dt
from typing import Union
from typing import cast

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import relation

from fastapi_web_app.data.modelbase import SqlAlchemyBase
from fastapi_web_app.data.release import Release


class Package(SqlAlchemyBase):
    __tablename__ = "packages"

    id: Union[Column, str] = Column(String, primary_key=True)
    created_date: dt.datetime = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    last_updated: dt.datetime = Column(
        DateTime, default=dt.datetime.now, index=True
    )
    summary: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    home_page: str = Column(String)
    docs_url: str = Column(String)
    package_url: str = Column(String)
    author_name: str = Column(String)
    author_email: str = Column(String, index=True)
    license: str = Column(String, index=True)

    # releases relationship

    releases: list[Release] = relation(
        "Release",
        order_by=[
            cast(Column, Release.major_ver).desc(),
            cast(Column, Release.minor_ver).desc(),
            cast(Column, Release.build_ver).desc(),
        ],
        back_populates="package",
    )

    def __repr__(self) -> str:
        return f"<Package {self.id}>"
