# Guess - Universal Conversion Utility

A simple command-line tool that converts numbers, timestamps, durations, and byte sizes between different formats.

## Features

- Number base conversion (decimal, hex, binary, octal)
- Timestamp conversion (Unix to human-readable)
- Duration conversion (seconds to readable format)
- Byte size conversion (bytes to KB/MB/GB)
- Smart detection of input types
- Clean table output

## Installation

```bash
git clone https://github.com/sigh/guess
cd guess
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

Requires Python 3.8+

## Usage

### Basic Usage

```bash
guess 1722628800
```

Shows all possible interpretations (number, timestamp, duration, byte size).

### Type-Specific Commands

```bash
guess time 1722628800    # Force timestamp interpretation
guess duration 3661      # Force duration interpretation
guess size 1048576       # Force byte size interpretation
guess number 255         # Force number base interpretation
```

### Input Formats

- **Numbers**: `255`, `0xFF`, `0b11111111`, `0o377`
- **Timestamps**: `1722628800` (Unix seconds), `-86400` (pre-1970)
- **Durations**: `3661` (seconds), `1h30m` (with units)
- **Byte Sizes**: `1048576` (bytes), `1GB`, `2.5GiB`

## Examples

```bash
# Number conversion
guess 255
# Shows: decimal, hex, binary, octal, RGB color

# Timestamp conversion
guess time 1722628800
# Shows: UTC time, local time, ISO format

# Duration with units
guess 1h30m
# Shows: 5400 seconds, 90 minutes, 01:30:00

# Byte size
guess 1GB
# Shows: decimal and binary interpretations
```
