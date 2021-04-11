from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get("/")
@template()
def index() -> dict[str, str]:
    return {"user_name": "derek"}


@router.get("/about")
@template()
def about() -> dict[str, str]:
    return {}
