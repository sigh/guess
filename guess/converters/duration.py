"""
Duration converter for time periods and human-readable durations.
"""

import re
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation


class DurationConverter(Converter):
    """Converts durations between different formats."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a duration."""
        cleaned = input_str.strip().lower()
        interpretations = []

        # Check for pure numbers (assume seconds)
        if cleaned.isdigit():
            seconds = int(cleaned)
            if 0 <= seconds < 604800:  # Less than 1 week
                interpretations.append(
                    Interpretation(description="seconds", value=float(seconds))
                )

        # Check for duration with units
        elif re.match(r"^(\d+[wdhms])+$", cleaned):
            try:
                value = self._parse_duration_units(cleaned)
                if value is not None:
                    interpretations.append(
                        Interpretation(description="string", value=float(value))
                    )
            except ValueError:
                pass

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a duration value to various formats."""
        total_seconds = int(value)

        # Human readable format
        human_readable = self._format_human_readable_duration(total_seconds)

        # Compact format
        compact = self._format_compact_duration(total_seconds)

        result = {
            "Human Readable": human_readable,
            "Compact": compact,
            "Seconds": str(total_seconds),
            "Minutes": f"{total_seconds / 60:.2f}",
            "Hours": f"{total_seconds / 3600:.2f}",
        }

        return result

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Duration"

    def choose_display_value(
        self, formats: Dict[str, Any], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for duration formats."""
        # Prioritize human readable format
        return formats.get("Human Readable")

    def _parse_duration_units(self, input_str: str) -> int:
        """Parse duration string with units like '1h30m', '2d4h', etc."""
        # Unit multipliers in seconds
        multipliers = {
            "w": 604800,  # week
            "d": 86400,  # day
            "h": 3600,  # hour
            "m": 60,  # minute
            "s": 1,  # second
        }

        total_seconds = 0

        # Find all number+unit combinations
        pattern = r"(\d+)([wdhms])"
        matches = re.findall(pattern, input_str)

        if not matches:
            return None

        for value_str, unit in matches:
            try:
                value = int(value_str)
                total_seconds += value * multipliers[unit]
            except (ValueError, KeyError):
                return None

        return total_seconds

    def _format_human_readable_duration(self, total_seconds: int) -> str:
        """Format duration as human readable string."""
        weeks = total_seconds // 604800
        days = (total_seconds % 604800) // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        human_parts = []
        if weeks > 0:
            human_parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days > 0:
            human_parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            human_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            human_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0:
            human_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        return ", ".join(human_parts) if human_parts else "0 seconds"

    def _format_compact_duration(self, total_seconds: int) -> str:
        """Format duration as compact string."""
        weeks = total_seconds // 604800
        days = (total_seconds % 604800) // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        compact_parts = []
        if weeks > 0:
            compact_parts.append(f"{weeks}w")
        if days > 0:
            compact_parts.append(f"{days}d")
        if hours > 0:
            compact_parts.append(f"{hours}h")
        if minutes > 0:
            compact_parts.append(f"{minutes}m")
        if seconds > 0:
            compact_parts.append(f"{seconds}s")

        return "".join(compact_parts) if compact_parts else "0s"
