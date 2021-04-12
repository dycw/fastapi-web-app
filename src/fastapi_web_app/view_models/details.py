from starlette.requests import Request

from fastapi_web_app.services.packages import get_latest_release_for_package
from fastapi_web_app.services.packages import get_package_by_id
from fastapi_web_app.view_models.base import ViewModelBase


class DetailsViewModel(ViewModelBase):
    def __init__(self, package_name: str, request: Request) -> None:
        super().__init__(request)
        self.package_name = package_name
        self.latest_version = "0.0.0"
        self.is_latest = True
        self.maintainers = []
        self.package = None
        self.latest_release = None

    async def load(self) -> None:
        self.package = await get_package_by_id(self.package_name)
        self.latest_release = await get_latest_release_for_package(
            self.package_name
        )
        if not self.package or not self.latest_version:
            return
        r = self.latest_release
        self.latest_version = f"{r.major_ver}.{r.minor_ver}.{r.build_ver}"
