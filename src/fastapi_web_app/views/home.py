from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get("/")
@template(template_file="home/index.html")
def index() -> dict[str, str]:
    return {"user_name": "derek"}


@router.get("/about")
def about() -> dict[str, str]:
    return {}
