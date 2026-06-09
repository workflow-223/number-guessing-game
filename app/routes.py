import uuid
from fastapi import APIRouter, HTTPException
from .models import GuessInput, GuessResponse, NewGameResponse, MIN_NUMBER, MAX_NUMBER
from .game import Game, games, proximity_hint

router = APIRouter()


@router.get("/")
def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


@router.post("/new-game", response_model=NewGameResponse)
def new_game():
    game_id = uuid.uuid4().hex
    games[game_id] = Game()
    return NewGameResponse(
        game_id=game_id,
        message=f"Game started! Guess a number between {MIN_NUMBER} and {MAX_NUMBER}.",
    )


@router.post("/guess", response_model=GuessResponse)
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
