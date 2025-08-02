"""
Simple integration tests for the guess CLI application.
"""

import subprocess
import sys


def test_basic_number_conversion():
    """Test basic number conversion works end-to-end."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "255"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 0
    assert "0xff" in result.stdout
    assert "0b11111111" in result.stdout


def test_help_command():
    """Test help command works."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "--help"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 0
    assert "Guess - Intelligent data format conversion utility" in result.stdout


def test_explicit_type_command():
    """Test explicit type commands work."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "number", "255"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 0
    assert "Hexadecimal" in result.stdout
    assert "0xff" in result.stdout


def test_duration_with_units():
    """Test duration parsing with units."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "1h30m"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 0
    assert "1 hour, 30 minutes" in result.stdout


def test_byte_size_with_units():
    """Test byte size parsing with units."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "1GB"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 0
    assert "1,000,000,000" in result.stdout


def test_error_handling():
    """Test error handling for invalid input."""
    result = subprocess.run(
        [sys.executable, "-m", "guess", "invalid-input"],
        capture_output=True,
        text=True,
        cwd="/Users/sigh/Projects/guess",
    )
    assert result.returncode == 1
    assert "Error" in result.stdout or "Unable" in result.stdout
