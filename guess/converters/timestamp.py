"""
Timestamp converter for Unix timestamps and date formats.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
import re
from dateutil import parser as dateutil_parser
from dateutil.parser import ParserError, parserinfo
from guess.converters.base import Converter, Interpretation
from guess.converters.duration import DurationConverter
from guess.utils import format_units


class NoHMSParserInfo(parserinfo):
    """Custom parserinfo that ignores HMS duration strings but keeps necessary jump words."""
    # Prevent hour/minute/second parsing.
    HMS = []
    JUMP = list(set(parserinfo.JUMP) - set(['m', 'ad']))


class TimestampConverter(Converter):
    """Converts Unix timestamps to human-readable date formats."""

    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """Get all possible interpretations of the input as a timestamp."""
        cleaned = input_str.strip()
        interpretations = []

        # Try parsing as a date/datetime string first
        datetime_interpretations = self._parse_datetime_string(cleaned)
        interpretations.extend(datetime_interpretations)

        # Try parsing as numeric timestamp
        unix_interpretations = self._parse_unix_timestamp(cleaned)
        interpretations.extend(unix_interpretations)

        # Try parsing as relative time expression
        relative_time_interpretations = self._parse_relative_time(cleaned)
        interpretations.extend(relative_time_interpretations)

        return interpretations

    def _is_reasonable_timestamp(self, timestamp_seconds: int) -> bool:
        """Check if a timestamp in seconds is within a reasonable range."""
        return -2208988800 <= timestamp_seconds <= 4102444800

    def _parse_datetime_string(self, input_str: str) -> List[Interpretation]:
        """Parse human-readable date/datetime strings using python-dateutil."""
        interpretations = []

        try:
            # Use custom parser info that ignores HMS strings and jump words to avoid conflicts with duration parsing
            parser_info = NoHMSParserInfo()
            dt = dateutil_parser.parse(input_str, fuzzy=False, parserinfo=parser_info, dayfirst=True)

            # Determine description based on content
            # Determine if this is a time-only input by checking if it's just time format.
            if re.match(r'^[\d:]+\s*(am|pm)?$', input_str.strip(), re.IGNORECASE):
                description = "time"
            elif dt.time() == datetime.min.time():
                # Midnight time suggests date-only input
                description = "date"
            else:
                # Has both date and time components
                description = "datetime"


            timestamp_ms = int(dt.timestamp() * 1000)
            interpretations.append(
                Interpretation(description=description, value=timestamp_ms)
            )

        except (ParserError, ValueError, OverflowError):
            # If dateutil can't parse it, fall back to nothing
            pass

        return interpretations

    def _parse_unix_timestamp(self, input_str: str) -> List[Interpretation]:
        """Parse numeric Unix timestamps in seconds, milliseconds, or microseconds."""
        interpretations = []

        try:
            timestamp = int(input_str)
        except ValueError:
            return interpretations

        if input_str.startswith("-"):
            abs_str = input_str[1:]
        else:
            abs_str = input_str

        length = len(abs_str)

        # Check for seconds interpretation (10 digits or reasonable range)
        if length == 10 or (timestamp < 0 and length >= 3):
            if self._is_reasonable_timestamp(timestamp):
                interpretations.append(
                    Interpretation(description="unix seconds", value=timestamp * 1000)
                )

        # Check for milliseconds interpretation (13 digits)
        if length == 13:
            if self._is_reasonable_timestamp(timestamp // 1000):
                interpretations.append(
                    Interpretation(description="unix milliseconds", value=timestamp)
                )

        # Check for microseconds interpretation (16 digits)
        if length == 16:
            if self._is_reasonable_timestamp(timestamp // 1000000):
                interpretations.append(
                    Interpretation(description="unix microseconds", value=timestamp // 1000)
                )

        return interpretations

    def _parse_relative_time(self, input_str: str) -> List[Interpretation]:
        """Parse relative time expressions like 'now', 'in 5 minutes', '2 hours ago', etc."""
        cleaned = input_str.strip().lower()

        # Handle "now"
        if cleaned == "now":
            now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            return [Interpretation(description="relative time", value=now_ms)]

        # Define patterns with their future/past indicators
        patterns = [
            (r'^in\s+(.+)$', True),           # "in 5 minutes"
            (r'^(.+)\s+from\s+now$', True),   # "5 minutes from now"
            (r'^(.+)\s+ago$', False),         # "5 minutes ago"
        ]

        # Try each pattern
        for pattern, is_future in patterns:
            match = re.match(pattern, cleaned)
            if match:
                duration_str = match.group(1)
                return self._create_relative_interpretation(duration_str, is_future)

        return []

    def _create_relative_interpretation(self, duration_str: str, is_future: bool) -> List[Interpretation]:
        """Create a relative time interpretation from a duration string."""
        interpretations = []

        duration_interpretations = DurationConverter().get_interpretations(duration_str)
        for duration_interpretation in duration_interpretations:
            duration_seconds = duration_interpretation.value
            if not is_future:
                duration_seconds = -duration_seconds
            target_time = datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)

            target_ms = int(target_time.timestamp() * 1000)
            interpretations.append(
                Interpretation(description="relative time", value=target_ms)
            )

        return interpretations

    def convert_value(self, value: Any) -> Dict[str, str]:
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
            time_diff = now - dt_utc
            relative_time = self._format_relative_time(time_diff)

            # Format results
            result = {
                "Unix Seconds": f"{int(timestamp_seconds)} (unix seconds)",
                "ISO 8601": dt_utc.isoformat().replace("+00:00", "Z"),
                "Relative": relative_time,
                "Human Readable": dt_local.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
            }

            # Add microseconds if there's subsecond precision (non-zero milliseconds part)
            if timestamp_ms % 1000 != 0:
                result["Unix Microseconds"] = f"{int(timestamp_ms * 1000)} (unix microseconds)"

            return result

        except (ValueError, OSError, OverflowError):
            return {}

    def _format_relative_time(self, time_diff):
        """Format time difference as relative time string."""
        total_seconds = abs(time_diff.total_seconds())
        is_future = time_diff.total_seconds() < 0
        suffix = "from now" if is_future else "ago"

        if total_seconds < 60:
            return "just now"
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            return f"{format_units(minutes, 'minute')} {suffix}"
        elif total_seconds < 86400:
            hours = int(total_seconds // 3600)
            return f"{format_units(hours, 'hour')} {suffix}"
        elif total_seconds < 31536000:  # Less than a year
            days = int(total_seconds // 86400)
            return f"{format_units(days, 'day')} {suffix}"
        else:
            years = int(total_seconds // 31536000)
            return f"{format_units(years, 'year')} {suffix}"

    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Timestamp"

    def choose_display_value(
        self, formats: Dict[str, str], interpretation_description: str
    ) -> str:
        """Choose the most readable display value for timestamp formats."""
        # Prioritize readable formats that show month names or UTC
        return formats.get("Human Readable")
