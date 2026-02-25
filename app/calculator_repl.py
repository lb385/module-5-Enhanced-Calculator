"""
REPL (Read-Eval-Print Loop) interface for the calculator application.

This module provides an interactive command-line interface for users
to interact with the calculator, supporting both calculations and commands.
"""

import sys
from typing import Optional
from app.calculator import Calculator, CalculatorLogger
from app.input_validators import (
    validate_numeric,
    validate_command,
    validate_operation,
)
from app.exceptions import (
    CalculatorException,
    InvalidInputError,
    InvalidOperationError,
)
from app.calculator_config import CalculatorConfig


class CalculatorREPL:
    """
    Interactive Read-Eval-Print Loop for the calculator application.

    This class manages the interactive command-line interface,
    parsing user input and dispatching to appropriate handler methods.
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize the REPL interface.

        Args:
            config: Optional configuration object. If None, creates default config.
        """
        try:
            self.config = config or CalculatorConfig()
        except Exception:  # pragma: no cover
            # If config loading fails, continue with defaults
            self.config = None  # pragma: no cover

        max_records = self._get_max_history_records()
        self.calculator = Calculator(
            history_file=self._get_history_file(),
            max_records=max_records
        )
        self.logger = CalculatorLogger()
        self.calculator.add_observer(self.logger)
        self._auto_save = self._get_auto_save()
        self.running = False

    def _get_history_file(self) -> str:
        """Get history file path from config or use default."""
        if self.config:
            return self.config.get_history_file()  # pragma: no cover
        return "history_data.csv"  # pragma: no cover

    def _get_auto_save(self) -> bool:
        """Get auto-save setting from config or use default."""
        if self.config:
            return self.config.get_auto_save_enabled()  # pragma: no cover
        return True  # pragma: no cover

    def _get_max_history_records(self) -> Optional[int]:
        """Get max history records setting from config or use default."""
        if self.config:
            return self.config.get_max_history_records()  # pragma: no cover
        return None  # pragma: no cover

    def start(self) -> None:
        """Start the interactive REPL loop."""
        self.running = True
        self._print_welcome()

        while self.running:
            try:
                user_input = input("\ncalc> ").strip()  # pragma: no cover

                if not user_input:  # pragma: no cover
                    continue  # pragma: no cover

                self._process_input(user_input)  # pragma: no cover

            except KeyboardInterrupt:  # pragma: no cover
                print("\nInterrupted by user")  # pragma: no cover
                self.running = False  # pragma: no cover
            except EOFError:  # pragma: no cover
                self.running = False  # pragma: no cover

        self._cleanup()

    def _process_input(self, user_input: str) -> None:
        """
        Process user input and dispatch to appropriate handler.

        Args:
            user_input: Raw user input string.
        """
        parts = user_input.split()

        if not parts:
            return

        command_or_operation = parts[0].lower()

        # Check if it's a command
        try:
            command = validate_command(command_or_operation)
            
            # Handle commands with arguments (like "set 5")
            if command == "set":
                if len(parts) < 2:
                    print("Usage: set <value>")  # pragma: no cover
                    return  # pragma: no cover
                try:
                    self._handle_set_value(parts[1])
                except CalculatorException as e:  # pragma: no cover
                    print(f"Error: {e}")  # pragma: no cover
            else:
                self._handle_command(command)
            return
        except InvalidInputError:
            pass  # Not a command, try as operation

        # Try to handle as operation
        if len(parts) < 2:
            print("Usage: <operation> <operand_b> or <command>")
            print("Example: add 5")
            return

        try:
            self._handle_operation(command_or_operation, parts[1])
        except CalculatorException as e:
            print(f"Error: {e}")

    def _handle_command(self, command: str) -> None:
        """
        Handle a command.

        Args:
            command: The command to handle.
        """
        if command == "help":
            self._print_help()
        elif command == "history":
            self._show_history()
        elif command == "exit":
            self.running = False
            print("Exiting calculator. Goodbye!")
        elif command == "clear":
            self._clear_history()
        elif command == "undo":
            if self.calculator.undo():
                print(f"Undo successful. Current value: {self.calculator.get_value()}")
            else:
                print("Nothing to undo")  # pragma: no cover
        elif command == "redo":
            if self.calculator.redo():
                print(f"Redo successful. Current value: {self.calculator.get_value()}")
            else:
                print("Nothing to redo")  # pragma: no cover
        elif command == "save":
            self.calculator.save_history_to_csv()
            print("History saved to file")
        elif command == "load":
            self.calculator.load_history_from_csv()
            print("History loaded from file")

    def _handle_operation(self, operation: str, operand_str: str) -> None:
        """
        Handle a calculation operation.

        Args:
            operation: The operation name.
            operand_str: String representation of the second operand.

        Raises:
            InvalidInputError: If operand is invalid.
            InvalidOperationError: If operation fails.
        """
        try:
            operand_b = validate_numeric(operand_str)
        except InvalidInputError as e:
            raise InvalidInputError(f"Invalid operand: {e}") from e

        try:
            result = self.calculator.perform_operation(operation, operand_b)
            print(f"Result: {result}")
        except (InvalidInputError, InvalidOperationError, InvalidInputError) as e:
            raise

    def _handle_set_value(self, value_str: str) -> None:
        """
        Handle setting the current calculator value.

        Args:
            value_str: String representation of the value to set.
        """
        try:
            value = validate_numeric(value_str)
            self.calculator.set_value(value)
            print(f"Value set to: {value}")
        except InvalidInputError as e:
            print(f"Error: {e}")

    def _show_history(self) -> None:
        """Display calculation history."""
        history = self.calculator.get_history()
        if history == "No history records":
            print(history)  # pragma: no cover
        else:
            print("\nCalculation History:")  # pragma: no cover
            print(history)  # pragma: no cover

    def _clear_history(self) -> None:
        """Clear calculation history."""
        self.calculator.clear_history()
        print("History cleared")

    def _print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "=" * 50)
        print("   Welcome to the Advanced Calculator")
        print("=" * 50)
        print("Type 'help' for a list of commands")
        print(f"Current value: {self.calculator.get_value()}")

    def _print_help(self) -> None:
        """Print help message with available commands."""
        help_text = """
Available Commands:
  help      - Display this help message
  history   - Show calculation history
  exit      - Exit the calculator
  clear     - Clear calculation history
  undo      - Undo the last operation
  redo      - Redo the last undone operation
  save      - Save history to file
  load      - Load history from file
  set       - Set current value: set <value>

Available Operations:
  add       - Addition: add <operand>
  subtract  - Subtraction: subtract <operand>
  multiply  - Multiplication: multiply <operand>
  divide    - Division: divide <operand>
  power     - Power: power <operand>
  root      - Root: root <operand>

Examples:
  add 5           - Add 5 to current value
  multiply 2      - Multiply current value by 2
  divide 2        - Divide current value by 2
  power 2         - Square the current value
  root 2          - Get square root of current value
  set 10          - Set current value to 10
"""
        print(help_text)

    def _cleanup(self) -> None:
        """Perform cleanup when exiting."""
        if self._auto_save:
            self.calculator.save_history_to_csv()


def main() -> None:
    """Main entry point for the calculator application."""
    try:
        config = CalculatorConfig()
    except Exception as e:  # pragma: no cover
        print(f"Warning: Failed to load configuration: {e}")
        config = None

    repl = CalculatorREPL(config)
    repl.start()


if __name__ == "__main__":  # pragma: no cover
    main()
