py-graspi Documentation
========================

Welcome to the documentation for **Py-Graspi**.
Py-GraSPI is Graph-based Structure Property Identifier software implemented as a Python package.
Py-GraSPI computes a library of descriptors for a segmented microstructure as well as performs graph operations using igraph.
The package represents microstructures as a graph and harnesses the graph-based theory to compute wide range of descriptors at low computational cost.
A suite of tools for data conversion between various formats and for post-processing the raw results from the graph analysis is provided.
This is a Python implementation of the GraSPI package which is originally implemented in C/C++

.. contents::
   :local:
   :depth: 10

Introduction
------------
This project provides tools for creating, filtering, and analyzing graphs, with benchmarks for runtime and memory performance.

.. toctree::
   :maxdepth: 10
   :caption: Contents:
   :includehidden:

   pyGraspiFunctionality
   pyGraspiDescriptors
   pyGraspiInputs
   pyGraspiExamples
   pyGraspiRepresentation
   pyGraspiDefinitions
   api_overview

Installation
------------
**Manual Installation**

Note: You must have Git, Python and pip installed onto your system

First, activate the virtual environment after opening a new project in your preferred IDE. Run this command:

.. code-block:: bash

   ./.venv/Scripts/activate

Clone the project repository by running this command:

.. code-block:: bash

   git clone https://github.com/owodolab/py-graspi.git

If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git.

Change directory into the py-graspi/ project directory by running this command:

.. code-block:: bash

   cd py-graspi/

Install the py-graspi module from PyPI by running this command:

.. code-block:: bash

   pip install py-graspi

Verify that the module has been installed correctly by ensuring that the following command DOES NOT give you a "Package not found" error.

.. code-block:: bash

   pip show py-graspi

If you do not have Python installed, please visit: https://www.python.org/downloads/

If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/

If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/

**Script Installation of Py-Graspi**

Note: You must have Git installed onto your system

Clone the project repository by running this command:

.. code-block:: bash

   git clone https://github.com/owodolab/py-graspi.git

Run the following script to set up and activate the virtual environment and install the py-graspi package:

.. code-block:: bash

   python py-graspi/startup.py

Verify that the module has been installed correctly by ensuring that the last output line on the command line says "Setup complete!" with no errors.

If you do not have Python installed, please visit: https://www.python.org/downloads/

If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/

If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/

**Installation and Set-Up of Jupyter Notebook for Py-Graspi**

First, activate the virtual environment after opening a new project in your preferred IDE. Run this command:

.. code-block:: bash

   ./.venv/Scripts/activate

Clone the project repository by running this command:

.. code-block:: bash

   git clone https://github.com/owodolab/py-graspi.git

If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git.

Change directory into the py-graspi/ project directory by running this command:

.. code-block:: bash

   cd py-graspi/

Install the py-graspi module from PyPI by running this command:

.. code-block:: bash

   pip install py-graspi

Install jupyter notebook by running this command:

.. code-block:: bash

   pip install notebook

Now, open the package in Jupyter Notebook for testing by running this command:

.. code-block:: bash

   jupyter notebook

A localhost jupyter notebook should open with the same directories and files as the py-graspi package.



Usage
-----
Below is a quick example of how to use the package to generate a graph and perform operations on it.

.. code-block:: python

   import graspi_igraph as ig

   # Generate a test file
   fileName = "10x10-testFile.txt"
   ig.testFileMaker(10, 1, fileName)

   # Generate a graph from the test file
   g = ig.generateGraph(fileName)

   # Visualize the graph (2D)
   ig.visual2D(g, "graph")

   # Compute connected components
   fg = ig.filterGraph(g)
   print(f"Number of Connected Components: {len(fg.connected_components())}")
   print(f"Connected Components: {fg.connected_components()}")

   # Produce a list of descriptors
   ig.descriptorsToTxt(ig.descriptors(g), "descriptors_list.txt")


