from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.token import Token
from app.core.config import settings

def create_token(db: Session, user_id: int, access_token: str):
    expires_at = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    db_token = Token(
        access_token=access_token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_user_by_token(db: Session, token_str: str):
    db_token = db.query(Token).filter(Token.access_token == token_str).first()
    if not db_token or db_token.expires_at < datetime.utcnow():
        return None
    return db_token.user
