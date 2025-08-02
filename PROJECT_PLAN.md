# Guess Project Plan

## Project Overview

Development of a command-line utility called "guess" that performs intelligent conversions between different data formats commonly used in programming and software management.

## Development Phases

### Phase 1: Project Setup and Core Architecture (1-2 days)

**Goal**: Establish project foundation and basic CLI structure

#### Tasks

1. **Project Structure Setup**
   - [ ] Create main project directory: `guess/`
   - [ ] Create Python package structure:
     - [ ] `guess/__init__.py`
     - [ ] `guess/main.py` (CLI entry point)
     - [ ] `guess/core/` (core logic modules)
     - [ ] `tests/` (test files)
   - [ ] Set up virtual environment: `python -m venv venv`
   - [ ] Create `pyproject.toml` with basic project metadata
   - [ ] Initialize git repository: `git init`
   - [ ] Create `.gitignore` file for Python projects

2. **Core Architecture Design**
   - [ ] Create `guess/core/detector.py` - input type detection
   - [ ] Create `guess/core/converter.py` - base converter class
   - [ ] Create `guess/core/formatter.py` - output formatting
   - [ ] Implement basic CLI with `argparse` in `main.py`
   - [ ] Create `guess/utils.py` for helper functions

3. **Development Environment**
   - [ ] Install development tools: `pip install black flake8 mypy pytest`
   - [ ] Create `.flake8` configuration file
   - [ ] Create `pyproject.toml` sections for black and mypy
   - [ ] Write basic `README.md` with installation instructions
   - [ ] Create `requirements-dev.txt` for development dependencies

**Deliverables**:

- [ ] Runnable CLI that accepts arguments (`python -m guess --help` works)
- [ ] Basic project structure with all files created
- [ ] Development tooling configured and working

---

### Phase 2: Smart Detection Engine (2-3 days)

**Goal**: Implement the core logic for intelligently detecting input types

#### Tasks

1. **Input Analysis Module**
   - [ ] Create `guess/core/detector.py` with `InputDetector` class
   - [ ] Implement `detect_number_ranges()` method:
     - [ ] Unix timestamp ranges (1B-2B for seconds, 1T-2T for milliseconds)
     - [ ] Common byte sizes (powers of 2: 1024, 2048, 4096, etc.)
     - [ ] Small duration numbers (< 3600 seconds)
     - [ ] RGB color range (0-255)
     - [ ] File permission patterns (3-4 digits, 0-7 range)
   - [ ] Implement `detect_format_patterns()` method using regex:
     - [ ] Date separators (`-`, `/`)
     - [ ] Time units (`s`, `m`, `h`, `d`, `w`)
     - [ ] Size units (`B`, `KB`, `MB`, `GB`, `TB`)
     - [ ] Number base prefixes (`0x`, `0b`, `0o`, `#`)
     - [ ] Scientific notation (`1.5e9`, `2E+6`)
   - [ ] Create confidence scoring system (0-100%)
   - [ ] Write unit tests for each detection method

2. **Base Converter Framework**
   - [ ] Create `guess/core/converter.py` with abstract `BaseConverter` class
   - [ ] Define standard methods: `can_convert()`, `convert()`, `format_output()`
   - [ ] Create `ConversionResult` class for structured output
   - [ ] Implement error handling patterns for invalid inputs
   - [ ] Create `guess/core/formatter.py` for table-based output

3. **Testing Infrastructure**
   - [ ] Create `tests/test_detector.py` with test cases for each input type
   - [ ] Create test data sets in `tests/data/` directory:
     - [ ] `valid_timestamps.txt`
     - [ ] `valid_durations.txt`
     - [ ] `valid_byte_sizes.txt`
     - [ ] `valid_numbers.txt`
     - [ ] `invalid_inputs.txt`
   - [ ] Write edge case tests (empty input, very large numbers, negative values)
   - [ ] Set up pytest configuration in `pyproject.toml`

**Deliverables**:

- [ ] Working input type detection with confidence scores
- [ ] Converter framework ready for specific implementations
- [ ] Comprehensive test suite with >90% coverage for detection logic

---

### Phase 3: Core Converters Implementation (3-4 days)

**Goal**: Implement the four main conversion types

#### Tasks

1. **Timestamp Converter** (1 day)
   - [ ] Create `guess/converters/timestamp.py` with `TimestampConverter` class
   - [ ] Implement Unix timestamp parsing:
     - [ ] Detect seconds vs milliseconds (length-based)
     - [ ] Handle both positive and negative timestamps
     - [ ] Validate reasonable date ranges (1970-2100)
   - [ ] Implement ISO 8601 parsing using `datetime.fromisoformat()`
   - [ ] Implement human-readable date parsing with `datetime.strptime()`
   - [ ] Create multiple output formats:
     - [ ] Local time with timezone detection
     - [ ] UTC time formatting
     - [ ] Unix timestamp (both seconds and milliseconds)
     - [ ] Relative time ("2 days ago", "in 3 hours")
     - [ ] ISO 8601 formatted output
   - [ ] Write comprehensive tests in `tests/test_timestamp.py`

