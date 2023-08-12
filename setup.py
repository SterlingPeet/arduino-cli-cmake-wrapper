#!/usr/bin/env python3
"""Setup script to install the ``arduino-cli-cmake-wrapper`` package."""

import re
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    """Read file and return contents as a string."""
    with Path(__file__).parent.joinpath(*names).open(
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='arduino-cli-cmake-wrapper',
    version='0.0.0',
    license='Apache-2.0',
    description='Arduino Cmake toolchain leveraging ``arduino-cli`` via python wrapper script',
    long_description='{}\n{}'.format(
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
            '', read('README.rst')
        ),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
    ),
    author='Sterling Lewis Peet',
    author_email='sterling.peet@ae.gatech.edu',
    url='https://github.com/SterlingPeet/arduino-cli-cmake-wrapper',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[path.stem for path in Path('src').glob('*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://arduino-cli-cmake-wrapper.readthedocs.io/',
        'Changelog': 'https://arduino-cli-cmake-wrapper.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.7',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'arduino-cli-wrapper = arduino_cli_cmake_wrapper.cli:main',
        ]
    },
)
