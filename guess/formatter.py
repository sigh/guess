"""
Clean hierarchical formatter for output display.
"""

from typing import Dict, Any, List


class TableFormatter:
    """
    Formats converter results into clean, hierarchical output.

    This class handles two display modes:
    1. Mode 1 (Ambiguous Input): Shows one readable format per interpretation type
    2. Mode 2 (Specific Type): Shows multiple formats of the same interpretation

    Uses simple indentation and clean spacing for readability without table formatting.
    """

    def format_multiple_results(self, results_list: List[Dict[str, Any]]) -> str:
        """
        Format multiple converter results with clean hierarchical formatting.

        Mode 1 (Multiple Interpretations): Shows one readable format per type
        Mode 2 (Single Type): Shows multiple formats of the same interpretation

        Args:
            results_list: List of converter results, each containing
                         'converter_name' and 'formats' keys

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

    def _format_single_result(self, result: Dict[str, Any]) -> str:
        """Format single converter result with multiple formats."""
        converter_name = result["converter_name"]
        interpretation_description = result.get("interpretation_description", "input")
        formats = result["formats"]

        lines = []
        # Use the specific interpretation description for accurate labeling
        lines.append(f"{converter_name} (from {interpretation_description}):")

        # Track seen values to avoid duplicates
        seen_values = set()
        for key, value in formats.items():
            if value not in seen_values:
                lines.append(f"  {value}")
                seen_values.add(value)

        return "\n".join(lines)

    def _format_multiple_interpretations(
        self, results_list: List[Dict[str, Any]]
    ) -> str:
        """Format multiple converter results showing one format per type."""
        lines = []

        for result in results_list:
            converter_name = result["converter_name"]
            interpretation_description = result.get(
                "interpretation_description", "input"
            )
            formats = result["formats"]
            converter = result.get("converter")

            # Get the most representative value for this interpretation
            if converter:
                display_value = converter.choose_display_value(
                    formats, interpretation_description
                )
                # If converter returns None, use the first available value
                if display_value is None and formats:
                    display_value = next(iter(formats.values()))
            else:
                # Fallback to internal method for backward compatibility
                display_value = self._get_primary_display_value(formats)

            # Use the specific interpretation description for accurate labeling
            lines.append(f"{converter_name} (from {interpretation_description}):")
            lines.append(f"  {display_value}")
            lines.append("")  # Empty line between interpretations

        # Remove trailing empty line
        if lines and lines[-1] == "":
            lines.pop()

        return "\n".join(lines)

    def _get_primary_display_value(self, formats: Dict[str, Any]) -> str:
        """Get the most representative single value to display for a converter.

        DEPRECATED: This method is kept for backward compatibility only.
        Use converter.choose_display_value() instead.
        """
        # Priority order for different converter types - choose most readable format

        # For byte size converter, show both decimal and binary
        if "Raw Bytes" in formats:  # This identifies byte size converter
            if "Decimal" in formats and "Binary" in formats:
                return f"{formats['Decimal']} / {formats['Binary']}"
            elif "Decimal" in formats:
                return str(formats["Decimal"])
            elif "Binary" in formats:
                return str(formats["Binary"])

        # For number converter, choose based on size and readability
        if "Human Readable" in formats:
            return str(formats["Human Readable"])
        elif "Decimal" in formats and "Scientific" in formats:
            decimal_val = str(formats["Decimal"])
            return decimal_val
        elif "Decimal" in formats:
            return str(formats["Decimal"])

        # For timestamp converter, prioritize readable formats
        if "Local Time" in formats:
            return str(formats["Local Time"])
        elif "UTC" in formats:
            return str(formats["UTC"])
        elif "Human Readable" in formats:
            return str(formats["Human Readable"])

        # For duration converter, prioritize human readable
        if "Human Readable" in formats:
            return str(formats["Human Readable"])

        # Default: return first available value
        if formats:
            return str(next(iter(formats.values())))

        return "Unknown"
