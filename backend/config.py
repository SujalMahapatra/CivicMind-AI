"""
CivicMind AI - Configuration Module

This module handles application configuration using pydantic-settings,
a powerful tool for managing application settings in a clean and type-safe way.

WHAT IS PYDANTIC-SETTINGS?
pydantic-settings is a library built on top of Pydantic that provides a simple,
automatic way to load configuration from environment variables and .env files.
It validates the data types automatically and provides clear error messages if
configuration values are invalid.

WHY USE ENVIRONMENT VARIABLES?
Environment variables keep sensitive data (like API keys) and environment-specific
settings (like database URLs) out of your source code. This makes your application:
- More secure: Secrets aren't hardcoded
- More portable: Same code runs in dev, staging, and production
- Easier to configure: Change settings without modifying code

WHY USE A SINGLETON SETTINGS OBJECT?
A singleton ensures that configuration is loaded only once when the application starts.
This provides:
- Performance: Settings are parsed once, not on every request
- Consistency: The same configuration is used throughout the application
- Simplicity: Import 'settings' anywhere without worrying about initialization
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    Application configuration settings for CivicMind AI.

    This class defines all configuration options for the application.
    Each field can be set via:
    1. Environment variables (e.g., export API_VERSION=2.0.0)
    2. A .env file in the project root
    3. Default values defined here (used as fallback)

    Attributes:
        APP_NAME: The display name of the application
        API_VERSION: Current API version (e.g., "1.0.0")
        ENVIRONMENT: Environment type (development, staging, production)
        DEBUG: Whether debug mode is enabled (shows detailed error messages)
        GEMINI_API_KEY: API key for Google Gemini AI service
        DATABASE_URL: Connection string for the SQL database
        VECTOR_DB_PATH: Directory path for ChromaDB vector storage
    """

    # =============================================================================
    # GENERAL APPLICATION SETTINGS
    # =============================================================================
    APP_NAME: str = "CivicMind AI"
    API_VERSION: str = "1.0.0"
    

    ENVIRONMENT: Literal[
        "development",
        "staging",
        "production"
    ] = "development"
    DEBUG: bool = False

    # =============================================================================
    # AI SERVICE CONFIGURATION
    # =============================================================================
    GEMINI_API_KEY: str 

    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    DATABASE_URL: str = "sqlite:///./civicmind.db"
    VECTOR_DB_PATH: str = "./vector_db"

    # =============================================================================
    # PYDANTIC-SETTINGS CONFIGURATION
    # =============================================================================
    model_config: SettingsConfigDict = SettingsConfigDict(
        # Look for a .env file in the current directory to load variables from
        env_file=".env",
        # Use UTF-8 encoding for the .env file
        env_file_encoding="utf-8",
        # Ignore extra fields in .env that aren't defined in this class
        extra="ignore"
    )
#Property_helper
@property
def is_production(self) -> bool:
    return self.ENVIRONMENT == "production"

#Future_model_config
MAX_UPLOAD_SIZE_MB: int = 50

DEFAULT_FORECAST_DAYS: int = 30

# Create a singleton settings instance
# This is imported throughout the application wherever configuration is needed.
# Example usage:
#   from config import settings
#   print(settings.APP_NAME)  # -> "CivicMind AI"
#   print(settings.DATABASE_URL)  # -> Value from .env or default
settings: Settings = Settings()

__all__ = ["settings", "Settings"]
