from starlette.requests import Request

from fastapi_web_app.services.package_service import latest_packages
from fastapi_web_app.services.package_service import package_count
from fastapi_web_app.services.package_service import release_count
from fastapi_web_app.services.user_service import user_count
from fastapi_web_app.view_models.base import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.package_count: int = package_count()
        self.release_count: int = release_count()
        self.user_count: int = user_count()
        self.packages: list[dict[str, str]] = latest_packages(limit=5)
