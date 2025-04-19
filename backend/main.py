from fastapi import FastAPI, Query, HTTPException
from backend.logic import generate_game, load_game
from backend.models import GameGrid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate", response_model=GameGrid)
def generate_grid(seed: str = Query(default=None, description="Optional seed (e.g. 2025-04-18)")):
    try:
        return generate_game(seed=seed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/game/{game_date}", response_model=GameGrid)
def get_grid(game_date: str):
    try:
        return load_game(game_date)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
