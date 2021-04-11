from fastapi import FastAPI
from starlette.responses import HTMLResponse
from uvicorn import run


app = FastAPI()


@app.get("/")
def index() -> HTMLResponse:
    content = """
    <h1>Hello FastAPI web app</h1>
    <div>This is where our fake PyPI app will live</div>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    run(app)
