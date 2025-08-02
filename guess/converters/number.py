"""
Number base converter for decimal, hex, binary, and octal formats.
"""

from typing import Dict, Any
from guess.converters.base import Converter


class NumberConverter(Converter):
    """Converts numbers between different bases."""
    
    def can_convert(self, input_str: str) -> bool:
        """Check if input is a valid decimal number."""
        # For now, only handle positive decimal integers
        return input_str.strip().isdigit()
    
    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert decimal number to different bases."""
        try:
            num = int(input_str.strip())
            
            return {
                "Decimal": str(num),
                "Hexadecimal": f"0x{num:x}",
                "Binary": f"0b{num:b}",
                "Octal": f"0o{num:o}"
            }
        except ValueError:
            return {}
    
    def get_name(self) -> str:
        """Get the name of this converter."""
        return "Number Base"
