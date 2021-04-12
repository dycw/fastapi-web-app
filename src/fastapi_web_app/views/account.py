from asyncio import sleep
from typing import Union

from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from fastapi_web_app.infrastructure.cookie_auth import logout_user
from fastapi_web_app.infrastructure.cookie_auth import set_auth
from fastapi_web_app.services.users import create_account
from fastapi_web_app.services.users import login_user
from fastapi_web_app.view_models.account import AccountViewModel
from fastapi_web_app.view_models.account import LoginViewModel
from fastapi_web_app.view_models.account import RegisterViewModel


router = APIRouter()


@router.get("/account", include_in_schema=False)
@template()
async def index(request: Request) -> dict[str, str]:
    model = AccountViewModel(request)
    await model.load()
    return model.to_dict()


@router.get("/account/register", include_in_schema=False)
@template()
async def register(request: Request) -> dict[str, str]:  # type: ignore
    model = RegisterViewModel(request)
    await model.load()
    return model.to_dict()


@router.post("/account/register", include_in_schema=False)
@template()
async def register(  # noqa: F811
    request: Request,
) -> Union[dict[str, str], RedirectResponse]:
    vm = RegisterViewModel(request)
    await vm.load()
    if vm.error or vm.name is None or vm.email is None or vm.password is None:
        return vm.to_dict()
    else:
        user = await create_account(vm.name, vm.email, vm.password)
        response = RedirectResponse("/account", status_code=HTTP_302_FOUND)
        set_auth(response, user.id)
        return response


@router.get("/account/login", include_in_schema=False)
@template()
async def login(request: Request) -> dict[str, str]:  # type: ignore
    model = LoginViewModel(request)
    await model.load()
    return model.to_dict()


@router.post("/account/login", include_in_schema=False)
@template()
async def login(  # noqa: F811
    request: Request,
) -> Union[dict[str, str], RedirectResponse]:
    vm = LoginViewModel(request)
    await vm.load()
    if vm.error or vm.email is None or vm.password is None:
        return vm.to_dict()
    else:
        user = await login_user(vm.email, vm.password)
        if user is None:
            await sleep(1.0)  # throttle
            vm.error = "The account does not exist or the password is wrong"
            return vm.to_dict()
        else:
            response = RedirectResponse("/account", status_code=HTTP_302_FOUND)
            set_auth(response, user.id)
            return response


@router.get("/account/logout", include_in_schema=False)
def logout() -> RedirectResponse:
    response = RedirectResponse("/", status_code=HTTP_302_FOUND)
    logout_user(response)
    return response
