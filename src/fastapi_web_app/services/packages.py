import datetime
import datetime as dt
from typing import Optional
from typing import cast

from sqlalchemy import Column
from sqlalchemy.orm import joinedload

from fastapi_web_app.data.db_session import create_session
from fastapi_web_app.data.package import Package
from fastapi_web_app.data.release import Release


def package_count() -> int:
    session = create_session()
    try:
        return session.query(Package).count()
    finally:
        session.close()


def release_count() -> int:
    session = create_session()
    try:
        return session.query(Release).count()
    finally:
        session.close()


def latest_packages(*, limit: int = 5) -> list[Package]:
    session = create_session()
    try:
        releases = (
            session.query(Release)
            .options(joinedload(Release.package))
            .order_by(cast(Column, Release.created_date).desc())
            .limit(limit)
            .all()
        )
        return [r.package for r in releases]
    finally:
        session.close()


def get_package_by_id(package_name: str) -> Optional[Package]:
    session = create_session()
    try:
        return session.query(Package).filter(Package.id == package_name).first()
    finally:
        session.close()


def get_latest_release_for_package(package_name: str) -> Release:  # noqa: U100
    return Release(
        major_ver=1, minor_ver=2, build_ver=0, created_date=dt.datetime.now()
    )
