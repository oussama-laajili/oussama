# docs/conf.py
import os
import sys


sys.path.insert(0, os.path.abspath('..'))  # so 'core' and 'models' import

project = 'Traffic'
copyright = '2025, Ahmed'
author = 'Ahmed'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',   # optional, for Google/NumPy docstrings
    'sphinx.ext.viewcode'    # optional, adds [source] links
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'     # or 'sphinx_rtd_theme' if you install it
html_static_path = ['_static']
