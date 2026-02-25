"""
Integration tests for the calculator application.

This module provides comprehensive integration tests that verify the complete
workflow of the calculator, including REPL operations, history management,
and state persistence.
"""

import pytest
import os
import tempfile
import shutil
from io import StringIO
from unittest.mock import patch, MagicMock
from app.calculator import Calculator, CalculatorLogger
from app.calculator_repl import CalculatorREPL
from app.calculator_config import CalculatorConfig
from app.history import CalculationHistory


class TestCalculatorIntegration:
    """Integration tests for Calculator class."""

    def test_full_calculation_workflow(self):
        """Test complete calculation workflow with multiple operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "history.csv")
            calc = Calculator(history_file=history_file)

            # Perform multiple operations
            result1 = calc.perform_operation("add", 5)
            assert result1 == 5

            result2 = calc.perform_operation("multiply", 2)
            assert result2 == 10

            result3 = calc.perform_operation("divide", 2)
            assert result3 == 5

            # Verify history
            history = calc.get_history_dataframe()
            assert len(history) == 3

    def test_undo_redo_workflow(self):
        """Test undo and redo functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))

            # Perform operations
            calc.perform_operation("add", 5)  # value = 5
            calc.perform_operation("add", 3)  # value = 8
            assert calc.get_value() == 8

            # Undo once
            calc.undo()
            assert calc.get_value() == 5

            # Redo once
            calc.redo()
            assert calc.get_value() == 8

    def test_observer_integration(self):
        """Test observer pattern integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))
            logger = CalculatorLogger()
            calc.add_observer(logger)

            # Perform operation
            calc.perform_operation("add", 5)

            # Verify observer was notified
            assert len(logger.events) > 0
            assert logger.events[-1]["type"] == "calculation_complete"

    def test_history_save_and_load(self):
        """Test saving and loading history from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "history.csv")

            # Create calculator and perform operations
            calc1 = Calculator(history_file=history_file)
            calc1.perform_operation("add", 5)
            calc1.perform_operation("multiply", 2)
            calc1.save_history_to_csv()

            # Load history in new calculator instance
            calc2 = Calculator(history_file=history_file)
            history = calc2.get_history_dataframe()
            assert len(history) == 2

    def test_max_records_enforcement(self):
        """Test that max_records limit is enforced."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "history.csv")
            calc = Calculator(history_file=history_file, max_records=3)

            # Add more operations than max_records
            for i in range(5):
                calc.perform_operation("add", 1)
                calc.save_history_to_csv()

            # Verify only max_records are kept
            history = calc.get_history_dataframe()
            assert len(history) == 3

    def test_reset_functionality(self):
        """Test calculator reset."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))

            # Perform operations
            calc.perform_operation("add", 5)
            calc.perform_operation("multiply", 2)
            assert calc.get_value() == 10

            # Reset
            calc.reset()
            assert calc.get_value() == 0

    def test_set_value_functionality(self):
        """Test setting arbitrary calculator value."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))

            # Set value
            calc.set_value(42)
            assert calc.get_value() == 42

            # Perform operation on new value
            result = calc.perform_operation("add", 8)
            assert result == 50

    def test_last_calculation_tracking(self):
        """Test that last calculation is tracked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))

            # No calculation yet
            assert calc.get_last_calculation() is None

            # Perform calculation
            calc.perform_operation("add", 5)
            last_calc = calc.get_last_calculation()
            assert last_calc is not None
            assert last_calc.operation == "add"
            assert last_calc.result == 5


