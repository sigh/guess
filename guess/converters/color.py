"""
Color converter for RGB values, hex codes, and color names.
"""

import re
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation


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

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a color."""
        cleaned = input_str.strip().lower()
        interpretations = []

        # Check for hex color codes
        if re.match(r"^#[0-9a-f]{6}$", cleaned):
            try:
                r = int(cleaned[1:3], 16)
                g = int(cleaned[3:5], 16)
                b = int(cleaned[5:7], 16)
                interpretations.append(
                    Interpretation(description="hex", value=(r, g, b))
                )
            except ValueError:
                pass

        # Check for color names
        elif cleaned in self.color_names:
            rgb = self.color_names[cleaned]
            interpretations.append(Interpretation(description="name", value=rgb))

        # Check for hex values (0xFF, 0xff)
        elif cleaned.startswith("0x"):
            try:
                value = int(cleaned, 16)
                if 0 <= value <= 255:
                    interpretations.append(
                        Interpretation(description="red", value=(value, 0, 0))
                    )
                    interpretations.append(
                        Interpretation(
                            description="grayscale", value=(value, value, value)
                        )
                    )
            except ValueError:
                pass

        # Check for RGB component values (0-255)
        elif cleaned.isdigit():
            value = int(cleaned)
            if 0 <= value <= 255:
                # When used with explicit color command, treat as red component
                interpretations.append(
                    Interpretation(description="red", value=(value, 0, 0))
                )
                # Also include grayscale interpretation
                interpretations.append(
                    Interpretation(description="grayscale", value=(value, value, value))
                )

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a color value to various formats."""
        r, g, b = value

        # Generate output formats
        result = {}

        # Hex color code
        result["Hex"] = f"#{r:02x}{g:02x}{b:02x}"

        # RGB values
        result["RGB"] = f"rgb({r}, {g}, {b})"

        # HSL values
        h, s, L = self._rgb_to_hsl(r, g, b)
        result["HSL"] = f"hsl({h}, {s}%, {L}%)"

        # Color name (if applicable)
        if (r, g, b) in self.rgb_to_name:
            result["Name"] = self.rgb_to_name[(r, g, b)]

        return result

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
        L = (max_val + min_val) / 2

        if diff == 0:
            h = s = 0  # achromatic
        else:
            # Saturation
            s = (
                diff / (2 - max_val - min_val)
                if L > 0.5
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

        return (int(h * 360), int(s * 100), int(L * 100))

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Color"

    def choose_display_value(
        self, formats: Dict[str, Any], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for color formats."""
        # Prefer hex format as it's most commonly used for colors
        return formats.get("Hex")
