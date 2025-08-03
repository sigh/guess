"""
Tests for the new hierarchical output formatting (without table formatting).
"""

from guess.formatter import TableFormatter
from guess.convert import ConversionResult
from guess.converters.number import NumberConverter
from guess.converters.duration import DurationConverter
from guess.converters.bytesize import ByteSizeConverter
from guess.converters.timestamp import TimestampConverter


class TestOutputFormatting:
    """Test the clean hierarchical output formatting."""

    def test_single_result_formatting(self):
        """Test Mode 2: Single interpretation with multiple formats."""
        formatter = TableFormatter()

        result = ConversionResult(
            converter_name="Number",
            interpretation_description="input",
            formats={
                "Decimal": "255",
                "Hexadecimal": "0xff",
                "Binary": "0b11111111",
                "Octal": "0o377",
            },
            display_value="255"
        )

        output = formatter.format_multiple_results([result])

        # Should show hierarchical format without table characters
        assert "Number from input:" in output
        assert "  255" in output
        assert "  0xff" in output
        assert "  0b11111111" in output
        assert "  0o377" in output

    def test_multiple_interpretations_formatting(self):
        """Test Mode 1: Multiple interpretations with one format each."""
        formatter = TableFormatter()

        results = [
            ConversionResult(
                converter_name="Number",
                interpretation_description="input",
                formats={
                    "Decimal": "1,722,628,800,000",
                    "Scientific": "1.72e+12",
                    "Hexadecimal": "0x190f4b62c00",
                },
                display_value="1,722,628,800,000"
            ),
            ConversionResult(
                converter_name="Timestamp",
                interpretation_description="input",
                formats={
                    "UTC": "2024-08-03 06:00:00 UTC",
                    "Local Time": "2024-08-02 23:00:00 PDT",
                },
                display_value="2024-08-03 06:00:00 UTC"
            ),
            ConversionResult(
                converter_name="Size",
                interpretation_description="input",
                formats={
                    "Human Readable": "1.72 TB",
                    "Decimal": "1,722,628,800,000",
                },
                display_value="1.72 TB"
            ),
        ]

        output = formatter.format_multiple_results(results)

        # Should show one format per interpretation type
        assert "Number from input" in output
        assert "Timestamp from input" in output
        assert "Size from input" in output

        # Should show primary values (most readable)
        assert "1,722,628,800,000" in output  # Number primary

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

    def test_clean_spacing_and_indentation(self):
        """Test that output has consistent spacing and indentation."""
        formatter = TableFormatter()

        # Test single result indentation
        result = ConversionResult(
            converter_name="Duration",
            interpretation_description="input",
            formats={
                "Human Readable": "1 hour, 30 minutes",
                "Compact": "1h30m",
                "Seconds": "5400",
            },
            display_value="1 hour, 30 minutes"
        )

        output = formatter.format_multiple_results([result])
        lines = output.split("\n")

        # Header should have no indentation
        assert lines[0].startswith("Duration from input:")

        # Values should have 2-space indentation
        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                assert line.startswith("  ")

    def test_context_aware_labels(self):
        """Test that converter names get appropriate context labels."""
        formatter = TableFormatter()

        # Test different converter types get correct labels
        test_cases = [
            ("Number", "Number from input:"),
            ("Timestamp", "Timestamp from input:"),
            ("Duration", "Duration from input:"),
            ("Size", "Size from input:"),
        ]

        for converter_name, expected_label in test_cases:
            result = ConversionResult(
                converter_name=converter_name,
                interpretation_description="input",
                formats={"Test": "value"},
                display_value="value"
            )
            output = formatter._format_single_result(result)
            assert expected_label in output

    def test_multiple_interpretation_labels(self):
        """Test labels for multiple interpretation mode."""
        formatter = TableFormatter()

        results = [ConversionResult(
            converter_name="Number",
            interpretation_description="input",
            formats={"Decimal": "255"},
            display_value="255"
        )]

        output = formatter._format_multiple_interpretations(results)
        assert "Number from input" in output
