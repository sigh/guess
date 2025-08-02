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
        """Test that valid decimal numbers are recognized."""
        assert self.converter.can_convert("255")
        assert self.converter.can_convert("0")
        assert self.converter.can_convert("1234567890")
        assert self.converter.can_convert("  123  ")  # with whitespace
    
    def test_can_convert_invalid_inputs(self):
        """Test that invalid inputs are rejected."""
        assert not self.converter.can_convert("abc")
        assert not self.converter.can_convert("-123")  # negative numbers not supported yet
        assert not self.converter.can_convert("12.34")  # decimals not supported yet
        assert not self.converter.can_convert("")
        assert not self.converter.can_convert("0x1F")  # hex input not supported yet
    
    def test_convert_basic_numbers(self):
        """Test basic number conversion."""
        result = self.converter.convert("255")
        expected = {
            "Decimal": "255",
            "Hexadecimal": "0xff",
            "Binary": "0b11111111",
            "Octal": "0o377"
        }
        assert result == expected
    
    def test_convert_zero(self):
        """Test conversion of zero."""
        result = self.converter.convert("0")
        expected = {
            "Decimal": "0",
            "Hexadecimal": "0x0",
            "Binary": "0b0",
            "Octal": "0o0"
        }
        assert result == expected
    
    def test_convert_with_whitespace(self):
        """Test conversion with whitespace."""
        result = self.converter.convert("  42  ")
        expected = {
            "Decimal": "42",
            "Hexadecimal": "0x2a",
            "Binary": "0b101010",
            "Octal": "0o52"
        }
        assert result == expected
    
    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Number Base"


if __name__ == "__main__":
    pytest.main([__file__])
