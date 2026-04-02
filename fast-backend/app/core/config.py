from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Gemini configuration
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"
    # Auth configuration
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
