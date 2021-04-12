from typing import Any
from typing import Optional

from starlette.requests import Request

from fastapi_web_app.infrastructure.cookie_auth import (
    get_user_id_via_auth_cookie,
)


class ViewModelBase:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.error: Optional[str] = None
        self.user_id: Optional[int] = get_user_id_via_auth_cookie(self.request)
        self.is_logged_in = self.user_id is not None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
