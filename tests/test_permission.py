"""
Tests for the permission converter.
"""

from guess.converters.permission import PermissionConverter


class TestPermissionConverter:
    """Test the permission converter functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = PermissionConverter()

    # Test get_interpretations method
    def test_get_interpretations_octal_notation(self):
        """Test interpretation of octal notation."""
        # Plain octal
        interpretations = self.converter.get_interpretations("755")
        assert len(interpretations) == 1
        assert interpretations[0].description == "octal"
        assert interpretations[0].value == 0o755

        # With 0 prefix
        interpretations = self.converter.get_interpretations("0755")
        assert len(interpretations) == 1
        assert interpretations[0].description == "octal"
        assert interpretations[0].value == 0o755

        # With 0o prefix
        interpretations = self.converter.get_interpretations("0o755")
        assert len(interpretations) == 1
        assert interpretations[0].description == "octal"
        assert interpretations[0].value == 0o755

    def test_get_interpretations_symbolic_notation(self):
        """Test interpretation of symbolic notation."""
        interpretations = self.converter.get_interpretations("rwxr-xr-x")
        assert len(interpretations) == 1
        assert (
            interpretations[0].description == "string"
        )  # Implementation uses "string" not "symbolic"
        assert interpretations[0].value == 0o755

        interpretations = self.converter.get_interpretations("rw-r--r--")
        assert len(interpretations) == 1
        assert interpretations[0].description == "string"
        assert interpretations[0].value == 0o644

        interpretations = self.converter.get_interpretations("---------")
        assert len(interpretations) == 1
        assert interpretations[0].description == "string"
        assert interpretations[0].value == 0o000

    def test_get_interpretations_decimal_equivalent(self):
        """Test interpretation of decimal equivalent."""
        interpretations = self.converter.get_interpretations("493")  # 755 in decimal
        assert len(interpretations) == 1
        assert interpretations[0].description == "decimal"
        assert interpretations[0].value == 493

        # Note: 420 is interpreted as octal "420" (not decimal), so it becomes 0o420 = 272 decimal
        interpretations = self.converter.get_interpretations("420")
        assert len(interpretations) == 1
        assert (
            interpretations[0].description == "octal"
        )  # 3-digit numbers treated as octal
        assert interpretations[0].value == 0o420  # 272 in decimal

    def test_get_interpretations_invalid_values(self):
        """Test rejection of invalid permission values."""
        assert (
            len(self.converter.get_interpretations("888")) == 0
        )  # Invalid octal digit
        assert len(self.converter.get_interpretations("rwxr-xr-xa")) == 0  # Too long
        assert len(self.converter.get_interpretations("abc")) == 0  # Invalid format
        assert len(self.converter.get_interpretations("1000")) == 0  # Out of range
        assert len(self.converter.get_interpretations("")) == 0  # Empty input

    # Test convert_value method
    def test_convert_value_basic_formats(self):
        """Test that convert_value produces all expected output formats."""
        result = self.converter.convert_value(0o755)

        assert "Symbolic" in result
        assert "Octal" in result
        assert "Decimal" in result
        assert "Breakdown" in result

        assert result["Symbolic"] == "rwxr-xr-x"
        assert result["Octal"] == "0o755"
        assert result["Decimal"] == "493"

    def test_convert_value_decimal_input(self):
        """Test conversion when input is decimal value."""
        result = self.converter.convert_value(493)  # 755 in decimal

        assert result["Symbolic"] == "rwxr-xr-x"
        assert result["Octal"] == "0o755"
        assert result["Decimal"] == "493"

    def test_convert_value_breakdown_formatting(self):
        """Test that permission breakdown is properly formatted."""
        result = self.converter.convert_value(0o755)
        breakdown = result["Breakdown"]
        assert "owner: read, write, execute" in breakdown
        assert "group: read, execute" in breakdown
        assert "others: read, execute" in breakdown

        # Test edge case with minimal permissions
        result = self.converter.convert_value(0o000)
        assert result["Symbolic"] == "---------"
        assert "owner: none" in result["Breakdown"]

    def test_get_name(self):
        """Test converter name."""
        assert self.converter.get_name() == "Permission"

    def test_choose_display_value(self):
        """Test display value selection."""
        formats = {
            "Symbolic": "rwxr-xr-x",
            "Octal": "0o755",
            "Decimal": "493",
            "Breakdown": "owner: read, write, execute, group: read, execute, others: read, execute",
        }

        # Should prefer Symbolic format
        display_value = self.converter.choose_display_value(formats, "octal")
        assert display_value == "rwxr-xr-x"

        # Should return None if Symbolic is missing
        formats_no_symbolic = {"Octal": "0o755", "Decimal": "493"}
        display_value = self.converter.choose_display_value(
            formats_no_symbolic, "octal"
        )
        assert display_value is None
