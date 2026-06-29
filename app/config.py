# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

settings = Settings()