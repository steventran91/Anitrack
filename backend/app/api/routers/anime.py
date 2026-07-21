import httpx
import logging
from app.services.anilist import search_anime, map_to_anime_search_results, get_anime_details, map_to_anime_detail
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/anime")
async def search_anime_route(search: str, page: int = 1, per_page: int = 20):
    try:
        raw = await search_anime(search, page=page, per_page=per_page)
    except httpx.HTTPError as e:
        logger.error(f"AniList request failed: {e}")
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    return map_to_anime_search_results(raw)

@router.get("/anime/{anime_id}")
async def get_anime_details_route(anime_id: int):
    try:
        raw = await get_anime_details(anime_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Anime not found")
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    return map_to_anime_detail(raw)