"""
Tests for the duration converter.
"""

from guess.converters.duration import DurationConverter


class TestDurationConverter:
    """Test the duration converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = DurationConverter()

    def test_get_interpretations_seconds_format(self):
        """Test that plain numbers are interpreted as seconds."""
        interpretations = self.converter.get_interpretations("3600")
        assert len(interpretations) == 1
        assert interpretations[0].description == "seconds"
        assert interpretations[0].value == 3600

        interpretations = self.converter.get_interpretations("90")
        assert len(interpretations) == 1
        assert interpretations[0].description == "seconds"
        assert interpretations[0].value == 90

    def test_get_interpretations_duration_format(self):
        """Test that duration strings are properly interpreted."""
        # Test compact duration format like "1h30m"
        interpretations = self.converter.get_interpretations("1h30m")
        assert len(interpretations) == 1
        assert interpretations[0].description == "mixed"
        assert interpretations[0].value == 5400  # 1 hour + 30 minutes

        # Test float unit format like "2.5 hours" (with space)
        interpretations = self.converter.get_interpretations("2.5 hours")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hours"
        assert interpretations[0].value == 9000  # 2.5 * 3600

        # Test float unit format like "2.5hours" (without space)
        interpretations = self.converter.get_interpretations("2.5hours")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hours"
        assert interpretations[0].value == 9000  # 2.5 * 3600

        # Test years format (with space)
        interpretations = self.converter.get_interpretations("1 year")
        assert len(interpretations) == 1
        assert interpretations[0].description == "years"
        assert interpretations[0].value == int(365.25 * 24 * 3600)

        # Test years format (without space)
        interpretations = self.converter.get_interpretations("1year")
        assert len(interpretations) == 1
        assert interpretations[0].description == "years"
        assert interpretations[0].value == int(365.25 * 24 * 3600)

        # Test various unit forms (with space)
        interpretations = self.converter.get_interpretations("30 minutes")
        assert len(interpretations) == 1
        assert interpretations[0].description == "minutes"
        assert interpretations[0].value == 1800

        # Test various unit forms (without space)
        interpretations = self.converter.get_interpretations("30minutes")
        assert len(interpretations) == 1
        assert interpretations[0].description == "minutes"
        assert interpretations[0].value == 1800

        interpretations = self.converter.get_interpretations("5 days")
        assert len(interpretations) == 1
        assert interpretations[0].description == "days"
        assert interpretations[0].value == 432000

        # Test milliseconds, microseconds, nanoseconds
        interpretations = self.converter.get_interpretations("500 milliseconds")
        assert len(interpretations) == 1
        assert interpretations[0].description == "milliseconds"
        assert interpretations[0].value == 0.5  # 500 * 0.001 = 0.5

        interpretations = self.converter.get_interpretations("1000 ms")
        assert len(interpretations) == 1
        assert interpretations[0].description == "milliseconds"
        assert interpretations[0].value == 1.0  # 1000 * 0.001 = 1.0

        interpretations = self.converter.get_interpretations("1000000 microseconds")
        assert len(interpretations) == 1
        assert interpretations[0].description == "microseconds"
        assert interpretations[0].value == 1.0  # 1000000 * 0.000001 = 1.0

        interpretations = self.converter.get_interpretations("1000000000 nanoseconds")
        assert len(interpretations) == 1
        assert interpretations[0].description == "nanoseconds"
        assert interpretations[0].value == 1.0  # 1000000000 * 0.000000001 = 1.0

    def test_get_interpretations_invalid_values(self):
        """Test that invalid values return no interpretations."""
        assert len(self.converter.get_interpretations("")) == 0  # Empty input
        assert (
            len(self.converter.get_interpretations("abc")) == 0
        )  # Non-numeric/duration
        assert len(self.converter.get_interpretations("1x 2y")) == 0  # Invalid units
        assert len(self.converter.get_interpretations("-1")) == 0  # Negative duration

    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        # Test with 3661 seconds (1 hour, 1 minute, 1 second)
        result = self.converter.convert_value(3661)

        # Check expected output formats (Human Readable and Seconds)
        expected_keys = {"Human Readable", "Seconds"}
        assert set(result.keys()) == expected_keys
        assert result["Seconds"] == "3661 seconds"
        assert result["Human Readable"] == "1 hour, 1 minute, 1 second"

    def test_convert_value_with_years(self):
        """Test conversion of large durations that include years output."""
        # Test with a duration longer than 1 year
        one_year_seconds = int(365.25 * 24 * 3600)
        result = self.converter.convert_value(
            one_year_seconds + 86400
        )  # 1 year + 1 day

        # Should include Years output for large durations
        expected_keys = {"Human Readable", "Seconds", "Years"}
        assert set(result.keys()) == expected_keys
        assert "Years" in result
        assert result["Years"] == "1.00 years"

    def test_convert_value_edge_cases(self):
        """Test conversion of edge case durations."""
        # Test very short duration
        result = self.converter.convert_value(1)
        assert result["Seconds"] == "1 second"

        # Test exactly 1 hour - check actual formatting
        result = self.converter.convert_value(3600)
        assert result["Seconds"] == "3600 seconds"  # No comma formatting

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Duration"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Human Readable format present
        formats_with_human = {
            "Seconds": "3661.0 seconds",
            "Human Readable": "1 hour, 1 minute, 1 second",
        }
        display_value = self.converter.choose_display_value(
            formats_with_human, "seconds"
        )
        assert display_value == "1 hour, 1 minute, 1 second"

        # Test without Human Readable format
        formats_no_human = {
            "Seconds": "3661.0 seconds",
            "Minutes": "61.02",
            "Hours": "1.02",
            "Days": "0.04",
        }
        display_value = self.converter.choose_display_value(formats_no_human, "seconds")
        assert display_value is None  # Should return None when preferred format missing
