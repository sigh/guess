# Guess - Universal Conversion Utility

## Overview

`guess` is a command-line utility designed to quickly interpret and convert values between different formats commonly used in programming and software management. The tool aims to reduce context switching by providing instant conversions for ambiguous values.

## Installation

Install from source:

```bash
git clone https://github.com/sigh/guess
cd guess
pip install -e .
```

## Core Functionality

### Basic Usage

```bash
guess <value>
```

When given a numeric value without additional context, `guess` will attempt to interpret it as:

- **Timestamp**: Unix timestamp (seconds/milliseconds) → human-readable date/time
- **Duration**: Seconds → human-readable duration (e.g., "2 days, 3 hours, 45 minutes")
- **Byte Size**: Bytes → human-readable size (e.g., "1.5 GB", "256 MB")

### Advanced Usage

```bash
guess <type> <value>     # Force specific interpretation
guess <value> <unit>     # Unit implies interpretation
```

**Examples**:

- `guess 1722628800` → Multiple interpretations (timestamp, duration, byte size)
- `guess time 1722628800` → Multiple timestamp formats only
- `guess 1722628800s` → Multiple timestamp formats only (unit implies type)
- `guess 2GB` → Multiple byte size formats only (unit implies type)
- `guess 0xFF` → Multiple number base formats only (prefix implies type)

## Functional Requirements

### 1. Timestamp Conversion

- **Input Formats**:
  - Unix timestamp (seconds): `1659456000`
  - Unix timestamp (milliseconds): `1659456000000`
  - ISO 8601: `2022-08-02T16:00:00Z`
  - Human readable: `2022-08-02 16:00:00`
- **Output Formats**:
  - Local time with timezone
  - UTC time
  - Unix timestamp (both seconds and milliseconds)
  - Relative time (e.g., "2 hours ago", "in 3 days")

### 2. Duration Conversion

- **Input Formats**:
  - Seconds: `3600`
  - With units: `1h`, `30m`, `2d`, `1w`
  - Combined: `1h30m`, `2d4h30m`
  - Milliseconds: `3600000ms`
- **Output Formats**:
  - Human readable: "1 hour, 30 minutes"
  - Different units: seconds, minutes, hours, days, weeks
  - Compact format: "1h30m"

### 3. Byte Size Conversion

- **Input Formats**:
  - Raw bytes: `1048576`
  - With units: `1MB`, `2.5GB`, `512KB` (decimal), `1MiB`, `2.5GiB`, `512KiB` (binary)
  - Binary vs decimal (1024 vs 1000 based)
- **Output Formats**:
  - Human readable with appropriate units
  - Multiple unit representations
  - Decimal (1000-based) with standard units: KB, MB, GB, TB
  - Binary (1024-based) with IEC units: KiB, MiB, GiB, TiB

### 4. Number Base Conversion

- **Input Formats**:
  - Decimal: `255`
  - Hexadecimal: `0xFF`, `FF`, `#FF`
  - Binary: `0b11111111`, `11111111b`
  - Octal: `0o377`, `377o`
- **Output Formats**:
  - All bases (decimal, hex, binary, octal) using least ambiguous notation
  - Decimal: standard and scientific notation for large numbers
  - Hexadecimal: `0xFF` (not `FF` or `#FF`)
  - Binary: `0b11111111` (not unprefixed)
  - Octal: `0o377` (not unprefixed)
  - Common programming contexts (RGB colors for 0-255, file permissions for 3-4 digit octals)

### 5. Type-Specific Commands

- `guess time <value>` - Force timestamp interpretation
- `guess duration <value>` - Force duration interpretation
- `guess size <value>` - Force byte size interpretation
- `guess number <value>` - Force number base conversion

### 6. Confidence Scoring & Prioritization

When showing multiple interpretations, display confidence scores to help users identify the most likely interpretation:

- **High confidence** (90%+): Strong indicators (explicit units, known ranges)
- **Medium confidence** (60-89%): Probable based on heuristics
- **Low confidence** (30-59%): Possible but less likely

### 7. Enhanced Input Validation

- **Range validation**: Silently exclude interpretations outside reasonable ranges
- **Timezone awareness**: Handle timestamps with timezone information
- **Scientific notation**: Support values like `1.5e9` or `2.4E+6`
- **Negative values**: Handle negative timestamps (pre-1970) and durations

## Non-Functional Requirements

### Performance

- Response time under 100ms for simple conversions
- Minimal memory footprint
- Fast startup time

### Usability

- Intuitive command-line interface
- Clear and formatted output
- Helpful error messages with suggestions
- Support for common unit abbreviations

### Reliability

- Handle edge cases gracefully
- Validate input formats
- Provide meaningful error messages
- No crashes on invalid input

### Portability

- Python 3.8+ compatibility
- Cross-platform support (macOS, Linux, Windows)
- Minimal external dependencies
- Simple source installation with pip

## Command Line Interface

### Basic Command Structure

```bash
guess [options] <value>
guess [options] <type> <value>
```

### Core Commands

