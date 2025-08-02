"""
Color converter for RGB values, hex codes, and color names.
"""

import re
from typing import Dict, Any
from guess.converters.base import Converter


class ColorConverter(Converter):
    """Converts colors between different formats."""

    def __init__(self):
        # Basic color name mappings
        self.color_names = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "pink": (255, 192, 203),
            "brown": (165, 42, 42),
            "gray": (128, 128, 128),
            "grey": (128, 128, 128),
        }

        # Reverse mapping for RGB to name
        self.rgb_to_name = {v: k for k, v in self.color_names.items() if k != "grey"}

    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like a color."""
        cleaned = input_str.strip().lower()

        # Check for hex color codes (#FF0000, #00FF00, etc.)
        if re.match(r"^#[0-9a-f]{6}$", cleaned):
            return True

        # Check for color names
        if cleaned in self.color_names:
            return True

        # Check for RGB values (0-255 range)
        if cleaned.isdigit():
            value = int(cleaned)
            return 0 <= value <= 255

        # Check for hex values that could be RGB components
        if re.match(r"^0x[0-9a-f]+$", cleaned):
            try:
                value = int(cleaned, 16)
                return 0 <= value <= 255
            except ValueError:
                return False

        return False

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert color to various formats."""
        try:
            cleaned = input_str.strip().lower()

            # Parse input to get RGB values
            rgb = self._parse_color_input(cleaned)
            if rgb is None:
                return {}

            r, g, b = rgb

            # Generate output formats
            result = {}

            # Hex color code
            result["Hex"] = f"#{r:02x}{g:02x}{b:02x}"

            # RGB values
            result["RGB"] = f"rgb({r}, {g}, {b})"

            # HSL values
            h, s, l = self._rgb_to_hsl(r, g, b)
            result["HSL"] = f"hsl({h}, {s}%, {l}%)"

            # Color name (if applicable)
            if rgb in self.rgb_to_name:
                result["Name"] = self.rgb_to_name[rgb]

            return result

        except (ValueError, TypeError):
            return {}

    def _parse_color_input(self, input_str: str):
        """Parse color input to RGB tuple."""
        # Hex color code (#FF0000)
        if input_str.startswith("#") and len(input_str) == 7:
            try:
                r = int(input_str[1:3], 16)
                g = int(input_str[3:5], 16)
                b = int(input_str[5:7], 16)
                return (r, g, b)
            except ValueError:
                return None

        # Color name
        if input_str in self.color_names:
            return self.color_names[input_str]

        # RGB value (assume grayscale)
        if input_str.isdigit():
            value = int(input_str)
            if 0 <= value <= 255:
                return (value, value, value)

        # Hex value (0xFF)
        if input_str.startswith("0x"):
            try:
                value = int(input_str, 16)
                if 0 <= value <= 255:
                    return (value, value, value)
            except ValueError:
                return None

        return None

    def _rgb_to_hsl(self, r: int, g: int, b: int):
        """Convert RGB to HSL."""
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val

        # Lightness
        l = (max_val + min_val) / 2

        if diff == 0:
            h = s = 0  # achromatic
        else:
            # Saturation
            s = (
                diff / (2 - max_val - min_val)
                if l > 0.5
                else diff / (max_val + min_val)
            )

            # Hue
            if max_val == r:
                h = (g - b) / diff + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / diff + 2
            elif max_val == b:
                h = (r - g) / diff + 4
            h /= 6

        return (int(h * 360), int(s * 100), int(l * 100))

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Color"
