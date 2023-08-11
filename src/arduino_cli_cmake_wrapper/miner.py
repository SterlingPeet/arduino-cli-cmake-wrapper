"""Data mining operations on the build stage data.

Handles the data mining operations on the output of the build stages.
"""
import logging
from functools import partial
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from .types import ArduinoCLIException
from .types import FilterProtocol
from .types import MissingStageException
from .types import MultipleInvocationException
from .types import Source
from .types import Stage
from .util import match_all
from .util import match_any
from .util import safe_split
from .util import string_dictionary_of_list

LOGGER = logging.getLogger(__name__)


def real_source_names(source_mappings: Dict[Source, Path]):
    """Get the real source names from the source map."""
    return {
        source: value.name if source != Source.INO else f'{value.name}.cpp'
        for source, value in source_mappings.items()
    }


def filter_by_flags(
    flags: Dict[str, bool], tokens: List[str], negate=False
) -> List[str]:
    """Filter a set of tokens based on a set of flags.

    Reduce the set of tokens to ensure that it does not include any of
    the matching flags, unless negate is specified then only the
    matching flags are exposed. Tokens is a list of tokens, and flags is
    a dictionary of the flag (e.g. -c) to a boolean indicating if the
    flag takes an argument.

    Args:
        flags: flag to argument boolean dictionary
        tokens: tokens to filter
        negate: restrict to matching flags

    Returns:
        list of filter tokens
    """

    def filterer(token: str, previous: Union[None, str]):
        """Filter function taking current and previous token."""
        value = match_any(flags.keys(), token[:2])
        value = value or match_any(
            [
                flag
                for flag, check in flags.items()
                if (callable(check) and check(previous))
                or (not callable(check) and check)
            ],
            previous[:2],
        )
        return not value if negate else value

    return [
        token
        for index, token in enumerate(tokens)
        if not filterer(token, tokens[max(0, index - 1)])
    ]


def filter_by_filenames(
    filenames: List[str], tokens: List[str], negate=False
) -> List[str]:
    """Filter a set of tokens based on a set of filenames.

    Filter a list of tokens by a list of filenames. In normal operation
    these filenames are removed. If negate is specified then only those
    tokens are kept.

    Args:
        filenames: flag to argument boolean dictionary
        tokens: tokens to filter
        negate: restrict to matching filenames

    Returns:
        list of filter tokens
    """

    def filterer(item: str):
        """Filter that can also negate."""
        value = match_any(filenames, item)
        return not value if negate else value

    filtered_tokens = [token for token in tokens if not filterer(token)]
    return filtered_tokens


def build_tokens(
    stages: Dict[Stage, List[str]], sources: Dict[Source, Path]
) -> Tuple[
    Dict[Source, str], Dict[Source, List[str]], Dict[Source, List[str]]
]:
    """Detect command line build tokens for each source type.

    Looks at the source build invocation for each file in the source
    mapping, and determines the command line arguments used for the
    build of that source file. The <source file>, <source_file>.o and -o
    flag proceeding the .o are all removed as these depend on the name
    of the source. The resulting tokens are split into three values:
    tool used for compiling the source, build tokens, and include
    directories. These are each indexed by source type.

    Args:
        stages: parsed and annotated build information
        sources: mapping of source type to test source used

    Return:
        tuple of dictionaries: source to compiler, source to include paths, and source to build flags
    """
    real_names = real_source_names(sources)
    source_lines = {
        source: identify_line(
            Stage.COMPILATION,
            stages,
            partial(match_all, [f'{real_names.get(source)}[ |$]']),
        )
        for source in Source
    }

    def cleaner(items: List[str]) -> List[str]:
        """Clean out -c -o <arg> and filename arguments."""
        return filter_by_filenames(
            list(real_names.values()),
            filter_by_flags({'-c': False, '-o': True}, items),
        )

    sorter = partial(filter_by_flags, {'-I': lambda item: item == '-I'})

    sorted_source_lines = {
        source: sort_line(line, cleaner, sorter)
        for source, line in source_lines.items()
    }
    tools = {source: sorted_source_lines[source][0] for source in Source}
    non_include_paths = {
        source: sorted_source_lines[source][1] for source in Source
    }
    include_paths = {
        source: [
            path.replace('-I', '')
            for path in sorted_source_lines[source][2]
            if path != '-I'
        ]
        for source in Source
    }
    LOGGER.debug(
        'Detected compilers:\n\t%s',
        '\n\t'.join([f'{source}: {value}' for source, value in tools.items()]),
    )
    LOGGER.debug(
        'Detected include paths:%s', string_dictionary_of_list(include_paths)
    )
    LOGGER.debug(
        'Detected build flags:%s', string_dictionary_of_list(non_include_paths)
    )

    return tools, include_paths, non_include_paths


