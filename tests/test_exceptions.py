"""
Tests for the exceptions module.
"""

import pytest
from app.exceptions import (
    CalculatorException,
    InvalidOperationError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidRootError,
    ConfigurationError,
    HistoryError,
)


class TestExceptions:
    """Test custom exception classes."""

    def test_calculator_exception_is_exception(self):
        """Test that CalculatorException is an Exception."""
        exc = CalculatorException("test message")
        assert isinstance(exc, Exception)

    def test_invalid_operation_error(self):
        """Test InvalidOperationError."""
        exc = InvalidOperationError("test")
        assert isinstance(exc, CalculatorException)

    def test_division_by_zero_error(self):
        """Test DivisionByZeroError."""
        exc = DivisionByZeroError("test")
        assert isinstance(exc, CalculatorException)

    def test_invalid_input_error(self):
        """Test InvalidInputError."""
        exc = InvalidInputError("test")
        assert isinstance(exc, CalculatorException)

    def test_invalid_root_error(self):
        """Test InvalidRootError."""
        exc = InvalidRootError("test")
        assert isinstance(exc, CalculatorException)

    def test_configuration_error(self):
        """Test ConfigurationError."""
        exc = ConfigurationError("test")
        assert isinstance(exc, CalculatorException)

    def test_history_error(self):
        """Test HistoryError."""
        exc = HistoryError("test")
        assert isinstance(exc, CalculatorException)

    def test_exception_message(self):
        """Test exception message preservation."""
        msg = "Custom error message"
        exc = CalculatorException(msg)
        assert str(exc) == msg
