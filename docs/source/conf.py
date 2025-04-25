import os
import sys
import inspect

sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../..'))
print(f"TEST: {os.path.abspath('../..')}")


project = 'py-graspi'
copyright = '2024, Olga Wodo, Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'
author = 'Michael Leung, Wenqi Zheng, Qi Pan, Jerry Zhou, Kevin Martinez'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.linkcode',
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
html_sidebars = {
    '**': ['localtoc.html'],  #Ensure the table of contents and search box are on every page
}

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

# def linkcode_resolve(domain, info):
#     """Resolve GitHub source link for each function."""
#     if domain != 'py' or not info['module']:
#         return None
#
#     try:
#         # Get the module
#         module_name = info['module']
#         obj = sys.modules.get(module_name)
#
#         if obj is None:
#             return None
#
#         # Traverse the object to find the actual function/class
#         for part in info['fullname'].split('.'):
#             obj = getattr(obj, part, None)
#             if obj is None:
#                 return None
#
#         # Get source file and line number
#         source_file = inspect.getsourcefile(obj)
#         source_lines, start_line = inspect.getsourcelines(obj)
#
#         if source_file is None:
#             return None
#
#         # Normalize path
#         source_file = os.path.abspath(source_file)
#
#         # GitHub repository details
#         github_repo = "https://github.com/owodolab/py-graspi"
#         branch = "dev"  # Make sure this matches your GitHub branch
#
#         # Adjust for your repo structure
#         project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
#         relative_path = os.path.relpath(source_file, project_root).replace(os.sep, '/')
#
#         # Ensure src/ is included in the path
#         if not relative_path.startswith("src/"):
#             relative_path = f"src/{relative_path}"
#
#         return f"{github_repo}/blob/{branch}/{relative_path}#L{start_line}"
#
#     except Exception as e:
#         print(f"Error in linkcode_resolve: {e}")
#         return None