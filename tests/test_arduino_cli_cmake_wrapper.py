"""Test ``arduino_cli_cmake_wrapper`` module functions and classes."""

import pytest

from arduino_cli_cmake_wrapper.cli import main


def test_main():
    """Test ``arduino_cli_cmake_wrapper`` main module."""
    with pytest.raises(SystemExit) as exit_info:
        main(['--help'])
    assert exit_info.value.code == 0
