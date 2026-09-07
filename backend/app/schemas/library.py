from pydantic import BaseModel
from datetime import date
from app.models.anime import AnimeStatus, MangaStatus


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

class MangaLibraryEntryCreate(BaseModel):
    manga_id: int
    status: MangaStatus = MangaStatus.PLAN_TO_READ

class MangaLibraryEntryUpdate(BaseModel):
    status: MangaStatus | None = None
    current_chapter: int | None = None 

class MangaLibraryEntryOut(BaseModel):
    id: int
    manga_id: int
    status: MangaStatus
    current_chapter: int
    start_date: date | None = None 

    model_config = {"from_attributes": True}