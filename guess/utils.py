"""
Utility functions and classes for converters.
"""

import re
from typing import Dict, Optional, Tuple, Union


def parse_float_unit(
    input_str: str,
    multipliers: Dict[str, Union[int, float]],
    aliases: Optional[Dict[str, str]] = None,
) -> Tuple[Optional[float], Optional[str]]:
    """
    Parse a string in the format '<float> <unit>' and convert to a base value.

    Args:
        input_str: Input string to parse (e.g., "2.5 hours", "2.5hours", "30 minutes")
        multipliers: Dictionary mapping canonical unit names to their multiplier values.
                    Example: {"seconds": 1, "minutes": 60, "hours": 3600}
        aliases: Optional dictionary mapping unit aliases to canonical unit names.
                Example: {"sec": "seconds", "min": "minutes", "hr": "hours"}

    Returns:
        Tuple of (converted_value, canonical_unit_name) or (None, None) if parsing fails.
        The converted_value is the input value multiplied by the unit's multiplier.

    Example:
        parse_float_unit("2.5 hours", {"hours": 3600}) -> (9000.0, "hours")
        parse_float_unit("2.5hours", {"hours": 3600}) -> (9000.0, "hours")
        parse_float_unit("30 mins", {"minutes": 60}, {"mins": "minutes"}) -> (1800.0, "minutes")
        parse_float_unit("invalid", {"hours": 3600}) -> (None, None)
    """
    aliases = aliases or {}

    # Extract number and unit using regex (space is optional)
    pattern = r"^(\d+(?:\.\d+)?)\s*(\w+)$"
    match = re.match(pattern, input_str.strip().lower())

    if not match:
        return None, None

    value_str, unit = match.groups()

    try:
        value = float(value_str)

        # Check if unit is a canonical unit
        if unit in multipliers:
            canonical_unit = unit
        # Check if unit is an alias
        elif unit in aliases and aliases[unit] in multipliers:
            canonical_unit = aliases[unit]
        else:
            return None, None

        multiplier = multipliers[canonical_unit]
        converted_value = float(value * multiplier)

        return converted_value, canonical_unit

    except (ValueError, KeyError):
        return None, None


def format_number_clean(value: Union[int, float]) -> str:
    """Format a number without unnecessary decimal points and limit large numbers to 2 decimal places."""
    if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
        return str(int(value))
    elif value > 1:
        # For numbers > 1, limit to 2 decimal places
        formatted = f"{value:.2f}"
        # Only strip trailing zeros if no precision was lost in truncation
        # Check if the number at higher precision equals the 2-decimal version
        truncated_value = round(value, 2)
        if abs(value - truncated_value) < 1e-10:  # No meaningful precision lost
            return formatted.rstrip('0').rstrip('.')
        else:
            return formatted  # Keep decimals to show truncation occurred
    else:
        # For numbers <= 1, preserve original precision
        return str(value)


def format_units(value: Union[int, float], unit: str) -> str:
    """Format a value with units, handling pluralization and number formatting.

    Args:
        value: The numeric value to format
        unit: The singular form of the unit (e.g., "second", "millisecond")

    Returns:
        Formatted string with clean number and appropriate plural/singular unit

    Examples:
        format_units(1, "second") -> "1 second"
        format_units(2, "second") -> "2 seconds"
        format_units(1.5, "hour") -> "1.5 hours"
        format_units(3.0, "minute") -> "3 minutes"
        format_units(0.5, "millisecond") -> "0.5 milliseconds"
    """
    formatted_value = format_number_clean(value)
    # Use the formatted value for pluralization to ensure consistency
    # This handles cases where 1.002 becomes "1" after formatting
    is_singular = (formatted_value == "1")
    plural_unit = unit + ('' if is_singular else 's')
    return f"{formatted_value} {plural_unit}"
