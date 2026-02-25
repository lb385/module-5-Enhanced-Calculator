"""
Tests for the calculator module.
"""

import pytest
from app.calculator import Calculator, Observer, CalculatorLogger
from app.calculation import Calculation
from app.exceptions import (
    InvalidOperationError,
    DivisionByZeroError,
    InvalidRootError,
    InvalidInputError,
)


class TestCalculator:
    """Test Calculator class."""

    def test_calculator_initialization(self, tmp_path):
        """Test calculator initialization."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        assert calc.get_value() == 0.0

    def test_set_value(self, tmp_path):
        """Test setting calculator value."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(42)
        assert calc.get_value() == 42

    @pytest.mark.parametrize(
        "operation,operand_b,initial,expected",
        [
            ("add", 5, 10, 15),
            ("subtract", 3, 10, 7),
            ("multiply", 4, 5, 20),
            ("divide", 2, 10, 5),
            ("power", 2, 2, 4),
            ("root", 2, 4, 2),
        ],
    )
    def test_operations(self, tmp_path, operation, operand_b, initial, expected):
        """Test various operations."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)
        calc.set_value(initial)

        result = calc.perform_operation(operation, operand_b)
        assert abs(result - expected) < 1e-10

    def test_operation_with_floats(self, tmp_path):
        """Test operations with float values."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(5.5)
        result = calc.perform_operation("add", 2.3)

        assert abs(result - 7.8) < 1e-10

    def test_division_by_zero(self, tmp_path):
        """Test division by zero raises error."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(10)
        with pytest.raises((DivisionByZeroError, InvalidOperationError)):
            calc.perform_operation("divide", 0)

    def test_invalid_root_error(self, tmp_path):
        """Test invalid root raises error."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(-4)
        with pytest.raises((InvalidRootError, InvalidOperationError)):
            calc.perform_operation("root", 2)

    def test_invalid_operation_name(self, tmp_path):
        """Test invalid operation name raises error."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        with pytest.raises(InvalidInputError):
            calc.perform_operation("invalid_op", 5)

    def test_undo_redo(self, tmp_path):
        """Test undo and redo functionality."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(10)
        calc.perform_operation("add", 5)
        assert calc.get_value() == 15

        calc.undo()
        assert calc.get_value() == 10

        calc.redo()
        assert calc.get_value() == 15

    def test_undo_empty_stack(self, tmp_path):
        """Test undo when stack is empty."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        result = calc.undo()
        assert result is False

    def test_redo_empty_stack(self, tmp_path):
        """Test redo when stack is empty."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        result = calc.redo()
        assert result is False

    def test_get_history(self, tmp_path):
        """Test getting history."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(5)
        calc.perform_operation("add", 3)

        history_str = calc.get_history()
        assert "5" in history_str or "add" in history_str

    def test_clear_history(self, tmp_path):
        """Test clearing history."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(5)
        calc.perform_operation("add", 3)
        calc.clear_history()

        history_str = calc.get_history()
        # After clearing, should have no records (empty DataFrame returns "Empty DataFrame...")
        assert calc._calculation_history.get_record_count() == 0

    def test_get_last_calculation(self, tmp_path):
        """Test getting last calculation."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        assert calc.get_last_calculation() is None

        calc.set_value(5)
        calc.perform_operation("add", 3)

        last_calc = calc.get_last_calculation()
        assert isinstance(last_calc, Calculation)
        assert last_calc.result == 8

    def test_reset(self, tmp_path):
        """Test resetting calculator."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(42)
        calc.reset()

        assert calc.get_value() == 0.0
        assert calc.get_last_calculation() is None

    def test_observer_notification(self, tmp_path):
        """Test observer pattern notification."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)
        logger = CalculatorLogger()

        calc.add_observer(logger)

        calc.set_value(10)
        calc.perform_operation("add", 5)

        assert len(logger.events) > 0

    def test_remove_observer(self, tmp_path):
        """Test removing observer."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)
        logger = CalculatorLogger()

        calc.add_observer(logger)
        calc.remove_observer(logger)

        initial_count = len(logger.events)
        calc.perform_operation("add", 5)

        # No new events should be added
        assert len(logger.events) == initial_count

    def test_multiple_operations_sequence(self, tmp_path):
        """Test sequence of multiple operations."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(10)
        result1 = calc.perform_operation("add", 5)  # 15
        assert result1 == 15

        result2 = calc.perform_operation("multiply", 2)  # 30
        assert result2 == 30

        result3 = calc.perform_operation("divide", 3)  # 10
        assert abs(result3 - 10) < 1e-10

    def test_case_insensitive_operations(self, tmp_path):
        """Test operations are case-insensitive."""
        history_file = str(tmp_path / "history.csv")
        calc = Calculator(history_file)

        calc.set_value(10)
        result1 = calc.perform_operation("ADD", 5)
        assert result1 == 15

        calc.set_value(10)
        result2 = calc.perform_operation("Multiply", 2)
        assert result2 == 20


class TestCalculatorLogger:
    """Test CalculatorLogger observer."""

    def test_logger_initialization(self):
        """Test logger initialization."""
        logger = CalculatorLogger()
        assert logger.events == []

    def test_logger_update(self):
        """Test logger update method."""
        logger = CalculatorLogger()

        calc = Calculation(5, 3, "add", 8)
        logger.update("calculation_complete", calc)

        assert len(logger.events) == 1
        assert logger.events[0]["type"] == "calculation_complete"

    def test_logger_error_event(self):
        """Test logger logging error events."""
        logger = CalculatorLogger()
        logger.update("error", error="Test error")

        assert len(logger.events) == 1
        assert logger.events[0]["type"] == "error"
        assert logger.events[0]["error"] == "Test error"


class TestObserverInterface:
    """Test Observer interface."""

    def test_observer_update_method(self):
        """Test observer can be created with update method."""

        class TestObserver(Observer):  # pragma: no cover
            def __init__(self):
                self.called = False

            def update(self, event_type, calculation=None, error=None):
                self.called = True

        observer = TestObserver()
        observer.update("test")
        assert observer.called
