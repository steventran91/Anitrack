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

class CharacterOut(BaseModel):
    id: int
    name: str | None = None 
    image: HttpUrl
    description: str | None = None 

class RecommendationOut(BaseModel):
    id: int
    title: str | None = None 
    image: HttpUrl

class RelationOut(BaseModel):
    id: int
    title: str | None = None 
    image: HttpUrl
    relation_type: str 

class AnimeDetail(AnimeSearchResult):
    description: str | None = None
    banner_image: HttpUrl | None = None 
    studios: list[str] 
    characters: list[CharacterOut]
    recommendations: list[RecommendationOut]
    relations: list[RelationOut]

class MangaDetail(MangaSearchResult):
    description: str | None = None
    banner_image: HttpUrl | None = None
    authors: list[str]
    characters: list[CharacterOut]
    recommendations: list[RecommendationOut]
    relations: list[RelationOut]




