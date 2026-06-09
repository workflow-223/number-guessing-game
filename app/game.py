import random
from .models import MIN_NUMBER, MAX_NUMBER


class Game:
    def __init__(self):
        self.secret = random.randint(MIN_NUMBER, MAX_NUMBER)
        self.attempts = 0
        self.over = False


games: dict[str, Game] = {}


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
