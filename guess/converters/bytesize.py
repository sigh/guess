"""
Byte size converter for data storage units.
"""

import re
from typing import Dict, Any
from guess.converters.base import Converter


class ByteSizeConverter(Converter):
    """Converts byte sizes between different units."""

    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like a byte size."""
        cleaned = input_str.strip().lower()

        # Check for pure numbers (assume bytes if large enough)
        if cleaned.isdigit():
            size = int(cleaned)
            # Consider it bytes if it's >= 1024 (1 KB)
            return size >= 1024

        # Check for unit-based input (1GB, 512MB, 2.5GiB, etc.)
        pattern = r"^\d+(?:\.\d+)?\s*([kmgt]?i?b)$"
        return bool(re.match(pattern, cleaned))

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert byte size to various units."""
        try:
            cleaned = input_str.strip().lower()

            if cleaned.isdigit():
                total_bytes = int(cleaned)
            else:
                # Parse unit-based input
                total_bytes = self._parse_byte_units(cleaned)
                if total_bytes is None:
                    return {}

            # Decimal (1000-based) units
            decimal_units = []
            if total_bytes >= 1000**4:
                decimal_units.append(f"{total_bytes / 1000**4:.2f} TB")
            if total_bytes >= 1000**3:
                decimal_units.append(f"{total_bytes / 1000**3:.2f} GB")
            if total_bytes >= 1000**2:
                decimal_units.append(f"{total_bytes / 1000**2:.2f} MB")
            if total_bytes >= 1000:
                decimal_units.append(f"{total_bytes / 1000:.2f} KB")

            # Binary (1024-based) units
            binary_units = []
            if total_bytes >= 1024**4:
                binary_units.append(f"{total_bytes / 1024**4:.2f} TiB")
            if total_bytes >= 1024**3:
                binary_units.append(f"{total_bytes / 1024**3:.2f} GiB")
            if total_bytes >= 1024**2:
                binary_units.append(f"{total_bytes / 1024**2:.2f} MiB")
            if total_bytes >= 1024:
                binary_units.append(f"{total_bytes / 1024:.2f} KiB")

            result = {
                "Raw Bytes": f"{total_bytes:,}",
                "Decimal (1000)": (
                    " / ".join(decimal_units[:2])
                    if decimal_units
                    else f"{total_bytes} bytes"
                ),
                "Binary (1024)": (
                    " / ".join(binary_units[:2])
                    if binary_units
                    else f"{total_bytes} bytes"
                ),
            }

            # Add more detailed breakdown if there are multiple units
            if len(decimal_units) > 2 or len(binary_units) > 2:
                result["Other Decimal"] = (
                    " / ".join(decimal_units[2:]) if len(decimal_units) > 2 else ""
                )
                result["Other Binary"] = (
                    " / ".join(binary_units[2:]) if len(binary_units) > 2 else ""
                )

            return result

        except (ValueError, TypeError):
            return {}

    def _parse_byte_units(self, input_str: str) -> int:
        """Parse byte size string with units like '1GB', '2.5GiB', etc."""
        # Unit multipliers
        decimal_multipliers = {
            "b": 1,
            "kb": 1000,
            "mb": 1000**2,
            "gb": 1000**3,
            "tb": 1000**4,
        }

        binary_multipliers = {
            "b": 1,
            "kib": 1024,
            "mib": 1024**2,
            "gib": 1024**3,
            "tib": 1024**4,
        }

        # Extract number and unit
        pattern = r"^(\d+(?:\.\d+)?)\s*([kmgt]?i?b)$"
        match = re.match(pattern, input_str)

        if not match:
            return None

        value_str, unit = match.groups()

        try:
            value = float(value_str)

            # Determine if it's binary (with 'i') or decimal
            if "i" in unit:
                multiplier = binary_multipliers.get(unit, 1)
            else:
                multiplier = decimal_multipliers.get(unit, 1)

            return int(value * multiplier)

        except ValueError:
            return None

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Byte Size"
