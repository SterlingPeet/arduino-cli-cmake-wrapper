"""Harvest the Arduino CLI for compilation arguments.

This script harvests the command line arguments, compiler/linker
commands, and built archive from a build of a test INO file in Arduino.
This allows the program to know how arduino should compile C and C++
files.
"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

from .parse import parse_compilation_commands
from .parse import parse_linker_commands
from .sketch import compile_sketch
from .sketch import make_sketch

HELP_TEXT = """Tool used to parse settings from a compilation run of Arduino CLI.

This tool will run a test compilation
"""


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """Parse input arguments to influence the execution.

    The script needs to know where to copy the core library into the
    build system. Additionally, the board target is needed in order to
    properly compile. These settings are parsed out of the command line
    input arguments using the argparse module.

    Args:
        arguments: command line argument list to be parsed

    Returns:
        Namespace containing parsed arguments
    """
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument(
        '-b',
        '--board',
        type=str,
        help='Target board FQBN supplied to the arduino build',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output',
        type=Path,
        help='Output destination for the pre-compiled arduino core',
        required=True,
    )
    return parser.parse_args(arguments)


def main(arguments: List[str] = None):
    """Perform entrypoint functions."""
    arguments = parse_arguments(arguments)

    with tempfile.TemporaryDirectory() as directory:
        try:
            directory = Path(directory)
            mappings = make_sketch(directory)
            compile_output = compile_sketch(arguments.board, directory)

            output_lines = compile_output.split('\n')
            command_mappings = parse_compilation_commands(
                output_lines, mappings
            )
            core_path, linker_args = parse_linker_commands(output_lines)

            core_destination = arguments.output / core_path.name
            shutil.copy2(core_path, core_destination)

            # Output destined for CMake
            print(str(core_destination), end=';')
            for output_type in ['S', 'c', 'cpp']:
                print(command_mappings[output_type][0], end=';')
                print('|'.join(command_mappings[output_type][1:]), end=';')
            print(linker_args[0], end=';')
            print('|'.join(linker_args[1:]), end=';')
        except Exception as exc:
            print(
                f'[ERROR] Problem occurred while mining Arduino. {exc}',
                file=sys.stderr,
            )
            return 1
    return 0
