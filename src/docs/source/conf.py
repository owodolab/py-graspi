import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))
sys.path.insert(0, os.path.abspath('../../..'))
print(f"TEST: {os.path.abspath('../../..')}")


project = 'py-graspi'
copyright = '2024, Olga Wodo, Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'
author = 'Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinxcontrib.details.directive',
]

autosummary_generate = True

templates_path = ['_templates']


exclude_patterns = [
    '**/setup.py',
    'api/setup.rst',
    '**/test.py',
    'api/graspi_igraph.tests.rst',
    '_build',
    'Thumbs.db', '.DS_Store',
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_baseurl = 'https://owodolab.github.io/py-graspi/'

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}

autodoc_mock_imports = ["matplotlib", "mpl_toolkits.mplot3d"]
autodoc_member_order = 'bysource'

