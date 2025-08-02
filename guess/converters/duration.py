"""
Duration converter for time periods and human-readable durations.
"""

import re
from typing import Dict, Any
from guess.converters.base import Converter


class DurationConverter(Converter):
    """Converts durations between different formats."""

    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like a duration."""
        cleaned = input_str.strip().lower()

        # Check for pure numbers (assume seconds if small enough)
        if cleaned.isdigit():
            seconds = int(cleaned)
            # Consider it a duration if it's less than 1 week (604800 seconds)
            return 0 <= seconds < 604800

        # Check for unit-based input (1h, 30m, 2d, 1h30m, etc.)
        # Pattern matches combinations like: 1d2h30m45s, 1h30m, 2d, 30s
        pattern = r"^(\d+[wdhms])+$"
        return bool(re.match(pattern, cleaned))

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert duration to various formats."""
        try:
            cleaned = input_str.strip().lower()

            if cleaned.isdigit():
                total_seconds = int(cleaned)
            else:
                # Parse unit-based input
                total_seconds = self._parse_duration_units(cleaned)
                if total_seconds is None:
                    return {}

            # Calculate time components
            weeks = total_seconds // 604800
            days = (total_seconds % 604800) // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            # Human readable format
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

            human_readable = ", ".join(human_parts) if human_parts else "0 seconds"

            # Compact format
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

            compact = "".join(compact_parts) if compact_parts else "0s"

            result = {
                "Human Readable": human_readable,
                "Compact": compact,
                "Seconds": f"{total_seconds:,}",
            }

            return result

        except (ValueError, TypeError):
            return {}

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Duration"

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
