"""
Tests for the permission converter.
"""

import pytest
from guess.converters.permission import PermissionConverter


class TestPermissionConverter:
    """Test the permission converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = PermissionConverter()

    def test_can_convert_octal_notation(self):
        """Test detection of octal notation."""
        assert self.converter.can_convert("755")
        assert self.converter.can_convert("644")
        assert self.converter.can_convert("0755")
        assert self.converter.can_convert("0o755")

    def test_can_convert_symbolic_notation(self):
        """Test detection of symbolic notation."""
        assert self.converter.can_convert("rwxr-xr-x")
        assert self.converter.can_convert("rw-r--r--")
        assert self.converter.can_convert("---------")
        assert self.converter.can_convert("rwxrwxrwx")

    def test_can_convert_decimal_equivalent(self):
        """Test detection of decimal equivalent."""
        assert self.converter.can_convert("493")  # 755 in decimal
        assert self.converter.can_convert("420")  # 644 in decimal

    def test_cannot_convert_invalid_values(self):
        """Test rejection of invalid permission values."""
        assert not self.converter.can_convert("888")  # Invalid octal digit
        assert not self.converter.can_convert("rwxr-xr-xa")  # Too long
        assert not self.converter.can_convert("abc")  # Invalid format
        assert not self.converter.can_convert("1000")  # Out of range

    def test_convert_octal_755(self):
        """Test conversion of 755 octal permissions."""
        result = self.converter.convert("755")

        assert "Symbolic" in result
        assert "Octal" in result
        assert "Decimal" in result
        assert "Breakdown" in result

        assert result["Symbolic"] == "rwxr-xr-x"
        assert result["Octal"] == "0o755"
        assert result["Decimal"] == "493"
        assert "owner: read, write, execute" in result["Breakdown"]
        assert "group: read, execute" in result["Breakdown"]
        assert "others: read, execute" in result["Breakdown"]

    def test_convert_octal_644(self):
        """Test conversion of 644 octal permissions."""
        result = self.converter.convert("644")

        assert result["Symbolic"] == "rw-r--r--"
        assert result["Octal"] == "0o644"
        assert result["Decimal"] == "420"

    def test_convert_prefixed_octal(self):
        """Test conversion of prefixed octal formats."""
        # Test 0755 format
        result = self.converter.convert("0755")
        assert result["Symbolic"] == "rwxr-xr-x"

        # Test 0o755 format
        result = self.converter.convert("0o755")
        assert result["Symbolic"] == "rwxr-xr-x"

    def test_convert_symbolic_notation(self):
        """Test conversion of symbolic notation."""
        result = self.converter.convert("rwxr-xr-x")

        assert result["Symbolic"] == "rwxr-xr-x"
        assert result["Octal"] == "0o755"
        assert result["Decimal"] == "493"

    def test_convert_readonly_file(self):
        """Test conversion of read-only file permissions."""
        result = self.converter.convert("rw-r--r--")

        assert result["Symbolic"] == "rw-r--r--"
        assert result["Octal"] == "0o644"
        assert "owner: read, write" in result["Breakdown"]
        assert "group: read" in result["Breakdown"]
        assert "others: read" in result["Breakdown"]

    def test_convert_no_permissions(self):
        """Test conversion of no permissions."""
        result = self.converter.convert("---------")

        assert result["Symbolic"] == "---------"
        assert result["Octal"] == "0o000"
        assert result["Decimal"] == "0"
        assert "owner: none" in result["Breakdown"]

    def test_convert_full_permissions(self):
        """Test conversion of full permissions."""
        result = self.converter.convert("rwxrwxrwx")

        assert result["Symbolic"] == "rwxrwxrwx"
        assert result["Octal"] == "0o777"
        assert result["Decimal"] == "511"

    def test_convert_decimal_input(self):
        """Test conversion of decimal input."""
        result = self.converter.convert("493")  # 755 in decimal

        assert result["Symbolic"] == "rwxr-xr-x"
        assert result["Octal"] == "0o755"
        assert result["Decimal"] == "493"

    def test_permission_breakdown_formatting(self):
        """Test permission breakdown formatting."""
        result = self.converter.convert("751")

        breakdown = result["Breakdown"]
        assert "owner: read, write, execute" in breakdown
        assert "group: read, execute" in breakdown
        assert "others: execute" in breakdown

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Permission"

    def test_empty_input(self):
        """Test handling of empty input."""
        result = self.converter.convert("")
        assert result == {}

    def test_invalid_input(self):
        """Test handling of invalid input."""
        result = self.converter.convert("invalid")
        assert result == {}
