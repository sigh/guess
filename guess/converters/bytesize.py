"""
Byte size converter for data storage units.
"""

import re
from typing import Dict, Any, List, Union, Tuple
from guess.converters.base import Converter, Interpretation


class ByteSizeConverter(Converter):
    """Converts byte sizes between different units."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a byte size."""
        cleaned = input_str.strip().lower()
        interpretations = []

        # Check for pure numbers (assume bytes)
        if cleaned.isdigit():
            size = int(cleaned)
            if size >= 1024:  # Only consider reasonable byte sizes
                interpretations.append(Interpretation(description="bytes", value=size))

        # Check for unit-based input
        elif re.match(r"^\d+(?:\.\d+)?\s*([kmgtpe]?i?b)$", cleaned):
            try:
                value, unit = self._parse_byte_units(cleaned)
                if value is not None:
                    interpretations.append(
                        Interpretation(
                            description=self._format_unit_display(unit), value=value
                        )
                    )
            except ValueError:
                pass

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, str]:
        """Convert a byte size value to various formats."""
        total_bytes = value

        # Decimal (1000-based) units
        decimal_units = []
        if total_bytes >= 1000**6:
            decimal_units.append(f"{total_bytes / 1000**6:.2f} EB")
        if total_bytes >= 1000**5:
            decimal_units.append(f"{total_bytes / 1000**5:.2f} PB")
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
        if total_bytes >= 1024**6:
            binary_units.append(f"{total_bytes / 1024**6:.2f} EiB")
        if total_bytes >= 1024**5:
            binary_units.append(f"{total_bytes / 1024**5:.2f} PiB")
        if total_bytes >= 1024**4:
            binary_units.append(f"{total_bytes / 1024**4:.2f} TiB")
        if total_bytes >= 1024**3:
            binary_units.append(f"{total_bytes / 1024**3:.2f} GiB")
        if total_bytes >= 1024**2:
            binary_units.append(f"{total_bytes / 1024**2:.2f} MiB")
        if total_bytes >= 1024:
            binary_units.append(f"{total_bytes / 1024:.2f} KiB")

        result = {}

        # Add raw byte count
        result["Raw Bytes"] = f"{total_bytes} bytes"

        # Add decimal units if available
        if decimal_units:
            result["Decimal"] = decimal_units[0]

        # Add binary units if available
        if binary_units:
            result["Binary"] = binary_units[0]

        return result

    def _parse_byte_units(self, input_str: str) -> Union[Tuple[int, str], Tuple[None, None]]:
        """Parse byte size string with units like '1GB', '2.5GiB', etc."""
        # Unit multipliers
        decimal_multipliers = {
            "b": 1,
            "kb": 1000,
            "mb": 1000**2,
            "gb": 1000**3,
            "tb": 1000**4,
            "pb": 1000**5,
            "eb": 1000**6,
        }

        binary_multipliers = {
            "b": 1,
            "kib": 1024,
            "mib": 1024**2,
            "gib": 1024**3,
            "tib": 1024**4,
            "pib": 1024**5,
            "eib": 1024**6,
        }

        # Extract number and unit
        pattern = r"^(\d+(?:\.\d+)?)\s*([kmgtpe]?i?b)$"
        match = re.match(pattern, input_str)

        if not match:
            return None, None

        value_str, unit = match.groups()

        try:
            value = float(value_str)

            # Determine if it's binary (with 'i') or decimal
            if "i" in unit:
                multiplier = binary_multipliers.get(unit, 1)
            else:
                multiplier = decimal_multipliers.get(unit, 1)

            return int(value * multiplier), unit

        except ValueError:
            return None, None

    def _format_unit_display(self, unit: str) -> str:
        """Format unit for display: uppercase letters but keep 'i' lowercase for binary units."""
        return unit.upper().replace("I", "i")

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Size"

    def choose_display_value(
        self, formats: Dict[str, str], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for byte size formats."""
        # Show both decimal and binary for byte sizes
        if "Decimal" in formats and "Binary" in formats:
            return f"{formats['Decimal']} / {formats['Binary']}"
        return formats.get("Decimal")
