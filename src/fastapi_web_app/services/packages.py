import datetime as dt
from typing import Optional

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


def latest_packages(*, limit: int = 5) -> list[dict[str, str]]:
    return [{"id": "fastapi", "summary": "What you want to master"}][:limit]


def get_package_by_id(package_name: str) -> Optional[Package]:
    return Package(
        package_name,
        "This is the summary",
        "Full details here",
        "https://fastapi.tiangolo.com/",
        "MIT",
        "Sebastian Ramirez",
        maintainers=[],
    )


def get_latest_release_for_package(package_name: str) -> Release:  # noqa: U100
    return Release("1.2.0", dt.datetime.now())
