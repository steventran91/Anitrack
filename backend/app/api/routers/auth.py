from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import hash_password
from app.models.user import User 
from app.schemas.user import UserCreate, UserOut, UserLogin, Token
from app.core.security import verify_password, create_access_token

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

@router.post("/login", response_model=Token)
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


