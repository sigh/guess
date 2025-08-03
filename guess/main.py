"""
Main entry point for the guess command-line utility.
"""

import sys
import argparse
from guess import registry
from guess.formatter import TableFormatter


def _display_results(results, converter_name=None, value=None):
    """Formats and prints conversion results or an error message."""
    if results:
        formatter = TableFormatter()
        print(formatter.format_multiple_results(results))
        sys.exit(0)
    else:
        if converter_name and value:
            print(f"Unable to convert '{value}' as {converter_name}")
        else:
            print("Unable to convert input.")
        sys.exit(1)


def main():
    """
    Main entry point for the guess CLI application.

    Handles two modes of operation:
    1. Explicit type commands: guess <type> <value...>
    2. Auto-detection mode: guess <value...>
    """
    subcommand_info = {
        "time": "Force timestamp interpretation",
        "duration": "Force duration interpretation",
        "size": "Force byte size interpretation",
        "number": "Force number base interpretation",
        "color": "Force color interpretation",
        "permission": "Force file permission interpretation",
    }

    # Define the parser and all common attributes once
    parser = argparse.ArgumentParser(
        prog="guess",
        description="Guess - Intelligent data format conversion utility.",
        epilog="Examples:\n"
        "  guess 1722628800              # Auto-detect input type\n"
        "  guess 2 GB                      # Auto-detect '2 GB' as a size\n"
        "  guess time 2025-08-03 12:00   # Force timestamp interpretation\n"
        "  guess color #FF5733 orange     # Force color interpretation\n"
        "  guess --help                    # Show this help message",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="guess 1.1.0")

    # Check sys.argv to determine which arguments to add to the parser
    is_subcommand_mode = len(sys.argv) > 1 and sys.argv[1] in subcommand_info

    if is_subcommand_mode:
        # --- Configure parser for SUBCOMMAND MODE ---
        subparsers = parser.add_subparsers(
            dest="converter_type",
            required=True,
            help="Force a specific converter type."
        )
        for name, help_text in subcommand_info.items():
            sub_parser = subparsers.add_parser(name, help=help_text)
            sub_parser.add_argument(
                "value",
                nargs="+",
                help=f"Value(s) to convert as {name}",
            )
    else:
        # --- Configure parser for AUTO-DETECT MODE ---
        parser.add_argument(
            "value",
            nargs="*", # Use '*' to allow `guess --help` without a value
            help="Value to convert (auto-detects type)",
        )

    # Now that the parser is fully configured for the correct mode, parse the args
    args = parser.parse_args()

    # The rest of the logic remains the same
    if is_subcommand_mode:
        value_str = " ".join(args.value)
        converter = registry.get_converter_by_name(args.converter_type)
        interpretations = converter.get_interpretations(value_str)

        results = []
        if interpretations:
            for interpretation in interpretations:
                formats = converter.convert_value(interpretation.value)
                if formats:
                    results.append({
                        "converter_name": converter.get_name(),
                        "interpretation_description": interpretation.description,
                        "formats": formats,
                    })

        _display_results(results, converter_name=args.converter_type, value=value_str)
    else:
        if not args.value:
            parser.print_help()
            sys.exit(1)

        value_str = " ".join(args.value)
        results = registry.try_convert(value_str)
        _display_results(results)


if __name__ == "__main__":
    main()