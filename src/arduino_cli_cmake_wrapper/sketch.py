"""Generate and compile Arduino sketches."""
import subprocess
from pathlib import Path
from typing import Dict


def make_sketch(directory: Path) -> Dict[str, Path]:
    """Create a sketch folder with at least a C, C++, and assembly file.

    Arduino must compile sketches and in order to determine the
    necessary compilation information we must create a sketch that uses
    each of these constructs for compilation. This function will
    generate a sketch using these constructs and return the mapping of
    the type extension (c, cpp, S) to the path to that created file

    Args:
        directory: directory to create the sketch within

    Returns:
        mapping between file extension string and temporary file
    """
    mappings = {
        extension: directory / f'special_input_file.{ extension }'
        for extension in ['S', 'c', 'cpp']
    }
    for _, path in mappings.items():
        path.touch()
    # Create main sketch as an ino file such that it is a valid sketch
    with open((directory / f'{ directory.name }.ino'), 'w') as file_handle:
        # file_handle.write("#include <TimerOne.h>\nvoid setup() {}\nvoid loop() {}")
        file_handle.write('void setup() {}\nvoid loop() {}')
    return mappings


def compile_sketch(board: str, directory: Path) -> str:
    """Compile the sketch to product core and output text.

    This will compile a sketch directory and produce the necessary core
    archive and output text. This information is created with the
    --clean flag to prevent cross-talk from any other builds. The board
    to compile against is passed in along with the directory containing
    the sketch. In order to capture all necessary information this
    command is run in verbose mode.

    Args:
        directory: sketch directory to compile
        board: compile board target FQBN

    Returns:
        standard out of the compiled sketch run
    """
    process_return = subprocess.run(
        # ["arduino-cli", "compile", "-v", "--clean", "-b", board, "--build-property", "build.extra_flags=-DTIMER1_A_PIN=13 -DTIMSK1=TIMSK", str(directory)],
        [
            'arduino-cli',
            'compile',
            '-v',
            '--clean',
            '-b',
            board,
            str(directory),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return process_return.stdout
