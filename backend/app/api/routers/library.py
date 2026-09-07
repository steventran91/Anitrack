from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User 
from app.models.anime import AnimeLibraryEntry, MangaLibraryEntry
from app.schemas.library import AnimeLibraryEntryCreate, AnimeLibraryEntryOut, AnimeLibraryEntryUpdate, MangaLibraryEntryCreate, MangaLibraryEntryOut, MangaLibraryEntryUpdate

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

@router.get("/library/manga",response_model=list[MangaLibraryEntryOut])
def list_manga_library(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    manga_list = db.query(MangaLibraryEntry).filter(MangaLibraryEntry.user_id == current_user.id).all()
    return manga_list

@router.post("/library/manga", response_model=MangaLibraryEntryOut, status_code=status.HTTP_201_CREATED)
def add_manga_to_library(entry_in: MangaLibraryEntryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entry = MangaLibraryEntry(
        user_id=current_user.id,
        manga_id=entry_in.manga_id,
        status=entry_in.status
    )
    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Manga already in library")
    db.refresh(entry)
    return entry

@router.patch("/library/manga/{manga_id}", response_model=MangaLibraryEntryOut)
def update_manga_library_entry(manga_id: int, entry_in: MangaLibraryEntryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    manga = db.query(MangaLibraryEntry).filter(MangaLibraryEntry.user_id == current_user.id, MangaLibraryEntry.manga_id == manga_id).first()

    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")
    if entry_in.status is not None:
        manga.status = entry_in.status
    if entry_in.current_chapter is not None:
        manga.current_chapter = entry_in.current_chapter
    db.commit()
    db.refresh(manga)
    return manga 

@router.delete("/library/manga/{manga_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manga_from_library(manga_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    manga = db.query(MangaLibraryEntry).filter(MangaLibraryEntry.user_id == current_user.id, MangaLibraryEntry.manga_id == manga_id).first()

    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")
    db.delete(manga)
    db.commit()
    return None


