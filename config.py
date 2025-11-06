"""Bot configuration."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# Get the directory where config.py is located
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings."""

    # Telegram
    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")

    # Google Gemini Pro
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_model_vision: str = Field(default="gemini-1.5-pro-latest", alias="GEMINI_MODEL_VISION")
    gemini_model_text: str = Field(default="gemini-1.5-pro-latest", alias="GEMINI_MODEL_TEXT")

    # MongoDB
    mongodb_uri: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URI")
    mongodb_database: str = Field(default="nutrition_bot", alias="MONGODB_DATABASE")

    # Bot Settings
    bot_language: str = Field(default="ru", alias="BOT_LANGUAGE")
    timezone: str = Field(default="Europe/Moscow", alias="TIMEZONE")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Reports Schedule
    daily_report_time: str = Field(default="21:00", alias="DAILY_REPORT_TIME")
    weekly_report_day: str = Field(default="monday", alias="WEEKLY_REPORT_DAY")
    weekly_report_time: str = Field(default="09:00", alias="WEEKLY_REPORT_TIME")

    # Rate Limiting
    rate_limit_messages: int = Field(default=30, alias="RATE_LIMIT_MESSAGES")

    # Image Optimization
    max_image_size: int = Field(default=2048, alias="MAX_IMAGE_SIZE")
    image_quality: int = Field(default=85, alias="IMAGE_QUALITY")

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
