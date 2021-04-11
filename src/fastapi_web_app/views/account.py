from fastapi import APIRouter


router = APIRouter()


@router.get("/account")
def index() -> dict[str, str]:
    return {}


@router.get("/account/register")
def register() -> dict[str, str]:
    return {}


@router.get("/account/login")
def login() -> dict[str, str]:
    return {}


@router.get("/account/logout")
def logout() -> dict[str, str]:
    return {}
