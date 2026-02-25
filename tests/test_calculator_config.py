"""
Tests for the calculator_config module.
"""

import pytest
import os
from unittest.mock import patch
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    """Test CalculatorConfig class."""

    @patch.dict(os.environ, {}, clear=False)
    def test_default_config_values(self, tmp_path):
        """Test default configuration values when .env doesn't exist."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        os.chdir(tmp_path)
        config = CalculatorConfig(str(tmp_path / "nonexistent.env"))

        assert config.get_history_file() == "history_data.csv"
        assert config.get_auto_save_enabled() is True
        assert config.get_logging_level() == "INFO"
        assert config.get_max_history_records() == 1000

    @patch.dict(os.environ, {}, clear=False)
    def test_config_with_env_file(self, tmp_path):
        """Test configuration loading from .env file."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text(
            "HISTORY_FILE=custom_history.csv\n"
            "AUTO_SAVE_ENABLED=false\n"
            "LOGGING_LEVEL=DEBUG\n"
            "MAX_HISTORY_RECORDS=500\n"
        )

        os.chdir(tmp_path)
        config = CalculatorConfig(str(env_file))

        assert config.get_history_file() == "custom_history.csv"
        assert config.get_auto_save_enabled() is False
        assert config.get_logging_level() == "DEBUG"
        assert config.get_max_history_records() == 500

    @patch.dict(os.environ, {}, clear=False)
    def test_invalid_auto_save_value(self, tmp_path):
        """Test that invalid AUTO_SAVE_ENABLED value raises error."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text("AUTO_SAVE_ENABLED=maybe\n")

        os.chdir(tmp_path)
        with pytest.raises(ConfigurationError):
            CalculatorConfig(str(env_file))

    @patch.dict(os.environ, {}, clear=False)
    def test_invalid_logging_level(self, tmp_path):
        """Test that invalid LOGGING_LEVEL value raises error."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text("LOGGING_LEVEL=INVALID\n")

        os.chdir(tmp_path)
        with pytest.raises(ConfigurationError):
            CalculatorConfig(str(env_file))

    @patch.dict(os.environ, {}, clear=False)
    def test_invalid_max_history_non_integer(self, tmp_path):
        """Test that non-integer MAX_HISTORY_RECORDS raises error."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text("MAX_HISTORY_RECORDS=not_a_number\n")

        os.chdir(tmp_path)
        with pytest.raises(ConfigurationError):
            CalculatorConfig(str(env_file))

    @patch.dict(os.environ, {}, clear=False)
    def test_invalid_max_history_negative(self, tmp_path):
        """Test that negative MAX_HISTORY_RECORDS raises error."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text("MAX_HISTORY_RECORDS=-100\n")

        os.chdir(tmp_path)
        with pytest.raises(ConfigurationError):
            CalculatorConfig(str(env_file))

    @patch.dict(os.environ, {}, clear=False)
    def test_invalid_max_history_zero(self, tmp_path):
        """Test that zero MAX_HISTORY_RECORDS raises error."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text("MAX_HISTORY_RECORDS=0\n")

        os.chdir(tmp_path)
        with pytest.raises(ConfigurationError):
            CalculatorConfig(str(env_file))

    @pytest.mark.parametrize(
        "level",
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    @patch.dict(os.environ, {}, clear=False)
    def test_valid_logging_levels(self, tmp_path, level):
        """Test all valid logging levels."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text(f"LOGGING_LEVEL={level}\n")

        os.chdir(tmp_path)
        config = CalculatorConfig(str(env_file))
        assert config.get_logging_level() == level

    @pytest.mark.parametrize(
        "value",
        ["true", "false"],
    )
    @patch.dict(os.environ, {}, clear=False)
    def test_valid_auto_save_values(self, tmp_path, value):
        """Test valid AUTO_SAVE_ENABLED values."""
        for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
            os.environ.pop(key, None)
        
        env_file = tmp_path / ".env"
        env_file.write_text(f"AUTO_SAVE_ENABLED={value}\n")

        os.chdir(tmp_path)
        config = CalculatorConfig(str(env_file))
        assert config.get_auto_save_enabled() == (value == "true")
