from typing import Optional

from starlette.requests import Request

from fastapi_web_app.data.user import User
from fastapi_web_app.services.users import get_user_by_email
from fastapi_web_app.services.users import get_user_by_id
from fastapi_web_app.view_models.base import ViewModelBase


class AccountViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.user: Optional[User] = None

    async def load(self) -> None:
        if self.user_id is None:
            raise TypeError("User ID cannot be None")
        else:
            self.user = await get_user_by_id(self.user_id)


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.name: Optional[str] = None
        self.password: Optional[str] = None
        self.email: Optional[str] = None

    async def load(self) -> None:
        form = await self.request.form()
        self.name = form.get("name")
        self.password = form.get("password")
        self.email = form.get("email")

        if not self.name or not self.name.strip():
            self.error = "Your name is required."
        elif not self.email or not self.email.strip():
            self.error = "Your email is required."
        elif not self.password or len(self.password) < 5:
            self.error = (
                "Your password is required and must be at least 5 chars"
            )
        elif (await get_user_by_email(self.email)) is not None:
            self.error = "User already exists"


class LoginViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self) -> None:
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("email")

        if not self.email or not self.email.strip():
            self.error = "Your email is required."
        elif not self.password:
            self.error = "Your password is required"
