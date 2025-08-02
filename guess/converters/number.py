"""
Number base converter for decimal, hex, binary, and octal formats.
"""

import re
from typing import Dict, Any
from guess.converters.base import Converter


class NumberConverter(Converter):
    """Converts numbers between different bases."""

    def can_convert(self, input_str: str) -> bool:
        """Check if input is a valid number in any supported format."""
        cleaned = input_str.strip().lower()

        # Check in order of specificity to avoid conflicts

        # Binary (check before hex to avoid conflicts)
        if re.match(r"^-?0b[01]+$", cleaned):
            return True
        if re.match(r"^-?[01]+b$", cleaned):
            return True

        # Octal (check before hex to avoid conflicts)
        if re.match(r"^-?0o[0-7]+$", cleaned):
            return True
        if re.match(r"^-?[0-7]+o$", cleaned):
            return True

        # Hexadecimal
        if re.match(r"^-?0x[0-9a-f]+$", cleaned):
            return True
        if re.match(r"^-?#[0-9a-f]+$", cleaned):
            return True
        # Only accept plain hex if it contains a-f characters and doesn't end
        # with b or o
        if (
            re.match(r"^-?[0-9a-f]+$", cleaned)
            and any(c in cleaned for c in "abcdef")
            and not cleaned.endswith("b")
            and not cleaned.endswith("o")
            and not cleaned.startswith("0b")
            and not cleaned.startswith("-0b")
        ):
            return True

        # Decimal numbers (including negative and scientific notation)
        if re.match(r"^-?\d+$", cleaned):
            return True
        if re.match(r"^-?\d+\.\d+$", cleaned):
            return True
        if re.match(r"^-?\d+(?:\.\d+)?e[+-]?\d+$", cleaned):
            return True
        if re.match(r"^-?[0-7]+o$", cleaned):
            return True

        return False

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert number to different bases and formats."""
        try:
            cleaned = input_str.strip().lower()
            num = self._parse_number(cleaned)

            if num is None:
                return {}

            result = {}

            # Basic number formats
            if num >= 1_000_000:
                result["Decimal"] = f"{num:,}"
                result["Scientific"] = f"{num:.2e}"
            else:
                result["Decimal"] = str(num)

            # Only show other bases for integers
            if isinstance(num, int):
                result["Hexadecimal"] = (
                    f"0x{abs(num):x}" if num >= 0 else f"-0x{abs(num):x}"
                )
                result["Binary"] = f"0b{abs(num):b}" if num >= 0 else f"-0b{abs(num):b}"
                result["Octal"] = f"0o{abs(num):o}" if num >= 0 else f"-0o{abs(num):o}"

                # Special contexts for certain ranges
                if 0 <= num <= 255:
                    result["RGB Context"] = f"#{num:02x}{num:02x}{num:02x} (grayscale)"

                # File permissions for 3-digit numbers between 0-777
                if 0 <= num <= 777 and len(str(num)) == 3:
                    perm = self._octal_to_permissions(str(num))
                    result["File Permission"] = f"{num:03o} ({perm})"

            return result

        except (ValueError, TypeError):
            return {}

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

    def _octal_to_permissions(self, octal_str: str) -> str:
        """Convert 3-digit octal to rwx permissions."""
        if len(octal_str) != 3:
            return "invalid"

        def digit_to_rwx(digit):
            d = int(digit)
            r = "r" if d & 4 else "-"
            w = "w" if d & 2 else "-"
            x = "x" if d & 1 else "-"
            return r + w + x

        try:
            owner = digit_to_rwx(octal_str[0])
            group = digit_to_rwx(octal_str[1])
            other = digit_to_rwx(octal_str[2])
            return f"{owner}{group}{other}"
        except (ValueError, IndexError):
            return "invalid"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Number Base"
