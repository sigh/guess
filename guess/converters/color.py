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
        cleaned = input_str.strip()
        interpretations = []

        # Check for 6-digit hex color codes (#112233)
        if re.match(r"^#[0-9a-fA-F]{6}$", cleaned):
            try:
                r = int(cleaned[1:3], 16)
                g = int(cleaned[3:5], 16)
                b = int(cleaned[5:7], 16)
                interpretations.append(
                    Interpretation(description="hex", value=(r, g, b))
                )
            except ValueError:
                pass

        # Check for 3-digit hex color codes (#123)
        elif re.match(r"^#[0-9a-fA-F]{3}$", cleaned):
            try:
                r = int(cleaned[1] * 2, 16)  # "1" becomes "11"
                g = int(cleaned[2] * 2, 16)  # "2" becomes "22"
                b = int(cleaned[3] * 2, 16)  # "3" becomes "33"
                interpretations.append(
                    Interpretation(description="hex", value=(r, g, b))
                )
            except ValueError:
                pass

        # Check for color names
        elif cleaned.lower() in self.color_names:
            rgb = self.color_names[cleaned.lower()]
            interpretations.append(Interpretation(description="name", value=rgb))

        # Check for rgb() format with integers [0-255]
        elif re.match(r"^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$", cleaned):
            try:
                # Extract numbers from rgb(r, g, b)
                numbers = re.findall(r"\d+", cleaned)
                r, g, b = map(int, numbers)
                if all(0 <= val <= 255 for val in [r, g, b]):
                    interpretations.append(
                        Interpretation(description="rgb", value=(r, g, b))
                    )
            except (ValueError, IndexError):
                pass

        # Check for rgb() format with floats [0-1]
        elif re.match(
            r"^rgb\(\s*\d*\.?\d+\s*,\s*\d*\.?\d+\s*,\s*\d*\.?\d+\s*\)$", cleaned
        ):
            try:
                # Extract float numbers from rgb(r, g, b)
                numbers = re.findall(r"\d*\.?\d+", cleaned)
                r_f, g_f, b_f = map(float, numbers)
                if all(0.0 <= val <= 1.0 for val in [r_f, g_f, b_f]):
                    # Convert to 0-255 range, preserving precision
                    r = r_f * 255
                    g = g_f * 255
                    b = b_f * 255
                    interpretations.append(
                        Interpretation(description="rgb", value=(r, g, b))
                    )
            except (ValueError, IndexError):
                pass

        # Check for rgb() format with percentages [0-100%]
        elif re.match(r"^rgb\(\s*\d+%\s*,\s*\d+%\s*,\s*\d+%\s*\)$", cleaned):
            try:
                # Extract percentage numbers from rgb(r%, g%, b%)
                numbers = re.findall(r"\d+", cleaned)
                r_p, g_p, b_p = map(int, numbers)
                if all(0 <= val <= 100 for val in [r_p, g_p, b_p]):
                    # Convert to 0-255 range, preserving precision
                    r = r_p * 255 / 100
                    g = g_p * 255 / 100
                    b = b_p * 255 / 100
                    interpretations.append(
                        Interpretation(description="rgb", value=(r, g, b))
                    )
            except (ValueError, IndexError):
                pass

        # Check for hsl() format
        elif re.match(r"^hsl\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*\)$", cleaned):
            try:
                # Extract numbers from hsl(h, s%, l%)
                numbers = re.findall(r"\d+", cleaned)
                h, s, lightness = map(int, numbers)
                if 0 <= h <= 360 and 0 <= s <= 100 and 0 <= lightness <= 100:
                    r, g, b = self._hsl_to_rgb(h, s, lightness)
                    interpretations.append(
                        Interpretation(description="hsl", value=(r, g, b))
                    )
            except (ValueError, IndexError):
                pass

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a color value to various formats."""
        # Handle both integer and float RGB values
        if isinstance(value[0], (int, float)):
            r, g, b = value
        else:
            r, g, b = value

        # Generate output formats
        result = {}

        # Hex color code - round for display
        result["Hex"] = f"#{round(r):02x}{round(g):02x}{round(b):02x}"

        # RGB values - round for display
        result["RGB"] = f"rgb({round(r)}, {round(g)}, {round(b)})"

        # RGB percent values (0-100% range)
        result["RGB Percent"] = (
            f"rgb({round(r / 255 * 100)}%, {round(g / 255 * 100)}%, {round(b / 255 * 100)}%)"
        )

        # HSL values
        h, s, L = self._rgb_to_hsl(r, g, b)
        result["HSL"] = f"hsl({round(h)}, {round(s)}%, {round(L)}%)"

        # Colored square using xterm-256 colors
        result["Color Square"] = self._get_color_square(r, g, b)

        # Color name (if applicable) - only check rounded values
        rounded_rgb = (round(r), round(g), round(b))
        if rounded_rgb in self.rgb_to_name:
            result["Name"] = self.rgb_to_name[rounded_rgb]

        return result

    def _rgb_to_hsl(self, r, g, b):
        """Convert RGB to HSL, preserving precision."""
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

        # Return precise floating-point values
        return (h * 360, s * 100, L * 100)

    def _hsl_to_rgb(self, h: int, s: int, lightness: int):
        """Convert HSL to RGB."""
        h = h / 360.0
        s = s / 100.0
        lightness = lightness / 100.0

        if s == 0:
            # Achromatic (gray)
            r = g = b = lightness
        else:

            def hue_to_rgb(p, q, t):
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p

            q = (
                lightness * (1 + s)
                if lightness < 0.5
                else lightness + s - lightness * s
            )
            p = 2 * lightness - q
            r = hue_to_rgb(p, q, h + 1 / 3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1 / 3)

        return (r * 255, g * 255, b * 255)

    def _get_color_square(self, r, g, b):
        """Generate a colored square using xterm-256 colors."""
        # Round to integers for xterm color calculation
        r_int = round(r)
        g_int = round(g)
        b_int = round(b)

        # Convert RGB to xterm-256 color index
        # xterm-256 uses a 6x6x6 color cube for colors 16-231
        # Each component (R, G, B) is mapped to 0-5 range
        def rgb_to_xterm_component(val):
            if val < 48:
                return 0
            elif val < 115:
                return 1
            else:
                return min(5, (val - 35) // 40)

        r_xterm = rgb_to_xterm_component(r_int)
        g_xterm = rgb_to_xterm_component(g_int)
        b_xterm = rgb_to_xterm_component(b_int)

        # Calculate xterm-256 color index
        color_index = 16 + (36 * r_xterm) + (6 * g_xterm) + b_xterm

        # Create colored square using ANSI escape sequences
        # Use both foreground and background to create a solid square
        reset = "\033[0m"
        bg_color = f"\033[48;5;{color_index}m"
        return f"{bg_color}  {reset}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Color"

    def choose_display_value(
        self, formats: Dict[str, Any], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for color formats."""
        # Return color square + RGB for visual and textual representation
        if "Color Square" in formats and "RGB" in formats:
            return f"{formats['Color Square']} {formats['RGB']}"
        # Should always have both Color Square and RGB, so return None if not
        return None
