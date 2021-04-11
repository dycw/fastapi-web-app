from fastapi import FastAPI
from fastapi_chameleon import global_init
from fastapi_chameleon import template
from uvicorn import run


app = FastAPI()
global_init("templates")


@app.get("/")
@template(template_file="index.html")
def index() -> dict[str, str]:
    return {"user_name": "derek"}


if __name__ == "__main__":
    run(app)