def sketch_cache(stages: Dict[Stage, List[str]]) -> Path:
    """Detect the sketch cache Arduino uses.

    Detects the cache used by Arduino for compiling the core, generating
    precompiled headers, and other scratch work that this tool can
    borrow as output.

    Args:
        stages: stages of the build output
    Return:
        path to Arduino cache directory
    """
    core_lines = stages.get(Stage.CORE)
    if not core_lines:
        raise MissingStageException(Stage.CORE)

    core_tokens = [
        token
        for token in safe_split(core_lines[-1])
        if token.endswith('core.a')
    ]
    assert core_tokens, 'Could not find core.a'
    core_archive = core_tokens[0]
    cache = Path(core_archive).parent.parent
    LOGGER.debug('Found Arduino sketch cache: %s', cache)
    return cache


def identify_line(
    stage: Stage,
    stages: Dict[Stage, List[str]],
    match: Callable[[str], bool],
    single: bool = True,
) -> str:
    """Identify a line based on the given stage and criteria.

    Args:
    - stage: The current stage to identify lines for.
    - stages: A dictionary mapping stages to lists of lines.
    - match: A function that checks if a line matches a certain condition.
    - single: If True (default), raises an exception if multiple matching lines are found.

    Returns:
    - The identified line (str).

    Raises:
    - MissingStageException: If no lines are found for the given stage.
    - MultipleInvocationException: If multiple matching lines are found when 'single' is True.
    """
    stage_lines = stages.get(stage, [])
    matching_lines = [line for line in stage_lines if match(line)]
    if not matching_lines:
        raise MissingStageException(stage)
    if single and len(matching_lines) > 1:
        print('\n'.join(matching_lines))
        raise MultipleInvocationException
    return matching_lines[0]


def sort_line(
    line: str, clean: FilterProtocol = None, sort: FilterProtocol = None
) -> Tuple[str, List[str], List[str]]:
    """Sort and process a line using filtering operations.

    This function takes a line of text and applies filtering and sorting
    operations on its tokens. The 'clean' filter is applied first to the
    tokens, followed by the 'sort' filter. The processed tokens are then
    used to construct a tuple containing the original command, sorted
    tokens, and sorted tokens in reverse order (negated).

    Args:
        line (str): The line to be processed.
        clean (FilterProtocol, optional): The filter to clean the tokens.
            Defaults to None.
        sort (FilterProtocol, optional): The filter to sort the tokens.
            Defaults to None.

    Returns:
        Tuple[str, List[str], List[str]]: A tuple containing the original
            command, sorted tokens, and sorted tokens in reverse order
            (negated).

    Raises:
        ArduinoCLIException: If no tokens are available after filtering.
    """
    clean = clean if clean else FilterProtocol.pass_all
    sort = sort if sort else FilterProtocol.pass_all

    tokens = clean(safe_split(line))
    if not tokens:
        raise ArduinoCLIException('No tokens available')
    return (tokens[0], sort(tokens[1:]), sort(tokens[1:], negate=True))


def identify_link_line(
    stages: Dict[Stage, List[str]], source_objects: List[str]
) -> str:
    """Identify the linking line based on source object names.

    This function identifies the linking line within the context of the
    LINK stage. It searches for lines within the LINK stage's list of
    lines and matches them against the provided source object names. The
    identified line is then returned.

    Args:
        stages (Dict[Stage, List[str]]): A dictionary mapping stages to
            lists of lines.
        source_objects (List[str]): List of source object names to match.

    Returns:
        str: The identified linking line.

    See Also:
        identify_line: A general function to identify lines based on
            stages and criteria.
    """
    link_line = identify_line(
        Stage.LINK, stages, partial(match_all, source_objects)
    )
    LOGGER.debug('Linking line: %s', link_line)
    return link_line


def identify_archive_line(stages: Dict[Stage, List[str]]) -> str:
    r"""Identify the archive line within the CORE stage.

    This function identifies the archive line within the context of the
    CORE stage. It searches for lines within the CORE stage's list of
    lines and matches them against the regular expression ``core\.a``.
    The identified archive line is then returned.

    Args:
        stages (Dict[Stage, List[str]]): A dictionary mapping stages to
            lists of lines.

    Returns:
        str: The identified archive line within the CORE stage.

    See Also:
        identify_line: A general function to identify lines based on
            stages and criteria.
    """
    archive_line = identify_line(
        Stage.CORE, stages, partial(match_all, [r'core\.a']), single=False
    )
    LOGGER.debug('Archive line: %s', archive_line)
    return archive_line


