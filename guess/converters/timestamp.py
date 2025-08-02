"""
Timestamp converter for Unix timestamps and date formats.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from guess.converters.base import Converter


class TimestampConverter(Converter):
    """Converts Unix timestamps to human-readable date formats."""

    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like a Unix timestamp."""
        cleaned = input_str.strip()

        # Check if it's a valid integer (including negative)
        try:
            timestamp = int(cleaned)
        except ValueError:
            return False

        # Check if it's a reasonable timestamp length
        # 10 digits = seconds since epoch (up to year 2286)
        # 13 digits = milliseconds since epoch (up to year 2286)
        # Handle negative numbers by checking absolute value length
        if cleaned.startswith("-"):
            abs_str = cleaned[1:]
        else:
            abs_str = cleaned

        length = len(abs_str)

        if length == 10 or length == 13 or (timestamp < 0 and length >= 3):
            # Convert to seconds for range check
            timestamp_seconds = timestamp
            if length == 13:
                timestamp_seconds = timestamp // 1000

            # Reasonable range: 1900 to 2100 (allows negative timestamps)
            # -2208988800 = 1900-01-01, 4102444800 = 2100-01-01
            return -2208988800 <= timestamp_seconds <= 4102444800

        return False

    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert Unix timestamp to various date formats."""
        try:
            timestamp_str = input_str.strip()
            timestamp = int(timestamp_str)

            # Determine if it's seconds or milliseconds
            abs_str = str(abs(timestamp))
            if len(abs_str) == 13:
                # Milliseconds
                timestamp_seconds = timestamp / 1000
                milliseconds = abs(timestamp) % 1000
            else:
                # Seconds
                timestamp_seconds = timestamp
                milliseconds = 0

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
                "Unix Seconds": str(int(timestamp_seconds)),
                "Unix Milliseconds": str(int(timestamp_seconds * 1000)),
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
