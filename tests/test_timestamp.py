"""
Tests for the timestamp converter.
"""

from guess.converters.timestamp import TimestampConverter


class TestTimestampConverter:
    """Test the timestamp converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = TimestampConverter()

    def test_get_interpretations_seconds_format(self):
        """Test that seconds format timestamps are properly interpreted."""
        # Standard 10-digit Unix timestamp
        interpretations = self.converter.get_interpretations("1234567890")
        assert len(interpretations) == 1
        assert interpretations[0].description == "unix seconds"
        assert interpretations[0].value == 1234567890000  # Converted to milliseconds

        # Negative timestamp
        interpretations = self.converter.get_interpretations("-123456")
        assert len(interpretations) == 1
        assert interpretations[0].description == "unix seconds"
        assert interpretations[0].value == -123456000

    def test_get_interpretations_milliseconds_format(self):
        """Test that milliseconds format timestamps are properly interpreted."""
        # Standard 13-digit Unix timestamp in milliseconds
        interpretations = self.converter.get_interpretations("1234567890123")
        assert len(interpretations) == 1
        assert interpretations[0].description == "unix milliseconds"
        assert interpretations[0].value == 1234567890123  # Kept as milliseconds

    def test_get_interpretations_invalid_values(self):
        """Test that invalid values return no interpretations."""
        assert len(self.converter.get_interpretations("")) == 0  # Empty input
        assert len(self.converter.get_interpretations("abc")) == 0  # Non-numeric
        assert len(self.converter.get_interpretations("12345")) == 0  # Wrong length
        assert (
            len(self.converter.get_interpretations("99999999999999")) == 0
        )  # Too long
        assert (
            len(self.converter.get_interpretations("0")) == 0
        )  # Too short for valid timestamp

    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        # Use a known timestamp: 1234567890000 ms = 1234567890 seconds = 2009-02-13
        result = self.converter.convert_value(1234567890000)

        # Should always have these formats
        expected_keys = {
            "Unix Seconds",
            "Unix Milliseconds",
            "UTC",
            "Local Time",
            "ISO 8601",
            "Relative",
            "Human Readable",
        }
        assert set(result.keys()) == expected_keys

        # Check basic format correctness
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        assert result["Unix Milliseconds"] == "1234567890000 (unix milliseconds)"
        assert "2009" in result["UTC"]
        assert "Z" in result["ISO 8601"]

    def test_convert_value_seconds_input(self):
        """Test conversion when input was interpreted as seconds."""
        # This would come from get_interpretations("1234567890") -> value = 1234567890000
        result = self.converter.convert_value(1234567890000)
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        assert result["Unix Milliseconds"] == "1234567890000 (unix milliseconds)"

    def test_convert_value_milliseconds_input(self):
        """Test conversion when input was interpreted as milliseconds."""
        # This would come from get_interpretations("1234567890123") -> value = 1234567890123
        result = self.converter.convert_value(1234567890123)
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        assert result["Unix Milliseconds"] == "1234567890123 (unix milliseconds)"

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Timestamp"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Human Readable format present
        formats_with_human = {
            "Unix Seconds": "1234567890 (unix seconds)",
            "Unix Milliseconds": "1234567890000 (unix milliseconds)",
            "UTC": "2009-02-13 23:31:30 UTC",
            "Local Time": "2009-02-13 18:31:30 EST",
            "ISO 8601": "2009-02-13T23:31:30Z",
            "Relative": "15 years ago",
            "Human Readable": "Feb 13, 2009 at 6:31 PM",
        }
        display_value = self.converter.choose_display_value(
            formats_with_human, "unix seconds"
        )
        assert display_value == "Feb 13, 2009 at 6:31 PM"

        # Test without Human Readable format
        formats_no_human = {
            "Unix Seconds": "1234567890 (unix seconds)",
            "Unix Milliseconds": "1234567890000 (unix milliseconds)",
            "UTC": "2009-02-13 23:31:30 UTC",
            "Local Time": "2009-02-13 18:31:30 EST",
            "ISO 8601": "2009-02-13T23:31:30Z",
            "Relative": "15 years ago",
        }
        display_value = self.converter.choose_display_value(
            formats_no_human, "unix seconds"
        )
        assert display_value is None  # Should return None when preferred format missing
