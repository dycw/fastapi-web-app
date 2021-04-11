from typing import TypedDict

from starlette.requests import Request

from fastapi_web_app.viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.package_count: int = 274000
        self.release_count: int = 2234847
        self.user_count: int = 73874

        class Package(TypedDict):
            id: str
            summary: str

        self.packages: list[Package] = [
            {"id": "fastapi", "summary": "What you want to master"}
        ]
