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
        
        # Check if it's a valid integer
        if not cleaned.isdigit():
            return False
        
        # Check if it's a reasonable timestamp length
        # 10 digits = seconds since epoch (up to year 2286)
        # 13 digits = milliseconds since epoch (up to year 2286)
        length = len(cleaned)
        if length == 10 or length == 13:
            # Additional check: reasonable timestamp range
            # After 1970-01-01 and before year 2100
            timestamp = int(cleaned)
            if length == 13:
                timestamp = timestamp // 1000  # Convert milliseconds to seconds
            
            # Reasonable range: 1970 to 2100
            return 0 <= timestamp <= 4102444800  # 2100-01-01 00:00:00 UTC
        
        return False
    
    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert Unix timestamp to various date formats."""
        try:
            timestamp_str = input_str.strip()
            timestamp = int(timestamp_str)
            
            # Determine if it's seconds or milliseconds
            if len(timestamp_str) == 13:
                # Milliseconds
                timestamp_seconds = timestamp / 1000
                milliseconds = timestamp % 1000
            else:
                # Seconds
                timestamp_seconds = timestamp
                milliseconds = 0
            
            # Create datetime objects
            dt_utc = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            dt_local = datetime.fromtimestamp(timestamp_seconds)
            
            # Format results
            result = {
                "Unix Timestamp": str(int(timestamp_seconds)),
                "UTC Time": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "Local Time": dt_local.strftime("%Y-%m-%d %H:%M:%S %Z").strip(),
                "ISO 8601": dt_utc.isoformat().replace("+00:00", "Z"),
                "Human Readable": dt_local.strftime("%A, %B %d, %Y at %I:%M:%S %p")
            }
            
            # Add milliseconds info if applicable
            if len(timestamp_str) == 13:
                result["Milliseconds"] = str(milliseconds)
                result["Unix Timestamp (ms)"] = timestamp_str
            
            return result
            
        except (ValueError, OSError, OverflowError):
            return {}
    
    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Timestamp"
