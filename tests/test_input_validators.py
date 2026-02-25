"""
Tests for the input_validators module.
"""

import pytest
from app.input_validators import (
    validate_numeric,
    validate_operation,
    validate_command,
    validate_positive_integer,
)
from app.exceptions import InvalidInputError


class TestValidateNumeric:
    """Test validate_numeric function."""

    @pytest.mark.parametrize(
        "input_val,expected",
        [
            ("5", 5.0),
            ("5.5", 5.5),
            ("-5", -5.0),
            ("0", 0.0),
            ("1e2", 100.0),
            ("-3.14", -3.14),
        ],
    )
    def test_valid_numeric_inputs(self, input_val, expected):
        """Test validation of valid numeric inputs."""
        assert validate_numeric(input_val) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "abc",
            "1a2",
            "",
            "12.34.56",
            "1.2.3",
        ],
    )
    def test_invalid_numeric_inputs(self, invalid_input):
        """Test validation rejects invalid numeric inputs."""
        with pytest.raises(InvalidInputError):
            validate_numeric(invalid_input)


class TestValidateOperation:
    """Test validate_operation function."""

    @pytest.mark.parametrize(
        "operation",
        ["add", "subtract", "multiply", "divide", "power", "root"],
    )
    def test_valid_operations(self, operation):
        """Test validation of valid operations."""
        result = validate_operation(operation)
        assert result == operation.lower()

    @pytest.mark.parametrize(
        "operation",
        ["ADD", "Subtract", "MULTIPLY", " divide ", "POWER", "Root"],
    )
    def test_case_insensitive_operations(self, operation):
        """Test that operations are case-insensitive."""
        result = validate_operation(operation)
        assert result == operation.lower().strip()

    @pytest.mark.parametrize(
        "invalid_op",
        ["invalid", "mod", "sqrt", "ln", "sin"],
    )
    def test_invalid_operations(self, invalid_op):
        """Test validation rejects invalid operations."""
        with pytest.raises(InvalidInputError):
            validate_operation(invalid_op)


class TestValidateCommand:
    """Test validate_command function."""

    @pytest.mark.parametrize(
        "command",
        ["help", "history", "exit", "clear", "undo", "redo", "save", "load", "set"],
    )
    def test_valid_commands(self, command):
        """Test validation of valid commands."""
        result = validate_command(command)
        assert result == command.lower()

    @pytest.mark.parametrize(
        "command",
        ["HELP", "History", "EXIT", " clear ", "UNDO", "SET"],
    )
    def test_case_insensitive_commands(self, command):
        """Test that commands are case-insensitive."""
        result = validate_command(command)
        assert result == command.lower().strip()

    @pytest.mark.parametrize(
        "invalid_cmd",
        ["invalid", "quit", "reset", "cls"],
    )
    def test_invalid_commands(self, invalid_cmd):
        """Test validation rejects invalid commands."""
        with pytest.raises(InvalidInputError):
            validate_command(invalid_cmd)


class TestValidatePositiveInteger:
    """Test validate_positive_integer function."""

    @pytest.mark.parametrize("value", ["1", "5", "100", "999"])
    def test_valid_positive_integers(self, value):
        """Test validation of valid positive integers."""
        result = validate_positive_integer(value)
        assert result == int(value)
        assert result > 0

    @pytest.mark.parametrize(
        "invalid_val",
        ["0", "-5", "abc", "1.5", ""],
    )
    def test_invalid_values(self, invalid_val):
        """Test validation rejects invalid values."""
        with pytest.raises(InvalidInputError):
            validate_positive_integer(invalid_val)

    def test_custom_param_name(self):
        """Test custom parameter name in error message."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_positive_integer("abc", "test_param")
        assert "test_param" in str(exc_info.value)
