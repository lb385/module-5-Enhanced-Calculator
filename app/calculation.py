"""
Calculation module representing a single calculation record.

This module defines the Calculation class which encapsulates a single
calculation with its operands, operation, and result.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Calculation:
    """
    Represents a single calculation.

    Attributes:
        operand_a: First operand.
        operand_b: Second operand.
        operation: The operation performed.
        result: The result of the calculation.
        timestamp: When the calculation was performed.
    """

    operand_a: float
    operand_b: float
    operation: str
    result: float
    timestamp: datetime = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Return a human-readable string representation of the calculation."""
        return (
            f"{self.operand_a} {self.operation} {self.operand_b} = {self.result}"
        )

    def to_dict(self) -> dict:
        """Convert calculation to dictionary format."""
        return {
            "operand_a": self.operand_a,
            "operand_b": self.operand_b,
            "operation": self.operation,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }
