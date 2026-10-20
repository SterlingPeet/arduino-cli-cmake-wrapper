"""Test ``arduino_cli_cmake_wrapper.miner`` link and core archive detection."""

import shlex
from pathlib import Path

from arduino_cli_cmake_wrapper.miner import expand_grouped_response_files
from arduino_cli_cmake_wrapper.miner import sketch_cache
from arduino_cli_cmake_wrapper.types import Stage


def test_sketch_cache_with_trailing_core_step():
    """Find core.a when another step follows the archive (newer esp32 cores)."""
    stages = {
        Stage.CORE: [
            'gcc -c core/main.cpp -o /cache/core/main.cpp.o',
            'gcc-ar cr /cache/core/core.a /cache/core/main.cpp.o',
            '/usr/bin/env bash -c ": > \'/cache/file_opts\'"',
        ]
    }
    assert sketch_cache(stages) == Path('/cache')


def test_expand_grouped_response_files(tmp_path):
    """Expand a response file inside a group and keep the others (esp32 3.x)."""
    ld_flags = tmp_path / 'ld_flags'
    ld_libs = tmp_path / 'ld_libs'
    ld_libs.write_text('-lxtensa -lfreertos\n')
    # Quoted as the esp32 core quotes them, which keeps Windows paths intact
    line = (
        f'g++ "@{ld_flags}" -Wl,--start-group sketch.o core.a "@{ld_libs}" '
        f'-Wl,--end-group "@{ld_libs}" -o sketch.elf'
    )
    assert shlex.split(expand_grouped_response_files(line)) == [
        'g++',
        f'@{ld_flags}',
        '-Wl,--start-group',
        'sketch.o',
        'core.a',
        '-lxtensa',
        '-lfreertos',
        '-Wl,--end-group',
        f'@{ld_libs}',
        '-o',
        'sketch.elf',
    ]
