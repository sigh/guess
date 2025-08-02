# Guess Project Plan

## Project Overview

Development of a command-line utility called "guess" that performs intelligent conversions between different data formats commonly used in programming and software management.

## Current Status (August 2, 2025)

**🎉 PHASE 5 COMPLETE - PROJECT READY FOR RELEASE! 🎉**

**✅ Completed Features:**

- All 4 converter types working (number, timestamp, duration, byte size)
- Enhanced number converter with hex/binary/octal input, RGB colors, file permissions
- Enhanced timestamp converter with negative timestamps and relative time
- Unit parsing for duration (`1h30m`) and byte size (`2.5GB`, `1GiB`)
- Beautiful table formatting for both single and multi-interpretation modes
- Complete CLI with explicit type commands and help system
- Integration tests covering main workflows
- Code quality improvements (89% test coverage, black formatting, flake8 linting)
- Comprehensive documentation with simplified README.md
- Production-ready package configuration
- Version v1.0.0 tagged and ready for GitHub release

**📦 Release Ready:**

- Source-installable package tested and working
- Complete documentation and release notes prepared
- All deliverables met or exceeded targets
- GitHub release preparation

**📝 Key Lessons Learned:**

- Always use virtual environments to avoid `externally-managed-environment` errors
- Read error messages completely - they contain the solution
- Test incrementally and fix environment issues first
- Separate data validation from presentation logic

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
   - [x] Write integration tests in `tests/test_integration.py`:
     - [x] Test full CLI workflows for each input type
     - [x] Test error handling scenarios with invalid inputs
     - [x] Test edge cases (empty input, very large numbers, negative values)
   - **Test**: Run full integration test suite and verify all pass ✅
   - **NOTES**:
     - Fixed table formatting truncation issue (octal format missing)
     - Fixed exit code handling for invalid input
     - Set up proper virtual environment for testing
   - **Test**: Performance should be acceptable for CLI tool
   - [x] Code quality improvements:
     - [x] Run `black` formatting on all files ✅
     - [x] Fix critical `flake8` linting issues ✅ (no issues found)
     - [x] Add type hints where beneficial ✅ (already present)
     - [x] Achieve >80% test coverage with `pytest --cov` ✅ (89% coverage)
   - **Test**: Basic quality checks should pass ✅

2. **Documentation and Examples**
   - [x] Write comprehensive `README.md`: ✅ (simplified and focused)
     - [x] Installation instructions ✅
     - [x] Basic usage examples for all features ✅
     - [x] Table of supported input formats ✅
   - [x] Add docstrings to all public methods ✅
   - **Test**: Documentation should be clear and examples should work as written

3. **Core Features and Edge Cases**
   - [x] Enhanced number converter features:
     - [x] Scientific notation for large numbers (>= 1,000,000) ✅
     - [x] Handle negative numbers appropriately ✅
     - [x] Basic RGB color representation for 0-255 values ✅
     - [x] File permission interpretation for 3-digit octal numbers ✅
     - [x] Support for hex/binary/octal input formats ✅
   - **Test**: Each feature should work with appropriate inputs ✅
   - [x] Enhanced timestamp converter features:
     - [x] Handle negative timestamps (pre-1970) ✅
     - [x] Add basic relative time calculations ✅
     - [x] Improve date format detection ✅
   - **Test**: Each enhancement should be verifiable and not break existing functionality ✅
   - [x] Enhanced duration converter features:
     - [x] Unit parsing (`1h`, `30m`, `2d`, `1h30m`) ✅
   - [x] Enhanced byte size converter features:
     - [x] Unit parsing (`1GB`, `2.5GiB`, `512MB`) ✅
     - [x] Both decimal and binary unit support ✅

**Deliverables**:

- [x] Core features working and tested ✅
- [x] Enhanced converters with advanced features ✅
- [x] Integration tests covering main workflows ✅
- [x] Production-ready codebase with >80% test coverage ✅ (89% achieved)
- [x] Complete documentation with examples ✅

---

### Phase 5: Final Polish and Distribution (0.5 days)

**Goal**: Prepare for source-only distribution and final validation

#### Tasks

