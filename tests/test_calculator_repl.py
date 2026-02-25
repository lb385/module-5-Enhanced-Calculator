"""
Tests for the calculator_repl module.
"""

import os
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from app.calculator_repl import CalculatorREPL, main
from app.exceptions import InvalidInputError
from app.calculator_config import CalculatorConfig


class TestCalculatorREPL:
    """Test CalculatorREPL class."""

    def test_repl_initialization(self, tmp_path):
        """Test REPL initialization."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            assert repl.calculator is not None
            assert repl.logger is not None
            assert repl.running is False

    def test_get_history_file_with_config(self, tmp_path):
        """Test getting history file path from config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            env_file = tmp_path / ".env"
            env_file.write_text("HISTORY_FILE=custom.csv\n")

            config = CalculatorConfig(str(env_file))
            repl = CalculatorREPL(config)

            assert repl._get_history_file() == "custom.csv"

    def test_get_history_file_without_config(self, tmp_path):
        """Test getting default history file when no config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            repl = CalculatorREPL(None)

            assert repl._get_history_file() == "history_data.csv"

    def test_get_auto_save_with_config(self, tmp_path):
        """Test getting auto-save setting from config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            env_file = tmp_path / ".env"
            env_file.write_text("AUTO_SAVE_ENABLED=false\n")

            config = CalculatorConfig(str(env_file))
            repl = CalculatorREPL(config)

            assert repl._get_auto_save() is False

    def test_get_auto_save_without_config(self, tmp_path):
        """Test default auto-save setting when no config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            repl = CalculatorREPL(None)

            assert repl._get_auto_save() is True

    def test_get_max_history_records_with_config(self, tmp_path):
        """Test getting max history records from config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            env_file = tmp_path / ".env"
            env_file.write_text("MAX_HISTORY_RECORDS=500\n")

            config = CalculatorConfig(str(env_file))
            repl = CalculatorREPL(config)

            assert repl._get_max_history_records() == 500

    def test_get_max_history_records_without_config(self, tmp_path):
        """Test default max history records when no config."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            
            # When config creation fails, _get_max_history_records should return None
            # But when config loads successfully, it returns the default 1000
            repl = CalculatorREPL(None)
            # Since CalculatorConfig is created by default, we get 1000
            assert repl._get_max_history_records() == 1000

    def test_process_input_with_command(self, tmp_path):
        """Test processing command input."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("help")
                # Should print help
                assert mock_print.called

    def test_process_input_with_operation(self, tmp_path):
        """Test processing operation input."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl.calculator.set_value(10)
                repl._process_input("add 5")
                assert mock_print.called

    def test_process_input_invalid_operation(self, tmp_path):
        """Test processing invalid operation."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("invalid_op 5")
                # Should print error
                assert mock_print.called

    def test_handle_command_help(self, tmp_path):
        """Test help command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._handle_command("help")
                assert mock_print.called

    def test_handle_command_history(self, tmp_path):
        """Test history command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._handle_command("history")
                assert mock_print.called

    def test_handle_command_exit(self, tmp_path):
        """Test exit command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()
            repl.running = True

            with patch("builtins.print"):
                repl._handle_command("exit")
                assert repl.running is False

    def test_handle_command_clear(self, tmp_path):
        """Test clear command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            repl.calculator.set_value(5)
            repl.calculator.perform_operation("add", 3)

            with patch("builtins.print"):
                repl._handle_command("clear")

    def test_handle_command_undo(self, tmp_path):
        """Test undo command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            repl.calculator.set_value(10)
            repl.calculator.perform_operation("add", 5)

            with patch("builtins.print") as mock_print:
                repl._handle_command("undo")
                assert mock_print.called

    def test_handle_command_redo_nothing_to_redo(self, tmp_path):
        """Test redo command when nothing to redo."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._handle_command("redo")
                # Should print "Nothing to redo"
                mock_print.assert_called()

    def test_show_history_with_records(self, tmp_path):
        """Test showing history when records exist."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()
            
            repl.calculator.perform_operation("add", 5)

            with patch("builtins.print") as mock_print:
                repl._show_history()
                # Should print "Calculation History:"
                assert any(
                    "Calculation History" in str(call)
                    for call in mock_print.call_args_list
                )

    def test_handle_command_save(self, tmp_path):
        """Test save command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._handle_command("save")
                assert mock_print.called

    def test_handle_command_load(self, tmp_path):
        """Test load command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._handle_command("load")
                assert mock_print.called

    def test_handle_operation_valid(self, tmp_path):
        """Test handling valid operation."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            repl.calculator.set_value(10)

            with patch("builtins.print") as mock_print:
                repl._handle_operation("add", "5")
                assert mock_print.called

    def test_handle_operation_invalid_operand(self, tmp_path):
        """Test handling operation with invalid operand."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with pytest.raises(InvalidInputError):
                repl._handle_operation("add", "invalid")

    def test_handle_set_value(self, tmp_path):
        """Test setting value."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print"):
                repl._handle_set_value("42")

            assert repl.calculator.get_value() == 42

    def test_handle_set_value_invalid(self, tmp_path):
        """Test setting invalid value."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print"):
                repl._handle_set_value("invalid")

    def test_show_history(self, tmp_path):
        """Test showing history."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._show_history()
                assert mock_print.called

    def test_clear_history_cmd(self, tmp_path):
        """Test clearing history command."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._clear_history()
                assert mock_print.called

    def test_print_welcome(self, tmp_path):
        """Test welcome message."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._print_welcome()
                assert mock_print.called

    def test_print_help(self, tmp_path):
        """Test help message."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._print_help()
                assert mock_print.called

    def test_process_input_empty(self, tmp_path):
        """Test processing empty input."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("")
                # Should not raise, but might not print

    def test_process_input_whitespace_only(self, tmp_path):
        """Test processing whitespace-only input."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("   ")
                # Should not raise

    def test_process_input_insufficient_args(self, tmp_path):
        """Test processing operation with missing operand."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("add")
                assert mock_print.called

    def test_process_input_set_command(self, tmp_path):
        """Test processing set command with value."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print"):
                repl._process_input("set 42")
                assert repl.calculator.get_value() == 42

    def test_process_input_set_command_missing_value(self, tmp_path):
        """Test processing set command without value."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print") as mock_print:
                repl._process_input("set")
                assert mock_print.called

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_start_keyboard_interrupt(self, mock_input, tmp_path):
        """Test REPL handles keyboard interrupt."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            with patch("builtins.print"):
                repl.start()

            assert repl.running is False

    @patch("builtins.input", side_effect=EOFError)
    def test_start_eof(self, mock_input, tmp_path):
        """Test REPL handles EOF."""
        os.chdir(tmp_path)
        with patch.dict(os.environ, {}, clear=False):
            for key in ['HISTORY_FILE', 'AUTO_SAVE_ENABLED', 'LOGGING_LEVEL', 'MAX_HISTORY_RECORDS']:
                os.environ.pop(key, None)
            repl = CalculatorREPL()

            repl.start()
            assert repl.running is False


class TestMainFunction:
    """Test main function."""

    @patch("app.calculator_repl.CalculatorREPL.start")
    def test_main_function(self, mock_start, tmp_path):
        """Test main function."""
        import os

        os.chdir(tmp_path)
        main()

        assert mock_start.called
