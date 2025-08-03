"""
Color converter for RGB values, hex codes, and color names.

This module implements color conversion algorithms based on established standards:
- CSS Color Module Level 3: https://www.w3.org/TR/css-color-3/
- sRGB Color Space: IEC 61966-2-1:1999
- CIE Colorimetry Standards: CIE 15:2004
- ANSI Escape Codes: ECMA-48 Standard
"""

import re
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation
from guess.css_colors import CSS_COLORS


class ColorConverter(Converter):
    """Converts colors between different formats."""

    def __init__(self):
        # Use CSS color names from W3C CSS Color Module Level 3 specification
        self.color_names = CSS_COLORS

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

        # Check for color names (normalize by removing spaces and converting to lowercase)
        elif self._normalize_color_name(cleaned) in self.color_names:
            rgb = self.color_names[self._normalize_color_name(cleaned)]
            interpretations.append(Interpretation(description="css name", value=rgb))

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

    def _normalize_color_name(self, name: str) -> str:
        """Normalize color name by removing spaces and converting to lowercase."""
        return name.replace(" ", "").lower()

    def _find_color_name(self, r: float, g: float, b: float) -> str:
        """Find color name for RGB values, preferring certain names over others."""
        rounded_rgb = (round(r), round(g), round(b))
        for name, rgb in self.color_names.items():
            if rgb == rounded_rgb and not name.endswith("grey") and name != "aqua":
                return name
        return None

    def _rgb_to_xyz(self, r: int, g: int, b: int) -> tuple:
        """Convert RGB to XYZ color space (intermediate step for CIELAB).

        References:
        - http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
        - https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
        - IEC 61966-2-1:1999 standard (sRGB color space)
        """
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        # Apply gamma correction (sRGB gamma function)
        # Reference: https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
        r_norm = ((r_norm + 0.055) / 1.055) ** 2.4 if r_norm > 0.04045 else r_norm / 12.92
        g_norm = ((g_norm + 0.055) / 1.055) ** 2.4 if g_norm > 0.04045 else g_norm / 12.92
        b_norm = ((b_norm + 0.055) / 1.055) ** 2.4 if b_norm > 0.04045 else b_norm / 12.92

        r_norm *= 100
        g_norm *= 100
        b_norm *= 100

        # Convert to XYZ using D65 observer at 2° (sRGB transformation matrix)
        # Reference: http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
        x = r_norm * 0.4124564 + g_norm * 0.3575761 + b_norm * 0.1804375
        y = r_norm * 0.2126729 + g_norm * 0.7151522 + b_norm * 0.0721750
        z = r_norm * 0.0193339 + g_norm * 0.1191920 + b_norm * 0.9503041

        return (x, y, z)

    def _xyz_to_lab(self, x: float, y: float, z: float) -> tuple:
        """Convert XYZ to CIELAB color space.

        References:
        - http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html
        - https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIEXYZ_to_CIELAB
        - CIE 15:2004 Colorimetry standard
        """
        # D65 reference white (CIE standard illuminant)
        # Reference: https://en.wikipedia.org/wiki/Illuminant_D65
        ref_x = 95.047
        ref_y = 100.000
        ref_z = 108.883

        x_norm = x / ref_x
        y_norm = y / ref_y
        z_norm = z / ref_z

        # CIE LAB conversion threshold and formula
        # Reference: http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html
        threshold = 0.008856
        x_norm = x_norm ** (1/3) if x_norm > threshold else (7.787 * x_norm) + 16/116
        y_norm = y_norm ** (1/3) if y_norm > threshold else (7.787 * y_norm) + 16/116
        z_norm = z_norm ** (1/3) if z_norm > threshold else (7.787 * z_norm) + 16/116

        L = (116 * y_norm) - 16
        a = 500 * (x_norm - y_norm)
        b = 200 * (y_norm - z_norm)

        return (L, a, b)

    def _rgb_to_lab(self, r: int, g: int, b: int) -> tuple:
        """Convert RGB to CIELAB color space."""
        xyz = self._rgb_to_xyz(r, g, b)
        return self._xyz_to_lab(*xyz)

    def _color_distance2(self, lab1: tuple, lab2: tuple) -> float:
        """Calculate perceptual distance between two LAB colors using Delta E* (1976).
        References:

        - https://en.wikipedia.org/wiki/Color_difference#CIE76
        - http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CIE76.html
        """
        delta_L = lab1[0] - lab2[0]
        delta_a = lab1[1] - lab2[1]
        delta_b = lab1[2] - lab2[2]

        # Return squared distance (no need for sqrt when just comparing magnitudes)
        return delta_L ** 2 + delta_a ** 2 + delta_b ** 2

    def _find_closest_color(self, r: float, g: float, b: float) -> str:
        """Find the closest CSS color name using perceptual distance in CIELAB color space.

        References:
        - https://en.wikipedia.org/wiki/Color_difference
        - http://www.brucelindbloom.com/index.html?ColorDifferenceCalc.html
        """
        # Convert target color to LAB space once
        target_lab = self._rgb_to_lab(round(r), round(g), round(b))

        min_distance = float('inf')
        closest_color = None

        for name, rgb in self.color_names.items():
            # Skip colors we don't want to suggest
            if name.endswith("grey") or name == "aqua":
                continue

            # Convert color to LAB space
            color_lab = self._rgb_to_lab(*rgb)

            distance = self._color_distance2(target_lab, color_lab)
            if distance < min_distance:
                min_distance = distance
                closest_color = name

        return closest_color

    def convert_value(self, value: Any) -> Dict[str, str]:
        """Convert a color value to various formats."""
        # Handle both integer and float RGB values
        if isinstance(value[0], (int, float)):
            r, g, b = value
        else:
            r, g, b = value

        # Generate output formats
        result = {}

        # RGB values - round for display with color square
        color_square = self._get_color_square(r, g, b)
        result["RGB"] = f"{color_square} rgb({round(r)}, {round(g)}, {round(b)})"

        # RGB percent values (0-100% range)
        result["RGB Percent"] = (
            f"rgb({round(r / 255 * 100)}%, {round(g / 255 * 100)}%, {round(b / 255 * 100)}%)"
        )

        # HSL values
        h, s, L = self._rgb_to_hsl(r, g, b)
        result["HSL"] = f"hsl({round(h)}, {round(s)}%, {round(L)}%)"

        # Hex color code - round for display
        result["Hex"] = f"#{round(r):02x}{round(g):02x}{round(b):02x}"

        # Color name (if applicable)
        color_name = self._find_color_name(r, g, b)
        if color_name:
            result["Name"] = f"{color_name} (css color)"
        else:
            # If no exact match, find the closest color
            closest_color = self._find_closest_color(r, g, b)
            if closest_color:
                result["Closest Color"] = f"{closest_color} (approximate css color)"

        return result

    def _rgb_to_hsl(self, r, g, b):
        """Convert RGB to HSL, preserving precision.

        References:
        - https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
        - https://www.w3.org/TR/css-color-3/#hsl-color
        """
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
        """Convert HSL to RGB.

        References:
        - https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB
        - https://www.w3.org/TR/css-color-3/#hsl-color
        """
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
        """Generate a colored square using truecolor (24-bit) ANSI escape sequences.

        References:
        - https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
        - https://github.com/termstandard/colors
        """
        # Round to integers for RGB values
        r_int = max(0, min(255, round(r)))
        g_int = max(0, min(255, round(g)))
        b_int = max(0, min(255, round(b)))

        # Create colored square using truecolor ANSI escape sequences
        # Format: \033[48;2;r;g;bm for background color
        reset = "\033[0m"
        bg_color = f"\033[48;2;{r_int};{g_int};{b_int}m"
        return f"{bg_color}  {reset}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Color"

    def choose_display_value(
        self, formats: Dict[str, str], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for color formats."""
        return formats.get("RGB")
