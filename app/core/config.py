from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenSMIL Signage"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/opensmil.db"
    
    # Security
    SECRET_KEY: str = "supersecretkeychangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Storage
    STORAGE_TYPE: str = "local" # local or s3
    MEDIA_LOCAL_PATH: str = "./media_local"
    S3_BUCKET: Optional[str] = None
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
