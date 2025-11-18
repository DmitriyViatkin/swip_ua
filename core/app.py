

from core.config.settings import user_settings
from core.infra.builder import FastAPIBuilder

builder = FastAPIBuilder(
    title=user_settings.TITLE,
    description=user_settings.DESCRIPTION,

)

app = builder.get_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


"""app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
"""