- `guess <value>` - Smart interpretation with multiple results
- `guess <type> <value>` - Force specific type interpretation
- `guess --help` - Show help and usage examples
- `guess --version` - Show version information

### Supported Types

- `time` - Force timestamp interpretation
- `duration` - Force duration interpretation
- `size` - Force byte size interpretation
- `number` - Force number base conversion

## Input/Output Specifications

### Output Behavior Modes

The program operates in two distinct modes based on input ambiguity:

#### Mode 1: Multiple Interpretations (Ambiguous Input)

When no explicit type is given and the input could reasonably be interpreted in multiple ways, show **one output for each plausible interpretation**.

**Example**: `guess 1722628800`

```text
Input: 1722628800

Interpretations:
┌─────────────┬──────────────────────────────────────┐
│ Type        │ Value                                │
├─────────────┼──────────────────────────────────────┤
│ Timestamp   │ 2024-08-02 16:00:00 UTC             │
│             │ Friday, August 2, 2024 (1 year ago)  │
├─────────────┼──────────────────────────────────────┤
│ Duration    │ 19,934 days, 2 hours, 53 minutes    │
│             │ 54.6 years                           │
├─────────────┼──────────────────────────────────────┤
│ Byte Size   │ 1.60 GB (1,722,628,800 bytes)       │
│             │ 1.49 GiB (binary)                    │
└─────────────┴──────────────────────────────────────┘
```

#### Mode 2: Multiple Formats (Unambiguous Input)

When the interpretation is clear (explicit type specified or units provided), show **semantically different formats of the same interpretation**. Avoid showing multiple syntactic variations that convey the same information.

**Semantic differences** (show multiple):

- Timestamp: seconds vs milliseconds (different precision)
- Timestamp: UTC vs local time (different timezones)
- Byte size: decimal (1000-based) vs binary (1024-based) calculations
- Duration: human readable vs compact vs raw units
- Numbers: decimal vs scientific notation (different representations)

**Syntactic differences** (show only the least ambiguous):

- Hex: `0xFF` vs `FF` vs `#FF` → show only `0xFF` (least ambiguous)
- Binary: `0b11111111` vs `11111111` → show only `0b11111111` (least ambiguous)
- Octal: `0o377` vs `377` → show only `0o377` (least ambiguous)

**Example**: `guess time 1722628800` or `guess 1722628800s`

```text
Input: 1722628800 (timestamp)

Formats:
┌─────────────────┬──────────────────────────────────────┐
│ Format          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Local Time      │ 2024-08-02 09:00:00 PDT             │
├─────────────────┼──────────────────────────────────────┤
│ UTC Time        │ 2024-08-02 16:00:00 UTC             │
├─────────────────┼──────────────────────────────────────┤
│ Unix Timestamp  │ 1722628800 (seconds)                │
│                 │ 1722628800000 (milliseconds)        │
├─────────────────┼──────────────────────────────────────┤
│ Relative        │ 1 year, 0 months ago                │
├─────────────────┼──────────────────────────────────────┤
│ ISO 8601        │ 2024-08-02T16:00:00.000Z            │
└─────────────────┴──────────────────────────────────────┘
```

├─────────────────┼──────────────────────────────────────┤
│ ISO 8601        │ 2024-08-02T16:00:00.000Z            │
└─────────────────┴──────────────────────────────────────┘

```

### Smart Detection Algorithm

When no type is specified, `guess` should use heuristics to determine plausible interpretations:

1. **Number range analysis**:
   - `1000000000` - `2000000000`: Likely Unix timestamp (seconds)
   - `1000000000000` - `2000000000000`: Likely Unix timestamp (milliseconds)
   - `1024`, `2048`, `4096`: Likely byte sizes (powers of 2)
   - Small numbers (`< 3600`): Likely duration in seconds
   - `0-255`: Could be RGB color values or byte values
   - `3-4 digits starting with 0-7`: Likely file permissions (e.g., `755`, `644`)

2. **Format detection** (forces single interpretation):
   - Contains date separators (`-`, `/`): Timestamp only
   - Contains time units (`s`, `m`, `h`, `d`): Duration only
   - Contains size units (`B`, `KB`, `MB`, `GB`, `KiB`, `MiB`, `GiB`): Byte size only
   - Contains base prefixes (`0x`, `0b`, `0o`): Number base only
   - Scientific notation (`1.5e9`, `2E+6`): Treat as decimal number

3. **Context-aware detection**:
   - Leading zeros with 3-4 digits: File permissions (`755`, `0644`)
   - Values 0-255: Include RGB color interpretation
   - Values 1-65535: Include port number context
   - Reasonable timestamp ranges: Exclude obviously invalid dates

4. **Explicit type commands** (forces single interpretation):
   - `guess time <value>`: Timestamp formats only
   - `guess duration <value>`: Duration formats only
   - `guess size <value>`: Byte size formats only
   - `guess number <value>`: Number base formats only

### Additional Examples

#### Duration with explicit type: `guess duration 3661`

```text
Input: 3661 (duration)

