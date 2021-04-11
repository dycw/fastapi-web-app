from typing import Any
from typing import Optional

from starlette.requests import Request


class ViewModelBase:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.error: Optional[str] = None
        self.user_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
