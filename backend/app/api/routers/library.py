from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User 
from app.models.anime import AnimeLibraryEntry
from app.schemas.library import AnimeLibraryEntryCreate, AnimeLibraryEntryOut, AnimeLibraryEntryUpdate

router = APIRouter()

@router.post("/library/anime", response_model=AnimeLibraryEntryOut, status_code=status.HTTP_201_CREATED)
def add_anime_to_library(
    entry_in: AnimeLibraryEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = AnimeLibraryEntry(
        user_id=current_user.id,
        anime_id=entry_in.anime_id,
        status=entry_in.status,
    )
    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Anime already in library")
    db.refresh(entry)
    return entry

@router.get("/library/anime", response_model=list[AnimeLibraryEntryOut])
def list_anime_library(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    anime_list = db.query(AnimeLibraryEntry).filter(AnimeLibraryEntry.user_id == current_user.id).all()
    return anime_list

@router.patch("/library/anime/{anime_id}", response_model=AnimeLibraryEntryOut)
def update_anime_library_entry(anime_id: int, entry_in: AnimeLibraryEntryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anime = db.query(AnimeLibraryEntry).filter(AnimeLibraryEntry.user_id == current_user.id, AnimeLibraryEntry.anime_id == anime_id).first()

    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    if entry_in.status is not None:
        anime.status = entry_in.status
    if entry_in.current_episode is not None:
        anime.current_episode = entry_in.current_episode
    
    db.commit()
    db.refresh(anime)
    return anime

@router.delete("/library/anime/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_anime_library_entry(anime_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anime = db.query(AnimeLibraryEntry).filter(AnimeLibraryEntry.user_id == current_user.id, AnimeLibraryEntry.anime_id == anime_id).first()

    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    db.delete(anime)
    db.commit()
    return None

