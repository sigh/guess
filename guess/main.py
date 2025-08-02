"""
Main entry point for the guess command-line utility.
"""

import sys
import argparse
from guess import registry
from guess.formatter import TableFormatter


def main():
    """
    Main entry point for the guess CLI application.

    Handles two modes of operation:
    1. Explicit type commands: guess <type> <value>
    2. Auto-detection mode: guess <value>

    In explicit type mode, forces interpretation using a specific converter.
    In auto-detection mode, tries all converters and shows multiple interpretations.

    Args:
        None (uses sys.argv for command-line arguments)

    Returns:
        None (exits with code 0 on success, 1 on error)

    Examples:
        guess 255                    # Multi-interpretation mode
        guess number 255             # Force number conversion
        guess time 1722628800        # Force timestamp conversion
        guess --help                 # Show help
    """
    # Check if first argument is a known subcommand
    subcommands = ["time", "duration", "size", "number"]

    if len(sys.argv) > 1 and sys.argv[1] in subcommands:
        # Use subcommand parser
        parser = argparse.ArgumentParser(
            description="Guess - Intelligent data format conversion utility",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        subparsers = parser.add_subparsers(
            dest="converter_type", help="Force specific converter type"
        )

        # Time/timestamp subcommand
        time_parser = subparsers.add_parser(
            "time", help="Force timestamp interpretation"
        )
        time_parser.add_argument("value", help="Value to convert as timestamp")

        # Duration subcommand
        duration_parser = subparsers.add_parser(
            "duration", help="Force duration interpretation"
        )
        duration_parser.add_argument("value", help="Value to convert as duration")

        # Size/byte size subcommand
        size_parser = subparsers.add_parser(
            "size", help="Force byte size interpretation"
        )
        size_parser.add_argument("value", help="Value to convert as byte size")

        # Number subcommand
        number_parser = subparsers.add_parser(
            "number", help="Force number base interpretation"
        )
        number_parser.add_argument("value", help="Value to convert as number")

        args = parser.parse_args()

        # Handle explicit converter type
        converter = registry.get_converter_by_name(args.converter_type)
        if converter and converter.can_convert(args.value):
            formats = converter.convert(args.value)
            if formats:
                formatter = TableFormatter()
                result = [{"converter_name": converter.get_name(), "formats": formats}]
                print(formatter.format_multiple_results(result))
                return

        print(f"Unable to convert '{args.value}' as {args.converter_type}")
        sys.exit(1)

    else:
        # Use simple parser for auto-detection
        parser = argparse.ArgumentParser(
            description="Guess - Intelligent data format conversion utility",
            epilog="Examples:\n"
            "  guess 255              # Convert number to different bases\n"
            "  guess 1234567890       # Show multiple interpretations\n"
            "  guess time 1722628800  # Force timestamp interpretation\n"
            "  guess number 255       # Force number interpretation\n"
            "  guess --help           # Show this help message",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument(
            "value", nargs="?", help="Value to convert (auto-detect type)"
        )

        parser.add_argument("--version", action="version", version="guess 1.0.0")

        args = parser.parse_args()

        if not args.value:
            parser.print_help()
            sys.exit(1)

        # Try all converters and get results
        results = registry.try_convert(args.value)

        # Format and display results
        formatter = TableFormatter()

        if results:
            output = formatter.format_multiple_results(results)
            print(output)
        else:
            print("Unable to convert input")
            sys.exit(1)


if __name__ == "__main__":
    main()
