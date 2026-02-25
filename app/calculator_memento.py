"""
Memento pattern implementation for calculator state management.

This module implements the Memento pattern to enable undo and redo
functionality by preserving and restoring the calculator's state.
"""

from typing import List, Optional


class CalculatorMemento:
    """
    Memento class that stores a snapshot of the calculator's state.

    Attributes:
        _state: The previous value stored in the calculator.
    """

    def __init__(self, state: float):
        """
        Initialize a memento with a calculator state.

        Args:
            state: The calculator state (previous value) to preserve.
        """
        self._state = state

    def get_state(self) -> float:
        """
        Get the preserved state.

        Returns:
            float: The stored state value.
        """
        return self._state


class CalculatorHistory:
    """
    History manager implementing the Memento pattern for undo/redo.

    This class manages a history of calculator states, enabling
    undo and redo operations.
    """

    def __init__(self):
        """Initialize the history manager."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def save_state(self, state: float) -> None:
        """
        Save the current state to the undo stack.

        Args:
            state: The current calculator state to save.
        """
        memento = CalculatorMemento(state)
        self._undo_stack.append(memento)
        # Clear redo stack when new operation is performed
        self._redo_stack.clear()

    def undo(self) -> Optional[float]:
        """
        Restore to the previous state.

        Returns:
            Optional[float]: The previous state if available, None otherwise.
        """
        if not self._undo_stack:
            return None

        memento = self._undo_stack.pop()
        # Save current state to redo stack (need to pass current state)
        return memento.get_state()

    def redo(self) -> Optional[float]:
        """
        Restore to the next state after undo.

        Returns:
            Optional[float]: The next state if available, None otherwise.
        """
        if not self._redo_stack:
            return None

        memento = self._redo_stack.pop()
        return memento.get_state()

    def push_to_redo(self, state: float) -> None:
        """
        Push a state to the redo stack.

        Args:
            state: The state to push to redo stack.
        """
        memento = CalculatorMemento(state)
        self._redo_stack.append(memento)

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0

    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
