from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router

app = FastAPI(title="Number Guessing Game")

app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")
app.include_router(router)
