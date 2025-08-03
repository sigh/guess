"""
Integration tests for the guess CLI application.
"""

import subprocess
import sys
import pytest
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class TestCLIIntegration:
    """Test full CLI workflows."""

    def run_guess(self, *args):
        """Helper to run the guess command and return output."""
        cmd = [sys.executable, "-m", "guess"] + list(args)
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def test_help_command(self):
        """Test --help flag works."""
        returncode, stdout, stderr = self.run_guess("--help")
        assert returncode == 0
        assert "Guess - Simple data format conversion utility" in stdout
        assert "Examples:" in stdout

    def test_version_command(self):
        """Test --version flag works."""
        returncode, stdout, stderr = self.run_guess("--version")
        assert returncode == 0
        assert "guess" in stdout.lower()

    def test_simple_number_conversion(self):
        """Test basic number conversion."""
        returncode, stdout, stderr = self.run_guess("255")
        assert returncode == 0
        assert "255" in stdout  # Shows in multiple interpretation mode
        assert "Number" in stdout  # Ensure number converter is triggered

    def test_timestamp_conversion(self):
        """Test timestamp conversion."""
        returncode, stdout, stderr = self.run_guess("1722628800")
        assert returncode == 0
        assert "2024" in stdout  # Year should be present in timestamp output
        assert (
            "August" in stdout or "UTC" in stdout
        )  # Month or UTC format should be present

    def test_duration_conversion(self):
        """Test duration conversion."""
        returncode, stdout, stderr = self.run_guess("3661")
        assert returncode == 0
        assert "1 hour" in stdout
        assert "1 minute" in stdout

    def test_byte_size_conversion(self):
        """Test byte size conversion."""
        returncode, stdout, stderr = self.run_guess("1048576")
        assert returncode == 0
        assert "1.05 MB" in stdout or "1.00 MB" in stdout
        assert "1.00 MiB" in stdout or "1 MiB" in stdout

    def test_explicit_type_commands(self):
        """Test explicit type specification."""
        # Test timestamp type
        returncode, stdout, stderr = self.run_guess("time", "1722628800")
        assert returncode == 0
        assert "UTC" in stdout
        assert "2024-08-02" in stdout or "2024-08-03" in stdout

        # Test number type
        returncode, stdout, stderr = self.run_guess("number", "255")
        assert returncode == 0
        assert "0xff" in stdout

        # Test duration type
        returncode, stdout, stderr = self.run_guess("duration", "3661")
        assert returncode == 0
        assert "1 hour, 1 minute, 1 second" in stdout

        # Test size type
        returncode, stdout, stderr = self.run_guess("size", "1048576")
        assert returncode == 0
        assert "1.05 MB" in stdout or "1.00 MB" in stdout

    def test_unit_parsing(self):
        """Test parsing of values with units."""
        # Duration with units
        returncode, stdout, stderr = self.run_guess("1h30m")
        assert returncode == 0
        assert "1 hour, 30 minutes" in stdout

        # Byte size with units
        returncode, stdout, stderr = self.run_guess("1GB")
        assert returncode == 0
        assert "1000000000" in stdout

        # Hex number
        returncode, stdout, stderr = self.run_guess("0xFF")
        assert returncode == 0
        assert "255" in stdout

    def test_multi_interpretation_mode(self):
        """Test that ambiguous inputs show multiple interpretations."""
        returncode, stdout, stderr = self.run_guess("1722628800")
        assert returncode == 0

        # Should show multiple interpretations
        assert "Number from decimal" in stdout
        assert "Timestamp from unix seconds" in stdout
        assert "Size from bytes" in stdout

    def test_single_interpretation_mode(self):
        """Test that unambiguous inputs show single interpretation."""
        returncode, stdout, stderr = self.run_guess("1h30m")
        assert returncode == 0

        # Should show single interpretation with multiple formats
        assert "Duration from mixed:" in stdout
        assert "1 hour, 30 minutes" in stdout
        assert "5400 seconds" in stdout

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Completely invalid input
        returncode, stdout, stderr = self.run_guess("not-a-number")
        assert returncode == 1
        assert "Error" in stderr or "Unable" in stderr

        # Invalid explicit type
        returncode, stdout, stderr = self.run_guess("time", "invalid")
        assert returncode == 1
        assert "Unable to convert" in stderr

    def test_negative_numbers(self):
        """Test handling of negative numbers."""
        # Negative timestamp
        returncode, stdout, stderr = self.run_guess("time", "-86400")
        assert returncode == 0
        assert "1969" in stdout

        # Negative number
        returncode, stdout, stderr = self.run_guess("number", "-123")
        assert returncode == 0
        assert "-123" in stdout

    def test_scientific_notation(self):
        """Test scientific notation handling."""
        returncode, stdout, stderr = self.run_guess("1.5e9")
        assert returncode == 0
        assert "1.5 billion" in stdout

    def test_large_numbers(self):
        """Test handling of large numbers."""
        returncode, stdout, stderr = self.run_guess("1500000000")
        assert returncode == 0
        assert "1.5 billion" in stdout  # Human readable format in multi-mode

    def test_special_contexts(self):
        """Test special context detection with dedicated converters."""
        # File permissions - now handled by permission converter
        returncode, stdout, stderr = self.run_guess("755")
        assert returncode == 0
        assert "Permission from octal" in stdout  # Permission converter triggered

        # RGB context - decimal values no longer trigger color converter
        # Test with explicit hex color instead
        returncode, stdout, stderr = self.run_guess("#FF0000")
        assert returncode == 0
        assert "Color from hex:" in stdout  # Color converter triggered

    def test_binary_and_octal_inputs(self):
        """Test binary and octal input parsing."""
        # Binary
        returncode, stdout, stderr = self.run_guess("0b11111111")
        assert returncode == 0
        assert "255" in stdout

        # Octal
        returncode, stdout, stderr = self.run_guess("0o377")
        assert returncode == 0
        assert "255" in stdout


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def run_guess(self, *args):
        """Helper to run the guess command and return output."""
        cmd = [sys.executable, "-m", "guess"] + list(args)
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def test_empty_input(self):
        """Test handling of empty input."""
        returncode, stdout, stderr = self.run_guess("")
        assert returncode == 1

    def test_very_large_timestamp(self):
        """Test handling of very large timestamps."""
        # Year 2100
        returncode, stdout, stderr = self.run_guess("time", "4102444800")
        assert returncode == 0
        assert "2100" in stdout

    def test_very_small_timestamp(self):
        """Test handling of very old timestamps."""
        # Year 1900
        returncode, stdout, stderr = self.run_guess("time", "-2208988800")
        assert returncode == 0
        assert "1900" in stdout

    def test_millisecond_timestamps(self):
        """Test millisecond timestamp handling."""
        returncode, stdout, stderr = self.run_guess("time", "1722628800000")
        assert returncode == 0
        assert "1722628800000" in stdout  # Shows milliseconds in output

    def test_zero_values(self):
        """Test handling of zero values."""
        returncode, stdout, stderr = self.run_guess("0")
        assert returncode == 0
        assert "0" in stdout  # Zero shows in multi-interpretation mode

    def test_whitespace_handling(self):
        """Test handling of whitespace in input."""
        returncode, stdout, stderr = self.run_guess("  255  ")
        assert returncode == 0
        assert "255" in stdout

    def test_multiple_arguments(self):
        """Test handling of multiple arguments in input."""
        returncode, stdout, stderr = self.run_guess("1", "GB")
        assert returncode == 0
        assert "1000000000 bytes" in stdout

        returncode, stdout, stderr = self.run_guess("size", "1", "GB")
        assert returncode == 0
        assert "1000000000 bytes" in stdout


if __name__ == "__main__":
    pytest.main([__file__])
