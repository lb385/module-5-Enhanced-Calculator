"""
Tests for the history module.
"""

import pytest
import os
import pandas as pd
from app.history import CalculationHistory
from app.exceptions import HistoryError


class TestCalculationHistory:
    """Test CalculationHistory class."""

    def test_history_initialization(self, tmp_path):
        """Test history initialization."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        assert history.get_record_count() == 0

    def test_add_calculation(self, tmp_path):
        """Test adding a calculation to history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)

        assert history.get_record_count() == 1

    def test_add_multiple_calculations(self, tmp_path):
        """Test adding multiple calculations."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)
        history.add_calculation(10, 2, "divide", 5)
        history.add_calculation(2, 8, "power", 256)

        assert history.get_record_count() == 3

    def test_get_history(self, tmp_path):
        """Test retrieving history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)
        history.add_calculation(10, 2, "divide", 5)

        df = history.get_history()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == [
            "operand_a",
            "operand_b",
            "operation",
            "result",
            "timestamp",
        ]

    def test_get_history_limit(self, tmp_path):
        """Test retrieving limited history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        for i in range(5):
            history.add_calculation(i, 1, "add", i + 1)

        df = history.get_history(limit=2)

        assert len(df) == 2

    def test_clear_history(self, tmp_path):
        """Test clearing history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)
        assert history.get_record_count() == 1

        history.clear_history()
        assert history.get_record_count() == 0

    def test_save_to_csv(self, tmp_path):
        """Test saving history to CSV."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)
        history.save_to_csv()

        assert os.path.exists(history_file)

        df = pd.read_csv(history_file)
        assert len(df) == 1
        assert df.iloc[0]["result"] == 8

    def test_load_from_csv(self, tmp_path):
        """Test loading history from CSV."""
        history_file = tmp_path / "test_history.csv"

        # Create and save history
        history1 = CalculationHistory(str(history_file))
        history1.add_calculation(5, 3, "add", 8)
        history1.save_to_csv()

        # Load history in new instance
        history2 = CalculationHistory(str(history_file))
        assert history2.get_record_count() == 1

    def test_get_record_count(self, tmp_path):
        """Test getting record count."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        assert history.get_record_count() == 0

        history.add_calculation(1, 1, "add", 2)
        assert history.get_record_count() == 1

        history.add_calculation(2, 2, "add", 4)
        assert history.get_record_count() == 2

    def test_get_statistics(self, tmp_path):
        """Test getting statistics."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        stats = history.get_statistics()
        assert stats["count"] == 0
        assert stats["average_result"] is None

        history.add_calculation(5, 3, "add", 8)
        history.add_calculation(10, 2, "add", 12)

        stats = history.get_statistics()
        assert stats["count"] == 2
        assert stats["average_result"] == 10.0

    def test_filter_by_operation(self, tmp_path):
        """Test filtering history by operation."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        history.add_calculation(5, 3, "add", 8)
        history.add_calculation(10, 2, "divide", 5)
        history.add_calculation(2, 3, "add", 5)

        add_only = history.filter_by_operation("add")
        assert len(add_only) == 2

        divide_only = history.filter_by_operation("divide")
        assert len(divide_only) == 1

    def test_truncate_to_limit(self, tmp_path):
        """Test truncating history to limit."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        for i in range(10):
            history.add_calculation(i, 1, "add", i + 1)

        assert history.get_record_count() == 10

        history.truncate_to_limit(5)
        assert history.get_record_count() == 5

    def test_len_operator(self, tmp_path):
        """Test len() operator on history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        assert len(history) == 0

        history.add_calculation(5, 3, "add", 8)
        assert len(history) == 1

    def test_str_representation(self, tmp_path):
        """Test string representation of history."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file))

        str_repr = str(history)
        assert str_repr == "No history records"

        history.add_calculation(5, 3, "add", 8)
        str_repr = str(history)
        assert "operand_a" in str_repr or "5" in str_repr

    def test_nonexistent_file_creates_empty_history(self, tmp_path):
        """Test that nonexistent file is handled gracefully."""
        history_file = tmp_path / "nonexistent.csv"
        history = CalculationHistory(str(history_file))

        assert history.get_record_count() == 0
    def test_save_to_csv_with_invalid_path(self):
        """Test saving history to an invalid path."""
        history = CalculationHistory("/invalid/path/that/does/not/exist/history.csv")
        history.add_calculation(5, 3, "add", 8)

        with pytest.raises(HistoryError):
            history.save_to_csv()

    def test_add_calculation_with_max_records_enforcement(self, tmp_path):
        """Test that max_records is enforced when adding calculations."""
        history_file = tmp_path / "test_history.csv"
        history = CalculationHistory(str(history_file), max_records=3)

        # Add more records than max
        for i in range(5):
            history.add_calculation(i, 1, "add", i + 1)

        # Should only have 3 records
        assert history.get_record_count() == 3