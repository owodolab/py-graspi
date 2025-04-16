from setuptools import setup, find_packages

setup(
    name="py_graspi",
    author="Wenqi Zheng",
    author_email="wenqizhe@buffalo.edu",
    version="0.1.1.9",
    description="Graph-based descriptor extraction tool for microstructures",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=["Programming Language :: Python"],
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
    python_requires=">=3.7"

)