from setuptools import setup, find_packages

setup(
    name="py_graspi",
    author="Olga Wodo",
    author_email="olgawodo@buffalo.edu",
    version="0.2.0.5",
    description="Graph-based descriptor for microstructure featurization",
    long_description="""
    # Py-GraSPI (Graph-based Structure Property Identifier)

    **Py-GraSPI** is a Python package designed to compute a comprehensive set of descriptors for segmented microstructures using a graph-based approach.

    ---

    ### Resources

    - **Source Code**: [GitHub Repository](https://github.com/owodolab/py-graspi)
    - **Documentation**: [Project Documentation](https://owodolab.github.io/py-graspi/)
    """,
    long_description_content_type="text/markdown",
    license="BSD 3-Clause License",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent"
                 ],

    url="https://github.com/owodolab/py-graspi",
    download_url='https://github.com/owodolab/py-graspi/archive/refs/tags/v_2.0.4.tar.gz',
    # need to get this link from the GitHub repo "Releases" section
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
    ],
    python_requires=">=3.7"

)
