# Guess - Universal Conversion Utility

A simple command-line tool that converts numbers, timestamps, durations, byte sizes, colors, and file permissions between different formats.

## Features

- **Number base conversion** (decimal, hex, binary, octal, scientific notation)
- **Timestamp conversion** (Unix to human-readable, relative time)
- **Duration conversion** (seconds to readable format, unit parsing)
- **Byte size conversion** (bytes to KB/MB/GB, decimal and binary)
- **Color conversion** (RGB, hex codes, color names, HSL)
- **File permission conversion** (octal, symbolic, decimal)
- **Smart detection** of input types with multiple interpretations
- **Clean hierarchical output** without table formatting

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

Shows all possible interpretations (number, timestamp, byte size).

### Type-Specific Commands

```bash
guess time 1722628800    # Force timestamp interpretation
guess duration 3661      # Force duration interpretation
guess size 1048576       # Force byte size interpretation
guess number 255         # Force number base interpretation
guess color #FF0000      # Force color interpretation
guess permission 755    # Force file permission interpretation
```

### Input Formats

- **Numbers**: `255`, `0xFF`, `0b11111111`, `0o377`, `1.5e9`
- **Timestamps**: `1722628800` (Unix seconds), `-86400` (pre-1970)
- **Durations**: `3661` (seconds), `1h30m` (with units)
- **Byte Sizes**: `1048576` (bytes), `1GB`, `2.5GiB`
- **Colors**: `255` (RGB), `#FF0000` (hex), `red` (names)
- **Permissions**: `755` (octal), `rwxr-xr-x` (symbolic), `493` (decimal)

## Examples

```bash
# Number conversion (shows human readable format)
guess 1500000000
# Number (from decimal): 1.5 billion

# Multi-interpretation (ambiguous input)
guess 255
# Number (from decimal): 255
# Color: #ffffff
# Permission: 173

# Color conversion
guess color #FF0000
# Color (from input):
#   #ff0000
#   rgb(255, 0, 0)
#   red
#   hsl(0, 100%, 50%)

# File permissions
guess permission 755
# Permission (from input):
#   rwxr-xr-x
#   0o755
#   493
#   owner: read, write, execute, group: read, execute, others: read, execute

# Timestamp with enhanced output
guess time 1722628800
# Timestamp (from input):
#   1722628800
#   1722628800000
#   2024-08-02 20:00:00 UTC
#   2024-08-03 06:00:00
#   Saturday, August 03, 2024 at 06:00:00 AM

# Scientific notation parsing
guess 1.5e9
# Number (from input):
#   1,500,000,000.0
#   1.50e+09
#   1.5 billion

# Byte size with both formats
guess 1048576
# Bytes (from byte count): 1.05 MB / 1.00 MiB
```
