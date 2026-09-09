from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User 
from app.models.anime import AnimeLibraryEntry, MangaLibraryEntry, AnimeStatus, MangaStatus
from app.schemas.library import Dashboard

router = APIRouter()

@router.get("/dashboard", response_model=Dashboard)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anime_list = db.query(AnimeLibraryEntry).filter(AnimeLibraryEntry.user_id == current_user.id, AnimeLibraryEntry.status == AnimeStatus.WATCHING).all()
    manga_list = db.query(MangaLibraryEntry).filter(MangaLibraryEntry.user_id == current_user.id, MangaLibraryEntry.status == MangaStatus.READING).all()
    return Dashboard(continue_watching=anime_list, continue_reading=manga_list)