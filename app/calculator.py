"""
Main calculator module implementing Facade and Observer patterns.

This module provides the Calculator class which serves as a facade
to the complex subsystems and supports observer pattern for event notifications.
"""

from typing import List, Callable, Optional
from app.operations import OperationFactory, OperationStrategy
from app.calculation import Calculation
from app.exceptions import (
    InvalidOperationError,
    InvalidInputError,
)
from app.input_validators import validate_operation
from app.calculator_memento import CalculatorHistory as MementoHistory
from app.history import CalculationHistory
from app.calculator_config import CalculatorConfig


class Observer:
    """Observer interface for calculator events."""

    def update(self, event_type: str, calculation: Optional[Calculation] = None, error: Optional[str] = None) -> None:
        """
        Handle calculator events.

        Args:
            event_type: Type of event ('calculation_complete', 'error', 'state_change').
            calculation: The calculation that triggered the event (if applicable).
            error: Error message (if applicable).
        """
        pass  # pragma: no cover


class CalculatorLogger(Observer):
    """Observer that logs calculation events."""

    def __init__(self):
        """Initialize the logger observer."""
        self.events: List[dict] = []

    def update(self, event_type: str, calculation: Optional[Calculation] = None, error: Optional[str] = None) -> None:
        """Log an event."""
        event = {
            "type": event_type,
            "calculation": str(calculation) if calculation else None,
            "error": error,
        }
        self.events.append(event)


class Calculator:
    """
    Main Calculator class implementing the Facade pattern.

    This class provides a simplified interface to the complex calculator
    subsystems including operations, history management, and state preservation.
    """

    def __init__(self, history_file: str = "history_data.csv", max_records: Optional[int] = None):
        """
        Initialize the calculator.

        Args:
            history_file: Path to the CSV file for history persistence.
            max_records: Maximum number of history records to keep. If None, no limit.
        """
        self._current_value: float = 0.0
        self._calculation_history = CalculationHistory(history_file, max_records)
        self._memento_history = MementoHistory()
        self._observers: List[Observer] = []
        self._last_calculation: Optional[Calculation] = None

    def add_observer(self, observer: Observer) -> None:
        """
        Add an observer to be notified of calculator events.

        Args:
            observer: The observer to add.
        """
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer.

        Args:
            observer: The observer to remove.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(
        self,
        event_type: str,
        calculation: Optional[Calculation] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Notify all observers of an event.

        Args:
            event_type: Type of event.
            calculation: Associated calculation if applicable.
            error: Associated error if applicable.
        """
        for observer in self._observers:
            observer.update(event_type, calculation, error)

    def perform_operation(
        self, operation: str, operand_b: float
    ) -> float:
        """
        Perform a calculation operation.

        Args:
            operation: Name of the operation ('add', 'subtract', etc.).
            operand_b: The second operand.

        Returns:
            float: The result of the operation.

        Raises:
            InvalidOperationError: If the operation is not supported.
            InvalidInputError: If input validation fails.
        """
        try:
            # Validate operation
            operation = validate_operation(operation)

            # Save current state for undo
            self._memento_history.save_state(self._current_value)

            # Get operation strategy using Factory pattern
            operation_strategy: OperationStrategy = OperationFactory.create_operation(
                operation
            )

            # Execute operation using Strategy pattern
            result = operation_strategy.execute(self._current_value, operand_b)

            # Create calculation record
            calculation = Calculation(
                operand_a=self._current_value,
                operand_b=operand_b,
                operation=operation,
                result=result,
            )

            # Update state
            self._current_value = result
            self._last_calculation = calculation

            # Add to history and save
            self._calculation_history.add_calculation(
                calculation.operand_a,
                calculation.operand_b,
                calculation.operation,
                calculation.result,
            )
            self._calculation_history.save_to_csv()

            # Notify observers of successful calculation
            self._notify_observers("calculation_complete", calculation)

            return result

        except (InvalidOperationError, InvalidInputError) as e:
            self._notify_observers("error", error=str(e))
            raise
        except Exception as e:
            self._notify_observers("error", error=str(e))
            raise InvalidOperationError(f"Operation failed: {e}") from e

    def set_value(self, value: float) -> None:
        """
        Set the current calculator value.

        Args:
            value: The value to set.
        """
        self._memento_history.save_state(self._current_value)
        self._current_value = value
        self._notify_observers("state_change")

    def get_value(self) -> float:
        """
        Get the current calculator value.

        Returns:
            float: The current value.
        """
        return self._current_value

    def undo(self) -> bool:
        """
        Undo the last operation.

        Returns:
            bool: True if undo was successful, False otherwise.
        """
        if not self._memento_history.can_undo():
            return False

        previous_value = self._memento_history.undo()
        if previous_value is not None:
            # Save current state to redo stack
            self._memento_history.push_to_redo(self._current_value)
            self._current_value = previous_value
            self._notify_observers("state_change")
            return True
        return False  # pragma: no cover

    def redo(self) -> bool:
        """
        Redo the last undone operation.

        Returns:
            bool: True if redo was successful, False otherwise.
        """
        if not self._memento_history.can_redo():
            return False

        next_value = self._memento_history.redo()
        if next_value is not None:
            # Save current state to undo stack
            self._memento_history.save_state(self._current_value)
            self._current_value = next_value
            self._notify_observers("state_change")
            return True
        return False  # pragma: no cover

    def get_history(self, limit: Optional[int] = None) -> str:
        """
        Get calculation history as a formatted string.

        Args:
            limit: Maximum number of recent records to return.

        Returns:
            str: Formatted history.
        """
        return str(self._calculation_history.get_history(limit))

    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._calculation_history.clear_history()
        self._calculation_history.save_to_csv()

    def get_last_calculation(self) -> Optional[Calculation]:
        """Get the last calculation performed."""
        return self._last_calculation

    def save_history_to_csv(self) -> None:
        """
        Save calculation history to CSV file.

        Raises:
            HistoryError: If saving fails.
        """
        self._calculation_history.save_to_csv()

    def load_history_from_csv(self) -> None:
        """
        Load calculation history from CSV file.

        Raises:
            HistoryError: If loading fails.
        """
        self._calculation_history._load_history()

    def get_history_dataframe(self):
        """
        Get the calculation history as a pandas DataFrame.

        Returns:
            pd.DataFrame: The history dataframe.
        """
        return self._calculation_history.get_history()

    def reset(self) -> None:
        """Reset the calculator to initial state."""
        self._current_value = 0.0
        self._memento_history.clear()
        self._last_calculation = None
        self._notify_observers("state_change")
