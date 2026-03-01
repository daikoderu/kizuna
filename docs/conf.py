# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path


# ---- PYTHONPATH configuration ----

sys.path.insert(0, str(Path(__file__).parent))


# ---- Project information ----
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Kizuna'
author = 'Daniel Pérez Porras "Daikoderu"'

# noinspection PyShadowingBuiltins
copyright = f'2026, {author}'


# ---- General configuration ----
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
]

templates_path = []
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]


# ---- Options for HTML output ----
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = []
