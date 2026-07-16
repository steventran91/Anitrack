from fastapi import FastAPI, Depends
from sqlalchemy import text 
from sqlalchemy.orm import Session
from app.api.routers.auth import router as auth_router
from app.api.routers.anime import router as anime_router
from app.api.routers.manga import router as manga_router

from app.api.deps import get_db

app = FastAPI(title="AniTrack API")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(anime_router)
app.include_router(manga_router)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}