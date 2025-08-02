"""
Simple converter registry for managing all available converters.
"""

from typing import List, Dict, Any, Optional
from guess.converters.base import Converter
from guess.converters.number import NumberConverter
from guess.converters.timestamp import TimestampConverter
from guess.converters.duration import DurationConverter
from guess.converters.bytesize import ByteSizeConverter


# List of all available converter classes
CONVERTER_CLASSES = [
    NumberConverter,
    TimestampConverter,
    DurationConverter,
    ByteSizeConverter,
]


def get_all_converters() -> List[Converter]:
    """
    Get instances of all available converters.

    Returns:
        A list of instantiated converter objects.

    Note:
        Creates new instances each time to avoid state issues.
    """
    return [converter_class() for converter_class in CONVERTER_CLASSES]


def try_convert(input_str: str) -> List[Dict[str, Any]]:
    """
    Try to convert input using all applicable converters.

    Iterates through all available converters and collects results from
    those that can handle the input. This enables the multi-interpretation
    feature where ambiguous input shows multiple possible meanings.

    Args:
        input_str: The input string to convert

    Returns:
        A list of results from converters that can handle the input.
        Each result is a dict with 'converter_name' and 'formats' keys.
        Returns empty list if no converters can handle the input.

    Example:
        [
            {
                'converter_name': 'Number Base',
                'formats': {'Decimal': '255', 'Hexadecimal': '0xff', ...}
            },
            {
                'converter_name': 'Duration',
                'formats': {'Seconds': '255', 'Minutes': '4.25', ...}
            }
        ]
    """
    results = []
    converters = get_all_converters()

    for converter in converters:
        if converter.can_convert(input_str):
            formats = converter.convert(input_str)
            if formats:  # Only add if conversion was successful
                results.append(
                    {"converter_name": converter.get_name(), "formats": formats}
                )

    return results


def get_converter_by_name(name: str) -> Optional[Converter]:
    """
    Get a specific converter by name for explicit type commands.

    This function supports the explicit type command feature where users
    can force a specific interpretation (e.g., 'guess number 255').

    Args:
        name: The converter name or alias (e.g., 'time', 'number', 'size')

    Returns:
        The matching converter instance, or None if not found.

    Supported Names:
        - 'time', 'timestamp' -> TimestampConverter
        - 'duration' -> DurationConverter
        - 'size', 'bytesize', 'bytes' -> ByteSizeConverter
        - 'number', 'num' -> NumberConverter
    """
    # Map command names to converter names
    name_mapping = {
        "time": "Timestamp",
        "timestamp": "Timestamp",
        "duration": "Duration",
        "size": "Byte Size",
        "bytesize": "Byte Size",
        "bytes": "Byte Size",
        "number": "Number Base",
        "num": "Number Base",
    }

    # Get the actual converter name
    converter_name = name_mapping.get(name.lower(), name)

    converters = get_all_converters()
    for converter in converters:
        if converter.get_name().lower() == converter_name.lower():
            return converter
    return None
