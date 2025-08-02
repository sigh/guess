# Guess - Intelligent Data Format Conversion Utility

A command-line utility that intelligently converts between different data formats commonly used in programming and software management.

## Features

- **Number Base Conversion**: Convert between decimal, hexadecimal, binary, and octal
- **Smart Detection**: Automatically detects input format and provides multiple interpretations
- **Clean CLI Interface**: Simple and intuitive command-line interface

## Installation

Clone the repository and install in development mode:

```bash
git clone <repository-url>
cd guess
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Usage

### Basic Usage

Convert a decimal number to different bases:
```bash
python -m guess 255
```

Output:
```
Decimal: 255
Hexadecimal: 0xff
Binary: 0b11111111
Octal: 0o377
```

### Help

Show help and usage information:
```bash
python -m guess --help
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black guess/ tests/
```

### Linting

```bash
flake8 guess/ tests/
```

## Requirements

- Python 3.8+
- No external dependencies (uses only Python standard library)

## Current Status

This is currently in Phase 1 development with basic number conversion functionality.

Coming soon:
- Timestamp conversion (Unix timestamps, ISO 8601, relative times)
- Duration conversion (seconds to human-readable, time units)
- Byte size conversion (bytes, KB, MB, GB, etc.)
- Enhanced output formatting with tables
