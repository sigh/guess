"""
Byte size converter for data storage units.
"""

from typing import Dict, Any
from guess.converters.base import Converter


class ByteSizeConverter(Converter):
    """Converts byte sizes between different units."""
    
    def can_convert(self, input_str: str) -> bool:
        """Check if input looks like a byte size."""
        cleaned = input_str.strip()
        
        # Check for pure numbers (assume bytes if large enough)
        if cleaned.isdigit():
            size = int(cleaned)
            # Consider it bytes if it's >= 1024 (1 KB)
            return size >= 1024
        
        return False
    
    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert byte size to various units."""
        try:
            total_bytes = int(input_str.strip())
            
            result = {
                "Bytes": f"{total_bytes:,}",
                "KB": f"{total_bytes / 1000:.2f}",
                "MB": f"{total_bytes / 1000**2:.2f}",
                "GB": f"{total_bytes / 1000**3:.2f}",
                "KiB": f"{total_bytes / 1024:.2f}",
                "MiB": f"{total_bytes / 1024**2:.2f}",
                "GiB": f"{total_bytes / 1024**3:.2f}"
            }
            
            return result
            
        except (ValueError, TypeError):
            return {}
    
    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Byte Size"
