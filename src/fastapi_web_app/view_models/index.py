from starlette.requests import Request

from fastapi_web_app.data.package import Package
from fastapi_web_app.services.packages import latest_packages
from fastapi_web_app.services.packages import package_count
from fastapi_web_app.services.packages import release_count
from fastapi_web_app.services.users import user_count
from fastapi_web_app.view_models.base import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.release_count: int = 0
        self.user_count: int = 0
        self.package_count: int = 0
        self.packages: list[Package] = []

    async def load(self) -> None:
        self.release_count = release_count()
        self.user_count: int = await user_count()
        self.package_count: int = package_count()
        self.packages: list[Package] = latest_packages(limit=5)
