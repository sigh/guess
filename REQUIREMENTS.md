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

- `guess 1722628800000` → Multiple interpretations (number, timestamp as seconds, timestamp as milliseconds, byte size)
- `guess time 1722628800` → Multiple timestamp formats only
- `guess 1722628800s` → Multiple timestamp formats only (unit implies type)
- `guess 2GB` → Multiple byte size formats only (unit implies type)
- `guess 0xFF` → Multiple number formats only (prefix implies type)
- `guess 255` → Multiple interpretations (number, duration, permission)
- `guess #FF0000` → Color formats only (hex color implies type)
- `guess 0755` → File permission formats only (octal with leading zero implies type)

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
  - Flexible whitespace: `2 GB`, `2.5 GiB`, `512 MB` (spaces between number and unit)
  - Binary vs decimal (1024 vs 1000 based)
- **Output Formats**:
  - Human readable with appropriate units
  - Multiple unit representations
  - Decimal (1000-based) with standard units: KB, MB, GB, TB
  - Binary (1024-based) with IEC units: KiB, MiB, GiB, TiB

### 4. Number Conversion

- **Input Formats**:
  - Decimal: `255`
  - Hexadecimal: `0xFF`, `FF`
  - Binary: `0b11111111`, `11111111b`
  - Octal: `0o377`, `377o`
  - Scientific notation: `1.5e9`, `2.4E+6`, `1.23e-4`, `5E10` (robust parsing of all standard forms)
- **Output Formats**:
  - All bases (decimal, hex, binary, octal) using least ambiguous notation
  - Decimal: standard and scientific notation for large numbers
  - Human readable: "1.3 billion", "2.7 million" for numbers between 0.1 million and 1000 quadrillion
  - Hexadecimal: `0xFF` (not `FF` or `#FF`)
  - Binary: `0b11111111` (not unprefixed)
  - Octal: `0o377` (not unprefixed)

### 5. Color Conversion

- **Input Formats**:
  - Color names: `red`, `blue`, `green`
  - Hex color codes (6-digit): `#FF0000`, `#00FF00`, `#0000FF`
  - Hex color codes (3-digit): `#F00`, `#0F0`, `#00F`
  - RGB with integers: `rgb(255, 0, 0)`, `rgb(128, 64, 192)`
  - RGB with floats: `rgb(1.0, 0.0, 0.5)`, `rgb(0.5, 0.25, 0.75)`
  - RGB with percentages: `rgb(100%, 0%, 50%)`, `rgb(50%, 25%, 75%)`
  - HSL format: `hsl(0, 100%, 50%)`
- **Output Formats**:
  - Hex color code: `#FF0000`
  - RGB values: `rgb(255, 0, 0)`
  - RGB percentages: `rgb(100%, 0%, 0%)`
  - HSL values: `hsl(0, 100%, 50%)`
  - Color square (visual representation with xterm-256 colors)
  - Color name (when applicable): `red`

### 6. File Permission Conversion

- **Input Formats**:
  - Octal notation: `755`, `0755`, `0o755`
  - Symbolic notation: `rwxr-xr-x`
  - Decimal equivalent: `493`
- **Output Formats**:
  - Symbolic notation: `rwxr-xr-x`
  - Octal notation: `0o755`
  - Decimal equivalent: `493`
  - Permission breakdown: `owner: rwx, group: r-x, others: r-x`

### 7. Type-Specific Commands

- `guess time <value>` - Force timestamp interpretation
- `guess duration <value>` - Force duration interpretation
- `guess size <value>` - Force byte size interpretation
- `guess number <value>` - Force number conversion
- `guess color <value>` - Force color interpretation
- `guess permission <value>` - Force file permission interpretation

### 8. Enhanced Input Validation

