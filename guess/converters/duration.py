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
        cleaned = input_str.strip()
        
        # Check for pure numbers (assume seconds if small enough)
        if cleaned.isdigit():
            seconds = int(cleaned)
            # Consider it a duration if it's less than 1 week (604800 seconds)
            return 0 <= seconds < 604800
        
        # Check for unit-based input (1h, 30m, 2d, etc.)
        pattern = r'^(\d+[dhms])+$'
        return bool(re.match(pattern, cleaned.lower()))
    
    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert duration to various formats."""
        try:
            cleaned = input_str.strip()
            
            if cleaned.isdigit():
                total_seconds = int(cleaned)
            else:
                return {}  # Simplified for now
            
            # Calculate time components
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            result = {
                "Total Seconds": str(total_seconds),
                "Total Minutes": f"{total_seconds / 60:.2f}",
                "Total Hours": f"{total_seconds / 3600:.2f}",
                "HH:MM:SS": f"{hours + days * 24:02d}:{minutes:02d}:{seconds:02d}"
            }
            
            return result
            
        except (ValueError, TypeError):
            return {}
    
    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Duration"
