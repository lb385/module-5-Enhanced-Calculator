"""
Operations module implementing the Strategy pattern.

This module defines the operation strategies used by the calculator.
Each operation is implemented as a class following the Strategy design pattern.
"""

from abc import ABC, abstractmethod
from app.exceptions import DivisionByZeroError, InvalidRootError


class OperationStrategy(ABC):
    """Abstract base class for all operation strategies."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Execute the operation on two operands.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            float: The result of the operation.
        """
        pass  # pragma: no cover

    @abstractmethod
    def name(self) -> str:
        """Get the name of the operation."""
        pass  # pragma: no cover


class AddOperation(OperationStrategy):
    """Strategy for addition operation."""

    def execute(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def name(self) -> str:
        """Get the name of the operation."""
        return "add"


class SubtractOperation(OperationStrategy):
    """Strategy for subtraction operation."""

    def execute(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b

    def name(self) -> str:
        """Get the name of the operation."""
        return "subtract"


class MultiplyOperation(OperationStrategy):
    """Strategy for multiplication operation."""

    def execute(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def name(self) -> str:
        """Get the name of the operation."""
        return "multiply"


class DivideOperation(OperationStrategy):
    """Strategy for division operation."""

    def execute(self, a: float, b: float) -> float:
        """Divide two numbers.

        Raises:
            DivisionByZeroError: If attempting to divide by zero.
        """
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return a / b

    def name(self) -> str:
        """Get the name of the operation."""
        return "divide"


class PowerOperation(OperationStrategy):
    """Strategy for power operation."""

    def execute(self, a: float, b: float) -> float:
        """Raise a number to a power."""
        return a**b

    def name(self) -> str:
        """Get the name of the operation."""
        return "power"


class RootOperation(OperationStrategy):
    """Strategy for root operation."""

    def execute(self, a: float, b: float) -> float:
        """Compute the b-th root of a.

        Raises:
            InvalidRootError: If the root index is zero or invalid for negative numbers.
        """
        if b == 0:
            raise InvalidRootError("Root index cannot be zero")
        if a < 0 and b % 2 == 0:
            raise InvalidRootError(
                "Cannot compute even root of a negative number"
            )
        return a ** (1 / b)

    def name(self) -> str:
        """Get the name of the operation."""
        return "root"


class OperationFactory:
    """Factory for creating operation strategy instances."""

    _operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> OperationStrategy:
        """
        Create an operation strategy instance.

        Args:
            operation_name: The name of the operation (e.g., 'add', 'divide').

        Returns:
            OperationStrategy: An instance of the requested operation strategy.

        Raises:
            ValueError: If the operation name is not recognized.
        """
        operation_name = operation_name.lower().strip()
        if operation_name not in cls._operations:
            raise ValueError(f"Unknown operation: {operation_name}")
        return cls._operations[operation_name]()

    @classmethod
    def get_supported_operations(cls) -> list:
        """Get a list of all supported operations."""
        return list(cls._operations.keys())
