# Guess - Conversion Utility

A simple command-line tool that converts numbers, timestamps, durations,
byte sizes, colors, and file permissions between different formats.

NOTE: Mostly coded using Claude Sonnet 4. See [REQUIREMENTS.md](REQUIREMENTS.md)
      and [PROJECT_PLAN.md](PROJECT_PLAN.md) for the plan Claude was following.

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
pip install .
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
