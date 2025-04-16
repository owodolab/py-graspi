from setuptools import setup, find_packages

setup(
    name = "py_graspi",
    author = "Wenqi Zheng",
    author_email = "wenqizhe@buffalo.edu",
    version = "0.1.1.4-beta",
    description = "Utilize Python-igraph to produce similar functionality as GraSPI",
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