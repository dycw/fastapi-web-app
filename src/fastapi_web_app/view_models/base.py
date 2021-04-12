from typing import Any
from typing import Optional

from starlette.requests import Request

from fastapi_web_app.infrastructure.cookie_auth import (
    get_user_id_from_auth_cookie,
)


class ViewModelBase:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.error: Optional[str] = None
        self.user_id: Optional[str] = None
        self.is_logged_in = get_user_id_from_auth_cookie(self.request)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