2. **Duration Converter** (1 day)
   - [ ] Create `guess/converters/duration.py` with `DurationConverter` class
   - [ ] Implement parsing for raw seconds input
   - [ ] Implement unit parsing:
     - [ ] Single units: `1h`, `30m`, `2d`, `1w`
     - [ ] Combined units: `1h30m`, `2d4h30m15s`
     - [ ] Milliseconds: `3600000ms`
   - [ ] Create human-readable output formatting
   - [ ] Create compact format output (`1h30m`)
   - [ ] Implement conversion to different units (seconds, minutes, hours, days)
   - [ ] Write tests in `tests/test_duration.py`

3. **Byte Size Converter** (1 day)
   - [ ] Create `guess/converters/bytesize.py` with `ByteSizeConverter` class
   - [ ] Implement raw byte parsing for large integers
   - [ ] Implement unit parsing with case-insensitive matching:
     - [ ] Binary units: `KB`, `MB`, `GB`, `TB` (1024-based)
     - [ ] Decimal units: `kB`, `mB`, `gB`, `tB` (1000-based)
     - [ ] Handle decimal inputs: `2.5GB`, `1.5TB`
   - [ ] Create dual output formatting:
     - [ ] Binary calculations (1024-based) with "iB" suffix
     - [ ] Decimal calculations (1000-based) with "B" suffix
     - [ ] Raw byte count with comma formatting
   - [ ] Implement multiple unit representations
   - [ ] Write tests in `tests/test_bytesize.py`

4. **Number Base Converter** (1 day)
   - [ ] Create `guess/converters/numberbase.py` with `NumberBaseConverter` class
   - [ ] Implement input parsing for all bases:
     - [ ] Decimal: plain numbers
     - [ ] Hexadecimal: `0xFF`, `FF`, `#FF`
     - [ ] Binary: `0b11111111`, `11111111b`
     - [ ] Octal: `0o377`, `377o`
   - [ ] Implement output formatting for all bases:
     - [ ] Decimal representation
     - [ ] Multiple hex formats (`0xFF`, `FF`, `#FF`)
     - [ ] Binary with and without prefix
     - [ ] Octal with and without prefix
   - [ ] Add context-aware features:
     - [ ] RGB color representation for 0-255 values
     - [ ] File permission interpretation for 3-4 digit octals
   - [ ] Handle large numbers appropriately (truncate binary display)
   - [ ] Write tests in `tests/test_numberbase.py`

**Deliverables**:

- [ ] Four working converter modules with complete functionality
- [ ] Test coverage >95% for each converter
- [ ] Integration with detection engine working
- [ ] All converters handling edge cases gracefully

---

### Phase 4: CLI Integration and Output Formatting (1-2 days)

**Goal**: Create polished command-line interface with beautiful output

#### Tasks

1. **Command-Line Interface Integration**
   - [ ] Update `guess/main.py` to integrate all converters
   - [ ] Implement smart interpretation mode (no type specified):
     - [ ] Call detector to get possible interpretations
     - [ ] Run applicable converters based on confidence scores
     - [ ] Format output showing multiple interpretations
   - [ ] Implement type-specific commands:
     - [ ] `guess time <value>` - force timestamp interpretation only
     - [ ] `guess duration <value>` - force duration interpretation only
     - [ ] `guess size <value>` - force byte size interpretation only
     - [ ] `guess number <value>` - force number base interpretation only
   - [ ] Add help system with `--help` flag showing examples
   - [ ] Add version information with `--version` flag
   - [ ] Implement graceful error handling for invalid inputs

2. **Output Formatting System**
   - [ ] Create `guess/core/table.py` for table-based output
   - [ ] Implement Unicode table formatting (┌─┐ characters)
   - [ ] Handle terminal width considerations (wrap long values)
   - [ ] Create different output modes:
     - [ ] Default: beautiful table format
     - [ ] Compact: simple key-value pairs
   - [ ] Ensure consistent column widths and alignment
   - [ ] Add proper spacing and padding

3. **User Experience Enhancements**
   - [ ] Create comprehensive help text with real examples
   - [ ] Implement helpful error messages:
     - [ ] Suggest valid formats for invalid input
     - [ ] Show usage examples in error messages
   - [ ] Add input validation with clear feedback
   - [ ] Test CLI with various terminal sizes and environments

**Deliverables**:

- [ ] Polished CLI interface that handles all input types
- [ ] Beautiful formatted output with proper tables
- [ ] Complete help system with examples
- [ ] Robust error handling with helpful messages

---

### Phase 5: Testing and Documentation (1-2 days)

**Goal**: Ensure reliability and create comprehensive documentation

#### Tasks

