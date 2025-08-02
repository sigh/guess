"""
Tests for the color converter.
"""

from guess.converters.color import ColorConverter


class TestColorConverter:
    """Test the color converter functionality."""

    def setup_method(self):
        """Se        # Test without Color Square format (should return None)
        formats_no_square = {
            "RGB": "rgb(255, 0, 0)",
            "Hex": "#FF0000",
            "HSL": "hsl(0, 100%, 50%)",
            "Name": "red",
        }
        display_value = self.converter.choose_display_value(formats_no_square, "name")
        assert display_value is None fixtures."""
        self.converter = ColorConverter()

    def test_get_interpretations_hex_color_codes(self):
        """Test that hex color codes are properly interpreted."""
        # Test standard 6-digit hex color code
        interpretations = self.converter.get_interpretations("#FF0000")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (255, 0, 0)

        # Test lowercase hex
        interpretations = self.converter.get_interpretations("#ffffff")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (255, 255, 255)

        # Test 3-digit hex color code
        interpretations = self.converter.get_interpretations("#F00")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (255, 0, 0)

        # Test 3-digit hex with mixed case
        interpretations = self.converter.get_interpretations("#abc")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (170, 187, 204)  # #aabbcc

    def test_get_interpretations_color_names(self):
        """Test that color names are properly interpreted."""
        interpretations = self.converter.get_interpretations("red")
        assert len(interpretations) == 1
        assert interpretations[0].description == "name"
        assert interpretations[0].value == (255, 0, 0)

        interpretations = self.converter.get_interpretations("white")
        assert len(interpretations) == 1
        assert interpretations[0].description == "name"
        assert interpretations[0].value == (255, 255, 255)

    def test_get_interpretations_rgb_formats(self):
        """Test that rgb() formats are properly interpreted."""
        # Test rgb() with integers [0-255]
        interpretations = self.converter.get_interpretations("rgb(255, 0, 0)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (255, 0, 0)

        # Test rgb() with spaces
        interpretations = self.converter.get_interpretations("rgb( 128 , 64 , 192 )")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (128, 64, 192)

        # Test rgb() with floats [0-1]
        interpretations = self.converter.get_interpretations("rgb(1.0, 0.0, 0.5)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (255.0, 0.0, 127.5)  # Preserve precision

        # Test rgb() with floats without leading zero
        interpretations = self.converter.get_interpretations("rgb(.5, .25, .75)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (127.5, 63.75, 191.25)  # Preserve precision

        # Test rgb() with percentages [0-100%]
        interpretations = self.converter.get_interpretations("rgb(100%, 0%, 50%)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (255.0, 0.0, 127.5)  # Preserve precision

        # Test rgb() with percentages and spaces
        interpretations = self.converter.get_interpretations("rgb( 50% , 25% , 75% )")
        assert len(interpretations) == 1
        assert interpretations[0].description == "rgb"
        assert interpretations[0].value == (127.5, 63.75, 191.25)  # Preserve precision

    def test_get_interpretations_hsl_format(self):
        """Test that hsl() format is properly interpreted."""
        # Test hsl() with percentages
        interpretations = self.converter.get_interpretations("hsl(0, 100%, 50%)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hsl"
        assert interpretations[0].value == (255, 0, 0)  # Red

        # Test hsl() without percentages
        interpretations = self.converter.get_interpretations("hsl(240, 100, 50)")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hsl"
        assert interpretations[0].value == (0, 0, 255)  # Blue

        # Test hsl() with spaces
        interpretations = self.converter.get_interpretations("hsl( 120 , 100% , 50% )")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hsl"
        assert interpretations[0].value == (0, 255, 0)  # Green

    def test_get_interpretations_invalid_values(self):
        """Test that invalid values return no interpretations."""
        assert len(self.converter.get_interpretations("")) == 0  # Empty input
        assert len(self.converter.get_interpretations("notacolor")) == 0  # Invalid name
        assert len(self.converter.get_interpretations("#GG0000")) == 0  # Invalid hex
        assert len(self.converter.get_interpretations("#FF00")) == 0  # Wrong hex length
        assert (
            len(self.converter.get_interpretations("#FF00000")) == 0
        )  # Wrong hex length
        assert len(self.converter.get_interpretations("255")) == 0  # No decimal values
        assert len(self.converter.get_interpretations("0xFF")) == 0  # No 0x prefix
        assert (
            len(self.converter.get_interpretations("rgb(256, 0, 0)")) == 0
        )  # Out of range
        assert (
            len(self.converter.get_interpretations("rgb(1.5, 0, 0)")) == 0
        )  # Float out of range
        assert (
            len(self.converter.get_interpretations("hsl(361, 50%, 50%)")) == 0
        )  # Hue out of range
        assert (
            len(self.converter.get_interpretations("hsl(0, 101%, 50%)")) == 0
        )  # Saturation out of range

    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        result = self.converter.convert_value((255, 0, 0))

        # Should always have these formats
        assert "Hex" in result
        assert "RGB" in result
        assert "RGB Percent" in result
        assert "HSL" in result
        assert "Color Square" in result

        # Check format correctness
        assert result["Hex"] == "#ff0000"
        assert result["RGB"] == "rgb(255, 0, 0)"
        assert result["RGB Percent"] == "rgb(100%, 0%, 0%)"
        assert result["HSL"] == "hsl(0, 100%, 50%)"
        # Color square should contain ANSI escape sequences
        assert "\033[" in result["Color Square"]
        assert "\033[0m" in result["Color Square"]

    def test_convert_value_with_color_name(self):
        """Test that known colors include their name."""
        result = self.converter.convert_value((255, 0, 0))
        assert "Name" in result
        assert result["Name"] == "red"

    def test_convert_value_without_color_name(self):
        """Test that unknown colors don't include a name."""
        result = self.converter.convert_value((123, 45, 67))
        assert "Name" not in result

    def test_convert_value_hsl_calculation(self):
        """Test HSL calculation for edge cases."""
        # Test achromatic colors (black, white, gray)
        result = self.converter.convert_value((0, 0, 0))
        assert "hsl(0, 0%, 0%)" in result["HSL"]

        result = self.converter.convert_value((255, 255, 255))
        assert "hsl(0, 0%, 100%)" in result["HSL"]

        # Test chromatic color
        result = self.converter.convert_value((0, 0, 255))
        assert "hsl(240, 100%, 50%)" in result["HSL"]

    def test_convert_value_rgb_percent_precision(self):
        """Test RGB percent output precision."""
        # Test precise float values
        result = self.converter.convert_value((127.5, 63.75, 191.25))
        assert result["RGB Percent"] == "rgb(50%, 25%, 75%)"

        # Test edge cases
        result = self.converter.convert_value((255.0, 0.0, 127.5))
        assert result["RGB Percent"] == "rgb(100%, 0%, 50%)"

        # Test small values
        result = self.converter.convert_value((2.55, 1.275, 0.0))
        assert result["RGB Percent"] == "rgb(1%, 0%, 0%)"

    def test_convert_value_color_square(self):
        """Test color square generation."""
        # Test basic colors
        result = self.converter.convert_value((255, 0, 0))
        square = result["Color Square"]
        assert "\033[48;5;" in square  # Should contain background color escape
        assert "\033[0m" in square  # Should contain reset escape

        # Test that different colors produce different squares
        result1 = self.converter.convert_value((255, 0, 0))
        result2 = self.converter.convert_value((0, 255, 0))
        assert result1["Color Square"] != result2["Color Square"]

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Color"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Color Square and RGB formats present
        formats_with_square = {
            "RGB": "rgb(255, 0, 0)",
            "Hex": "#FF0000",
            "HSL": "hsl(0, 100%, 50%)",
            "Color Square": "\033[48;5;196m  \033[0m",
            "Name": "red",
        }
        display_value = self.converter.choose_display_value(formats_with_square, "name")
        assert display_value == "\033[48;5;196m  \033[0m rgb(255, 0, 0)"

        # Test without Color Square format (should return None)
        formats_no_square = {
            "RGB": "rgb(255, 0, 0)",
            "Hex": "#FF0000",
            "HSL": "hsl(0, 100%, 50%)",
            "Name": "red",
        }
        display_value = self.converter.choose_display_value(formats_no_square, "name")
        assert display_value is None
