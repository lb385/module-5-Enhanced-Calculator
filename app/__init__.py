"""
Advanced Calculator Application.

A sophisticated, modular calculator with design patterns, persistent data
management, and a command-line REPL interface.
"""

from app.calculator import Calculator, Observer, CalculatorLogger
from app.calculator_repl import CalculatorREPL
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, CalculatorHistory
from app.calculation import Calculation
from app.exceptions import (
    CalculatorException,
    InvalidOperationError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidRootError,
    ConfigurationError,
    HistoryError,
)
from app.history import CalculationHistory
from app.input_validators import (
    validate_numeric,
    validate_operation,
    validate_command,
    validate_positive_integer,
)
from app.operations import (
    OperationStrategy,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    OperationFactory,
)

__all__ = [
    "Calculator",
    "CalculatorREPL",
    "CalculatorConfig",
    "CalculatorMemento",
    "CalculatorHistory",
    "CalculationHistory",
    "Calculation",
    "Observer",
    "CalculatorLogger",
    "CalculatorException",
    "InvalidOperationError",
    "DivisionByZeroError",
    "InvalidInputError",
    "InvalidRootError",
    "ConfigurationError",
    "HistoryError",
    "validate_numeric",
    "validate_operation",
    "validate_command",
    "validate_positive_integer",
    "OperationStrategy",
    "AddOperation",
    "SubtractOperation",
    "MultiplyOperation",
    "DivideOperation",
    "PowerOperation",
    "RootOperation",
    "OperationFactory",
]
