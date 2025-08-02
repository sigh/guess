"""
Tests for the new hierarchical output formatting (without table formatting).
"""

from guess.formatter import TableFormatter


class TestOutputFormatting:
    """Test the clean hierarchical output formatting."""

    def test_single_result_formatting(self):
        """Test Mode 2: Single interpretation with multiple formats."""
        formatter = TableFormatter()

        result = {
            "converter_name": "Number Base",
            "formats": {
                "Decimal": "255",
                "Hexadecimal": "0xff",
                "Binary": "0b11111111",
                "Octal": "0o377",
            },
        }

        output = formatter.format_multiple_results([result])

        # Should show hierarchical format without table characters
        assert "Number Base (from input):" in output
        assert "  255" in output
        assert "  0xff" in output
        assert "  0b11111111" in output
        assert "  0o377" in output

        # Should NOT contain table characters
        assert "┌" not in output
        assert "─" not in output
        assert "│" not in output
        assert "└" not in output

    def test_multiple_interpretations_formatting(self):
        """Test Mode 1: Multiple interpretations with one format each."""
        formatter = TableFormatter()

        results = [
            {
                "converter_name": "Number Base",
                "formats": {
                    "Decimal": "1,722,628,800,000",
                    "Scientific": "1.72e+12",
                    "Hexadecimal": "0x190f4b62c00",
                },
            },
            {
                "converter_name": "Timestamp",
                "formats": {
                    "UTC": "2024-08-03 06:00:00 UTC",
                    "Local Time": "2024-08-02 23:00:00 PDT",
                },
            },
            {
                "converter_name": "Byte Size",
                "formats": {
                    "Human Readable": "1.72 TB",
                    "Decimal": "1,722,628,800,000",
                },
            },
        ]

        output = formatter.format_multiple_results(results)

        # Should show one format per interpretation type
        assert "Number Base (from input):" in output
        assert "Timestamp (from input):" in output
        assert "Byte Size (from input):" in output

        # Should show primary values (most readable)
        assert "1,722,628,800,000" in output  # Number primary
        # Should contain timestamp and byte values

        # Should NOT contain table characters
        assert "┌" not in output
        assert "─" not in output
        assert "│" not in output
        assert "└" not in output

        # Should have clean spacing
        lines = output.strip().split("\n")
        interpretation_lines = [
            line for line in lines if line and not line.startswith("  ")
        ]
        assert len(interpretation_lines) == 3  # One line per interpretation

    def test_empty_results_handling(self):
        """Test handling of empty results."""
        formatter = TableFormatter()

        output = formatter.format_multiple_results([])
        assert output == ""

    def test_primary_display_value_selection(self):
        """Test that the most readable value is selected for display."""
        formatter = TableFormatter()

        # Test number converter prioritizes decimal over scientific
        number_formats = {
            "Decimal": "1500000",
            "Scientific": "1.5e+06",
            "Hexadecimal": "0x16e360",
        }
        value = formatter._get_primary_display_value(number_formats)
        assert value == "1500000"

        # Test timestamp converter prioritizes local time
        timestamp_formats = {
            "UTC": "2024-08-02 16:00:00 UTC",
            "Local Time": "2024-08-02 09:00:00 PDT",
            "Unix Seconds": "1722628800",
        }
        value = formatter._get_primary_display_value(timestamp_formats)
        assert value == "2024-08-02 09:00:00 PDT"

    def test_clean_spacing_and_indentation(self):
        """Test that output has consistent spacing and indentation."""
        formatter = TableFormatter()

        # Test single result indentation
        result = {
            "converter_name": "Duration",
            "formats": {
                "Human Readable": "1 hour, 30 minutes",
                "Compact": "1h30m",
                "Seconds": "5400",
            },
        }

        output = formatter.format_multiple_results([result])
        lines = output.split("\n")

        # Header should have no indentation
        assert lines[0].startswith("Duration (from input):")

        # Values should have 2-space indentation
        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                assert line.startswith("  ")

    def test_context_aware_labels(self):
        """Test that converter names get appropriate context labels."""
        formatter = TableFormatter()

        # Test different converter types get correct labels
        test_cases = [
            ("Number Base", "Number Base (from input):"),
            ("Timestamp", "Timestamp (from input):"),
            ("Duration", "Duration (from input):"),
            ("Byte Size", "Byte Size (from input):"),
        ]

        for converter_name, expected_label in test_cases:
            result = {"converter_name": converter_name, "formats": {"Test": "value"}}
            output = formatter._format_single_result(result)
            assert expected_label in output

    def test_multiple_interpretation_labels(self):
        """Test labels for multiple interpretation mode."""
        formatter = TableFormatter()

        results = [{"converter_name": "Number Base", "formats": {"Decimal": "255"}}]

        output = formatter._format_multiple_interpretations(results)
        assert "Number Base (from input):" in output
