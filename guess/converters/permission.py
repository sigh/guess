"""
File permission converter for octal and symbolic notation.
"""

import re
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation


class PermissionConverter(Converter):
    """Converts file permissions between different formats."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as file permissions."""
        cleaned = input_str.strip()
        interpretations = []

        # Check for octal permissions (755, 0755, 0o755, etc.)
        if re.match(r"^0?[0-7]{3,4}$", cleaned) or cleaned.startswith("0o"):
            try:
                if cleaned.startswith("0o"):
                    # Python octal notation
                    octal_value = int(cleaned, 8)
                elif cleaned.startswith("0"):
                    # Traditional octal notation
                    octal_value = int(cleaned, 8)
                else:
                    # Interpret non-prefixed 3-digit numbers as octal
                    octal_value = int(cleaned, 8)

                if 0 <= octal_value <= 511:  # 0777 in octal = 511 in decimal
                    interpretations.append(
                        Interpretation(description="octal", value=octal_value)
                    )
            except ValueError:
                pass

        # Check for symbolic permissions (rwxr-xr-x)
        elif re.match(r"^[rwx-]{9}$", cleaned):
            try:
                octal_value = self._symbolic_to_octal(cleaned)
                if octal_value is not None:
                    interpretations.append(
                        Interpretation(description="string", value=octal_value)
                    )
            except ValueError:
                pass

        # Check for decimal values that could be permissions
        elif cleaned.isdigit():
            value = int(cleaned)
            if 0 <= value <= 511:
                interpretations.append(
                    Interpretation(description="decimal", value=value)
                )

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a permission value to various formats."""
        octal_value = value

        # Generate output formats
        result = {}

        # Symbolic notation
        result["Symbolic"] = self._octal_to_symbolic(octal_value)

        # Octal notation
        result["Octal"] = f"0o{octal_value:03o}"

        # Decimal equivalent
        result["Decimal"] = str(octal_value)

        # Permission breakdown
        result["Breakdown"] = self._format_breakdown(octal_value)

        return result

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

    def _format_breakdown(self, octal_value: int) -> str:
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

    def _octal_to_symbolic(self, octal_value: int) -> str:
        """Convert octal permission to symbolic notation."""
        symbolic = ""
        for shift in [6, 3, 0]:  # owner, group, other
            digit = (octal_value >> shift) & 7
            symbolic += "r" if digit & 4 else "-"
            symbolic += "w" if digit & 2 else "-"
            symbolic += "x" if digit & 1 else "-"
        return symbolic

    def _symbolic_to_octal(self, symbolic: str) -> int:
        """Convert symbolic permission to octal value."""
        if len(symbolic) != 9:
            return None

        octal_value = 0
        for i in range(3):  # owner, group, other
            section = symbolic[i * 3 : (i + 1) * 3]
            digit = 0
            if section[0] == "r":
                digit |= 4
            if section[1] == "w":
                digit |= 2
            if section[2] == "x":
                digit |= 1
            octal_value |= digit << (6 - i * 3)

        return octal_value

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Permission"

    def choose_display_value(
        self, formats: Dict[str, Any], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for permission formats."""
        # Prefer symbolic format as it's more intuitive
        return formats.get("Symbolic")
