# Number Guessing Game

Classic "guess the number" web game with a FastAPI backend, proximity-based hint system, and session management via UUIDs.

## Deployment

The frontend is deployed to GitHub Pages at:
`https://workflow-223.github.io/number-game/`

**Setup:** In repo Settings → Pages → Source: **Deploy from a branch**, branch: `main`, folder: `/docs`.

Note: The static frontend is deployed. For the full experience including the FastAPI backend, run locally.

## Local Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# Visit http://localhost:8000
```
