"""
Tests for the number converter.
"""

import pytest
from guess.converters.number import NumberConverter


class TestNumberConverter:
    """Test cases for NumberConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = NumberConverter()

    def test_can_convert_valid_numbers(self):
        """Test that valid numbers are recognized."""
        # Decimal numbers
        assert self.converter.can_convert("255")
        assert self.converter.can_convert("0")
        assert self.converter.can_convert("1234567890")
        assert self.converter.can_convert("  123  ")  # with whitespace

        # Hexadecimal numbers
        assert self.converter.can_convert("0xFF")
        assert self.converter.can_convert("abc")  # hex without prefix
        assert self.converter.can_convert("#FF")

        # Binary numbers
        assert self.converter.can_convert("0b101010")
        assert self.converter.can_convert("101010b")

        # Octal numbers
        assert self.converter.can_convert("0o777")
        assert self.converter.can_convert("777o")

        # Negative numbers
        assert self.converter.can_convert("-123")

        # Scientific notation
        assert self.converter.can_convert("1.5e9")

    def test_can_convert_invalid_inputs(self):
        """Test that invalid inputs are rejected."""
        assert not self.converter.can_convert("")
        assert not self.converter.can_convert("xyz")  # invalid hex
        assert not self.converter.can_convert("12g34")  # invalid mixed format
        assert not self.converter.can_convert("0b12345")  # invalid binary

    def test_convert_basic_numbers(self):
        """Test basic number conversion."""
        result = self.converter.convert("255")
        expected_keys = {
            "Decimal",
            "Hexadecimal",
            "Binary",
            "Octal",
        }
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "255"
        assert result["Hexadecimal"] == "0xff"
        assert result["Binary"] == "0b11111111"
        assert result["Octal"] == "0o377"

    def test_convert_zero(self):
        """Test conversion of zero."""
        result = self.converter.convert("0")
        expected_keys = {"Decimal", "Hexadecimal", "Binary", "Octal"}
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "0"
        assert result["Hexadecimal"] == "0x0"
        assert result["Binary"] == "0b0"
        assert result["Octal"] == "0o0"

    def test_convert_with_whitespace(self):
        """Test conversion with whitespace."""
        result = self.converter.convert("  42  ")
        expected_keys = {"Decimal", "Hexadecimal", "Binary", "Octal"}
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "42"
        assert result["Hexadecimal"] == "0x2a"
        assert result["Binary"] == "0b101010"
        assert result["Octal"] == "0o52"

    def test_convert_hex_input(self):
        """Test conversion of hexadecimal input."""
        result = self.converter.convert("0xFF")
        assert result["Decimal"] == "255"
        assert result["Hexadecimal"] == "0xff"

    def test_convert_large_number(self):
        """Test conversion of large numbers with scientific notation."""
        result = self.converter.convert("1500000000")
        expected_keys = {
            "Decimal",
            "Scientific",
            "Hexadecimal",
            "Binary",
            "Octal",
            "Human Readable",
        }
        assert set(result.keys()) == expected_keys
        assert result["Decimal"] == "1,500,000,000"
        assert result["Scientific"] == "1.50e+09"

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Number Base"


if __name__ == "__main__":
    pytest.main([__file__])
