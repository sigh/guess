"""
Number base converter for decimal, hex, binary, and octal formats.
"""

import re
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation


class NumberConverter(Converter):
    """Converts numbers between different bases."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a number."""
        cleaned = input_str.strip().lower()
        interpretations = []

        # Try different number format interpretations in order of specificity

        # Scientific notation
        if "e" in cleaned and re.match(r"^-?\d+(?:\.\d+)?e[+-]?\d+$", cleaned):
            try:
                value = float(cleaned)
                interpretations.append(
                    Interpretation(description="scientific", value=value)
                )
            except ValueError:
                pass

        # Hexadecimal patterns
        if cleaned.startswith("0x") and re.match(r"^-?0x[0-9a-f]+$", cleaned):
            try:
                value = int(cleaned, 16)
                interpretations.append(Interpretation(description="hex", value=value))
            except ValueError:
                pass
        elif (
            re.match(r"^-?[0-9a-f]+$", cleaned)
            and any(c in cleaned for c in "abcdef")
            and not cleaned.endswith("b")
            and not cleaned.endswith("o")
            and not cleaned.startswith("0b")
            and not cleaned.startswith("0o")
        ):
            try:
                value = int(cleaned, 16)
                interpretations.append(Interpretation(description="hex", value=value))
            except ValueError:
                pass

        # Binary patterns
        if cleaned.startswith("0b") and re.match(r"^-?0b[01]+$", cleaned):
            try:
                value = int(cleaned, 2)
                interpretations.append(
                    Interpretation(description="binary", value=value)
                )
            except ValueError:
                pass
        elif cleaned.endswith("b") and re.match(r"^-?[01]+b$", cleaned):
            try:
                value = int(cleaned[:-1], 2)
                interpretations.append(
                    Interpretation(description="binary", value=value)
                )
            except ValueError:
                pass

        # Octal patterns
        if cleaned.startswith("0o") and re.match(r"^-?0o[0-7]+$", cleaned):
            try:
                value = int(cleaned, 8)
                interpretations.append(Interpretation(description="octal", value=value))
            except ValueError:
                pass
        elif cleaned.endswith("o") and re.match(r"^-?[0-7]+o$", cleaned):
            try:
                value = int(cleaned[:-1], 8)
                interpretations.append(Interpretation(description="octal", value=value))
            except ValueError:
                pass

        # Decimal patterns
        if re.match(r"^-?\d+\.\d+$", cleaned):
            try:
                value = float(cleaned)
                interpretations.append(
                    Interpretation(description="decimal", value=value)
                )
            except ValueError:
                pass
        elif re.match(r"^-?\d+$", cleaned):
            try:
                value = int(cleaned)
                interpretations.append(
                    Interpretation(description="decimal", value=value)
                )
            except ValueError:
                pass

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, str]:
        """Convert a number value to various formats."""
        result = {}

        # Basic number formats
        if value >= 1_000_000:
            result["Decimal"] = str(value)
            result["Scientific"] = f"{value:.2e}"
            # Add human readable format for large numbers
            human_readable = self._format_human_readable(value)
            if human_readable:
                result["Human Readable"] = human_readable
        else:
            result["Decimal"] = str(value)
            # Add human readable for smaller numbers too if applicable
            if isinstance(value, int) and value >= 100_000:
                human_readable = self._format_human_readable(value)
                if human_readable:
                    result["Human Readable"] = human_readable

        # Only show other bases for integers
        if isinstance(value, int):
            result["Hexadecimal"] = (
                f"0x{abs(value):x}" if value >= 0 else f"-0x{abs(value):x}"
            )
            result["Binary"] = (
                f"0b{abs(value):b}" if value >= 0 else f"-0b{abs(value):b}"
            )
            result["Octal"] = (
                f"0o{abs(value):o}" if value >= 0 else f"-0o{abs(value):o}"
            )

        return result

    def _parse_number(self, input_str: str):
        """Parse number from various formats."""
        try:
            # Scientific notation
            if "e" in input_str:
                return float(input_str)

            # Hexadecimal
            if input_str.startswith("0x"):
                return int(input_str, 16)
            elif input_str.startswith("#"):
                return int(input_str[1:], 16)
            elif (
                any(c in input_str for c in "abcdef")
                and not input_str.endswith("b")
                and not input_str.endswith("o")
                and not input_str.startswith("0b")
            ):
                return int(input_str, 16)

            # Binary
            elif input_str.startswith("0b"):
                return int(input_str, 2)
            elif input_str.endswith("b") and all(c in "01" for c in input_str[:-1]):
                return int(input_str[:-1], 2)

            # Octal
            elif input_str.startswith("0o"):
                return int(input_str, 8)
            elif input_str.endswith("o") and all(
                c in "01234567" for c in input_str[:-1]
            ):
                return int(input_str[:-1], 8)

            # Decimal (int or float)
            elif "." in input_str:
                return float(input_str)
            else:
                return int(input_str)

        except ValueError:
            return None

    def _format_human_readable(self, num: float) -> str:
        """Format number in human readable form (million, billion, etc.)."""
        # Support range 100,000 to 1,000,000,000,000,000 (0.1 million to 1000 quadrillion)
        abs_num = abs(num)

        if abs_num < 100_000:
            return None
        elif abs_num >= 1_000_000_000_000_000:  # 1 quadrillion or more
            return None
        elif abs_num >= 1_000_000_000_000:  # trillion
            value = num / 1_000_000_000_000
            unit = "trillion"
        elif abs_num >= 1_000_000_000:  # billion
            value = num / 1_000_000_000
            unit = "billion"
        elif abs_num >= 1_000_000:  # million
            value = num / 1_000_000
            unit = "million"
        else:
            return None

        # Format with appropriate precision
        if value == int(value):
            return f"{int(value)} {unit}"
        elif abs(value - round(value, 1)) < 0.001:
            return f"{value:.1f} {unit}"
        else:
            return f"{value:.2f} {unit}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Number"

    def choose_display_value(
        self, formats: Dict[str, str], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for number formats."""
        # Prefer human readable for large numbers
        return formats.get("Human Readable")
