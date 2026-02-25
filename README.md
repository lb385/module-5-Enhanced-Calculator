# Advanced Calculator Application

A sophisticated, modular calculator application built with Python that integrates advanced design patterns, persistent data management via pandas, and comprehensive test automation with GitHub Actions.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Design Patterns](#design-patterns)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Configuration](#configuration)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Features

### Core Calculator Functionality
- **Interactive REPL Interface**: Read-Eval-Print Loop for continuous user interaction
- **Advanced Arithmetic Operations**: Addition, subtraction, multiplication, division, power, and root operations
- **State Management**: Undo and redo functionality with memento pattern
- **Command-Line Interface**: User-friendly commands for history, settings, and control
- **Set Value**: Arbitrary value setting for quick calculator state management

### Data Management
- **Persistent History**: Calculation history stored in CSV format using pandas DataFrames
- **Auto-Save**: Automatic saving of calculation history after each operation
- **Load/Save Commands**: Manual control over history persistence
- **History Statistics**: Count and average calculations
- **Maximum Records Enforcement**: Configurable limit for history records

### Design Patterns

#### 1. **Strategy Pattern**
- Individual operation classes (`Add`, `Subtract`, `Multiply`, `Divide`, `Power`, `Root`)
- Interchangeable operation execution strategies
- Location: `app/operations.py`

#### 2. **Factory Pattern**
- `OperationFactory` class for creating operation instances
- Case-insensitive operation selection
- Centralized operation instantiation
- Location: `app/operations.py`

#### 3. **Memento Pattern**
- `CalculatorMemento` stores calculator state snapshots
- `CalculatorHistory` manages undo/redo stacks
- Complete state preservation and restoration
- Location: `app/calculator_memento.py`

#### 4. **Observer Pattern**
- `Observer` interface for event notifications
- `CalculatorLogger` logs calculation events
- Event types: `calculation_complete`, `error`, `state_change`
- Location: `app/calculator.py`

#### 5. **Facade Pattern**
- `Calculator` class provides simplified interface to complex subsystems
- Encapsulates operations, history, state management, and observers
- Location: `app/calculator.py`

#### 6. **Configuration Management Pattern**
- `CalculatorConfig` manages environment variables
- `.env` file support via `python-dotenv`
- Validation of configuration settings
- Location: `app/calculator_config.py`

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd module5
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file (optional)**
   ```bash
   cat > .env << EOF
   HISTORY_FILE=history_data.csv
   AUTO_SAVE_ENABLED=true
   LOGGING_LEVEL=INFO
   MAX_HISTORY_RECORDS=1000
   EOF
   ```

## Usage

### Running the Calculator

Start the interactive REPL:
```bash
python -m app.calculator_repl
```

### Example Session

```
==================================================
   Welcome to the Advanced Calculator
==================================================
Type 'help' for a list of commands
Current value: 0

calc> add 5
Result: 5

calc> multiply 2
Result: 10

calc> divide 2
Result: 5

calc> history
Calculation History:
   operand_a operand_b operation  result                 timestamp
0        0.0       5.0       add     5.0  2024-02-24T10:30:15.123456
1        5.0       2.0   multiply   10.0  2024-02-24T10:30:18.456789
2       10.0       2.0    divide     5.0  2024-02-24T10:30:21.789012

calc> undo
Undo successful. Current value: 10

calc> redo
Redo successful. Current value: 5

calc> set 100
Value set to: 100

calc> exit
Exiting calculator. Goodbye!
```

## Commands

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <operand>` | Addition | `add 5` |
| `subtract <operand>` | Subtraction | `subtract 3` |
| `multiply <operand>` | Multiplication | `multiply 2` |
| `divide <operand>` | Division | `divide 2` |
| `power <operand>` | Power operation | `power 2` |
| `root <operand>` | Root operation | `root 2` |
| `help` | Display help message | `help` |
| `history` | Show calculation history | `history` |
| `clear` | Clear all history | `clear` |
| `undo` | Undo last operation | `undo` |
| `redo` | Redo last undone operation | `redo` |
| `save` | Save history to file | `save` |
| `load` | Load history from file | `load` |
| `set <value>` | Set current value | `set 42` |
| `exit` | Exit calculator | `exit` |

## Configuration

### Environment Variables

Create a `.env` file in the project root to customize settings:

```env
# Path to history CSV file
HISTORY_FILE=history_data.csv

# Enable/disable auto-save (true/false)
AUTO_SAVE_ENABLED=true

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOGGING_LEVEL=INFO

# Maximum number of history records to keep
MAX_HISTORY_RECORDS=1000
```

### Default Values

| Setting | Default |
|---------|---------|
| `HISTORY_FILE` | `history_data.csv` |
| `AUTO_SAVE_ENABLED` | `true` |
| `LOGGING_LEVEL` | `INFO` |
| `MAX_HISTORY_RECORDS` | `1000` |

## Testing

### Running Tests

Run all tests with coverage:
```bash
pytest --cov=app --cov-report=html tests/
```

Run specific test file:
```bash
pytest tests/test_calculator.py -v
```

Run with coverage report in terminal:
```bash
pytest --cov=app --cov-report=term-missing tests/
```

### Test Coverage

The project achieves **100% test coverage** with:
- Unit tests for individual components
- Parameterized tests for multiple scenarios
- Integration tests for complete workflows
- Edge case and error condition testing

### Test Files

| Test File | Coverage |
|-----------|----------|
| `tests/test_calculation.py` | Calculation dataclass |
| `tests/test_calculator.py` | Main calculator logic |
| `tests/test_operations.py` | Arithmetic operations |
| `tests/test_history.py` | History management |
| `tests/test_calculator_memento.py` | Undo/redo functionality |
| `tests/test_calculator_config.py` | Configuration management |
| `tests/test_calculator_repl.py` | REPL interface |
| `tests/test_exceptions.py` | Exception handling |
| `tests/test_input_validators.py` | Input validation |
| `tests/test_integration.py` | Integration scenarios |

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes automated CI/CD with GitHub Actions (`.github/workflows/python-app.yml`):

- **Trigger**: On push to main/master or pull request
- **Python Version**: 3.9
- **Steps**:
  1. Checkout code
  2. Set up Python environment
  3. Install dependencies (pytest, pytest-cov, pandas, python-dotenv)
  4. Run tests with coverage
  5. Enforce 100% coverage requirement

### Setting Up GitHub Actions

1. Push code to GitHub repository
2. Enable GitHub Actions in repository settings
3. Workflow automatically runs on each push/PR
4. Coverage report available in workflow logs

## Project Structure

```
module5/
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── calculator.py               # Main Calculator facade
│   ├── calculator_config.py        # Configuration management
│   ├── calculator_memento.py       # Undo/redo implementation
│   ├── calculator_repl.py          # REPL interface
│   ├── calculation.py              # Calculation dataclass
│   ├── exceptions.py               # Custom exceptions
│   ├── history.py                  # History management with pandas
│   ├── input_validators.py         # Input validation utilities
│   ├── operations.py               # Operation strategies & factory
│   └── __pycache__/
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py         # Calculation tests
│   ├── test_calculator.py          # Calculator tests
│   ├── test_calculator_config.py   # Configuration tests
│   ├── test_calculator_memento.py  # Memento tests
│   ├── test_calculator_repl.py     # REPL tests
│   ├── test_exceptions.py          # Exception tests
│   ├── test_history.py             # History tests
│   ├── test_input_validators.py    # Validator tests
│   ├── test_integration.py         # Integration tests
│   ├── test_operations.py          # Operation tests
│   └── __pycache__/
├── .github/
│   └── workflows/
│       └── python-app.yml          # GitHub Actions workflow
├── .env                             # Configuration file (optional)
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── history_data.csv                 # Calculation history (auto-created)
```

## Code Examples

### Programmatic Usage

```python
from app.calculator import Calculator, CalculatorLogger

# Create calculator instance
calc = Calculator(history_file="my_history.csv", max_records=500)

# Add observer for logging
logger = CalculatorLogger()
calc.add_observer(logger)

# Perform calculations
calc.perform_operation("add", 5)      # Result: 5
calc.perform_operation("multiply", 2) # Result: 10
calc.perform_operation("power", 2)    # Result: 100

# Get current value
print(calc.get_value())  # Output: 100

# Undo operation
calc.undo()
print(calc.get_value())  # Output: 10

# View history
history = calc.get_history()
print(history)

# Save to CSV
calc.save_history_to_csv()

# Set arbitrary value
calc.set_value(42)

# Get last calculation
last_calc = calc.get_last_calculation()
print(last_calc)  # Output: 10 power 2 = 100

# Reset calculator
calc.reset()
print(calc.get_value())  # Output: 0
```

### Error Handling

```python
from app.calculator import Calculator
from app.exceptions import InvalidOperationError, InvalidInputError

calc = Calculator()

try:
    # Invalid operation
    calc.perform_operation("invalid_op", 5)
except InvalidOperationError as e:
    print(f"Operation error: {e}")

try:
    # Division by zero
    calc.perform_operation("divide", 0)
except InvalidOperationError as e:
    print(f"Math error: {e}")
```

## Error Handling

The application implements comprehensive error handling using both LBYL (Look Before You Leap) and EAFP (Easier to Ask Forgiveness than Permission) paradigms:

### Custom Exceptions

- `CalculatorException`: Base exception
- `InvalidOperationError`: Invalid operation requested
- `InvalidInputError`: Invalid input provided
- `DivisionByZeroError`: Division by zero attempted
- `InvalidRootError`: Invalid root operation
- `HistoryError`: History management error
- `ConfigurationError`: Configuration error

### EAFP Usage

```python
try:
    result = operation_strategy.execute(operand_a, operand_b)
except Exception as e:
    raise InvalidOperationError(f"Operation failed: {e}")
```

### LBYL Usage

```python
if len(user_input) < 2:
    print("Usage: <operation> <operand_b>")
    return
```

## Best Practices Implemented

1. **DRY Principle**: Code reuse through strategy and factory patterns
2. **Modular Design**: Separated concerns across multiple modules
3. **Type Hints**: Full type annotations for better IDE support
4. **Docstrings**: Comprehensive documentation for all classes and methods
5. **Error Handling**: Graceful error handling with meaningful messages
6. **Testing**: 100% test coverage with parameterized tests
7. **Configuration**: Flexible configuration via environment variables
8. **Logging**: Observer pattern for event tracking and logging
9. **Persistence**: Automatic history saving and loading
10. **Code Quality**: Following PEP 8 style guidelines

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest --cov=app tests/`
6. Ensure 100% coverage before committing
7. Commit with descriptive message: `git commit -m "Add feature: description"`
8. Push to branch: `git push origin feature/your-feature`
9. Create a Pull Request

### Code Quality Requirements

- All tests must pass
- 100% code coverage required
- Follow PEP 8 style guidelines
- Include docstrings for new functions/classes
- Add unit tests for new features

## Troubleshooting

### Issue: Tests not running

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Coverage below 100%

**Solution**: Check which lines are not covered:
```bash
pytest --cov=app --cov-report=html tests/
# Open htmlcov/index.html in browser to see uncovered lines
```

### Issue: .env file not being loaded

**Solution**: Ensure `.env` file is in the project root and readable:
```bash
ls -la .env
cat .env
```

### Issue: History file not found

**Solution**: The history file will be created automatically on first run. Ensure write permissions in the project directory.

## License

This project is provided as part of an educational assignment.

## Support

For issues or questions, please create an issue in the repository or contact the maintainers.

---

**Last Updated**: February 24, 2026
**Version**: 1.0.0
**Python Version**: 3.8+
**Status**: Production Ready
