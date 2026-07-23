from pydantic import BaseModel
from datetime import date
from app.models.anime import AnimeStatus

class AnimeLibraryEntryCreate(BaseModel):
    anime_id: int
    status: AnimeStatus = AnimeStatus.PLAN_TO_WATCH

class AnimeLibraryEntryUpdate(BaseModel):
    status: AnimeStatus | None = None 
    current_episode: int | None = None

class AnimeLibraryEntryOut(BaseModel):
    id: int
    anime_id: int
    status: AnimeStatus
    current_episode: int 
    start_date: date | None = None 

    model_config = {"from_attributes": True}