"""Configuration management for EUMAS."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for EUMAS."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def validate(cls) -> Optional[str]:
        """Validate the configuration.

        Returns:
            Optional[str]: Error message if validation fails, None otherwise.
        """
        if not cls.OPENAI_API_KEY:
            return "OPENAI_API_KEY is not set"
        if not cls.WEAVIATE_URL:
            return "WEAVIATE_URL is not set"
        return None
