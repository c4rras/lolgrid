import json
import random
from datetime import date
from pathlib import Path
from typing import List, Dict, Optional
from backend.models import GameGrid, GridCondition

DATA_PATH = Path("backend/data/champions.json")
GAMES_DIR = Path("backend/data/generated_games")
GAMES_DIR.mkdir(parents=True, exist_ok=True)

with open(DATA_PATH) as f:
    CHAMPIONS = json.load(f)

REGIONS = sorted({r for c in CHAMPIONS for r in c["regions"]})
POSITIONS = sorted({p for c in CHAMPIONS for p in c["positions"]})
RANGES = sorted({r for c in CHAMPIONS for r in c["range_type"]})
RESOURCES = sorted({c["resource"] for c in CHAMPIONS})
SPECIES = sorted({s for c in CHAMPIONS for s in c["species"]})
GENDERS = sorted({c["gender"] for c in CHAMPIONS})

CONDITION_CATEGORIES = {
    "regions": REGIONS,
    "positions": POSITIONS,
    "range_type": RANGES,
    "resource": RESOURCES,
    "species": SPECIES,
    "gender": GENDERS,
}


def filter_champions(field: str, value: str) -> List[str]:
    return [
        c["championName"]
        for c in CHAMPIONS
        if value in c.get(field, []) or c.get(field) == value
    ]


def generate_game(seed: Optional[str] = None, max_attempts: int = 20) -> GameGrid:
    if seed:
        # Check if the seed's date is in the future
        seed_date = date.fromisoformat(seed)
        if seed_date > date.today():
            raise ValueError("Seed date is in the future. Cannot generate game.")
        random.seed(seed)
    else:
        seed = str(date.today())

    # Check if a game already exists for today
    if (GAMES_DIR / f"{seed}.json").exists():
        return get_todays_game()

    # Build valid conditions (≥4 champs)
    valid_conditions: List[GridCondition] = []
    for field, values in CONDITION_CATEGORIES.items():
        for val in values:
            if len(filter_champions(field, val)) >= 4:
                valid_conditions.append(GridCondition(label=val, field=field, value=val))

    # Build all valid pairs (row x col) with ≥4 champs
    valid_pairs = []
    for row in valid_conditions:
        for col in valid_conditions:
            if row == col:
                continue
            matched = [
                c["championName"]
                for c in CHAMPIONS
                if (row.value in c.get(row.field, []) or c.get(row.field) == row.value)
                and (col.value in c.get(col.field, []) or c.get(col.field) == col.value)
            ]
            if len(matched) >= 4:
                valid_pairs.append((row, col, matched))

    # Try to sample a 3x3 grid
    for _ in range(max_attempts * 5):
        sample = random.sample(valid_pairs, 9)
        rows = {r.label: r for r, _, _ in sample}
        cols = {c.label: c for _, c, _ in sample}
        if len(rows) >= 3 and len(cols) >= 3:
            row_list = list(rows.values())[:3]
            col_list = list(cols.values())[:3]

            answers = {}
            for i, row in enumerate(row_list):
                for j, col in enumerate(col_list):
                    matched = [
                        c["championName"]
                        for c in CHAMPIONS
                        if (row.value in c.get(row.field, []) or c.get(row.field) == row.value)
                        and (col.value in c.get(col.field, []) or c.get(col.field) == col.value)
                    ]
                    if len(matched) < 4:
                        break
                    answers[f"{i}-{j}"] = matched
                else:
                    continue
                break
            else:
                # All cells valid
                game = GameGrid(date=seed, rows=row_list, columns=col_list, answers=answers)
                with open(GAMES_DIR / f"{seed}.json", "w") as f:
                    json.dump(game.dict(), f, indent=2)
                return game

    raise ValueError("Unable to generate a valid grid after multiple attempts.")


def load_game(game_date: str) -> GameGrid:
    with open(GAMES_DIR / f"{game_date}.json") as f:
        data = json.load(f)
    return GameGrid(**data)

def get_todays_game() -> GameGrid:
    today = str(date.today())
    return load_game(today)