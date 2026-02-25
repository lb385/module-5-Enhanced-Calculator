"""
Input validation module for the calculator application.

This module provides utilities for validating user inputs, including
numeric values, operations, and command inputs.
"""

from app.exceptions import InvalidInputError


def validate_numeric(value: str) -> float:
    """
    Validate and convert a string to a numeric value.

    Args:
        value: String representation of a number.

    Returns:
        float: The converted numeric value.

    Raises:
        InvalidInputError: If the value cannot be converted to a float.
    """
    try:
        return float(value)
    except ValueError as e:
        raise InvalidInputError(f"Invalid numeric input: '{value}'") from e


def validate_operation(operation: str) -> str:
    """
    Validate that an operation is supported.

    Args:
        operation: The operation name to validate.

    Returns:
        str: The validated operation name (lowercase).

    Raises:
        InvalidInputError: If the operation is not supported.
    """
    valid_operations = {"add", "subtract", "multiply", "divide", "power", "root"}
    op_lower = operation.lower().strip()

    if op_lower not in valid_operations:
        raise InvalidInputError(
            f"Unsupported operation: '{operation}'. "
            f"Valid operations: {', '.join(sorted(valid_operations))}"
        )

    return op_lower


def validate_command(command: str) -> str:
    """
    Validate that a command is recognized.

    Args:
        command: The command to validate.

    Returns:
        str: The validated command (lowercase).

    Raises:
        InvalidInputError: If the command is not recognized.
    """
    valid_commands = {
        "help",
        "history",
        "exit",
        "clear",
        "undo",
        "redo",
        "save",
        "load",
        "set",
    }
    cmd_lower = command.lower().strip()

    if cmd_lower not in valid_commands:
        raise InvalidInputError(
            f"Unknown command: '{command}'. "
            f"Valid commands: {', '.join(sorted(valid_commands))}"
        )

    return cmd_lower


def validate_positive_integer(value: str, param_name: str = "value") -> int:
    """
    Validate that a string is a positive integer.

    Args:
        value: String representation of an integer.
        param_name: Name of the parameter (for error messages).

    Returns:
        int: The converted positive integer.

    Raises:
        InvalidInputError: If the value is not a positive integer.
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            raise ValueError("must be positive")
        return int_value
    except ValueError as e:
        raise InvalidInputError(
            f"Invalid {param_name}: '{value}' must be a positive integer"
        ) from e
