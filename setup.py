from setuptools import setup, find_packages

setup(
    name = "py_graspi",
    author = "Wenqi Zheng",
    author_email = "wenqizhe@buffalo.edu",
    version = "0.1.2.0",
    description = "Utilize Python-igraph to produce similar functionality as GraSPI",
    packages = find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers = ["Programming Language :: Python"],
    url="https://github.com/owodolab/py-graspi",
    download_url='', #need to get this link from the GitHub repo "Releases" section
    install_requires=[
        "igraph",
        "matplotlib",
        "numpy",
        "contourpy",
        "cycler",
        "fonttools",
        "kiwisolver",
        "packaging",
        "pillow",
        "psutil",
        "pyparsing",
        "python-dateutil",
        "six",
        "texttable",
        "fpdf",
        "notebook"
    ],
    python_requires = ">=3.7"
    
)
