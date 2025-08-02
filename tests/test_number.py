"""
Tests for the number converter.
"""

from guess.converters.number import NumberConverter


class TestNumberConverter:
    """Test cases for NumberConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = NumberConverter()

    # Test get_interpretations method
    def test_get_interpretations_decimal_numbers(self):
        """Test that decimal numbers are properly interpreted."""
        # Basic decimal number
        interpretations = self.converter.get_interpretations("255")
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == 255

        # Zero
        interpretations = self.converter.get_interpretations("0")
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == 0

        # Large number
        interpretations = self.converter.get_interpretations("1234567890")
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == 1234567890

        # With whitespace
        interpretations = self.converter.get_interpretations("  123  ")
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == 123

    def test_get_interpretations_hexadecimal_numbers(self):
        """Test that hexadecimal numbers are properly interpreted."""
        # 0x prefix
        interpretations = self.converter.get_interpretations("0xFF")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == 255

        # Plain hex (no prefix)
        interpretations = self.converter.get_interpretations("abc")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == 2748  # 0xabc

    def test_get_interpretations_binary_numbers(self):
        """Test that binary numbers are properly interpreted."""
        # 0b prefix
        interpretations = self.converter.get_interpretations("0b101010")
        assert len(interpretations) == 1
        assert interpretations[0].description == "binary"
        assert interpretations[0].value == 42

        # b suffix
        interpretations = self.converter.get_interpretations("101010b")
        assert len(interpretations) == 1
        assert interpretations[0].description == "binary"
        assert interpretations[0].value == 42

    def test_get_interpretations_octal_numbers(self):
        """Test that octal numbers are properly interpreted."""
        # 0o prefix
        interpretations = self.converter.get_interpretations("0o777")
        assert len(interpretations) == 1
        assert interpretations[0].description == "octal"
        assert interpretations[0].value == 511

        # o suffix
        interpretations = self.converter.get_interpretations("777o")
        assert len(interpretations) == 1
        assert interpretations[0].description == "octal"
        assert interpretations[0].value == 511

    def test_get_interpretations_scientific_numbers(self):
        """Test that scientific notation numbers are properly interpreted."""
        interpretations = self.converter.get_interpretations("1.5e9")
        assert len(interpretations) == 1
        assert interpretations[0].description == "scientific"
        assert interpretations[0].value == 1500000000

        interpretations = self.converter.get_interpretations("2.3E-4")
        assert len(interpretations) == 1
        assert interpretations[0].description == "scientific"
        assert interpretations[0].value == 0.00023

    def test_get_interpretations_negative_numbers(self):
        """Test that negative numbers are properly interpreted."""
        interpretations = self.converter.get_interpretations("-123")
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == -123

    def test_get_interpretations_invalid_inputs(self):
        """Test that invalid inputs return no interpretations."""
        assert len(self.converter.get_interpretations("")) == 0
        assert len(self.converter.get_interpretations("xyz")) == 0  # invalid hex
        assert len(self.converter.get_interpretations("12g34")) == 0  # invalid mixed
        assert len(self.converter.get_interpretations("0b12345")) == 0  # invalid binary
        assert (
            len(self.converter.get_interpretations("#FF")) == 0
        )  # # prefix reserved for colors

    # Test convert_value method
    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        result = self.converter.convert_value(255)
        expected_keys = {"Decimal", "Hexadecimal", "Binary", "Octal"}
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "255"
        assert result["Hexadecimal"] == "0xff"
        assert result["Binary"] == "0b11111111"
        assert result["Octal"] == "0o377"

    def test_convert_value_large_number_with_scientific(self):
        """Test conversion of large numbers includes scientific notation and formatting."""
        result = self.converter.convert_value(1500000000)
        expected_keys = {
            "Decimal",
            "Scientific",
            "Hexadecimal",
            "Binary",
            "Octal",
            "Human Readable",
        }
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "1500000000"  # No commas
        assert result["Scientific"] == "1.50e+09"

    def test_convert_value_negative_number(self):
        """Test that negative numbers include all formats with proper signs."""
        result = self.converter.convert_value(-42)
        assert result["Decimal"] == "-42"
        # Negative numbers do show hex/binary/octal with minus signs
        assert result["Hexadecimal"] == "-0x2a"
        assert result["Binary"] == "-0b101010"
        assert result["Octal"] == "-0o52"

    def test_convert_value_float(self):
        """Test that floats exclude integer base formats."""
        result = self.converter.convert_value(123.456)
        assert result["Decimal"] == "123.456"
        # Should not have integer formats for floats
        assert "Binary" not in result
        assert "Hexadecimal" not in result
        assert "Octal" not in result
        # Small floats don't get scientific notation automatically
        assert "Scientific" not in result

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Number"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Human Readable format present (large number)
        formats_with_human = {
            "Decimal": "1500000000",
            "Scientific": "1.50e+09",
            "Human Readable": "1.5 billion",
            "Hexadecimal": "0x59682f00",
            "Binary": "0b1011001011010000010111100000000",
            "Octal": "0o13150057400",
        }
        display_value = self.converter.choose_display_value(
            formats_with_human, "decimal"
        )
        assert display_value == "1.5 billion"

        # Test without Human Readable format (smaller number)
        formats_no_human = {
            "Decimal": "255",
            "Hexadecimal": "0xff",
            "Binary": "0b11111111",
            "Octal": "0o377",
        }
        display_value = self.converter.choose_display_value(formats_no_human, "decimal")
        assert display_value is None  # Should return None when preferred format missing
