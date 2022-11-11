"""Parse output from ``arduino-cli``."""
import shlex
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional


def lines_between(
    output_lines: List[str],
    start_phrase: str,
    end_phrase: Optional[str] = None,
) -> List[str]:
    """Subset the supplied lines into those between start_phrase and end_phrase.

    This function will return the subset of the input lines between
    start_phrase and end_phrase. These lines are non-inclusive not
    containing either the start or end phrase.

    Args:
        output_lines: lines to subset
        start_phrase: start string
        end_phrase: end string
    Returns:
        List of lines between start and end strings
    """
    start_index = output_lines.index(start_phrase)
    stop_index = -1 if end_phrase is None else output_lines.index(end_phrase)
    return output_lines[(start_index + 1) : stop_index]


def parse_compilation_commands(
    output_lines: List[str], mapping: Dict[str, Path]
) -> Dict[str, List[str]]:
    """Parse compilation commands and flags per type.

    This function will parse out each command needed to compile each of
    the types specified in the mapping object. These commands are parsed
    in the section after the "Compiling sketch..." message

    Args:
        output_lines: lines of the output of arduino-cli
        mapping: mapping of type to path to object

    Return:
        mapping of type (cpp, c, S) to a list of needed command lines (command, flags)
    """
    output_mapping = {}
    compilation_lines = lines_between(
        output_lines, 'Compiling sketch...', 'Compiling libraries...'
    )

    for file_type, path in mapping.items():
        filename = path.name
        matching_lines = filter(
            lambda compilation_line: f'{ filename }.o' in compilation_line,
            compilation_lines,
        )
        if not matching_lines:
            raise Exception(
                f'Failed to find compilation line for { filename }'
            )
        shell_split = shlex.split(list(matching_lines)[0])

        def filter_function(item: str) -> bool:
            """Filter out -o flag, input and output specifiers."""
            return (
                item != '-o'
                and not item.endswith(filename)
                and not item.endswith(f'{ filename }.o')
                and item != '-c'
            )

        necessary_command_values = list(filter(filter_function, shell_split))
        expected_command_values = shell_split[:1] + shell_split[2:-3]
        assert (
            necessary_command_values == expected_command_values
        ), f'Necessary arguments are usually all but the last 3:\n\t{necessary_command_values}\n\t{expected_command_values}'
        output_mapping[file_type] = necessary_command_values
    return output_mapping


def parse_linker_commands(output_lines: List[str]):
    """Parse out the linker and post-linker commands.

    This function will parse out the linker command as well as the post
    linker command steps. These can then be used to construct the
    necessary build steps to replace arduino-cli.

    Args:
        output_lines: lines from arduino CLI
    Return:
        List of post linker commands filtered for input / outputs
    """
    # Find lines that match the linking call
    linking_lines = lines_between(
        output_lines, 'Linking everything together...'
    )
    if not linking_lines:
        raise Exception('Failed to find linking lines')
    linker_shell_split = shlex.split(linking_lines[0])
    # Figure out the path to the core library
    core_library = filter(
        lambda item: item.endswith('core.a'), linker_shell_split
    )
    if not core_library:
        raise Exception('Failed to find core in linking line')
    core_path = Path(list(core_library)[0])

    def filter_function(item: str) -> bool:
        """Filter out -o flag, input and output specifiers."""
        return (
            item != '-o'
            and not item.endswith('ino.elf')
            and not item.endswith('.o')
            and not item.endswith('core.a')
            and not item.endswith(str(core_path.parent.parent))
        )

    necessary_command_values = list(
        filter(filter_function, linker_shell_split)
    )
    return core_path, necessary_command_values
