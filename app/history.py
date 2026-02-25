"""
History management module using pandas DataFrame.

This module provides persistent storage and manipulation of calculation
history using pandas DataFrames and CSV files.
"""

import os
from typing import List, Optional
import pandas as pd
from datetime import datetime
from app.exceptions import HistoryError


class CalculationHistory:
    """
    Manages calculation history with pandas DataFrame backend.

    This class provides methods to add, retrieve, save, and load
    calculation history from CSV files.
    """

    def __init__(self, history_file: str = "history_data.csv", max_records: Optional[int] = None):
        """
        Initialize the history manager.

        Args:
            history_file: Path to the CSV file for persisting history.
            max_records: Maximum number of records to keep. If None, no limit is enforced.
        """
        self.history_file = history_file
        self.max_records = max_records
        self._df: pd.DataFrame = pd.DataFrame(
            columns=["operand_a", "operand_b", "operation", "result", "timestamp"]
        )
        self._load_history()

    def add_calculation(
        self, operand_a: float, operand_b: float, operation: str, result: float
    ) -> None:
        """
        Add a calculation to the history.

        Args:
            operand_a: First operand.
            operand_b: Second operand.
            operation: The operation performed.
            result: The result of the calculation.

        Raises:
            HistoryError: If adding to history fails.
        """
        try:
            new_record = {
                "operand_a": operand_a,
                "operand_b": operand_b,
                "operation": operation,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
            new_df = pd.DataFrame([new_record])
            self._df = pd.concat([self._df, new_df], ignore_index=True)
            
            # Enforce max_records limit if set
            if self.max_records is not None and len(self._df) > self.max_records:
                self.truncate_to_limit(self.max_records)
        except Exception as e:  # pragma: no cover
            raise HistoryError(f"Failed to add calculation to history: {e}") from e

    def get_history(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Get calculation history.

        Args:
            limit: Maximum number of recent records to return. None returns all.

        Returns:
            pd.DataFrame: History records.
        """
        if limit is None:
            return self._df.copy()
        return self._df.tail(limit).copy()

    def clear_history(self) -> None:
        """Clear all history records."""
        self._df = pd.DataFrame(
            columns=["operand_a", "operand_b", "operation", "result", "timestamp"]
        )

    def save_to_csv(self) -> None:
        """
        Save history to CSV file.

        Raises:
            HistoryError: If saving fails.
        """
        try:
            self._df.to_csv(self.history_file, index=False)
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {e}") from e

    def _load_history(self) -> None:
        """
        Load history from CSV file if it exists.

        Raises:
            HistoryError: If loading fails.
        """
        try:
            if os.path.exists(self.history_file):
                self._df = pd.read_csv(self.history_file)
            else:
                self._df = pd.DataFrame(
                    columns=[
                        "operand_a",
                        "operand_b",
                        "operation",
                        "result",
                        "timestamp",
                    ]
                )
        except Exception as e:  # pragma: no cover
            raise HistoryError(
                f"Failed to load history from CSV: {e}"
            ) from e

    def get_record_count(self) -> int:
        """Get the number of records in history."""
        return len(self._df)

    def get_statistics(self) -> dict:
        """
        Get statistics about the history.

        Returns:
            dict: Statistics including count and average result.
        """
        if len(self._df) == 0:
            return {"count": 0, "average_result": None}

        return {
            "count": len(self._df),
            "average_result": self._df["result"].mean(),
        }

    def filter_by_operation(self, operation: str) -> pd.DataFrame:
        """
        Get all calculations for a specific operation.

        Args:
            operation: The operation to filter by.

        Returns:
            pd.DataFrame: Filtered history records.
        """
        return self._df[self._df["operation"] == operation].copy()

    def truncate_to_limit(self, limit: int) -> None:
        """
        Truncate history to a maximum number of records.

        Args:
            limit: Maximum number of records to keep.
        """
        if len(self._df) > limit:
            self._df = self._df.iloc[-limit:].reset_index(drop=True)

    def __len__(self) -> int:
        """Return the number of records in history."""
        return len(self._df)

    def __str__(self) -> str:
        """Return a string representation of the history."""
        if len(self._df) == 0:
            return "No history records"
        return self._df.to_string()
