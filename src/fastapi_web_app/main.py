from fastapi import FastAPI
from fastapi_chameleon import global_init
from uvicorn import run

from fastapi_web_app.views import account
from fastapi_web_app.views import home
from fastapi_web_app.views import packages


app = FastAPI()


def main() -> None:
    configure()
    run(app, host="127.0.0.1", port=8000)


def configure() -> None:
    configure_routes()
    configure_templates()


def configure_routes() -> None:
    app.include_router(account.router)
    app.include_router(home.router)
    app.include_router(packages.router)


def configure_templates() -> None:
    global_init("src/fastapi_web_app/templates")


if __name__ == "__main__":
    main()
else:
    configure()