Formats:
┌─────────────────┬──────────────────────────────────────┐
│ Format          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Human Readable  │ 1 hour, 1 minute, 1 second          │
├─────────────────┼──────────────────────────────────────┤
│ Compact         │ 1h1m1s                               │
├─────────────────┼──────────────────────────────────────┤
│ Seconds         │ 3661                                 │
├─────────────────┼──────────────────────────────────────┤
│ Minutes         │ 61.02                                │
├─────────────────┼──────────────────────────────────────┤
│ Hours           │ 1.02                                 │
└─────────────────┴──────────────────────────────────────┘
```

#### Byte size with units: `guess 2.5GB`

```text
Input: 2.5GB (byte size)

Formats:
┌─────────────────┬──────────────────────────────────────┐
│ Format          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Decimal (1000)  │ 2.5 GB (2,500,000,000 bytes)        │
├─────────────────┼──────────────────────────────────────┤
│ Binary (1024)   │ 2.33 GiB (2,500,000,000 bytes)      │
├─────────────────┼──────────────────────────────────────┤
│ Raw Bytes       │ 2,500,000,000                       │
├─────────────────┼──────────────────────────────────────┤
│ Other Units     │ 2500 MB / 2328.31 MiB               │
│                 │ 2,500,000 KB / 2,441,406.25 KiB     │
└─────────────────┴──────────────────────────────────────┘
```

#### Number base with prefix: `guess 0xFF`

```text
Input: 0xFF (number)

Formats:
┌─────────────────┬──────────────────────────────────────┐
│ Format          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Decimal         │ 255                                  │
├─────────────────┼──────────────────────────────────────┤
│ Hexadecimal     │ 0xFF                                 │
├─────────────────┼──────────────────────────────────────┤
│ Binary          │ 0b11111111                           │
├─────────────────┼──────────────────────────────────────┤
│ Octal           │ 0o377                                │
├─────────────────┼──────────────────────────────────────┤
│ Context         │ RGB Color: #FF0000 (red)             │
│                 │ File permission: 255 (invalid)       │
└─────────────────┴──────────────────────────────────────┘
```

#### Large number with scientific notation: `guess number 1500000000`

```text
Input: 1500000000 (number)

Formats:
┌─────────────────┬──────────────────────────────────────┐
│ Format          │ Value                                │
├─────────────────┼──────────────────────────────────────┤
│ Decimal         │ 1,500,000,000                       │
├─────────────────┼──────────────────────────────────────┤
│ Scientific      │ 1.5e+09                             │
├─────────────────┼──────────────────────────────────────┤
│ Hexadecimal     │ 0x59682F00                          │
├─────────────────┼──────────────────────────────────────┤
│ Binary          │ 0b1011001011010000010111100000000   │
├─────────────────┼──────────────────────────────────────┤
│ Octal           │ 0o13132027400                       │
└─────────────────┴──────────────────────────────────────┘
```

#### Ambiguous input with confidence: `guess 755`

```text
Input: 755

Interpretations (sorted by confidence):
┌─────────────┬─────────────────────────────────────┬────────────┐
│ Type        │ Value                               │ Confidence │
├─────────────┼─────────────────────────────────────┼────────────┤
│ Permission  │ rwxr-xr-x (owner: rwx, group: r-x, │ 95%        │
│             │ other: r-x)                         │            │
├─────────────┼─────────────────────────────────────┼────────────┤
│ Number      │ Dec: 755, Hex: 0x2F3, Bin: 1011110011│ 70%        │
├─────────────┼─────────────────────────────────────┼────────────┤
│ Duration    │ 12 minutes, 35 seconds             │ 40%        │
└─────────────┴─────────────────────────────────────┴────────────┘
```

## Error Handling

### Invalid Input

- Provide suggestions for correct format
- Show examples of valid inputs
- Graceful degradation when possible

**Example**:

```text
$ guess "not-a-number"
Error: Unable to parse input "not-a-number"

Suggestions:
- For timestamps: try "1722628800" or "2024-08-02 16:00:00"
- For durations: try "3600" or "1h30m"
- For byte sizes: try "1048576" or "1GB"
- For numbers: try "255" or "0xFF"
```

### Ambiguous Input

- Show multiple interpretations when applicable
- Silently exclude interpretations that don't make sense
- Allow user to specify type explicitly for focused output

**Example**:

```text
$ guess 999999999999999999
Input: 999999999999999999

Interpretations:
┌─────────────┬──────────────────────────────────────┐
│ Type        │ Value                                │
├─────────────┼──────────────────────────────────────┤
│ Number      │ Dec: 999999999999999999              │
│             │ Hex: 0xDE0B6B3A763FFFF              │
│             │ Bin: 110111100...                    │
└─────────────┴──────────────────────────────────────┘
```

## Future Enhancements (Out of Scope for v1.0)

- Configuration file for default behaviors
- Custom output formats
- Plugin system for additional conversions
- Interactive mode
- Batch processing of multiple values
- Integration with clipboard
- JSON/XML output for scripting
- Currency conversion
- Temperature conversion
- Network address conversion (IP, CIDR)
- Hash verification (MD5, SHA256)
