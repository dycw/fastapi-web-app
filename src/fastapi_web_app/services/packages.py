from typing import Optional

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from fastapi_web_app.data.db_session import create_async_session
from fastapi_web_app.data.package import Package
from fastapi_web_app.data.release import Release


async def package_count() -> int:
    sel = select(func.count(Package.id))
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar()


async def release_count() -> int:
    sel = select(func.count(Release.id))
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar()


async def latest_packages(*, limit: int = 5) -> list[Package]:
    sel = (
        select(Release)
        .options(joinedload(Release.package))
        .order_by(Release.created_date.desc())
        .limit(limit)
    )
    async with create_async_session() as session:
        releases: list[Release] = (await session.execute(sel)).scalars()
        return [r.package for r in releases]


async def get_package_by_id(package_name: str) -> Optional[Package]:
    sel = select(Package).filter(Package.id == package_name).limit(1)
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar_one_or_none()


async def get_latest_release_for_package(
    package_name: str,
) -> Optional[Release]:
    sel = (
        select(Release)
        .filter(Release.package_id == package_name)
        .order_by(Release.created_date.desc())
        .limit(1)
    )
    async with create_async_session() as session:
        return (await session.execute(sel)).scalar_one_or_none()
