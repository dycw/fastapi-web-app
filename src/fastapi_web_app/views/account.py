from typing import Union

from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from fastapi_web_app.services.users import create_account
from fastapi_web_app.view_models.account import AccountViewModel
from fastapi_web_app.view_models.account import LoginViewModel
from fastapi_web_app.view_models.account import RegisterViewModel


router = APIRouter()


@router.get("/account")
@template()
def index(request: Request) -> dict[str, str]:
    return AccountViewModel(request).to_dict()


@router.get("/account/register")
@template()
def register(request: Request) -> dict[str, str]:
    return RegisterViewModel(request).to_dict()


@router.post("/account/register")
@template()
async def register_p(
    request: Request,
) -> Union[dict[str, str], RedirectResponse]:
    vm = RegisterViewModel(request)
    await vm.load()
    if vm.error:
        return vm.to_dict()
    else:
        create_account(vm.name, vm.email, vm.password)
        return RedirectResponse("/account", status_code=HTTP_302_FOUND)


@router.get("/account/login")
@template()
def login(request: Request) -> dict[str, str]:
    return LoginViewModel(request).to_dict()


@router.get("/account/logout")
@template()
def logout() -> dict[str, str]:
    return {}