def link_tokens(
    stages: Dict[Stage, List[str]], sources: Dict[Source, Path]
) -> Tuple[str, List[str], List[str], List[str]]:
    """Extract linker, flags, objects, and libraries from the link line.

    This function identifies the link line within the context of the
    LINK stage using the `identify_link_line` function. It then extracts
    the linker, link flags, link objects, and link libraries from the
    link line using the `sort_line` function with the appropriate
    cleaning and sorting filters.

    Parameters:
        stages (Dict[Stage, List[str]]): A dictionary mapping stages to
            lists of lines.
        sources (Dict[Source, Path]): A dictionary mapping source types to
            their corresponding paths.

    Returns:
        Tuple[str, List[str], List[str], List[str]]: A tuple containing the
            identified linker, a list of link flags, a list of link objects,
            and a list of link libraries.
    """
    object_names = [
        f'{name}.o' for name in real_source_names(sources).values()
    ]
    link_line = identify_link_line(stages, object_names)

    def cleaner(items: List[str]) -> List[str]:
        """Clean out -c -o <arg> and filename arguments."""
        return filter_by_filenames(
            object_names, filter_by_flags({'-o': True}, items)
        )

    link_sorter = partial(
        filter_by_filenames,
        [r'\.o$', r'\.a$', r'^-l', '--start-group$', '--end-group$'],
    )
    linker, link_flags, linkables = sort_line(link_line, cleaner, link_sorter)

    link_objects = filter_by_filenames([r'\.o$'], linkables, negate=True)
    link_libraries = filter_by_filenames(
        [r'\.a$', r'^-l', '--start-group$', '--end-group$'],
        linkables,
        negate=True,
    )

    LOGGER.debug('Detected linker: %s', linker)
    LOGGER.debug('Detected linker flags:\n\t%s', '\n\t'.join(link_flags))
    LOGGER.debug('Detected link libraries:\n\t%s', '\n\t'.join(link_libraries))
    LOGGER.debug('Detected link objects:\n\t%s', '\n\t'.join(link_objects))
    return linker, link_flags, link_objects, link_libraries


def archive_tokens(stages: Dict[Stage, List[str]]) -> Tuple[str, List[str]]:
    """Extract archive tool and flags from the archive line.

    This function identifies the archive line within the context of the
    CORE stage using the `identify_archive_line` function. It then
    extracts the archiver, archive flags, and ignored list from the
    archive line using the `sort_line` function with the appropriate
    cleaning and sorting filters.

    Parameters:
        stages (Dict[Stage, List[str]]): A dictionary mapping stages to
            lists of lines.

    Returns:
        Tuple[str, List[str]]: A tuple containing the identified archiver
            and a list of archive flags.

    Raises:
        AssertionError: If the ignored list from sorting is not empty.
    """
    archive_line = identify_archive_line(stages)
    archive_cleaner = partial(filter_by_filenames, [r'core\.a', r'\.o'])
    archiver, archive_flags, _ = sort_line(archive_line, archive_cleaner)
    assert _ == [], 'Sort list not empty'

    LOGGER.debug('Detected archive tool: %s', archiver)
    LOGGER.debug('Detected archive flags:\n\t%s', '\n\t'.join(archive_flags))
    return archiver, archive_flags


def post_link_lines(
    stages: Dict[Stage, List[str]], sources: Dict[Source, Path]
) -> List[str]:
    """Get the post-link steps based on identified link line.

    This function extracts the post-link steps from the lines following
    the identified linking line within the context of the LINK stage.
    It first generates a list of object names from the provided sources,
    then identifies the linking line using the object names. Subsequently,
    it extracts the lines that follow the identified link line and returns
    them as a list of post-link steps.

    Args:
        stages (Dict[Stage, List[str]]): A dictionary mapping stages to
            lists of lines.
        sources (Dict[Source, Path]): A dictionary mapping source types to
            their corresponding paths.

    Returns:
        List[str]: A list of post-link steps following the identified
            linking line.

    See Also:
        identify_link_line: A function to identify the linking line based
            on source object names.
    """
    object_names = [
        f'{name}.o' for name in real_source_names(sources).values()
    ]
    link_line = identify_link_line(stages, object_names)
    stage_lines = stages.get(Stage.LINK, [])
    post_links = stage_lines[stage_lines.index(link_line) + 1 :]

    LOGGER.debug('Post link steps:\n\t%s', '\n\t'.join(post_links))
    return post_links
