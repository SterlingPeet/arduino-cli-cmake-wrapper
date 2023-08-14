"""Utility functions for the Arudino wrapper."""
import re
import shlex
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List


def match_any(matches: Iterable[str], item: str) -> bool:
    """Return true iff item matches anything in the list."""
    matchers = [re.compile(pattern) for pattern in matches]
    for potential in matchers:
        if potential.search(item) is not None:
            return True
    return False


def match_all(matches: Iterable[str], item: str) -> bool:
    """Return true iff item matches all items in the list."""
    matchers = [re.compile(pattern) for pattern in matches]
    for potential in matchers:
        if potential.search(item) is None:
            return False
    return True


def get_path_from_flag(item: str) -> Path:
    """Extract a path from a given flag."""
    if item.startswith('-'):
        try:
            return Path(item[item.index('=') + 1 :])
        except ValueError:
            return Path(item[2:])
    return Path(item)


def safe_split(line: str, ignore_errors: bool = False) -> List[str]:
    """Split a line based on shell rules in a verbose manner.

    Shell rules split based on spaces, quotes, etc. This function will
    attempt to split the line based on these rules, and reports an error
    with the failing line's text should an error occur.  If
    ignore_errors is True, an empty list is returned such that is can be
    called safely when errors are otherwise handled.

    Args:
        line: line to split into shell tokens
        ignore_errors: return [] instead of raising an exception on error

    Returns:
        list of shell tokens that compose the line, [] on error when ignore_errors is True
    """
    try:
        return shlex.split(line.strip())
    except ValueError as ve:
        if ignore_errors:
            return []
        raise ValueError(f"{ve} in '{line}'") from ve


def prefixed_join(join_string: str, lines: List[str]) -> str:
    """Join with the join string including join string as prefix."""
    return f'{join_string}{join_string.join(lines)}'


def string_dictionary_of_list(mapping: Dict[Any, List[str]], base_indent=1):
    """Print the build sections to standard output."""
    joiner = '\n' + ('\t' * base_indent)
    return prefixed_join(
        joiner,
        [
            f'{key}' + prefixed_join(joiner + '\t', lines)
            for key, lines in mapping.items()
        ],
    )
