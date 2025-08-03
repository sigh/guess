"""
Tests for utility functions.
"""

from guess.utils import parse_float_unit, format_number_clean, format_units


class TestParseFloatUnit:
    """Test the parse_float_unit utility function."""

    def test_basic_parsing(self):
        """Test basic float unit parsing."""
        multipliers = {"seconds": 1, "minutes": 60, "hours": 3600}
        aliases = {"sec": "seconds", "min": "minutes", "hr": "hours"}

        # Test canonical units with spaces
        value, unit = parse_float_unit("30 seconds", multipliers, aliases)
        assert value == 30.0
        assert unit == "seconds"

        value, unit = parse_float_unit("2.5 hours", multipliers, aliases)
        assert value == 9000.0  # 2.5 * 3600
        assert unit == "hours"

        # Test canonical units without spaces
        value, unit = parse_float_unit("30seconds", multipliers, aliases)
        assert value == 30.0
        assert unit == "seconds"

        value, unit = parse_float_unit("2.5hours", multipliers, aliases)
        assert value == 9000.0  # 2.5 * 3600
        assert unit == "hours"

        # Test aliases with spaces
        value, unit = parse_float_unit("45 min", multipliers, aliases)
        assert value == 2700.0  # 45 * 60
        assert unit == "minutes"

        # Test aliases without spaces
        value, unit = parse_float_unit("45min", multipliers, aliases)
        assert value == 2700.0  # 45 * 60
        assert unit == "minutes"

    def test_invalid_inputs(self):
        """Test parsing invalid inputs."""
        multipliers = {"seconds": 1, "minutes": 60}

        # Invalid format
        value, unit = parse_float_unit("not a number", multipliers)
        assert value is None
        assert unit is None

        # Unknown unit
        value, unit = parse_float_unit("5 unknown", multipliers)
        assert value is None
        assert unit is None

        # Missing unit
        value, unit = parse_float_unit("5", multipliers)
        assert value is None
        assert unit is None

    def test_without_aliases(self):
        """Test parsing without aliases."""
        multipliers = {"meters": 1, "kilometers": 1000}

        value, unit = parse_float_unit("2.5 kilometers", multipliers)
        assert value == 2500.0
        assert unit == "kilometers"

        # Should fail for non-canonical unit when no aliases provided
        value, unit = parse_float_unit("2.5 km", multipliers)
        assert value is None
        assert unit is None

    def test_float_precision(self):
        """Test that float values are preserved correctly."""
        multipliers = {"hours": 3600}

        value, unit = parse_float_unit("0.5 hours", multipliers)
        assert value == 1800.0  # 0.5 * 3600
        assert unit == "hours"

        value, unit = parse_float_unit("1.25 hours", multipliers)
        assert value == 4500.0  # 1.25 * 3600
        assert unit == "hours"


class TestFormatNumberClean:
    """Test the format_number_clean utility function."""

    def test_integer_inputs(self):
        """Test formatting integer inputs."""
        assert format_number_clean(42) == "42"
        assert format_number_clean(0) == "0"
        assert format_number_clean(-5) == "-5"
        assert format_number_clean(1000) == "1000"

    def test_float_whole_numbers(self):
        """Test formatting floats that are whole numbers."""
        assert format_number_clean(42.0) == "42"
        assert format_number_clean(0.0) == "0"
        assert format_number_clean(-5.0) == "-5"
        assert format_number_clean(1000.0) == "1000"

    def test_float_with_decimals(self):
        """Test formatting floats with decimal parts."""
        assert format_number_clean(42.5) == "42.5"  # Strips trailing zero
        assert format_number_clean(3.14159) == "3.14"  # Limited to 2 decimal places for numbers > 1
        assert format_number_clean(-2.75) == "-2.75"
        assert format_number_clean(0.001) == "0.001"  # Preserves precision for numbers <= 1
        assert format_number_clean(0.123456) == "0.123456"  # Preserves precision for numbers <= 1
        assert format_number_clean(1.123456) == "1.12"  # Limited to 2 decimal places for numbers > 1

    def test_edge_cases(self):
        """Test edge cases and special float values."""
        assert format_number_clean(1.0000000000001) == "1"  # Negligible precision loss, strips to integer
        assert format_number_clean(999999999.0) == "999999999"
        # Very small numbers get scientific notation (Python's default behavior)
        assert format_number_clean(0.0000001) == "1e-07"
        assert format_number_clean(0.001) == "0.001"
        # Test rounding behavior
        assert format_number_clean(1.999) == "2.00"  # Precision lost in rounding, keeps decimals
        assert format_number_clean(1.995) == "2.00"  # Precision lost in rounding, keeps decimals

    def test_truncation_precision_behavior(self):
        """Test that trailing zeros are stripped only when no precision is lost."""
        # Cases where no precision is lost - should strip zeros
        assert format_number_clean(1.5) == "1.5"
        assert format_number_clean(1.50) == "1.5"
        assert format_number_clean(3.10) == "3.1"
        assert format_number_clean(42.00) == "42"  # Should be caught by is_integer()

        # Cases where precision is lost due to truncation - should keep decimals
        assert format_number_clean(1.500001) == "1.50"
        assert format_number_clean(2.000001) == "2.00"
        assert format_number_clean(3.14159) == "3.14"

        # Edge case: rounding behavior with precision loss
        assert format_number_clean(1.005) == "1.00"  # Rounds down due to banker's rounding, precision lost
        assert format_number_clean(1.004) == "1.00"  # Rounds down, precision lost
        assert format_number_clean(1.015) == "1.01"  # Rounds down, precision lost


