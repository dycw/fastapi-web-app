from typing import Any

from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get("/")
@template()
def index() -> dict[str, Any]:
    return {
        "user_name": "derek",
        "package_count": 274000,
        "release_count": 2234847,
        "user_count": 73874,
        "packages": [{"id": "fastapi", "summary": "What you want to master"}],
    }


@router.get("/about")
@template()
def about() -> dict[str, str]:
    return {}