- **Range validation**: Silently exclude interpretations outside reasonable ranges
- **Timezone awareness**: Handle timestamps with timezone information
- **Scientific notation**: Robust support for all standard forms including `1.5e9`, `2.4E+6`, `1.23e-4`, `5E10`
- **Negative values**: Handle negative timestamps (pre-1970) and durations
- **Flexible unit parsing**: Handle whitespace variations between numbers and units (`2GB`, `2 GB`, `2.5 GiB`)
- **Color recognition**: Detect hex color codes (#RRGGBB, #RGB), rgb() format, hsl() format, and common color names
- **Permission detection**: Recognize octal file permissions (755, 0644) and symbolic notation (rwxr-xr-x)
- **Human readable numbers**: Convert large numbers to readable format (million, billion, trillion, quadrillion) for range 100,000 to 1,000,000,000,000,000 (0.1 million to 1000 quadrillion)

## Non-Functional Requirements

### Performance

- Response time under 100ms for simple conversions
- Minimal memory footprint
- Fast startup time

### Usability

- Intuitive command-line interface
- Compact, clear output without complex table formatting
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

### Output Formatting

- **Compact display**: Use simple, readable formatting without complex Unicode tables
- **Avoid table overhead**: Eliminate table formatting problems, column width issues, and text truncation
- **Clear hierarchy**: Show results in a clean, hierarchical format that's easy to scan
- **Consistent spacing**: Use consistent indentation and spacing for readability

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
- `number` - Force number conversion
- `color` - Force color interpretation
- `permission` - Force file permission interpretation

## Input/Output Specifications

### Output Behavior Modes

The program operates in two distinct modes based on input ambiguity:

#### Mode 1: Multiple Interpretations (Ambiguous Input)

When no explicit type is given and the input could reasonably be interpreted in multiple ways, show **one output for each plausible interpretation** with the most readable format for each type.

**Example**: `guess 1722628800000`

```text
Number (from decimal):
  1.72 trillion

Timestamp (from unix milliseconds):
  2024-08-02 16:00:00 UTC

Bytes (from byte count):
  1.72 TB
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
Timestamp (from unix timestamp):
  2024-08-02 09:00:00 PDT
  2024-08-02 16:00:00 UTC
  1722628800 (unix seconds)
  1722628800000 (unix milliseconds)
  1 year, 0 months ago
  2024-08-02T16:00:00.000Z
```

### Smart Detection Algorithm

When no type is specified, `guess` should use heuristics to determine plausible interpretations. When a single type has multiple valid interpretations, show each separately:

1. **Number range analysis**:
   - `1000000000` - `2000000000`: Likely Unix timestamp (seconds)
   - `1000000000000` - `2000000000000`: Likely Unix timestamp (milliseconds)
   - Numbers that fall in both ranges: Show both timestamp interpretations separately
   - `1024`, `2048`, `4096`: Likely byte sizes (powers of 2)
   - Small numbers (`< 3600`): Likely duration in seconds

2. **Format detection** (forces single interpretation):
   - Contains date separators (`-`, `/`): Timestamp only
   - Contains time units (`s`, `m`, `h`, `d`): Duration only
   - Contains size units (`B`, `KB`, `MB`, `GB`, `KiB`, `MiB`, `GiB`): Byte size only
   - Contains base prefixes (`0x`, `0b`, `0o`): Number base only
   - Scientific notation (`1.5e9`, `2E+6`): Treat as decimal number
   - Hex color codes (`#FF0000`): Color only
   - Symbolic permissions (`rwxr-xr-x`): File permission only

3. **Context-aware detection**:
   - Leading zeros with 3-4 digits: File permissions (`755`, `0644`)
   - Color names (`red`, `blue`, `green`): Color interpretation
   - Values 1-65535: Include port number context
   - Reasonable timestamp ranges: Exclude obviously invalid dates

4. **Explicit type commands** (forces single interpretation):
   - `guess time <value>`: Timestamp formats only
   - `guess duration <value>`: Duration formats only
   - `guess size <value>`: Byte size formats only
   - `guess number <value>`: Number formats only
   - `guess color <value>`: Color formats only
   - `guess permission <value>`: File permission formats only

### Additional Examples

#### Duration with explicit type: `guess duration 3661`

```text
Duration (from seconds):
  1 hour, 1 minute, 1 second
  3661 seconds
  1.02 hours
```

#### Byte size with units: `guess 2.5GB`

```text
Bytes (from GB):
  2.5 GB
  2.33 GiB
  2500000000 bytes
  2500 MB / 2328.31 MiB
  2500000 KB / 2441406.25 KiB
```

#### Number base with prefix: `guess 0xFF`

```text
Number (from hex):
  255
  0xFF
  0b11111111
  0o377
```

#### Color value: `guess color #FF0000`

```text
Color (from hex):
  #ff0000
  rgb(255, 0, 0)
  rgb(100%, 0%, 0%)
  hsl(0, 100%, 50%)
  <red square>
  red
```

#### File permissions: `guess permission 0755`

```text
Permission (from octal):
  rwxr-xr-x
  0755
  owner: rwx, group: r-x, others: r-x
```

#### Large number with scientific notation: `guess number 1500000000`

```text
Number (from decimal):
  1500000000
  1.5 billion
  1.5e+09
  0x59682F00
  0b1011001011010000010111100000000
  0o13132027400
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
- For colors: try "255" or "#FF0000" or "red"
- For permissions: try "755" or "rwxr-xr-x"
```

### Ambiguous Input

- Show multiple interpretations when applicable
- Silently exclude interpretations that don't make sense
- Allow user to specify type explicitly for focused output
