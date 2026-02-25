"""
Configuration management module.

This module handles loading and managing configuration settings
using environment variables and the python-dotenv library.
"""

import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration settings."""

    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration by loading from .env file.

        Args:
            env_file: Path to the .env file to load.

        Raises:
            ConfigurationError: If configuration loading fails.
        """
        self._load_env(env_file)
        self._validate_config()

    @staticmethod
    def _load_env(env_file: str) -> None:
        """Load environment variables from .env file."""
        if os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            # If .env doesn't exist, just use defaults
            pass

    @staticmethod
    def _validate_config() -> None:
        """Validate configuration settings."""
        auto_save = os.getenv("AUTO_SAVE_ENABLED", "true").lower()
        if auto_save not in ("true", "false"):
            raise ConfigurationError(
                f"Invalid AUTO_SAVE_ENABLED value: {auto_save}. "
                "Must be 'true' or 'false'."
            )

        logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if logging_level not in valid_levels:
            raise ConfigurationError(
                f"Invalid LOGGING_LEVEL value: {logging_level}. "
                f"Must be one of: {', '.join(valid_levels)}"
            )

        try:
            max_history = int(os.getenv("MAX_HISTORY_RECORDS", "1000"))
            if max_history <= 0:
                raise ValueError("MAX_HISTORY_RECORDS must be positive")
        except ValueError as e:
            raise ConfigurationError(
                f"Invalid MAX_HISTORY_RECORDS: {e}"
            ) from e

    @staticmethod
    def get_history_file() -> str:
        """Get the history file path from configuration."""
        return os.getenv("HISTORY_FILE", "history_data.csv")

    @staticmethod
    def get_auto_save_enabled() -> bool:
        """Check if auto-saving is enabled."""
        return os.getenv("AUTO_SAVE_ENABLED", "true").lower() == "true"

    @staticmethod
    def get_logging_level() -> str:
        """Get the logging level from configuration."""
        return os.getenv("LOGGING_LEVEL", "INFO").upper()

    @staticmethod
    def get_max_history_records() -> int:
        """Get the maximum number of history records to keep."""
        return int(os.getenv("MAX_HISTORY_RECORDS", "1000"))
