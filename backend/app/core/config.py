from pydantic_settings import BaseSettings
from typing import List
import secrets
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "MU OneLink Viewer"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.4.2-alpha"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://mu_user:changeMe123!@localhost:5432/mu_onelink"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # Email
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = 587
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # Feature Flags
    ENABLE_AI_ANALYSIS: bool = True
    ENABLE_FINANCIAL_INTEGRATION: bool = False
    ENABLE_AUDIT_EXPORT: bool = True
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_DEVICE_GPS: bool = False
    
    # Limits
    MAX_FILE_SIZE_MB: int = 100
    MAX_DEVICES_PER_WORKER: int = 5
    MAX_CREDENTIALS_PER_DEVICE: int = 3
    EVENT_RETENTION_DAYS: int = 90
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
