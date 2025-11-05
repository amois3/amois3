"""Bot configuration."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # Telegram
    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")

    # OpenAI
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_model_vision: str = Field(default="gpt-4o", alias="OPENAI_MODEL_VISION")
    openai_model_text: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL_TEXT")

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

    # OpenAI Cost Tracking
    openai_cost_limit_daily: float = Field(default=10.0, alias="OPENAI_COST_LIMIT_DAILY")
    openai_cost_warn_threshold: float = Field(default=0.8, alias="OPENAI_COST_WARN_THRESHOLD")

    # Image Optimization
    max_image_size: int = Field(default=2048, alias="MAX_IMAGE_SIZE")
    image_quality: int = Field(default=85, alias="IMAGE_QUALITY")

    # Rate Limiting
    rate_limit_messages: int = Field(default=30, alias="RATE_LIMIT_MESSAGES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
