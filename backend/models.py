from pydantic import BaseModel

class GridCondition(BaseModel):
    label: str
    field: str
    value: str

class GameGrid(BaseModel):
    date: str
    rows: list[GridCondition]
    columns: list[GridCondition]
    answers: dict[str, list[str]]
