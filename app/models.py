from pydantic import BaseModel, Field

MIN_NUMBER = 1
MAX_NUMBER = 100


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