1. **Comprehensive Testing & Quality Assurance**
   - [ ] Write integration tests in `tests/test_integration.py`:
     - [ ] Test full CLI workflows for each input type
     - [ ] Test error handling scenarios
     - [ ] Test edge cases (empty input, very large numbers)
   - [ ] Performance testing:
     - [ ] Measure response times for various inputs
     - [ ] Ensure <100ms response time target is met
     - [ ] Profile memory usage during conversions
   - [ ] Cross-platform testing:
     - [ ] Test on macOS, Linux, and Windows (if possible)
     - [ ] Test with different Python versions (3.8, 3.9, 3.10+)
   - [ ] Code quality checks:
     - [ ] Run `black` formatting on all files
     - [ ] Fix all `flake8` linting issues
     - [ ] Resolve `mypy` type checking errors
     - [ ] Achieve >95% test coverage

2. **Documentation Creation**
   - [ ] Write comprehensive `README.md`:
     - [ ] Installation instructions
     - [ ] Usage examples for all features
     - [ ] Table of supported formats
     - [ ] Troubleshooting section
   - [ ] Create `CHANGELOG.md` with version history
   - [ ] Add inline code documentation (docstrings)
   - [ ] Create usage examples file `examples.md`

3. **Final Code Review & Optimization**
   - [ ] Review all code for clarity and maintainability
   - [ ] Optimize performance bottlenecks if any found
   - [ ] Ensure consistent error handling across all modules
   - [ ] Validate that silent filtering of invalid interpretations works
   - [ ] Final security review (input validation, no code execution)

**Deliverables**:

- [ ] Production-ready codebase with >95% test coverage
- [ ] Complete documentation package
- [ ] Performance benchmarks meeting requirements
- [ ] All quality checks passing

---

### Phase 6: Source Distribution (0.5 days)

**Goal**: Prepare for source-only distribution

#### Tasks

1. **Source Package Preparation**
   - [ ] Finalize `pyproject.toml` configuration:
     - [ ] Set correct package name, version, and description
     - [ ] Define minimal dependencies (only built-in modules if possible)
     - [ ] Configure entry points for CLI command
     - [ ] Add development dependencies section
   - [ ] Test installation in clean environments:
     - [ ] Create fresh virtual environment
     - [ ] Test `pip install -e .` from project root
     - [ ] Verify CLI command works after installation
     - [ ] Test uninstallation process
   - [ ] Create installation documentation in `README.md`
   - [ ] Tag version with `git tag v1.0.0`

2. **GitHub Release Setup**
   - [ ] Create GitHub release v1.0.0 with source archive
   - [ ] Write release notes with feature list and examples
   - [ ] Add clear installation and usage instructions
   - [ ] Include example commands and expected output in release notes

**Deliverables**:

- [ ] Source-installable package working correctly
- [ ] GitHub release v1.0.0 with complete documentation
- [ ] Clear installation process documented and tested

---

## Technical Stack

### Core Dependencies

- **Python 3.8+**: Core language
- **argparse**: Built-in CLI argument parsing
- **datetime**: Built-in date/time handling
- **re**: Built-in regex for pattern matching

### Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **click** (alternative): More advanced CLI framework if needed

### Optional Dependencies

- **rich**: Enhanced terminal output (tables, colors)
- **python-dateutil**: Advanced date parsing
- **humanize**: Human-readable formatting

## Risk Assessment

### High Risk

- **Ambiguous input handling**: May require iterative refinement of heuristics
- **Timezone complexity**: Proper timezone handling can be tricky

### Medium Risk

- **Performance requirements**: 100ms response time may need optimization
- **Cross-platform compatibility**: Different behavior on Windows vs Unix

### Low Risk

- **Basic conversions**: Core conversion logic is straightforward
- **CLI interface**: Well-established patterns available

## Success Criteria

### Minimum Viable Product (MVP)

- [ ] Accept numeric input and provide multiple interpretations
- [ ] Core four conversion types working
- [ ] Clean command-line interface
- [ ] Basic error handling

### Version 1.0

- [ ] Smart input detection with high accuracy
- [ ] Beautiful formatted output
- [ ] Comprehensive help system
- [ ] Type-specific command options
- [ ] Response time under 100ms
- [ ] Simple source installation process

### Post-1.0 Enhancements

- [ ] Configuration file support
- [ ] Plugin architecture
- [ ] Additional conversion types
- [ ] Interactive mode
- [ ] JSON output for scripting

## Timeline Summary

- **Total Estimated Time**: 7.5-12 days
- **MVP Delivery**: 4-6 days (Phases 1-3 complete)
- **Production Ready**: 7.5-12 days (All phases complete)

**Phase Breakdown**:

- Phase 1: 1-2 days (Setup & Architecture)
- Phase 2: 2-3 days (Detection Engine)
- Phase 3: 3-4 days (Core Converters)
- Phase 4: 1-2 days (CLI & Output)
- Phase 5: 1-2 days (Testing & Documentation)
- Phase 6: 0.5 days (Source Distribution)

The project is designed for incremental development with each phase building upon the previous one. Each task is broken down for a junior developer with clear deliverables and checkboxes to track progress.
