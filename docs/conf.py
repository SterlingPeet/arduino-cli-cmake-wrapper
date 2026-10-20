"""Configure the ``sphinx`` documentation build for the project."""

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
year = '2022-2024'
author = 'Sterling Lewis Peet'
copyright = f'{year}, {author}'
try:
    from importlib.metadata import version as distribution_version

    version = release = distribution_version('arduino-cli-cmake-wrapper')
except Exception:
    import traceback

    traceback.print_exc()
    version = release = '0.0.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': (
        'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/issues/%s',
        '#%s',
    ),
    'pr': (
        'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/pull/%s',
        'PR #%s',
    ),
}
# FIXME: remove these exceptions when the links are made real
linkcheck_ignore = [
    r'https://arduino-cli-cmake-wrapper.readthedocs.io/',
    r'https://pypi.org/project/arduino-cli-cmake-wrapper',
]

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'githuburl': 'https://github.com/SterlingPeet/arduino-cli-cmake-wrapper/',
}

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_short_title = f'{project}-{version}'

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
