import httpx
import logging 
from app.services.anilist import search_manga, map_to_manga_search_results, get_manga_details, map_to_manga_detail
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/manga")
async def search_manga_route(search: str, page: int = 1, per_page: int = 20):
    try:
        raw = await search_manga(search, page=page, per_page=per_page)
    except httpx.HTTPError as e:
        logger.error(f"AniList request failed: {e}")
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    return map_to_manga_search_results(raw)

@router.get("/manga/{manga_id}")
async def get_manga_details_route(manga_id: int):
    try:
        raw = await get_manga_details(manga_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Manga not found")
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="AniList is currently unavailable")
    return map_to_manga_detail(raw)