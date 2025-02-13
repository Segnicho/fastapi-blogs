import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mmyy-secret-keyy")
    ALOGORITHM: str = os.getenv("ALOGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 15))
    
    APP_NAME: str = os.getenv("APP_NAME", "Blog API")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8080))

# Create an instance to use across the app
settings = Settings()
