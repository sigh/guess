"""
Base converter class that all converters inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Converter(ABC):
    """
    Base class for all data format converters.

    This abstract base class defines the interface that all converters must implement.
    Each converter is responsible for:
    1. Detecting if it can handle a given input string
    2. Converting the input to various related formats
    3. Providing a human-readable name for display
    """

    @abstractmethod
    def can_convert(self, input_str: str) -> bool:
        """
        Check if this converter can handle the input string.

        Args:
            input_str: The input string to check

        Returns:
            True if this converter can process the input, False otherwise

        Note:
            This method should be fast and not perform expensive operations.
            It's used to filter which converters apply to a given input.
        """
        pass

    @abstractmethod
    def convert(self, input_str: str) -> Dict[str, Any]:
        """
        Convert the input string to various formats.

        Args:
            input_str: The input string to convert

        Returns:
            A dictionary mapping format names to converted values.
            Returns empty dict if conversion fails.

        Example:
            {"Decimal": "255", "Hexadecimal": "0xff", "Binary": "0b11111111"}
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the human-readable name of this converter.

        Returns:
            A string name used for display in tables and help text.

        Example:
            "Number Base", "Timestamp", "Duration"
        """
        pass
