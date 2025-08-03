"""
Duration converter for time periods and human-readable durations.
"""

import re
from typing import Dict, Any, List, Tuple
from guess.converters.base import Converter, Interpretation
from guess.utils import parse_float_unit, format_units


class DurationConverter(Converter):
    """Converts durations between different formats."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a duration."""
        cleaned = input_str.strip().lower()

        # Check for pure numbers (assume seconds) - support both integers and floats
        try:
            seconds = float(cleaned)
            if seconds >= 0:  # Only accept non-negative durations
                return [Interpretation(description="seconds", value=seconds)]
        except ValueError:
            pass

        # Check for <float> <unit> format (e.g., "2.5 hours", "2.5hours", "1.5 years")
        value, unit = self._parse_float_unit(cleaned)
        if value is not None:
            return [Interpretation(description=unit, value=float(value))]

        # Check for duration with units (compact format like 1h30m)
        if re.match(r"^(\d+[wdhms])+$", cleaned):
            value = self._parse_duration_units(cleaned)
            if value is not None:
                return [
                    Interpretation(description="mixed", value=float(value))
                ]

        return []

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a duration value to various formats."""
        total_seconds = float(value)

        if total_seconds >= 1:
            human_readable = self._format_human_readable_duration(total_seconds)
        else:
            # For sub-second durations, use a threshold-based display
            if total_seconds >= 0.001:
                human_readable = format_units(total_seconds * 1000, "millisecond")
            elif total_seconds >= 0.000001:
                human_readable = format_units(total_seconds * 1000000, "microsecond")
            else:
                human_readable = format_units(total_seconds * 1000000000, "nanosecond")

        # Format seconds using utility function to avoid unnecessary decimal points
        seconds_display = format_units(total_seconds, "second")

        result = {
            "Human Readable": human_readable,
            "Seconds": seconds_display,
        }

        # For sub-second durations, also add the smart formatting as alternative
        if total_seconds < 1:
            smart_format = self._format_subsecond_duration(total_seconds)
            result["Alternative"] = smart_format

        # Add years output if duration is large enough (>= 1 year)
        if total_seconds >= 365.25 * 24 * 3600:  # 1 year in seconds
            years = total_seconds / (365.25 * 24 * 3600)
            result["Years"] = format_units(years, "year")

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

    def _parse_float_unit(self, input_str: str) -> Tuple[float, str]:
        """Parse float unit format like '2.5 hours', '1.5 years'."""
        # Define time unit multipliers (in seconds)
        time_multipliers = {
            "years": 365.25 * 24 * 3600,
            "weeks": 604800,
            "days": 86400,
            "hours": 3600,
            "minutes": 60,
            "seconds": 1,
            "milliseconds": 0.001,
            "microseconds": 0.000001,
            "nanoseconds": 0.000000001,
        }

        # Define aliases for time units
        time_aliases = {
            "year": "years",
            "y": "years",
            "week": "weeks",
            "w": "weeks",
            "day": "days",
            "d": "days",
            "hour": "hours",
            "hrs": "hours",
            "hr": "hours",
            "h": "hours",
            "minute": "minutes",
            "mins": "minutes",
            "min": "minutes",
            "m": "minutes",
            "second": "seconds",
            "secs": "seconds",
            "sec": "seconds",
            "s": "seconds",
            "millisecond": "milliseconds",
            "ms": "milliseconds",
            "microsecond": "microseconds",
            "us": "microseconds",
            "μs": "microseconds",
            "nanosecond": "nanoseconds",
            "ns": "nanoseconds",
        }

        value, canonical_unit = parse_float_unit(
            input_str, time_multipliers, time_aliases
        )

        if value is None or canonical_unit is None:
            return None, None

        return value, canonical_unit

    def _format_human_readable_duration(self, total_seconds_input) -> str:
        """Format duration as human readable string."""
        # Convert to float to handle both int and float inputs
        total_seconds_float = float(total_seconds_input)

        # Extract whole seconds for time unit calculations
        total_whole_seconds = int(total_seconds_float)
        fractional_seconds = total_seconds_float - total_whole_seconds

        # Don't include years in human readable - use precise calculations only
        weeks = total_whole_seconds // 604800
        days = (weeks % 604800) // 86400
        hours = (total_whole_seconds % 86400) // 3600
        minutes = (total_whole_seconds % 3600) // 60
        whole_seconds_remainder = total_whole_seconds % 60

        # Combine whole seconds remainder with fractional part
        final_seconds = whole_seconds_remainder + fractional_seconds

        human_parts = []
        if weeks > 0:
            human_parts.append(format_units(weeks, "week"))
        if days > 0:
            human_parts.append(format_units(days, "day"))
        if hours > 0:
            human_parts.append(format_units(hours, "hour"))
        if minutes > 0:
            human_parts.append(format_units(minutes, "minute"))
        if final_seconds > 0:
            human_parts.append(format_units(final_seconds, "second"))

        return ", ".join(human_parts) if human_parts else "0 seconds"

    def _format_subsecond_duration(self, total_seconds: float) -> str:
        """Format sub-second duration using the largest unit with no fractional part."""
        # Try milliseconds first (1000 ms = 1 second)
        milliseconds = total_seconds * 1000
        if milliseconds == int(milliseconds):
            return format_units(int(milliseconds), "millisecond")

        # Try microseconds (1,000,000 μs = 1 second)
        microseconds = total_seconds * 1000000
        if microseconds == int(microseconds):
            return format_units(int(microseconds), "microsecond")

        # Fall back to nanoseconds (1,000,000,000 ns = 1 second)
        nanoseconds = total_seconds * 1000000000
        return format_units(nanoseconds, "nanosecond")
