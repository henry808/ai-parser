# parser.py
#
# Example: ./main.py --input input.txt --output output.txt
# Display Help: ./main.py -h
# Check Version: ./main.py --version

import argparse

def create_parser() -> argparse.ArgumentParser:
    """
    Creates and returns the argument parser for the file processing utility.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="A utility for processing input files and generating output files."
    )

    # Input File Argument
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to the input file. Required.'
    )

    # Output File Argument
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to the output file. Required.'
    )

    # Mode Argument: choose between 'prose' and 'exchange'
    parser.add_argument(
        '-m', '--mode',
        type=str,
        choices=['prose', 'exchange'],
        default='exchange',  # Default mode is 'exchange'
        help='Mode of output. "prose" outputs only model responses, "exchange" alternates between user and model. Default is "exchange".'
    )

    # Version Argument
    parser.add_argument(
        '--version',
        action='version',
        version='ai_processor .1 alpha',
        help='Show the application version and exit.'
    )

    return parser
