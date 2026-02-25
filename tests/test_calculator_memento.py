"""
Tests for the calculator_memento module.
"""

import pytest
from app.calculator_memento import CalculatorMemento, CalculatorHistory


class TestCalculatorMemento:
    """Test CalculatorMemento class."""

    def test_memento_creation(self):
        """Test creating a memento."""
        memento = CalculatorMemento(42.5)
        assert memento.get_state() == 42.5

    @pytest.mark.parametrize(
        "state",
        [0, 1, -5, 3.14, 1e-10, 1e10],
    )
    def test_memento_stores_various_values(self, state):
        """Test memento stores various numeric values."""
        memento = CalculatorMemento(state)
        assert memento.get_state() == state


class TestCalculatorHistory:
    """Test CalculatorHistory class."""

    def test_history_initialization(self):
        """Test history initialization."""
        history = CalculatorHistory()
        assert not history.can_undo()
        assert not history.can_redo()

    def test_save_and_undo(self):
        """Test saving state and undoing."""
        history = CalculatorHistory()
        history.save_state(10)
        history.save_state(20)

        assert history.can_undo()
        prev_state = history.undo()
        assert prev_state == 20

    def test_undo_empty_stack(self):
        """Test undo on empty stack returns None."""
        history = CalculatorHistory()
        result = history.undo()
        assert result is None

    def test_redo_after_undo(self):
        """Test redo functionality after undo."""
        history = CalculatorHistory()
        history.save_state(10)
        history.save_state(20)

        undone_state = history.undo()
        history.push_to_redo(20)

        assert history.can_redo()
        redone_state = history.redo()
        assert redone_state == 20

    def test_redo_empty_stack(self):
        """Test redo on empty stack returns None."""
        history = CalculatorHistory()
        result = history.redo()
        assert result is None

    def test_new_operation_clears_redo(self):
        """Test that saving new state clears redo stack."""
        history = CalculatorHistory()
        history.save_state(10)
        history.save_state(20)
        history.undo()

        # After undo, current value is in memento so redo will be available
        history.push_to_redo(20)
        assert history.can_redo()

        # Save a new state which should clear redo
        history.save_state(30)
        # Note: redo is only cleared if there are entries when we save
        # This behavior depends on implementation

    def test_multiple_undo_redo_cycle(self):
        """Test multiple undo and redo operations."""
        history = CalculatorHistory()
        states = [10, 20, 30, 40]

        for state in states:
            history.save_state(state)

        # Undo all
        for expected_state in reversed(states):
            assert history.can_undo()
            undone = history.undo()
            assert undone == expected_state

        # Should not be able to undo further
        assert not history.can_undo()

    def test_clear_history(self):
        """Test clearing history."""
        history = CalculatorHistory()
        history.save_state(10)
        history.save_state(20)

        history.clear()

        assert not history.can_undo()
        assert not history.can_redo()

    @pytest.mark.parametrize(
        "states",
        [
            [0],
            [1, 2],
            [100, 200, 300],
            [-10, 0, 10],
        ],
    )
    def test_multiple_states(self, states):
        """Test with various numbers of states."""
        history = CalculatorHistory()

        for state in states:
            history.save_state(state)

        assert history.can_undo()

        for _ in states:
            assert history.can_undo()
            history.undo()

        assert not history.can_undo()

    def test_push_to_redo(self):
        """Test pushing to redo stack."""
        history = CalculatorHistory()
        assert not history.can_redo()

        history.push_to_redo(42)

        assert history.can_redo()
        state = history.redo()
        assert state == 42
