from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.crud import user as crud_user
from app.crud import token as crud_token
from app.core.security import generate_random_token
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_in.password != user_in.confirm_pass:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return crud_user.create_user(db, user_in=user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    # Note: Using UserCreate for login for simplicity (email/password)
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if not user or user.password != user_in.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = generate_random_token()
    crud_token.create_token(db, user_id=user.id, access_token=access_token)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    """
    Returns the currently logged-in user's profile.
    """
    return current_user
