"""
Main entry point for the guess command-line utility.
"""

import sys
import argparse
from guess.formatter import TableFormatter
from guess.convert import try_convert
from guess.converters.number import NumberConverter
from guess.converters.timestamp import TimestampConverter
from guess.converters.duration import DurationConverter
from guess.converters.bytesize import ByteSizeConverter
from guess.converters.color import ColorConverter
from guess.converters.permission import PermissionConverter


# Mapping from command names to converter classes
COMMAND_TO_CONVERTER = {
    "time": TimestampConverter,
    "timestamp": TimestampConverter,
    "duration": DurationConverter,
    "size": ByteSizeConverter,
    "bytes": ByteSizeConverter,
    "number": NumberConverter,
    "num": NumberConverter,
    "color": ColorConverter,
    "permission": PermissionConverter,
    "perm": PermissionConverter,
}


def main():
    """
    Main entry point for the guess CLI application.

    Handles two modes of operation:
    1. Explicit type commands: guess <type> <value...>
    2. Auto-detection mode: guess <value...>
    """
    # Generate list of available commands for help text
    available_commands = ", ".join(sorted(set(COMMAND_TO_CONVERTER.keys())))

    # Define the parser and all common attributes once
    parser = argparse.ArgumentParser(
        prog="guess",
        description="Guess - Simple data format conversion utility.",
        epilog="Examples:\n"
        "  guess 1722628800              # Auto-detect input type\n"
        "  guess 2 GB                    # Auto-detect '2 GB' as a size\n"
        "  guess time 2025-08-03 12:00   # Force timestamp interpretation\n"
        "  guess color #FF5733 orange    # Force color interpretation\n"
        "  guess --help                  # Show this help message\n\n"
        f"Available converter types: {available_commands}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="guess 1.1.0")
    parser.add_argument(
        "value",
        nargs="*",
        help="Value to convert (optionally prefixed with converter type)",
    )

    args = parser.parse_args()

    if not args.value:
        parser.print_help()
        sys.exit(1)

    converter_classes = []

    # Check if first argument is a converter type
    if args.value[0] in COMMAND_TO_CONVERTER:
        # Explicit converter mode
        converter_type = args.value[0]
        if len(args.value) < 2:
            print(f"Error: {converter_type} requires a value to convert", file=sys.stderr)
            sys.exit(1)

        value_str = " ".join(args.value[1:])
        converter_classes = [COMMAND_TO_CONVERTER[converter_type]]
    else:
        # Auto-detection mode
        value_str = " ".join(args.value)
        converter_classes = list(set(COMMAND_TO_CONVERTER.values()))

    results = try_convert(
        value_str,
        [cls() for cls in converter_classes])

    if not results:
        maybe_command = args.value[0]
        if maybe_command in COMMAND_TO_CONVERTER:
            print(f"Unable to convert value as {maybe_command}", file=sys.stderr)
        elif maybe_command.isalpha():
            print(f"'{maybe_command}' is not a valid converter type.", file=sys.stderr)
            print(f"Valid types: {available_commands}", file=sys.stderr)
        else:
            print("Unable to convert input.", file=sys.stderr)
        sys.exit(1)

    formatter = TableFormatter()
    print(formatter.format_multiple_results(results))

if __name__ == "__main__":
    main()