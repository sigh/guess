"""
Timestamp converter for Unix timestamps and date formats.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
from guess.converters.base import Converter, Interpretation


class TimestampConverter(Converter):
    """Converts Unix timestamps to human-readable date formats."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a timestamp."""
        cleaned = input_str.strip()
        interpretations = []

        try:
            timestamp = int(cleaned)
        except ValueError:
            return interpretations

        # Check if it's a reasonable timestamp length
        if cleaned.startswith("-"):
            abs_str = cleaned[1:]
        else:
            abs_str = cleaned

        length = len(abs_str)

        # Check for seconds interpretation (10 digits or reasonable range)
        if length == 10 or (timestamp < 0 and length >= 3):
            timestamp_seconds = timestamp
            # Reasonable range check
            if -2208988800 <= timestamp_seconds <= 4102444800:
                interpretations.append(
                    Interpretation(description="unix seconds", value=timestamp * 1000)
                )

        # Check for milliseconds interpretation (13 digits)
        if length == 13:
            timestamp_seconds = timestamp // 1000
            # Reasonable range check
            if -2208988800 <= timestamp_seconds <= 4102444800:
                interpretations.append(
                    Interpretation(description="unix milliseconds", value=timestamp)
                )

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, Any]:
        """Convert a timestamp value to various formats."""
        # Value is always in milliseconds from get_interpretations()
        timestamp_ms = value

        try:
            # Convert to seconds for datetime operations
            timestamp_seconds = timestamp_ms / 1000

            # Create datetime objects
            dt_utc = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            dt_local = datetime.fromtimestamp(timestamp_seconds)

            # Calculate relative time
            now = datetime.now(tz=timezone.utc)
            dt_utc_aware = dt_utc.replace(tzinfo=timezone.utc)
            time_diff = now - dt_utc_aware
            relative_time = self._format_relative_time(time_diff)

            # Format results
            result = {
                "Unix Seconds": f"{int(timestamp_seconds)} (unix seconds)",
                "Unix Milliseconds": f"{int(timestamp_ms)} (unix milliseconds)",
                "UTC": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "Local Time": dt_local.strftime("%Y-%m-%d %H:%M:%S"),
                "ISO 8601": dt_utc.isoformat().replace("+00:00", "Z"),
                "Relative": relative_time,
                "Human Readable": dt_local.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
            }

            return result

        except (ValueError, OSError, OverflowError):
            return {}

    def _format_relative_time(self, time_diff):
        """Format time difference as relative time string."""
        total_seconds = abs(time_diff.total_seconds())
        is_future = time_diff.total_seconds() < 0

        if total_seconds < 60:
            return "just now"
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            suffix = "from now" if is_future else "ago"
            return f"{minutes} minute{'s' if minutes != 1 else ''} {suffix}"
        elif total_seconds < 86400:
            hours = int(total_seconds // 3600)
            suffix = "from now" if is_future else "ago"
            return f"{hours} hour{'s' if hours != 1 else ''} {suffix}"
        elif total_seconds < 31536000:  # Less than a year
            days = int(total_seconds // 86400)
            suffix = "from now" if is_future else "ago"
            return f"{days} day{'s' if days != 1 else ''} {suffix}"
        else:
            years = int(total_seconds // 31536000)
            suffix = "from now" if is_future else "ago"
            return f"{years} year{'s' if years != 1 else ''} {suffix}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Timestamp"

    def choose_display_value(
        self, formats: Dict[str, Any], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for timestamp formats."""
        # Prioritize readable formats that show month names or UTC
        return formats.get("Human Readable")
