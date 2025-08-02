"""
Tests for the color converter.
"""

import pytest
from guess.converters.color import ColorConverter


class TestColorConverter:
    """Test the color converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = ColorConverter()

    def test_can_convert_hex_color_codes(self):
        """Test detection of hex color codes."""
        assert self.converter.can_convert("#FF0000")
        assert self.converter.can_convert("#00FF00")
        assert self.converter.can_convert("#0000FF")
        assert self.converter.can_convert("#ffffff")
        assert self.converter.can_convert("#000000")

    def test_can_convert_color_names(self):
        """Test detection of color names."""
        assert self.converter.can_convert("red")
        assert self.converter.can_convert("blue")
        assert self.converter.can_convert("green")
        assert self.converter.can_convert("white")
        assert self.converter.can_convert("black")

    def test_can_convert_rgb_values(self):
        """Test detection of RGB values (0-255)."""
        assert self.converter.can_convert("255")
        assert self.converter.can_convert("128")
        assert self.converter.can_convert("0")
        assert self.converter.can_convert("0xFF")

    def test_cannot_convert_invalid_values(self):
        """Test rejection of invalid color values."""
        assert not self.converter.can_convert("256")  # Out of RGB range
        assert not self.converter.can_convert("-1")  # Negative
        assert not self.converter.can_convert("#GG0000")  # Invalid hex
        assert not self.converter.can_convert("invalidcolor")  # Unknown color name
        assert not self.converter.can_convert("0x100")  # Out of RGB range

    def test_convert_hex_color_code(self):
        """Test conversion of hex color codes."""
        result = self.converter.convert("#FF0000")

        assert "Hex" in result
        assert "RGB" in result
        assert "HSL" in result
        assert result["Hex"] == "#ff0000"
        assert result["RGB"] == "rgb(255, 0, 0)"
        assert "Name" in result
        assert result["Name"] == "red"

    def test_convert_color_name(self):
        """Test conversion of color names."""
        result = self.converter.convert("red")

        assert "Hex" in result
        assert "RGB" in result
        assert "HSL" in result
        assert result["Hex"] == "#ff0000"
        assert result["RGB"] == "rgb(255, 0, 0)"
        assert result["Name"] == "red"

    def test_convert_rgb_value_grayscale(self):
        """Test conversion of RGB values (grayscale)."""
        result = self.converter.convert("128")

        assert "Hex" in result
        assert "RGB" in result
        assert "HSL" in result
        assert result["Hex"] == "#808080"
        assert result["RGB"] == "rgb(128, 128, 128)"

    def test_convert_white_color(self):
        """Test conversion of white color."""
        result = self.converter.convert("255")

        assert result["Hex"] == "#ffffff"
        assert result["RGB"] == "rgb(255, 255, 255)"
        assert result["Name"] == "white"

    def test_convert_black_color(self):
        """Test conversion of black color."""
        result = self.converter.convert("0")

        assert result["Hex"] == "#000000"
        assert result["RGB"] == "rgb(0, 0, 0)"
        assert result["Name"] == "black"

    def test_hsl_conversion(self):
        """Test HSL color conversion."""
        # Test pure red
        result = self.converter.convert("#FF0000")
        assert "hsl(0, 100%, 50%)" in result["HSL"]

        # Test pure blue
        result = self.converter.convert("#0000FF")
        assert "hsl(240, 100%, 50%)" in result["HSL"]

    def test_hex_value_input(self):
        """Test hex value input (0xFF format)."""
        result = self.converter.convert("0xFF")

        assert "Hex" in result
        assert result["Hex"] == "#ffffff"  # Grayscale 255,255,255
        assert result["RGB"] == "rgb(255, 255, 255)"

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Color"

    def test_empty_input(self):
        """Test handling of empty input."""
        result = self.converter.convert("")
        assert result == {}

    def test_invalid_input(self):
        """Test handling of invalid input."""
        result = self.converter.convert("notacolor")
        assert result == {}
