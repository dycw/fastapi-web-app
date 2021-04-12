from starlette.requests import Request

from fastapi_web_app.services.packages import get_latest_release_for_package
from fastapi_web_app.services.packages import get_package_by_id
from fastapi_web_app.view_models.base import ViewModelBase


class DetailsViewModel(ViewModelBase):
    def __init__(self, package_name: str, request: Request) -> None:
        super().__init__(request)
        self.package_name = package_name
        self.package = get_package_by_id(package_name)
        self.latest_release = get_latest_release_for_package(package_name)
        self.latest_version = "0.0.0"
        self.is_latest = True
        self.maintainers = []
        if not self.package or not self.latest_version:
            return
        self.latest_version = self.latest_release.version
        self.maintainers = self.package.maintainers