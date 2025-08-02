"""
File permission converter for octal and symbolic notation.
"""

import re
from typing import Dict, Any
from guess.converters.base import Converter


class PermissionConverter(Converter):
    """Converts file permissions between different formats."""

    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like file permissions."""
        cleaned = input_str.strip()

        # Check for octal notation (755, 0755, 0o755)
        if re.match(r"^0?o?[0-7]{3}$", cleaned):
            return True

        # Check for symbolic notation (rwxr-xr-x)
        if re.match(r"^[r-][w-][x-][r-][w-][x-][r-][w-][x-]$", cleaned):
            return True

        # Check for decimal equivalent (493 for 755)
        if cleaned.isdigit():
            value = int(cleaned)
            # Common permission range (0-777 in octal = 0-511 in decimal)
            if 0 <= value <= 511:
                return True

        return False

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert file permissions to various formats."""
        try:
            cleaned = input_str.strip()

            # Parse input to get octal value
            octal_value = self._parse_permission_input(cleaned)
            if octal_value is None:
                return {}

            # Generate output formats
            result = {}

            # Symbolic notation
            result["Symbolic"] = self._octal_to_symbolic(octal_value)

            # Octal notation
            result["Octal"] = f"0o{octal_value:03o}"

            # Decimal equivalent
            result["Decimal"] = str(octal_value)

            # Permission breakdown
            result["Breakdown"] = self._format_permission_breakdown(octal_value)

            return result

        except (ValueError, TypeError):
            return {}

    def _parse_permission_input(self, input_str: str):
        """Parse permission input to octal integer."""
        # Symbolic notation (rwxr-xr-x)
        if len(input_str) == 9 and all(c in "rwx-" for c in input_str):
            return self._symbolic_to_octal(input_str)

        # Octal notation variations
        if input_str.startswith("0o"):
            # 0o755 format
            try:
                return int(input_str[2:], 8)
            except ValueError:
                return None
        elif input_str.startswith("0") and len(input_str) == 4:
            # 0755 format
            try:
                return int(input_str[1:], 8)
            except ValueError:
                return None
        elif len(input_str) == 3 and all(d in "01234567" for d in input_str):
            # 755 format
            try:
                return int(input_str, 8)
            except ValueError:
                return None
        elif input_str.isdigit():
            # Decimal format
            value = int(input_str)
            if 0 <= value <= 511:  # 777 octal = 511 decimal
                return value

        return None

    def _symbolic_to_octal(self, symbolic: str) -> int:
        """Convert symbolic notation to octal."""

        def triplet_to_octal(triplet):
            value = 0
            if triplet[0] == "r":
                value += 4
            if triplet[1] == "w":
                value += 2
            if triplet[2] == "x":
                value += 1
            return value

        owner = triplet_to_octal(symbolic[0:3])
        group = triplet_to_octal(symbolic[3:6])
        other = triplet_to_octal(symbolic[6:9])

        return owner * 64 + group * 8 + other

    def _octal_to_symbolic(self, octal_value: int) -> str:
        """Convert octal to symbolic notation."""

        def digit_to_rwx(digit):
            r = "r" if digit & 4 else "-"
            w = "w" if digit & 2 else "-"
            x = "x" if digit & 1 else "-"
            return r + w + x

        # Extract individual digits
        owner = (octal_value >> 6) & 7
        group = (octal_value >> 3) & 7
        other = octal_value & 7

        return digit_to_rwx(owner) + digit_to_rwx(group) + digit_to_rwx(other)

    def _format_permission_breakdown(self, octal_value: int) -> str:
        """Format permission breakdown."""

        def digit_to_description(digit):
            perms = []
            if digit & 4:
                perms.append("read")
            if digit & 2:
                perms.append("write")
            if digit & 1:
                perms.append("execute")
            return ", ".join(perms) if perms else "none"

        owner = (octal_value >> 6) & 7
        group = (octal_value >> 3) & 7
        other = octal_value & 7

        return f"owner: {digit_to_description(owner)}, group: {digit_to_description(group)}, others: {digit_to_description(other)}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Permission"
