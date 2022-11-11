"""Configure the ``sphinx`` documentation build for the project."""

import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'Arduino CLI Wrapper for CMake'
year = '2022'
author = 'Sterling Lewis Peet'
copyright = f'{year}, {author}'
version = release = '0.0.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': (
        'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/issues/%s',
        '#',
    ),
    'pr': (
        'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/pull/%s',
        'PR #',
    ),
}
# FIXME: remove these exceptions when the links are made real
linkcheck_ignore = [
    r'https://arduino-cli-cmake-wrapper.readthedocs.io/',
    r'https://pypi.org/project/arduino-cli-cmake-wrapper',
]
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
    '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = f'{project}-{version}'

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
