import os
import sys

# Add the 'graspi_igraph' directory to sys.path
sys.path.insert(0, os.path.abspath('../../../py-graspi'))  # Adjust if necessary
sys.path.insert(0, os.path.abspath('../../graspi_igraph'))

# -- Project information -----------------------------------------------------
project = 'py-graspi'
copyright = '2024, Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'
author = 'Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Generate documentation from docstrings
    'sphinx.ext.napoleon',     # Support for Google/NumPy style docstrings
    'sphinx.ext.viewcode',     # Link to highlighted source code
    'sphinx.ext.autosummary',  # Automatically generate summary tables
]

# Generate autosummary files automatically
autosummary_generate = True

templates_path = ['_templates']

# Exclude setup.py and other irrelevant files
exclude_patterns = [
    '**/setup.py',         # Exclude setup.py everywhere
    'api/setup.rst',       # Exclude generated setup.rst
    '**/test.py',         # Exclude setup.py everywhere
    'api/graspi_igraph.tests.rst',       # Exclude generated setup.rst
    '_build',              # Exclude the build directory
    'Thumbs.db', '.DS_Store',  # Ignore OS-specific files
]

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_baseurl = 'https://owodolab.github.io/py-graspi/'

# Autodoc options for generating detailed class/function documentation
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}

# Mock imports for packages that may not be available during documentation build
autodoc_mock_imports = ["matplotlib", "mpl_toolkits.mplot3d"]

