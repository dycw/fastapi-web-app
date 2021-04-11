from fastapi import FastAPI
from uvicorn import run


app = FastAPI()


@app.get("/")
def index() -> dict[str, str]:
    return {"message": "Hello world"}


run(app)
