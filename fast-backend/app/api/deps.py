from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import token as crud_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = crud_token.get_user_by_token(db, token_str=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user
