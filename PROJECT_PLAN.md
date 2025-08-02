# Guess Project Plan

## Project Overview

Development of a command-line utility called "guess" that performs intelligent conversions between different data formats commonly used in programming and software management.

## Development Phases

### Phase 1: Project Setup and Minimal Working Version (1-2 days)

**Goal**: Establish project foundation with a working end-to-end flow for one simple conversion

**Incremental Verification**: After each task, you should be able to run and test the functionality

#### Tasks

1. **Project Structure Setup**
   - [x] Create Python package structure:
     - [x] `guess/__init__.py`
     - [x] `guess/main.py` (CLI entry point)
     - [x] `guess/converters/` (converter modules)
     - [x] `guess/converters/__init__.py`
     - [x] `tests/` (test files)
   - [x] Set up virtual environment: `python3 -m venv venv`
   - [x] Create :`pyproject.toml` with basic project metadata and CLI entry point
   - [x] Create `.gitignore` file for Python projects
   - **Test**: `python3 -m guess --help` should work ✅

2. **Minimal CLI with One Converter (Number Base)**
   - [x] Create `guess/converters/base.py` with simple `Converter` base class:
     - [x] `can_convert(input_str) -> bool` method
     - [x] `convert(input_str) -> dict` method
     - [x] `get_name() -> str` method
   - [x] Create `guess/converters/number.py` with `NumberConverter` class:
     - [x] Handle decimal input only initially
     - [x] Output decimal, hex, binary, octal
     - [x] Simple string-based output (no tables yet)
   - [x] Create `guess/main.py` with basic CLI:
     - [x] Parse command line arguments
     - [x] Try number converter on input
     - [x] Print results or "Unable to convert"
   - **Test**: `python3 -m guess 255` should output number formats ✅

3. **Development Environment**
   - [x] Install development tools: `pip install black flake8 mypy pytest`
   - [x] Create `.flake8` configuration file
   - [x] Create `pyproject.toml` sections for black and mypy
   - [x] Write basic test for number converter in `tests/test_number.py`
   - [x] Write basic `README.md` with installation and usage
   - **Test**: `pytest` should run and pass basic tests ✅

**Deliverables**:

- [x] Working CLI that converts decimal numbers to other bases
- [x] Basic project structure with proper package setup
- [x] Development tooling configured and one passing test
- [x] Can run: `python3 -m guess 255` and get meaningful output ✅

---

### Phase 2: Add More Converters with Simple Registry (2-3 days)

**Goal**: Implement remaining converters with a simple modular system

**Incremental Verification**: After each converter, test it independently and integrated

#### Tasks

1. **Simple Converter Registry**
   - [x] Create `guess/registry.py` with simple list of converter classes
   - [x] Update `guess/main.py` to try each converter in order
   - [x] Move number converter to use the same pattern
   - **Test**: Existing number conversion should still work with new architecture ✅

2. **Timestamp Converter** (Start Simple)
   - [x] Create `guess/converters/timestamp.py` with `TimestampConverter` class
   - [x] Implement basic Unix timestamp detection (10-digit numbers only)
   - [x] Output: UTC time, local time, human-readable format
   - [x] Add to converter list in registry
   - **Test**: `python3 -m guess 1722628800` should show timestamp interpretation ✅
   - [x] Add millisecond support (13-digit numbers)
   - **Test**: `python3 -m guess 1722628800000` should work ✅
   - [ ] Add more timestamp formats incrementally
   - **Test**: Each addition should work without breaking existing functionality

3. **Duration Converter** (Start Simple)
   - [x] Create `guess/converters/duration.py` with `DurationConverter` class
   - [x] Start with small numbers detection (< 86400 seconds)
   - [x] Output: human readable (HH:MM:SS), seconds, minutes, hours
   - [x] Add to converter list in registry
   - **Test**: `python3 -m guess 3661` should show duration interpretation ✅
   - [ ] Add basic unit parsing (`1h`, `30m`, `2d`)
   - **Test**: `python3 -m guess 1h` should work
   - [ ] Add combined units incrementally (`1h30m`)
   - **Test**: Each addition should work reliably

4. **Byte Size Converter** (Start Simple)
   - [x] Create `guess/converters/bytesize.py` with `ByteSizeConverter` class
   - [x] Start with large number detection (> 1024 bytes)
   - [x] Output: bytes, KB, MB, GB (decimal) and KiB, MiB, GiB (binary)
   - [x] Add to converter list in registry
   - **Test**: `python3 -m guess 1048576` should show byte size interpretation ✅
   - [ ] Add unit parsing (`1GB`, `512MB`)
   - **Test**: `python3 -m guess 1GB` should work
   - [ ] Add both decimal and binary unit support
   - **Test**: Each addition should work without conflicts

**Deliverables**:

- [x] Four working converter modules integrated via simple registry
- [x] Each converter can be tested independently
- [x] Smart multi-interpretation works: `python3 -m guess 1722628800` shows multiple formats ✅
- [x] Foundation ready for enhanced CLI commands in next phase ✅

---

### Phase 3: Enhanced Output and User Experience (1-2 days)

**Goal**: Add beautiful table formatting and improve user experience

**Incremental Verification**: Test output formatting improvements with existing converters

#### Tasks

1. **Simple Table Output System**
   - [x] Create `guess/formatter.py` with `TableFormatter` class:
     - [x] `format_single_result(converter_name, formats_dict) -> str` method
     - [x] `format_multiple_results(results_list) -> str` method
     - [x] Start with simple ASCII tables (|, -, +)
   - [x] Update converters to return structured data instead of formatted strings
   - [x] Update main.py to use table formatter
   - **Test**: All existing conversions should now have table output ✅
   - [ ] Add basic Unicode table characters for better appearance
   - [ ] Add column width handling for long values
   - **Test**: Tables should look clean and readable

