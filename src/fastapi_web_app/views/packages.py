from typing import Any

from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from fastapi_web_app.view_models.details import DetailsViewModel


router = APIRouter()


@router.get("/project/{package_name}")
@template()
def details(package_name: str, request: Request) -> dict[str, Any]:
    return DetailsViewModel(package_name, request).to_dict()
