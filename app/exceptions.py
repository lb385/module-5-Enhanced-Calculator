"""
Custom exceptions for the calculator application.

This module defines custom exception classes used throughout the calculator
to handle various error conditions in a standardized manner.
"""


class CalculatorException(Exception):
    """Base exception class for all calculator-related errors."""

    pass


class InvalidOperationError(CalculatorException):
    """Raised when an invalid operation is requested."""

    pass


class DivisionByZeroError(CalculatorException):
    """Raised when attempting to divide by zero."""

    pass


class InvalidInputError(CalculatorException):
    """Raised when invalid input is provided by the user."""

    pass


class InvalidRootError(CalculatorException):
    """Raised when attempting to compute root with invalid parameters."""

    pass


class ConfigurationError(CalculatorException):
    """Raised when configuration loading or validation fails."""

    pass


class HistoryError(CalculatorException):
    """Raised when history-related operations fail."""

    pass
