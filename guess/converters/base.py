"""
Base converter class that all converters inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, NamedTuple


class Interpretation(NamedTuple):
    """
    Represents a single interpretation of input data.

    Attributes:
        description: Human-readable description of how input was interpreted
                    (e.g., "decimal number", "unix timestamp in seconds", "hex color code")
        value: Format-agnostic parsed value that the converter can use for formatting
               (e.g., 255, 1722628800, (255, 0, 0))
    """

    description: str
    value: Any


class Converter(ABC):
    """
    Base class for all data format converters.

    This abstract base class defines the interface that all converters must implement.
    Each converter is responsible for:
    1. Detecting possible interpretations of input strings
    2. Converting each interpretation to various related formats
    3. Providing a human-readable name for display
    """

    @abstractmethod
    def get_interpretations(self, input_str: str) -> List[Interpretation]:
        """
        Get all possible interpretations of the input string.

        Args:
            input_str: The input string to interpret

        Returns:
            A list of Interpretation objects, each containing a description
            and parsed value. Returns empty list if no interpretations are possible.

        Example:
            For input "255":
            [
                Interpretation(description="decimal number", value=255),
                Interpretation(description="duration in seconds", value=255.0),
                Interpretation(description="rgb color component", value=255)
            ]
        """
        pass

    @abstractmethod
    def convert_value(self, value: Any) -> Dict[str, str]:
        """
        Convert a parsed value to various output formats.

        Args:
            value: The parsed value to convert (e.g., 255, (255,0,0), 1722628800)

        Returns:
            A dictionary mapping format names to converted string values.
            Returns empty dict if conversion fails.

        Example:
            For value=255 in NumberConverter:
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

    @abstractmethod
    def choose_display_value(
        self, formats: Dict[str, str], interpretation_description: str
    ) -> str:
        """
        Choose the most representative single value to display for this converter.

        Args:
            formats: Dictionary of format names to converted string values
            interpretation_description: Description of how the input was interpreted

        Returns:
            The preferred format value, or None if the preferred format doesn't exist.
            The caller will use the first available value if None is returned.

        Example:
            For NumberConverter: return formats.get("Human Readable")
        """
        pass
