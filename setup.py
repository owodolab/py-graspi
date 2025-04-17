from setuptools import setup, find_packages

setup(
    name = "py_graspi",
    author = "Olga Wodo",
    author_email = "olgawodo@buffalo.edu",
    version = "0.1.1.4-beta",
    description = "Graph-based descriptor for microstructures featurization",
    packages = find_packages(),
    classifiers = ["Programming Language :: Python"],
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
        "fpdf"
    ],
    python_requires = ">=3.7"
    
)