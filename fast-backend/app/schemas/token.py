from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenCreate(BaseModel):
    access_token: str
    user_id: int
    expires_at: datetime
