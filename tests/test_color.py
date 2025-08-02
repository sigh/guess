"""
Tests for the color converter.
"""

from guess.converters.color import ColorConverter


class TestColorConverter:
    """Test the color converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = ColorConverter()

    def test_get_interpretations_hex_color_codes(self):
        """Test that hex color codes are properly interpreted."""
        # Test standard hex color code
        interpretations = self.converter.get_interpretations("#FF0000")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (255, 0, 0)

        # Test lowercase hex
        interpretations = self.converter.get_interpretations("#ffffff")
        assert len(interpretations) == 1
        assert interpretations[0].description == "hex"
        assert interpretations[0].value == (255, 255, 255)

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

    def test_get_interpretations_rgb_values(self):
        """Test that RGB values return multiple interpretations."""
        # Test 255 - should give both red and grayscale interpretations
        interpretations = self.converter.get_interpretations("255")
        assert len(interpretations) == 2

        # Should have red interpretation
        red_interp = next((i for i in interpretations if i.description == "red"), None)
        assert red_interp is not None
        assert red_interp.value == (255, 0, 0)

        # Should have grayscale interpretation
        gray_interp = next(
            (i for i in interpretations if i.description == "grayscale"), None
        )
        assert gray_interp is not None
        assert gray_interp.value == (255, 255, 255)

        # Test 128 - should also give both interpretations
        interpretations = self.converter.get_interpretations("128")
        assert len(interpretations) == 2
        red_interp = next((i for i in interpretations if i.description == "red"), None)
        gray_interp = next(
            (i for i in interpretations if i.description == "grayscale"), None
        )
        assert red_interp.value == (128, 0, 0)
        assert gray_interp.value == (128, 128, 128)

    def test_get_interpretations_hex_values(self):
        """Test that hex values with 0x prefix are interpreted."""
        interpretations = self.converter.get_interpretations("0xFF")
        assert len(interpretations) == 2

        red_interp = next((i for i in interpretations if i.description == "red"), None)
        gray_interp = next(
            (i for i in interpretations if i.description == "grayscale"), None
        )
        assert red_interp.value == (255, 0, 0)
        assert gray_interp.value == (255, 255, 255)

    def test_get_interpretations_invalid_values(self):
        """Test that invalid values return no interpretations."""
        assert len(self.converter.get_interpretations("256")) == 0  # Out of RGB range
        assert len(self.converter.get_interpretations("-1")) == 0  # Negative
        assert len(self.converter.get_interpretations("#GG0000")) == 0  # Invalid hex
        assert (
            len(self.converter.get_interpretations("invalidcolor")) == 0
        )  # Unknown color name
        assert len(self.converter.get_interpretations("0x100")) == 0  # Out of RGB range
        assert len(self.converter.get_interpretations("")) == 0  # Empty input

    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        result = self.converter.convert_value((255, 0, 0))

        # Should always have these formats
        assert "Hex" in result
        assert "RGB" in result
        assert "HSL" in result

        # Check format correctness
        assert result["Hex"] == "#ff0000"
        assert result["RGB"] == "rgb(255, 0, 0)"
        assert result["HSL"] == "hsl(0, 100%, 50%)"

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

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Color"

    def test_choose_display_value(self):
        """Test display value selection."""
        # Test with Hex format present
        formats_with_hex = {
            "RGB": "rgb(255, 0, 0)",
            "Hex": "#FF0000",
            "HSL": "hsl(0, 100%, 50%)",
            "Name": "red",
        }
        display_value = self.converter.choose_display_value(formats_with_hex, "name")
        assert display_value == "#FF0000"

        # Test without Hex format
        formats_no_hex = {
            "RGB": "rgb(255, 0, 0)",
            "HSL": "hsl(0, 100%, 50%)",
            "Name": "red",
        }
        display_value = self.converter.choose_display_value(formats_no_hex, "name")
        assert display_value is None  # Should return None when preferred format missing