class TestREPLIntegration:
    """Integration tests for REPL interface."""

    def test_repl_initialization(self):
        """Test REPL initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()
            assert repl is not None
            assert repl.calculator is not None
            assert repl.running is False

    def test_repl_with_config(self):
        """Test REPL with configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = os.path.join(tmpdir, ".env")
            history_file = os.path.join(tmpdir, "history.csv")

            # Create .env file
            with open(env_file, "w") as f:
                f.write(f"HISTORY_FILE={history_file}\n")
                f.write("AUTO_SAVE_ENABLED=true\n")
                f.write("MAX_HISTORY_RECORDS=100\n")

            # Mock os.path.exists and dotenv to use test env file
            with patch.dict(os.environ, {"HISTORY_FILE": history_file}):
                repl = CalculatorREPL()
                assert repl.calculator is not None

    def test_repl_help_command(self):
        """Test help command output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._handle_command("help")
                output = fake_out.getvalue()
                assert "Available Commands" in output
                assert "Available Operations" in output

    def test_repl_history_command(self):
        """Test history command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            # No history yet
            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._show_history()
                output = fake_out.getvalue()
                # Empty dataframe or no history message acceptable
                assert "No history records" in output or "Empty DataFrame" in output

            # Add calculation and check history
            repl.calculator.perform_operation("add", 5)
            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._show_history()
                output = fake_out.getvalue()
                assert "Calculation History" in output

    def test_repl_clear_command(self):
        """Test clear history command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            # Add some history
            repl.calculator.perform_operation("add", 5)
            repl.calculator.perform_operation("multiply", 2)
            assert len(repl.calculator.get_history_dataframe()) == 2

            # Clear history
            repl._clear_history()
            assert len(repl.calculator.get_history_dataframe()) == 0

    def test_repl_undo_redo_commands(self):
        """Test undo and redo commands via REPL."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            # Perform operations
            repl._handle_operation("add", "5")
            repl._handle_operation("add", "3")
            assert repl.calculator.get_value() == 8

            # Undo via command
            repl._handle_command("undo")
            assert repl.calculator.get_value() == 5

            # Redo via command
            repl._handle_command("redo")
            assert repl.calculator.get_value() == 8

    def test_repl_save_load_commands(self):
        """Test save and load history commands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            history_file = os.path.join(tmpdir, "history.csv")
            repl = CalculatorREPL()
            repl.calculator = Calculator(history_file=history_file)

            # Add calculation
            repl.calculator.perform_operation("add", 5)

            # Save
            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._handle_command("save")
                output = fake_out.getvalue()
                assert "History saved" in output

            # Verify file exists
            assert os.path.exists(history_file) or len(repl.calculator.get_history_dataframe()) > 0

    def test_repl_set_command(self):
        """Test set value command via REPL."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._handle_set_value("42")
                output = fake_out.getvalue()
                assert "Value set to" in output
                assert repl.calculator.get_value() == 42

    def test_repl_operation_handling(self):
        """Test REPL operation handling."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._handle_operation("add", "5")
                output = fake_out.getvalue()
                assert "Result" in output
                assert repl.calculator.get_value() == 5

    def test_repl_invalid_operation_handling(self):
        """Test REPL error handling for invalid operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with pytest.raises(Exception):
                repl._handle_operation("invalid_op", "5")

    def test_repl_process_input_with_operation(self):
        """Test process input with operation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()):
                repl._process_input("add 5")
                assert repl.calculator.get_value() == 5

    def test_repl_process_input_with_command(self):
        """Test process input with command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            repl.calculator.perform_operation("add", 5)
            assert len(repl.calculator.get_history_dataframe()) == 1

            with patch("sys.stdout", new=StringIO()):
                repl._process_input("clear")
                assert len(repl.calculator.get_history_dataframe()) == 0

    def test_repl_process_input_with_set_command(self):
        """Test process input with set command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()):
                repl._process_input("set 100")
                assert repl.calculator.get_value() == 100

    def test_repl_process_input_empty(self):
        """Test process input with empty string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            # Should not raise any exception
            repl._process_input("")
            repl._process_input("   ")

    def test_repl_process_input_missing_operand(self):
        """Test process input with missing operand."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repl = CalculatorREPL()

            with patch("sys.stdout", new=StringIO()) as fake_out:
                repl._process_input("add")
                output = fake_out.getvalue()
                assert "Usage" in output


class TestHistoryIntegration:
    """Integration tests for History management."""

    def test_history_persistence(self):
        """Test that history persists across calculator instances."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "test_history.csv")

            # First calculator
            calc1 = Calculator(history_file=history_file)
            calc1.perform_operation("add", 10)
            calc1.perform_operation("multiply", 2)
            calc1.save_history_to_csv()

            # Second calculator loads same file
            calc2 = Calculator(history_file=history_file)
            history = calc2.get_history_dataframe()
            assert len(history) == 2
            assert history["operation"].tolist() == ["add", "multiply"]

    def test_history_with_max_records_persistence(self):
        """Test that max_records limit persists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "test_history.csv")

            # Create calculator with max 2 records
            calc = Calculator(history_file=history_file, max_records=2)
            calc.perform_operation("add", 1)
            calc.perform_operation("add", 2)
            calc.perform_operation("add", 3)
            calc.save_history_to_csv()

            # Verify only 2 records
            history = calc.get_history_dataframe()
            assert len(history) == 2

    def test_history_dataframe_access(self):
        """Test accessing history as dataframe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))
            calc.perform_operation("add", 5)
            calc.perform_operation("multiply", 2)

            df = calc.get_history_dataframe()
            assert len(df) == 2
            assert list(df.columns) == [
                "operand_a",
                "operand_b",
                "operation",
                "result",
                "timestamp",
            ]

    def test_history_clear_via_calculator(self):
        """Test clearing history via calculator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))
            calc.perform_operation("add", 5)
            calc.perform_operation("add", 3)
            assert len(calc.get_history_dataframe()) == 2

            calc.clear_history()
            assert len(calc.get_history_dataframe()) == 0

    def test_empty_history_handling(self):
        """Test handling empty history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            calc = Calculator(history_file=os.path.join(tmpdir, "history.csv"))
            history = calc.get_history_dataframe()
            assert len(history) == 0

            # Should return empty dataframe without error
            assert history is not None
