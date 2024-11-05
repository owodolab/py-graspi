from setuptools import setup, find_packages

setup(
    name = "graspi_igraph",
    author = "Wenqi Zheng",
    author_email = "wenqizhe@buffalo.edu",
    version = "0.0.2.6",
    description = "Utilize Python-igraph to produce similar functionality as GraSPI",
    packages = find_packages(),
    classifiers = ["Programming Language :: Python"],
    install_requires=[
        "igraph",
        "matplotlib",
        "numpy"
    ],
    python_requires = ">=3.7"
    
)