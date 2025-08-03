"""
Clean hierarchical formatter for output display.
"""

from typing import List
from .convert import ConversionResult


class TableFormatter:
    """
    Formats converter results into clean, hierarchical output.

    This class handles two display modes:
    1. Mode 1 (Ambiguous Input): Shows one readable format per interpretation type
    2. Mode 2 (Specific Type): Shows multiple formats of the same interpretation

    Uses simple indentation and clean spacing for readability without table formatting.
    """

    def format_multiple_results(self, results_list: List[ConversionResult]) -> str:
        """
        Format multiple converter results with clean hierarchical formatting.

        Mode 1 (Multiple Interpretations): Shows one readable format per type
        Mode 2 (Single Type): Shows multiple formats of the same interpretation

        Args:
            results_list: List of ConversionResult objects

        Returns:
            Clean formatted string ready for display, or empty string if no results

        Example:
            Mode 1: "Number: 255\nTimestamp: 2024-08-02 16:00:00 UTC"
            Mode 2: "Number (from decimal):\n  255\n  0xFF\n  0b11111111"
        """
        if not results_list:
            return ""

        if len(results_list) == 1:
            # Mode 2: Single interpretation - show multiple formats
            return self._format_single_result(results_list[0])
        else:
            # Mode 1: Multiple interpretations - show one format per type
            return self._format_multiple_interpretations(results_list)

    def _format_single_result(self, result: ConversionResult) -> str:
        """Format single converter result with multiple formats."""
        converter_name = result.converter_name
        interpretation_description = result.interpretation_description
        formats = result.formats

        lines = []
        # Use the specific interpretation description for accurate labeling
        lines.append(f"{converter_name} from {interpretation_description}:")

        # Track seen values to avoid duplicates
        seen_values = set()
        for value in formats.values():
            if value not in seen_values:
                lines.append(f"  {value}")
                seen_values.add(value)

        return "\n".join(lines)

    def _format_multiple_interpretations(
        self, results_list: List[ConversionResult]
    ) -> str:
        """Format multiple converter results showing one format per type."""
        lines = []

        # Build formatted results first
        formatted_results = []

        for result in results_list:
            converter_name = result.converter_name
            interpretation_description = result.interpretation_description
            formats = result.formats
            display_value = result.display_value

            # If no display_value provided, use the first available value as fallback
            if display_value is None and formats:
                display_value = next(iter(formats.values()))

            label = f"{converter_name} from {interpretation_description}:"
            formatted_results.append((label, display_value))

        # Calculate maximum label width for alignment
        max_label_width = max(len(label) for label, _ in formatted_results)

        # Format with aligned columns
        for label, display_value in formatted_results:
            lines.append(f"{label:<{max_label_width + 2}}{display_value}")

        return "\n".join(lines)