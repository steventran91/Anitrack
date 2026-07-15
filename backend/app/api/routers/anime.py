import httpx
import logging
from app.services.anilist import search_anime, map_to_anime_search_results
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