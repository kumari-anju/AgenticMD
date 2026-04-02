from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.models.base import Base

class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True, unique=True, nullable=False)
    token_type = Column(String, default="bearer")
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)
    
    user = relationship("User")
