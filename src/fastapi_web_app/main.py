from pathlib import Path

from fastapi import FastAPI
from fastapi_chameleon import global_init
from git import Repo
from starlette.staticfiles import StaticFiles
from uvicorn import run

from fastapi_web_app.data import db_session
from fastapi_web_app.views import account
from fastapi_web_app.views import home
from fastapi_web_app.views import packages


app = FastAPI()


def main() -> None:
    configure(dev_mode=True)
    run(app, host="127.0.0.1", port=8000, debug=True)


def configure(*, dev_mode: bool) -> None:
    configure_db(dev_mode=dev_mode)
    configure_routes()
    configure_templates(dev_mode=dev_mode)


def configure_db(*, dev_mode: bool) -> None:  # noqa: U100
    root = Path(Repo(".", search_parent_directories=True).working_tree_dir)
    file = root.joinpath("db", "pypi.sqlite")
    db_session.global_init(file)


def configure_routes() -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(account.router)
    app.include_router(home.router)
    app.include_router(packages.router)


def configure_templates(*, dev_mode: bool) -> None:
    global_init("templates", auto_reload=dev_mode)


if __name__ == "__main__":
    main()
else:
    configure(dev_mode=False)