1. **Source Package Preparation**
   - [x] Finalize `pyproject.toml` configuration: ✅
     - [x] Set correct package name, version, and description ✅
     - [x] Define minimal dependencies (only built-in modules if possible) ✅
     - [x] Configure entry points for CLI command ✅
     - [x] Add development dependencies section ✅
     - [x] Add proper package discovery configuration ✅
   - [x] Test installation in clean environments: ✅
     - [x] Create fresh virtual environment ✅
     - [x] Test `pip install -e .` from project root ✅
     - [x] Verify CLI command works after installation ✅
     - [x] Test uninstallation process ✅
   - [x] Create LICENSE file ✅
   - [x] Update installation documentation in `README.md` ✅
   - [x] Tag version with `git tag v1.0.0` ✅

2. **GitHub Release Setup**
   - [x] Create GitHub release v1.0.0 with source archive ✅ (ready)
   - [x] Add clear installation and usage instructions ✅ (in RELEASE_NOTES.md)

**Deliverables**:

- [x] Source-installable package working correctly ✅
- [x] GitHub release v1.0.0 with complete documentation ✅ (ready for upload)
- [x] Clear installation process documented and tested ✅

---

### Phase 6: Enhanced Features Implementation (3-4 days)

**Goal**: Implement all the enhanced features specified in the updated requirements, including new converter types, improved formatting, and advanced parsing capabilities.

**Based on Updated Requirements Analysis**: The requirements now include significant enhancements for color conversion, file permissions, improved output formatting, scientific notation parsing, flexible unit parsing, and human-readable number formats.

#### Tasks

1. **Output Format Refactoring**
   - [ ] **Remove Table Formatting Dependencies**:
     - [ ] Update formatter.py to use simple hierarchical output
     - [ ] Remove Unicode table characters and complex formatting
     - [ ] Implement clean indentation-based display
     - [ ] Ensure consistent spacing and readability
     - [ ] **Write Test**: Create `test_output_formatting.py` to verify clean output without table characters
     - [ ] **Test Manually**: All existing converters produce clean, readable output

   - [ ] **Mode-Based Output Implementation**:
     - [ ] **Mode 1 (Ambiguous Input)**: Show one readable format per type
       - [ ] Example: `guess 1722628800000` → Number: "1.72 trillion", Timestamp: "2024-08-02 16:00:00 UTC", Bytes: "1.72 TB"
     - [ ] **Mode 2 (Specific Type)**: Show multiple formats of same type
       - [ ] Example: `guess time 1722628800` → Multiple timestamp formats
     - [ ] **Write Test**: Add tests to verify different output modes in main test file
     - [ ] **Test Manually**: Compare output for `guess 255` vs `guess number 255`

2. **Enhanced Duration Converter**
   - [ ] **Improved Output Format**:
     - [ ] Remove fractional minutes/hours output (not useful)
     - [ ] Keep only: human readable, compact format, canonical seconds
     - [ ] Example output: "1 hour, 1 minute, 1 second", "1h1m1s", "3661 seconds"
     - [ ] Remove redundant HH:MM:SS format
     - [ ] **Update Tests**: Modify `test_duration.py` to verify new output formats
     - [ ] **Test Manually**: `python3 -m guess duration 3661` should show clean, useful formats only

3. **Enhanced Number Converter**
   - [ ] **Scientific Notation Support**:
     - [ ] Robust parsing for all standard forms: `1.5e9`, `2.4E+6`, `1.23e-4`, `5E10`
     - [ ] Handle positive and negative exponents
     - [ ] Auto-detect scientific notation input and treat as decimal number
     - [ ] **Update Tests**: Add scientific notation test cases to `test_number.py`
     - [ ] **Test Manually**: `python3 -m guess 1.5e9` should show as number

   - [ ] **Human Readable Numbers**:
     - [ ] Convert large numbers to readable format: "1.3 billion", "2.7 million"
     - [ ] Support range 100,000 to 1,000,000,000,000,000 (0.1 million to 1000 quadrillion)
     - [ ] Include units: million, billion, trillion, quadrillion
     - [ ] **Update Tests**: Add human readable number test cases to `test_number.py`
     - [ ] **Test Manually**: `python3 -m guess 1500000000` should show "1.5 billion"

   - [ ] **Remove Color/Permission Context**:
     - [ ] Remove RGB color context from number converter (now separate type)
     - [ ] Remove file permission context from number converter (now separate type)
     - [ ] Focus purely on base conversions and scientific notation
     - [ ] **Update Tests**: Ensure number converter tests no longer check color/permission
     - [ ] **Test Manually**: `python3 -m guess 255` should show both number and color interpretations

