from pydantic import BaseModel
from typing import Optional


class GameCreate(BaseModel):
    title: str
    genre: str
    rating: float
    image_url: Optional[str] = None


class GameUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None

class GameResponse(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    image_url: Optional[str] = None