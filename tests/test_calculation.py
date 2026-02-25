"""
Tests for the calculation module.
"""

import pytest
from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Test Calculation class."""

    def test_calculation_creation(self):
        """Test creating a calculation."""
        calc = Calculation(5, 3, "add", 8)
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.operation == "add"
        assert calc.result == 8

    def test_calculation_timestamp_auto_created(self):
        """Test that timestamp is automatically created."""
        calc = Calculation(5, 3, "add", 8)
        assert calc.timestamp is not None
        assert isinstance(calc.timestamp, datetime)

    def test_calculation_timestamp_explicit(self):
        """Test creating calculation with explicit timestamp."""
        ts = datetime.now()
        calc = Calculation(5, 3, "add", 8, ts)
        assert calc.timestamp == ts

    def test_calculation_str_representation(self):
        """Test string representation of calculation."""
        calc = Calculation(5, 3, "add", 8)
        str_repr = str(calc)
        assert "5" in str_repr
        assert "3" in str_repr
        assert "add" in str_repr
        assert "8" in str_repr

    @pytest.mark.parametrize(
        "a,b,op,res",
        [
            (10, 2, "divide", 5),
            (2, 8, "power", 256),
            (16, 2, "root", 4),
            (-5, 3, "multiply", -15),
        ],
    )
    def test_various_calculations(self, a, b, op, res):
        """Test calculations with various operations."""
        calc = Calculation(a, b, op, res)
        assert calc.result == res
        assert calc.operation == op

    def test_calculation_to_dict(self):
        """Test conversion to dictionary."""
        ts = datetime.now()
        calc = Calculation(5, 3, "add", 8, ts)
        calc_dict = calc.to_dict()

        assert calc_dict["operand_a"] == 5
        assert calc_dict["operand_b"] == 3
        assert calc_dict["operation"] == "add"
        assert calc_dict["result"] == 8
        assert calc_dict["timestamp"] == ts.isoformat()

    def test_calculation_with_floats(self):
        """Test calculation with float values."""
        calc = Calculation(5.5, 2.3, "add", 7.8)
        assert abs(calc.operand_a - 5.5) < 1e-10
        assert abs(calc.operand_b - 2.3) < 1e-10
        assert abs(calc.result - 7.8) < 1e-10
