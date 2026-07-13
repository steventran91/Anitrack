from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import hash_password
from app.models.user import User 
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(
        first_name = user_in.first_name,
        last_name = user_in.last_name,
        email = user_in.email,
        hashed_password = hash_password(user_in.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail = "Email already registered")
    db.refresh(user)
    return user