2. **Basic CLI Enhancements**
   - [x] Add explicit type commands to main.py:
     - [x] `guess time <value>` - force timestamp interpretation only
     - [x] `guess duration <value>` - force duration interpretation only
     - [x] `guess size <value>` - force byte size interpretation only
     - [x] `guess number <value>` - force number base interpretation only
   - **Test**: Each explicit command should work correctly ✅
   - [x] Add basic help system with `--help` flag and examples
   - [x] Add version information with `--version` flag
   - **Test**: Help should show clear usage examples and work reliably ✅

3. **Error Handling and Validation**
   - [x] Implement graceful error handling for invalid inputs
   - [x] Add helpful error messages with suggestions
   - [x] Add input validation with clear feedback
   - **Test**: Try invalid inputs and verify helpful error messages ✅

**Deliverables**:

- [x] Beautiful table-formatted output for all conversions
- [x] Complete CLI with help system and explicit type commands
- [x] Robust error handling with helpful messages
- [x] All features work end-to-end ✅

---

### Phase 4: Testing and Polish (1-2 days)

**Goal**: Ensure production quality through comprehensive testing and documentation

**Incremental Verification**: Each improvement should be immediately testable

#### Tasks

1. **Comprehensive Testing**
   - [ ] Write integration tests in `tests/test_integration.py`:
     - [ ] Test full CLI workflows for each input type
     - [ ] Test error handling scenarios with invalid inputs
     - [ ] Test edge cases (empty input, very large numbers, negative values)
   - **Test**: Run full integration test suite and verify all pass
   - [ ] Basic performance testing:
     - [ ] Measure response times for various inputs
     - [ ] Ensure reasonable response time (< 200ms for simple cases)
     - [ ] Test with various input sizes
   - **Test**: Performance should be acceptable for CLI tool
   - [ ] Code quality improvements:
     - [ ] Run `black` formatting on all files
     - [ ] Fix critical `flake8` linting issues
     - [ ] Add type hints where beneficial
     - [ ] Achieve >80% test coverage with `pytest --cov`
   - **Test**: Basic quality checks should pass

2. **Documentation and Examples**
   - [ ] Write comprehensive `README.md`:
     - [ ] Installation instructions
     - [ ] Basic usage examples for all features
     - [ ] Table of supported input formats
     - [ ] Simple troubleshooting section
   - [ ] Add docstrings to all public methods
   - [ ] Create `examples.md` with common usage scenarios
   - **Test**: Documentation should be clear and examples should work as written

3. **Core Features and Edge Cases**
   - [ ] Enhanced number converter features:
     - [ ] Scientific notation for large numbers (>= 1,000,000)
     - [ ] Handle negative numbers appropriately
     - [ ] Basic RGB color representation for 0-255 values
   - **Test**: Each feature should work with appropriate inputs
   - [ ] Enhanced timestamp converter features:
     - [ ] Handle negative timestamps (pre-1970)
     - [ ] Add basic relative time calculations
     - [ ] Improve date format detection
   - **Test**: Each enhancement should be verifiable and not break existing functionality

**Deliverables**:

- [ ] Production-ready codebase with >80% test coverage
- [ ] Complete documentation with examples
- [ ] Core features working and tested
- [ ] Reasonable performance for CLI tool usage

---

### Phase 5: Final Polish and Distribution (0.5 days)

**Goal**: Prepare for source-only distribution and final validation

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
   - [ ] Update installation documentation in `README.md`
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
- **mypy**: Type checking (optional)

### Optional Enhancements (Post-MVP)

- **rich**: Enhanced terminal output (tables, colors)
- **python-dateutil**: Advanced date parsing
- **humanize**: Human-readable formatting

## Risk Assessment

### Medium Risk

- **Ambiguous input handling**: May require iterative refinement of detection logic
- **Edge cases**: Handling negative numbers, very large numbers, malformed input

### Low Risk

- **Basic conversions**: Core conversion logic is straightforward
- **CLI interface**: Well-established patterns available
- **Performance**: Simple operations should be fast enough
- **Cross-platform compatibility**: Using only built-in Python modules

## Success Criteria

### Minimum Viable Product (MVP)

- [ ] Accept numeric input and provide multiple interpretations
- [ ] Core four conversion types working (number, timestamp, duration, byte size)
- [ ] Clean command-line interface with help
- [ ] Basic error handling for invalid input

### Version 1.0

- [ ] Smart input detection with reasonable accuracy
- [ ] Clean formatted output (simple tables)
- [ ] Type-specific command options (`guess time 1234567890`)
- [ ] Good response time for typical usage
- [ ] Simple source installation process (`pip install -e .`)

### Post-1.0 Enhancements

- [ ] Enhanced table formatting with rich library
- [ ] Configuration file support
- [ ] Additional conversion types (colors, permissions, etc.)
- [ ] JSON output for scripting
- [ ] Interactive mode

## Timeline Summary

- **Total Estimated Time**: 6-10 days
- **MVP Delivery**: 4-6 days (Phases 1-3 complete)
- **Production Ready**: 6-10 days (All phases complete)

**Phase Breakdown**:

- Phase 1: 1-2 days (Setup & Basic Number Converter)
- Phase 2: 2-3 days (All Converters with Simple Registry)
- Phase 3: 1-2 days (Enhanced Output & CLI)
- Phase 4: 1-2 days (Testing & Documentation)
- Phase 5: 0.5-1 days (Final Polish & Distribution)

The project is designed for incremental development with each phase building upon the previous one. Each task is broken down for practical development with clear deliverables and checkboxes to track progress.
