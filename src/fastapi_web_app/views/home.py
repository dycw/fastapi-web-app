from typing import Any

from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from fastapi_web_app.view_models.base import ViewModelBase
from fastapi_web_app.view_models.index import IndexViewModel


router = APIRouter()


@router.get("/")
@template()
def index(request: Request) -> dict[str, Any]:
    return IndexViewModel(request).to_dict()


@router.get("/about")
@template()
def about(request: Request) -> dict[str, str]:
    return ViewModelBase(request).to_dict()
