================================
🎉 Arduino CLI Wrapper for CMake
================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - 🔨 Code
      - | |black| |isort| |ruff| |contributors| |commit| |license| |semver|
    * - 📝 Docs
      - | |gitmoji| |docs| |docformatter| |mypy| |docstyle| |gitchangelog|
    * - 🧪 Tests
      - | |github-actions| |pre-commit|
    * - 📦️ Package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|


.. |black| image:: https://img.shields.io/badge/%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: The Uncompromising Code Formatter

.. |isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1
    :target: https://pycqa.github.io/isort/
    :alt: isort your imports, so you don't have to

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
    :target: https://github.com/charliermarsh/ruff
    :alt: An extremely fast Python linter, written in Rust

.. |contributors| image:: https://img.shields.io/github/contributors/SterlingPeet/arduino-cli-cmake-wrapper
    :target: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/graphs/contributors
    :alt: Contributors to this project

.. |commit| image:: https://img.shields.io/github/last-commit/SterlingPeet/arduino-cli-cmake-wrapper

.. |license| image:: https://img.shields.io/badge/License-Apache_2.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache Software License 2.0

.. |semver| image:: https://img.shields.io/badge/Semantic%20Versioning-2.0.0-brightgreen.svg?style=flat
    :target: https://semver.org/
    :alt: Semantic Versioning - 2.0.0

.. |gitmoji| image:: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg
    :target: https://github.com/carloscuesta/gitmoji
    :alt: Gitmoji Commit Messages

.. |docs| image:: https://readthedocs.org/projects/arduino-cli-cmake-wrapper/badge/?style=flat
    :target: https://arduino-cli-cmake-wrapper.readthedocs.io/
    :alt: Documentation Status

.. |docformatter| image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: Docformatter

.. |mypy| image:: https://img.shields.io/badge/types-Mypy-blue.svg
    :target: https://github.com/python/mypy
    :alt: Mypy

.. |docstyle| image:: https://img.shields.io/badge/%20style-google-3666d6.svg
    :target: https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings
    :alt: Documentation Style

.. |gitchangelog| image:: https://img.shields.io/badge/changes-gitchangelog-76b5c5
    :target: https://github.com/vaab/gitchangelog
    :alt: Changelog from Git Log

.. |github-actions| image:: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/actions

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |version| image:: https://img.shields.io/pypi/v/arduino-cli-cmake-wrapper.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/arduino-cli-cmake-wrapper

.. |wheel| image:: https://img.shields.io/pypi/wheel/arduino-cli-cmake-wrapper.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/arduino-cli-cmake-wrapper

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/arduino-cli-cmake-wrapper.svg
    :alt: Supported versions
    :target: https://pypi.org/project/arduino-cli-cmake-wrapper

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/arduino-cli-cmake-wrapper.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/arduino-cli-cmake-wrapper

.. |commits-since| image:: https://img.shields.io/github/commits-since/SterlingPeet/arduino-cli-cmake-wrapper/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/compare/v0.0.0...main



.. end-badges

Arduino Cmake toolchain leveraging ``arduino-cli`` via python wrapper script.
It does not intend to replace the ``arduino-cli`` tool, nor is it intended to be a full featured IDE-like solution.

This project seeks to programmatically scrape up the necessary parts of the compile and link calls from the ``arduino-cli`` tool, set CMake variables, and allow a CMake project to roughly emulate the Arduino compile process.

The goal is to make it possible to leverge the Arduino libraries in a CMake-bound framework, for Arduino supported targets.
If you just want to compile a normal Arduino project from the command line, skip this project and CMake altogether and just use the ``arduino-cli`` as intended.

On the other hand, if you are trying to use a CMake-bound project as the primary development process, you need a way to extract the working compile process from the Arduino IDE and reformat it into a CMake Toolchain.

E.g.: To compile an `F Prime`_ project for an Arduino target using Arduino libraries, you need a shim like this to avoid hard dependence on the exact version or Arduino, Arduino Core, and the specific versions of installed libraries.

🚀 Installation
===============

Most typically, the cmake tooling is included as a git submodule in your project, or it is
included as an external project dependency.  If you want to install the python wrapper
directly, it can be done like this::

    pip install arduino-cli-cmake-wrapper

You can also install the in-development version with::

    pip install https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/archive/main.zip


📝 Documentation
================

During initial development, documentation is sparse.
It should be set up on readthedocs when the project is mature.

https://arduino-cli-cmake-wrapper.readthedocs.io/


🤝 Contributing and Development
===============================

If you are working on developing the software, head on over to the
`Developer Notes`_ page for orientation and quick reference.
You can also take a look at the `Contributing Guide`_.

🌎 Similar Projects
===================

This project was not created in a vacuum.
Here is a list of projects that came before this one and why they are different or not appropriate.

#. `Arduino CMake`_: Original project to compile for Arduino in CMake, abandoned circa 2014
#. `Arduino-CMake NG`_: Next Generation Arduino CMake tool, abandoned circa 2018, `officially abandoned in 2020 <https://github.com/arduino-cmake/Arduino-CMake-NG/issues/100>`_
#. `Arduino CMake Toolchain`_: Named successor to NG, Abandoned almost immediately thereafter, circa 2020
#. `Arduino AVR CMake`_: AVR-only CMake toolchain with support for VScode, intended as a template `as explained on the Arduino forum <https://forum.arduino.cc/t/cmake-with-arduino/897587/5>`_

.. _`F Prime`: https://github.com/nasa/fprime
.. _Developer Notes: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/blob/main/DEVELOPER_NOTES.rst
.. _Contributing Guide: https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/blob/main/CONTRIBUTING.rst
.. _`Arduino CMake`: https://github.com/queezythegreat/arduino-cmake
.. _`Arduino-CMake NG`: https://github.com/arduino-cmake/Arduino-CMake-NG
.. _`Arduino CMake Toolchain`: https://github.com/a9183756-gh/Arduino-CMake-Toolchain
.. _`Arduino AVR CMake`: https://github.com/tttapa/Arduino-AVR-CMake
