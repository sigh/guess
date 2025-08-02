"""
Tests for the bytesize converter.
"""

from guess.converters.bytesize import ByteSizeConverter


class TestByteSizeConverter:
    """Test the bytesize converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = ByteSizeConverter()

    def test_get_interpretations_plain_numbers(self):
        """Test that plain numbers are interpreted as bytes."""
        interpretations = self.converter.get_interpretations("1024")
        assert len(interpretations) == 1
        assert interpretations[0].description == "bytes"
        assert interpretations[0].value == 1024

        interpretations = self.converter.get_interpretations("1000000")
        assert len(interpretations) == 1
        assert interpretations[0].description == "bytes"
        assert interpretations[0].value == 1000000

    def test_get_interpretations_byte_size_format(self):
        """Test that byte size strings are properly interpreted."""
        # Various byte size formats
        interpretations = self.converter.get_interpretations("1KB")
        assert len(interpretations) == 1
        assert interpretations[0].description == "byte size"
        assert interpretations[0].value == 1000

        interpretations = self.converter.get_interpretations("1MB")
        assert len(interpretations) == 1
        assert interpretations[0].description == "byte size"
        assert interpretations[0].value == 1000000

        interpretations = self.converter.get_interpretations("1GB")
        assert len(interpretations) == 1
        assert interpretations[0].description == "byte size"
        assert interpretations[0].value == 1000000000

        # Binary units
        interpretations = self.converter.get_interpretations("1KiB")
        assert len(interpretations) == 1
        assert interpretations[0].description == "byte size"
        assert interpretations[0].value == 1024

    def test_get_interpretations_invalid_values(self):
        """Test that invalid values return no interpretations."""
        assert len(self.converter.get_interpretations("")) == 0  # Empty input
        assert len(self.converter.get_interpretations("abc")) == 0  # Non-numeric
        assert len(self.converter.get_interpretations("1XB")) == 0  # Invalid unit
        assert len(self.converter.get_interpretations("-1")) == 0  # Negative size

    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        # Test with 1048576 bytes (1 MiB)
        result = self.converter.convert_value(1048576)

        # Should have these key formats based on actual implementation
        assert "Raw Bytes" in result
        assert "Binary" in result
        assert "Decimal" in result

        # Check format correctness
        assert result["Raw Bytes"] == "1048576 bytes"  # With unit
        assert "MiB" in result["Binary"]
        assert "MB" in result["Decimal"]

    def test_convert_value_small_sizes(self):
        """Test conversion of small byte sizes."""
        result = self.converter.convert_value(512)
        assert result["Raw Bytes"] == "512 bytes"

    def test_convert_value_large_sizes(self):
        """Test conversion of large byte sizes."""
        # Test 1 GB
        result = self.converter.convert_value(1000000000)
        assert result["Raw Bytes"] == "1000000000 bytes"

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Size"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with both Decimal and Binary formats present (should return combined format)
        formats_with_both = {
            "Raw Bytes": "1048576 bytes",
            "Decimal": "1.05 MB",
            "Binary": "1.00 MiB",
        }
        display_value = self.converter.choose_display_value(formats_with_both, "bytes")
        assert display_value == "1.05 MB / 1.00 MiB"

        # Test with only Decimal format (should return Decimal)
        formats_decimal_only = {
            "Raw Bytes": "1000000 bytes",
            "Decimal": "1.00 MB",
        }
        display_value = self.converter.choose_display_value(
            formats_decimal_only, "bytes"
        )
        assert display_value == "1.00 MB"

        # Test without Decimal format (should return None)
        formats_no_decimal = {
            "Raw Bytes": "1024 bytes",
            "Binary": "1.00 KiB",
        }
        display_value = self.converter.choose_display_value(formats_no_decimal, "bytes")
        assert display_value is None  # Should return None when preferred format missing
