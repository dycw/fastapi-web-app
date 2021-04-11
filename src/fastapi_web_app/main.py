from fastapi import FastAPI
from fastapi_chameleon import global_init
from uvicorn import run

from fastapi_web_app.views import account
from fastapi_web_app.views import home
from fastapi_web_app.views import packages


app = FastAPI()
app.include_router(account.router)
app.include_router(home.router)
app.include_router(packages.router)
global_init("src/templates")


if __name__ == "__main__":
    run(app)