4. **Enhanced Byte Size Converter**
   - [ ] **Flexible Unit Parsing**:
     - [ ] Handle whitespace variations: `2GB`, `2 GB`, `2.5 GiB`
     - [ ] Support spaces between numbers and units: `512 MB`
     - [ ] Maintain existing decimal/binary unit support
     - [ ] **Update Tests**: Add whitespace parsing test cases to `test_bytesize.py`
     - [ ] **Test Manually**: `python3 -m guess "2 GB"` should work (with quotes for spaces)
     - [ ] **Test Manually**: `python3 -m guess 2.5GiB` should work

5. **Enhanced Timestamp Converter**
   - [ ] **Improved Format Selection**:
     - [ ] Add context labels to timestamp outputs
     - [ ] Include unix timestamp in both seconds and milliseconds
     - [ ] Add relative time with context ("1 year ago")
     - [ ] Add ISO 8601 format for standards compliance
     - [ ] **Update Tests**: Add new format test cases to `test_timestamp.py`
     - [ ] **Test Manually**: Timestamp outputs should be clear and comprehensive

6. **New Converter Types**
   - [ ] **Color Converter** (`guess/converters/color.py`):
     - [ ] Create `ColorConverter` class inheriting from base converter
     - [ ] Handle RGB input values (0-255): `255`, `0xFF`
     - [ ] Handle hex color codes: `#FF0000`, `#00FF00`, `#0000FF`
     - [ ] Handle color names: `red`, `blue`, `green`, `black`, `white`
     - [ ] Output formats:
       - [ ] Hex color code: `#FF0000`
       - [ ] RGB values: `rgb(255, 0, 0)`
       - [ ] Color name (when applicable): `red`
       - [ ] HSL values: `hsl(0, 100%, 50%)`
     - [ ] **Write Tests**: Create `tests/test_color.py` with RGB, hex, and color name tests
     - [ ] **Test Manually**: `python3 -m guess color 255` should show color formats
     - [ ] **Test Manually**: `python3 -m guess #FF0000` should auto-detect as color

   - [ ] **File Permission Converter** (`guess/converters/permission.py`):
     - [ ] Create `PermissionConverter` class inheriting from base converter
     - [ ] Handle octal notation: `755`, `0755`, `0o755`
     - [ ] Handle symbolic notation: `rwxr-xr-x`
     - [ ] Handle decimal equivalent: `493`
     - [ ] Output formats:
       - [ ] Symbolic notation: `rwxr-xr-x`
       - [ ] Octal notation: `0o755`
       - [ ] Decimal equivalent: `493`
       - [ ] Permission breakdown: `owner: rwx, group: r-x, others: r-x`
     - [ ] **Write Tests**: Create `tests/test_permission.py` with octal and symbolic tests
     - [ ] **Test Manually**: `python3 -m guess permission 0755` should show permission formats
     - [ ] **Test Manually**: `python3 -m guess rwxr-xr-x` should auto-detect as permission

