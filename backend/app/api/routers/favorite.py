from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session 

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.favorite import Favorite, FavoriteType
from app.schemas.favorite import FavoriteEntryCreate, FavoriteEntryOut


# DELETE /favorite/{item_type}/{item_id}
router = APIRouter()

@router.post("/favorites", response_model=FavoriteEntryOut, status_code=status.HTTP_201_CREATED)
def add_to_favorite(entry_in: FavoriteEntryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorite = Favorite(
        user_id=current_user.id,
        item_type=entry_in.item_type,
        item_id=entry_in.item_id,
    )
    db.add(favorite)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{entry_in.item_type} already favorited")
    db.refresh(favorite)
    return favorite

@router.get("/favorites", response_model=list[FavoriteEntryOut])
def list_favorite(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorites_list = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    return favorites_list 

@router.delete("/favorites/{item_type}/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite_entry(item_type: FavoriteType ,item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorite = db.query(Favorite).filter(Favorite.item_id == item_id, Favorite.item_type == item_type, Favorite.user_id == current_user.id).first()


    if not favorite:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    db.delete(favorite)
    db.commit()
    return None 

