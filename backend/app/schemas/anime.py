from pydantic import BaseModel, HttpUrl

class AnimeSearchResult(BaseModel):
    id: int
    title_english: str | None = None
    title_native: str | None = None 
    image: HttpUrl
    episodes: int | None = None 
    status: str 
    genres: list[str]
    average_score: int | None = None 

class MangaSearchResult(BaseModel):
    id: int
    title_english: str | None = None
    title_native: str | None = None
    image: HttpUrl
    chapters: int | None = None 
    volumes: int | None = None 
    status: str
    genres: list[str]
    average_score: int | None = None 
