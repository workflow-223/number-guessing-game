import random
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Number Guessing Game")

app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")

MIN_NUMBER = 1
MAX_NUMBER = 100


class Game:
    def __init__(self):
        self.secret = random.randint(MIN_NUMBER, MAX_NUMBER)
        self.attempts = 0
        self.over = False


games: dict[str, Game] = {}


class GuessInput(BaseModel):
    game_id: str
    number: int = Field(ge=MIN_NUMBER, le=MAX_NUMBER)


class GuessResponse(BaseModel):
    result: str
    hint: str | None = None
    attempts: int
    secret: int | None = None


class NewGameResponse(BaseModel):
    game_id: str
    message: str


def proximity_hint(diff: int) -> str:
    if diff <= 2:
        return "Burning hot!"
    if diff <= 5:
        return "Very close"
    if diff <= 10:
        return "Close"
    if diff <= 20:
        return "Warm"
    if diff <= 35:
        return "Cool"
    if diff <= 50:
        return "Cold"
    return "Freezing"


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.post("/new-game", response_model=NewGameResponse)
def new_game():
    game_id = uuid.uuid4().hex
    games[game_id] = Game()
    return NewGameResponse(
        game_id=game_id,
        message=f"Game started! Guess a number between {MIN_NUMBER} and {MAX_NUMBER}.",
    )


@app.post("/guess", response_model=GuessResponse)
def guess(body: GuessInput):
    game = games.get(body.game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.over:
        raise HTTPException(status_code=400, detail="Game is already over. Start a new game.")

    game.attempts += 1

    diff = abs(body.number - game.secret)
    if body.number < game.secret:
        return GuessResponse(result="too low", hint=proximity_hint(diff), attempts=game.attempts)
    elif body.number > game.secret:
        return GuessResponse(result="too high", hint=proximity_hint(diff), attempts=game.attempts)
    else:
        game.over = True
        return GuessResponse(result="correct", attempts=game.attempts, secret=game.secret)
