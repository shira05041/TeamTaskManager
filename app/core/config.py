from pydantic import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    #App settings
    PROJECT_NAME: str = "TeamTaskManager"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    #JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    #Database
    DATABASE_URL: str

    #Optional settings
    CORS_ORIGINS: List[str] = ["*"]
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
