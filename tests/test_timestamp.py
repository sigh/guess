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
            "ISO 8601",
            "Relative",
            "Human Readable",
        }
        assert set(result.keys()) == expected_keys

        # Check basic format correctness
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        assert "Z" in result["ISO 8601"]
        assert "2009" in result["ISO 8601"]

    def test_convert_value_seconds_input(self):
        """Test conversion when input was interpreted as seconds."""
        # This would come from get_interpretations("1234567890") -> value = 1234567890000
        result = self.converter.convert_value(1234567890000)
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        # Should not have microseconds for round milliseconds timestamp
        assert "Unix Microseconds" not in result

    def test_convert_value_milliseconds_input(self):
        """Test conversion when input was interpreted as milliseconds."""
        # This would come from get_interpretations("1234567890123") -> value = 1234567890123
        result = self.converter.convert_value(1234567890123)
        assert result["Unix Seconds"] == "1234567890 (unix seconds)"
        # Should have microseconds since there's subsecond precision
        assert "Unix Microseconds" in result
        assert result["Unix Microseconds"] == "1234567890123000 (unix microseconds)"

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Timestamp"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Human Readable format present
        formats_with_human = {
            "Unix Seconds": "1234567890 (unix seconds)",
            "Unix Milliseconds": "1234567890000 (unix milliseconds)",
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
            "ISO 8601": "2009-02-13T23:31:30Z",
            "Relative": "15 years ago",
        }
        display_value = self.converter.choose_display_value(
            formats_no_human, "unix seconds"
        )
        assert display_value is None  # Should return None when preferred format missing

    def test_get_interpretations_datetime_strings(self):
        """Test parsing various date and datetime string formats."""
        converter = TimestampConverter()

        # ISO date formats
        interpretations = converter.get_interpretations("2024-01-15")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        interpretations = converter.get_interpretations("2024-01-15 10:30:00")
        assert len(interpretations) > 0
        assert interpretations[0].description == "datetime"

        interpretations = converter.get_interpretations("2024-01-15T10:30:00Z")
        assert len(interpretations) > 0
        assert interpretations[0].description == "datetime"

        # US date formats
        interpretations = converter.get_interpretations("01/15/2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        # European date formats
        interpretations = converter.get_interpretations("15/01/2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        interpretations = converter.get_interpretations("15.01.2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        # Month name formats
        interpretations = converter.get_interpretations("January 15, 2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        interpretations = converter.get_interpretations("Jan 15, 2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        interpretations = converter.get_interpretations("15 January 2024")
        assert len(interpretations) > 0
        assert interpretations[0].description == "date"

        # Time-only formats (should use today's date)
        interpretations = converter.get_interpretations("10:30:00")
        assert len(interpretations) > 0
        assert interpretations[0].description == "time"

        interpretations = converter.get_interpretations("10:30")
        assert len(interpretations) > 0
        assert interpretations[0].description == "time"

    def test_get_interpretations_invalid_datetime_strings(self):
        """Test that invalid datetime strings are not parsed."""
        converter = TimestampConverter()

        # Invalid formats should return no interpretations (they'll fall through to numeric parsing)
        invalid_dates = [
            "not-a-date",
            "2024-01-32",  # Invalid day
            "25:00:00",    # Invalid hour
            "hello world",
            "random text"
        ]

        for invalid_date in invalid_dates:
            interpretations = converter.get_interpretations(invalid_date)
            # Should either be empty or not contain datetime interpretations
            datetime_interpretations = [i for i in interpretations
                                      if i.description in ["date", "datetime", "time"]]
            assert len(datetime_interpretations) == 0, \
                f"Invalid date '{invalid_date}' should not be parsed as datetime"

    def test_datetime_parsing_consistency(self):
        """Test that same dates in different formats produce the same timestamp."""
        converter = TimestampConverter()

        # All these should represent the same date
        date_formats = [
            "2024-01-15",
            "01/15/2024",
            "January 15, 2024",
            "Jan 15, 2024",
            "15 January 2024"
        ]

        timestamps = []
        for date_format in date_formats:
            interpretations = converter.get_interpretations(date_format)
            assert len(interpretations) > 0, f"Failed to parse: {date_format}"
            timestamps.append(interpretations[0].value)

        # All timestamps should be the same (within reasonable tolerance for timezone differences)
        base_timestamp = timestamps[0]
        for i, timestamp in enumerate(timestamps[1:], 1):
            assert timestamp == base_timestamp, \
                f"Date format '{date_formats[i]}' produced different timestamp"

    def test_dateutil_flexible_formats(self):
        """Test that dateutil can parse more flexible date formats."""
        converter = TimestampConverter()

        # Test formats that dateutil can handle but standard strptime cannot
        flexible_formats = [
            ("August 3rd, 2024", "date"),
            ("3rd August 2024", "date"),
            ("Aug 3rd, 2024", "date"),
            ("8/3/24", "date"),
            ("2024/08/03", "date"),
            ("03-Aug-2024", "date"),
            ("2024-08-03 2:30 PM", "datetime"),
            ("2:30 PM", "time"),
            ("2:30PM", "time"),
            ("14:30:45", "time"),
        ]

        for date_str, expected_desc in flexible_formats:
            interpretations = converter.get_interpretations(date_str)
            assert len(interpretations) > 0, f"Failed to parse flexible format: {date_str}"
            assert interpretations[0].description == expected_desc, \
                f"Wrong description for '{date_str}': got '{interpretations[0].description}', expected '{expected_desc}'"

    def test_dateutil_ordinal_numbers(self):
        """Test parsing dates with ordinal numbers (1st, 2nd, 3rd, etc.)."""
        converter = TimestampConverter()

        ordinal_dates = [
            "January 1st, 2024",
            "February 2nd, 2024",
            "March 3rd, 2024",
            "April 4th, 2024",
            "1st Jan 2024",
            "2nd Feb 2024",
            "3rd Mar 2024",
        ]

        for date_str in ordinal_dates:
            interpretations = converter.get_interpretations(date_str)
            assert len(interpretations) > 0, f"Failed to parse ordinal date: {date_str}"
            assert interpretations[0].description == "date", \
                f"Ordinal date '{date_str}' should be recognized as 'date'"

    def test_dateutil_various_separators(self):
        """Test parsing dates with various separators."""
        converter = TimestampConverter()

        separator_formats = [
            ("2024/08/03", "date"),
            ("2024.08.03", "date"),
            ("08-03-2024", "date"),
            ("03.08.2024", "date"),
        ]

        for date_str, expected_desc in separator_formats:
            interpretations = converter.get_interpretations(date_str)
            assert len(interpretations) > 0, f"Failed to parse date with separators: {date_str}"
            # Find the date interpretation (there might be multiple interpretations)
            date_interpretations = [i for i in interpretations if i.description == expected_desc]
            assert len(date_interpretations) > 0, \
                f"No '{expected_desc}' interpretation found for '{date_str}', got: {[i.description for i in interpretations]}"

    def test_relative_time_parsing(self):
        """Test parsing of relative time expressions."""
        converter = TimestampConverter()

        # Test "now"
        interpretations = converter.get_interpretations("now")
        assert len(interpretations) == 1
        assert interpretations[0].description == "relative time"

        # Test "in <duration>"
        interpretations = converter.get_interpretations("in 5 minutes")
        assert len(interpretations) == 1
        assert interpretations[0].description == "relative time"

        # Test "<duration> ago"
        interpretations = converter.get_interpretations("2 hours ago")
        assert len(interpretations) == 1
        assert interpretations[0].description == "relative time"

        # Test "<duration> from now"
        interpretations = converter.get_interpretations("30 minutes from now")
        assert len(interpretations) == 1
        assert interpretations[0].description == "relative time"

        # Test with complex durations
        interpretations = converter.get_interpretations("in 1h30m")
        assert len(interpretations) == 1
        assert interpretations[0].description == "relative time"

        # Test invalid relative expressions
        interpretations = converter.get_interpretations("in yesterday")
        assert len(interpretations) == 0

        interpretations = converter.get_interpretations("5 minutes")  # Missing "ago" or "in"
        assert len(interpretations) == 0
