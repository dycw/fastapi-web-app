from typing import Any

from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from fastapi_web_app.view_models.home.index import IndexViewModel


router = APIRouter()


@router.get("/")
@template()
def index(request: Request) -> dict[str, Any]:
    vm = IndexViewModel(request)
    return vm.to_dict()


@router.get("/about")
@template()
def about() -> dict[str, str]:
    return {}
