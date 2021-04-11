from fastapi import APIRouter
from starlette.requests import Request

from fastapi_web_app.view_models.account import AccountViewModel
from fastapi_web_app.view_models.account import LoginViewModel
from fastapi_web_app.view_models.account import RegisterViewModel


router = APIRouter()


@router.get("/account")
def index(request: Request) -> dict[str, str]:
    return AccountViewModel(request).to_dict()


@router.get("/account/register")
def register(request: Request) -> dict[str, str]:
    return RegisterViewModel(request).to_dict()


@router.get("/account/login")
def login(request: Request) -> dict[str, str]:
    return LoginViewModel(request).to_dict()


@router.get("/account/logout")
def logout() -> dict[str, str]:
    return {}
