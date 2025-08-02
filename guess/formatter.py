"""
Table formatter for pretty output display.
"""

from typing import Dict, Any, List


class TableFormatter:
    """Formats converter results into nice tables."""

    def format_multiple_results(self, results_list: List[Dict[str, Any]]) -> str:
        """Format multiple converter results with table formatting."""
        if not results_list:
            return ""

        if len(results_list) == 1:
            # Single result - use format table
            return self._format_single_table(results_list[0])
        else:
            # Multiple results - use interpretations table
            return self._format_interpretations_table(results_list)

    def _format_single_table(self, result: Dict[str, Any]) -> str:
        """Format single converter result as a formats table."""
        converter_name = result["converter_name"]
        formats = result["formats"]

        lines = []
        lines.append(f"Input: (converted as {converter_name.lower()})")
        lines.append("")
        lines.append("Formats:")

        # Calculate column widths
        max_format_width = max(len(key) for key in formats.keys()) if formats else 0
        max_value_width = (
            max(len(str(value)) for value in formats.values()) if formats else 0
        )

        # Ensure minimum widths
        format_width = max(max_format_width, 15)
        value_width = max(max_value_width, 30)

        # Table borders
        top_border = f"┌─{'─' * format_width}─┬─{'─' * value_width}─┐"
        separator = f"├─{'─' * format_width}─┼─{'─' * value_width}─┤"
        bottom_border = f"└─{'─' * format_width}─┴─{'─' * value_width}─┘"

        lines.append(top_border)
        lines.append(f"│ {'Format':<{format_width}} │ {'Value':<{value_width}} │")
        lines.append(separator)

        for key, value in formats.items():
            lines.append(f"│ {key:<{format_width}} │ {str(value):<{value_width}} │")

        lines.append(bottom_border)

        return "\n".join(lines)

    def _format_interpretations_table(self, results_list: List[Dict[str, Any]]) -> str:
        """Format multiple converter results as interpretations table."""
        lines = []
        lines.append("Interpretations:")
        lines.append("")

        # Calculate column widths
        max_type_width = max(len(result["converter_name"]) for result in results_list)
        type_width = max(max_type_width, 12)
        value_width = 40

        # Table borders
        top_border = f"┌─{'─' * type_width}─┬─{'─' * value_width}─┐"
        separator = f"├─{'─' * type_width}─┼─{'─' * value_width}─┤"
        bottom_border = f"└─{'─' * type_width}─┴─{'─' * value_width}─┘"

        lines.append(top_border)
        lines.append(f"│ {'Type':<{type_width}} │ {'Value':<{value_width}} │")
        lines.append(separator)

        for i, result in enumerate(results_list):
            converter_name = result["converter_name"]
            formats = result["formats"]

            # Get the most representative values for display
            display_values = self._get_display_values(formats)

            # Add first line
            first_value = display_values[0] if display_values else ""
            lines.append(
                f"│ {converter_name:<{type_width}} │ {first_value:<{value_width}} │"
            )

            # Add additional lines for this converter
            for value in display_values[1:]:
                lines.append(f"│ {'':<{type_width}} │ {value:<{value_width}} │")

            # Add separator between converters (except for last one)
            if i < len(results_list) - 1:
                lines.append(separator)

        lines.append(bottom_border)

        return "\n".join(lines)

    def _get_display_values(self, formats: Dict[str, Any]) -> List[str]:
        """Get the most representative values to display for a converter."""
        # This prioritizes the most useful formats for display
        values = []

        # For number base converter, prioritize the core bases
        if "Decimal" in formats and "Hexadecimal" in formats:
            # This is likely a number converter - show core number formats first
            priority_keys = ["Decimal", "Hexadecimal", "Binary", "Octal"]
            for key in priority_keys:
                if key in formats:
                    formatted_value = str(formats[key])
                    if len(formatted_value) > 38:  # Leave room for padding
                        formatted_value = formatted_value[:35] + "..."
                    values.append(formatted_value)

            # Add other formats if space allows
            for key, value in formats.items():
                if key not in priority_keys and len(values) < 5:  # Increased limit
                    formatted_value = str(value)
                    if len(formatted_value) > 38:
                        formatted_value = formatted_value[:35] + "..."
                    values.append(formatted_value)
        else:
            # For other converters, add all format values
            for key, value in formats.items():
                formatted_value = str(value)
                if len(formatted_value) > 38:  # Leave room for padding
                    formatted_value = formatted_value[:35] + "..."
                values.append(formatted_value)

        return values[:4]  # Increased from 3 to 4 lines per converter
