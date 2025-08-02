"""
Base converter class that all converters inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Converter(ABC):
    """Base class for all data format converters."""
    
    @abstractmethod
    def can_convert(self, input_str: str) -> bool:
        """Check if this converter can handle the input string."""
        pass
    
    @abstractmethod
    def convert(self, input_str: str) -> Dict[str, Any]:
        """Convert the input string to various formats."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this converter."""
        pass
