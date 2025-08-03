"""
Conversion logic for handling converter operations.
"""

from typing import List, Dict, NamedTuple


class ConversionResult(NamedTuple):
    """
    Represents the result of a successful conversion.

    Attributes:
        converter_name: Human-readable name of the converter that produced this result
        interpretation_description: Description of how the input was interpreted
        formats: Dictionary mapping format names to converted values
        display_value: The preferred single value to display for this conversion
    """
    converter_name: str
    interpretation_description: str
    formats: Dict[str, str]
    display_value: str


def _build_result_dict(converter, interpretation, formats: Dict[str, str]) -> ConversionResult:
    """
    Build a result object for a successful conversion.

    Args:
        converter: The converter instance
        interpretation: The interpretation object with value and description
        formats: Dictionary of format names to converted values

    Returns:
        A ConversionResult containing converter_name, interpretation_description, formats, and display_value
    """
    # Get the preferred display value for multi-interpretation mode
    display_value = converter.choose_display_value(formats, interpretation.description)
    # If converter returns None, use the first available value
    if display_value is None and formats:
        display_value = next(iter(formats.values()))

    return ConversionResult(
        converter_name=converter.get_name(),
        interpretation_description=interpretation.description,
        formats=formats,
        display_value=display_value,
    )


def try_convert(input_str: str, converters: List) -> List[ConversionResult]:
    """
    Try to convert input using all applicable converters.

    Iterates through all available converters and collects interpretations from
    those that can handle the input. This enables the multi-interpretation
    feature where ambiguous input shows multiple possible meanings.

    Args:
        input_str: The input string to convert
        converters: List of converter instances to try

    Returns:
        A list of ConversionResult objects from converters that can handle the input.
        Returns empty list if no converters can handle the input.
    """
    results = []

    for converter in converters:
        interpretations = converter.get_interpretations(input_str)

        for interpretation in interpretations:
            formats = converter.convert_value(interpretation.value)
            if formats:
                results.append(
                    _build_result_dict(converter, interpretation, formats)
                )

    return results