7. **Registry and Detection Updates**
   - [ ] **Update Smart Detection Algorithm**:
     - [ ] Add color detection for RGB values (0-255) and hex codes (#RRGGBB)
     - [ ] Add permission detection for octal patterns (755, 0644) and symbolic (rwxr-xr-x)
     - [ ] Remove color/permission detection from number converter
     - [ ] Update registry.py to include new converter types
     - [ ] **Update Tests**: Modify `test_detection.py` to test new converter detection
     - [ ] **Test Manually**: `python3 -m guess 255` should show number AND color interpretations
     - [ ] **Test Manually**: `python3 -m guess 0755` should auto-detect as permission
     - [ ] **Test Manually**: `python3 -m guess #FF0000` should auto-detect as color

8. **Enhanced CLI Commands**
   - [ ] **Add New Type Commands**:
     - [ ] Add `guess color <value>` command to main.py
     - [ ] Add `guess permission <value>` command to main.py
     - [ ] Update help text to include new commands
     - [ ] Update supported types in CLI documentation
     - [ ] **Update Tests**: Add CLI tests for new commands to `test_main.py`
     - [ ] **Test Manually**: `python3 -m guess --help` should show all 6 converter types
     - [ ] **Test Manually**: Each new command should work correctly

9. **Final Integration and Validation**
   - [ ] **Run Complete Test Suite**:
     - [ ] Ensure all individual test files pass (test_color.py, test_permission.py, etc.)
     - [ ] Update `tests/test_integration.py` for new converter types
     - [ ] Verify test coverage remains >80% with new features
     - [ ] **Test Manually**: Run `python -m pytest tests/` to verify all tests pass

   - [ ] **Enhanced Error Handling**:
     - [ ] Add color and permission suggestions to error messages
     - [ ] Update help text examples to include new types
     - [ ] Test invalid inputs for new converter types
     - [ ] **Update Tests**: Add error handling tests to existing test files
     - [ ] **Test Manually**: Error messages should be helpful for all converter types

   - [ ] **Integration Testing**:
     - [ ] Test all 6 converter types work independently
     - [ ] Test ambiguous input shows multiple interpretations
     - [ ] Test specific type commands work correctly
     - [ ] **Test Manually**: Each converter type should function properly

**Deliverables for Phase 6**:

- [ ] Two new converter types (color, permission) fully implemented with tests
- [ ] Enhanced number converter with scientific notation and human readable formats (tested)
- [ ] Improved output formatting without table dependencies (tested)
- [ ] Enhanced byte size converter with flexible whitespace parsing (tested)
- [ ] Mode-based output (simple format for ambiguous, detailed for specific types) (tested)
- [ ] Updated CLI with all 6 converter type commands (tested)
- [ ] Test suite coverage >80% maintained throughout development
- [ ] All integration tests passing

**Estimated Timeline**: 3-4 days for a junior developer, with testing integrated into each task

**Development Notes**:

- **Testing Strategy**: Each major component should be tested immediately after implementation
- **Quality Gates**: No task is complete until both implementation and tests pass
- **Manual Verification**: After automated tests, manually verify key examples work as expected
- **Incremental Approach**: Build and test one converter at a time before moving to the next

---

### Phase 7: Documentation and Final Release (1 day)

**Goal**: Update all documentation to reflect the enhanced features and prepare for v1.1.0 release

#### Tasks

1. **Update Core Documentation**
   - [ ] **Update README.md**:
     - [ ] Add examples for color and permission converters
     - [ ] Update supported input formats table
     - [ ] Add examples of new output formatting
     - [ ] Update installation and usage sections
     - [ ] **Verify Examples**: Test all README examples manually to ensure they work

   - [ ] **Update REQUIREMENTS.md**:
     - [ ] Verify all requirements are implemented correctly
     - [ ] Update examples to match actual output formatting
     - [ ] Ensure consistency between requirements and implementation
     - [ ] **Cross-check**: Implementation should match requirements exactly

2. **Version and Release Preparation**
   - [ ] **Update Version Information**:
     - [ ] Update version in pyproject.toml to v1.1.0
     - [ ] Update version strings in code if any
     - [ ] Create comprehensive CHANGELOG.md documenting all v1.1.0 changes
     - [ ] **Test Package**: Test package installation and CLI functionality in clean environment
     - [ ] **Verify Version**: `python3 -m guess --version` should show v1.1.0

   - [ ] **Final Integration Testing**:
     - [ ] Run full test suite and ensure >80% coverage maintained
     - [ ] Test installation in fresh virtual environment
     - [ ] Test all CLI commands and converter types
     - [ ] Verify error handling and help text
     - [ ] **Complete Regression Testing**: Verify all original functionality still works
     - [ ] **New Feature Testing**: Verify all new features work as specified

3. **Release Artifacts**
   - [ ] **Git and Release Management**:
     - [ ] Commit all changes with clear commit messages
     - [ ] Tag release with `git tag v1.1.0`
     - [ ] Prepare GitHub release notes highlighting new features
     - [ ] Update PROJECT_PLAN.md status to reflect completion
     - [ ] **Final Verification**: Source package should install and work correctly from git

**Deliverables for Phase 7**:

- [ ] Updated documentation with all examples manually verified
- [ ] Comprehensive changelog documenting enhancements
- [ ] Tagged v1.1.0 release tested and ready for distribution
- [ ] Complete regression testing passed with all new features verified
- [ ] Project plan updated with final status

**Final Success Criteria**:

- All 6 converter types working (number, timestamp, duration, byte size, color, permission)
- Enhanced features implemented and tested per requirements specification
- Clean, readable output formatting without table dependencies
- Comprehensive CLI with help system and error handling
- >80% test coverage maintained with all tests passing
- Complete documentation with verified working examples
- Source-installable package ready for distribution
- All manual tests pass in clean environment