class TestFormatUnits:
    """Test the format_units utility function."""

    def test_singular_units(self):
        """Test formatting with singular units."""
        assert format_units(1, "second") == "1 second"
        assert format_units(1, "minute") == "1 minute"
        assert format_units(1, "hour") == "1 hour"
        assert format_units(1, "day") == "1 day"
        assert format_units(1, "week") == "1 week"
        assert format_units(1, "millisecond") == "1 millisecond"
        assert format_units(1, "microsecond") == "1 microsecond"
        assert format_units(1, "nanosecond") == "1 nanosecond"

    def test_plural_units(self):
        """Test formatting with plural units."""
        assert format_units(2, "second") == "2 seconds"
        assert format_units(5, "minute") == "5 minutes"
        assert format_units(10, "hour") == "10 hours"
        assert format_units(3, "day") == "3 days"
        assert format_units(2, "week") == "2 weeks"
        assert format_units(500, "millisecond") == "500 milliseconds"
        assert format_units(1000, "microsecond") == "1000 microseconds"
        assert format_units(1500, "nanosecond") == "1500 nanoseconds"

    def test_zero_value(self):
        """Test formatting with zero value."""
        assert format_units(0, "second") == "0 seconds"
        assert format_units(0, "minute") == "0 minutes"
        assert format_units(0, "hour") == "0 hours"

    def test_fractional_values(self):
        """Test formatting with fractional values."""
        assert format_units(1.5, "hour") == "1.5 hours"
        assert format_units(2.25, "minute") == "2.25 minutes"
        assert format_units(0.5, "second") == "0.5 seconds"
        assert format_units(3.0, "day") == "3 days"  # Should show as whole number

    def test_large_numbers(self):
        """Test formatting with large numbers."""
        assert format_units(1500, "second") == "1500 seconds"
        assert format_units(3661.5, "second") == "3661.5 seconds"
        assert format_units(86400, "second") == "86400 seconds"

    def test_number_formatting_integration(self):
        """Test that format_units properly uses format_number_clean."""
        # Test whole number conversion
        assert format_units(3.0, "second") == "3 seconds"
        assert format_units(1.0, "minute") == "1 minute"

        # Test decimal limiting for numbers > 1
        assert format_units(3.14159, "hour") == "3.14 hours"
        assert format_units(2.999, "day") == "3.00 days"  # Rounds to 3.00, keeps decimal

        # Test precision preservation for numbers <= 1
        assert format_units(0.123456, "second") == "0.123456 seconds"

    def test_pluralization_edge_cases(self):
        """Test pluralization edge cases where formatting affects the result."""
        # Test case where value > 1 but formats to "1.00"
        assert format_units(1.002737850787132, "year") == "1.00 years"

        # Test exact 1 values
        assert format_units(1, "minute") == "1 minute"
        assert format_units(1.0, "hour") == "1 hour"

        # Test clearly plural values
        assert format_units(0.999, "second") == "0.999 seconds"
        assert format_units(1.01, "day") == "1.01 days"
        assert format_units(2.0, "week") == "2 weeks"

    def test_fractional_values(self):
        """Test formatting with fractional values."""
        assert format_units(1.5, "hour") == "1.5 hours"  # Strips trailing zero
        assert format_units(2.25, "minute") == "2.25 minutes"
        assert format_units(0.5, "second") == "0.5 seconds"
        assert format_units(3.0, "day") == "3 days"  # Should show as whole number function."""