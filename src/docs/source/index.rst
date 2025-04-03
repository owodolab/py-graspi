py-graspi Documentation
========================

Welcome to the documentation for **Py-Graspi**.
**Py-GraSPI** (Graph-based Structure Property Identifier) is a Python package designed to compute a comprehensive set of
descriptors for segmented microstructures using a graph-based approach. It leverages the **igraph** library to represent microstructures
as graphs, enabling efficient computation of a wide range of descriptors with low computational overhead. Py-GraSPI is the Python
implementation of the original **GraSPI package**, which was developed in C/C++. In addition to descriptor computation,
Py-GraSPI offers tools for data conversion across various formats and for post-processing the raw outputs of the graph analysis.

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
Below is a quick example of how to use the package to generate a test graph file, construct a graph from the file,
visualize it in 2D, compute the connected components, and finally, extract the descriptors.

This example usage will output the number of connected components and additional details as well as
return a txt file containing a list of the descriptors. This package's functionality in returning the descriptors
for a microstructure is thorough. A full list of descriptors and their definitions can be found on the descriptors tab.

1. To use the package in your project files, import the py-graspi package.

.. code-block:: python

   import graspi_igraph as ig

2. To generate graphs, call the generateGraph(file) function which takes in an input test file name.

.. code-block:: python

   # Generate a graph from the test file
   g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")   # utilizing the test file found in 2D-testFiles folder as an example

3. To visualize graphs, call the visualize(graph, is_2D) function.

.. code-block:: python

   # Visualize the graph (2D)
   ig.visualize(g, "graph")

4. To filter a graph and compute the number of connected components, call filterGraph(graph)

.. code-block:: python

   # Compute connected components
   fg = ig.filterGraph(g)
   print(f"Number of Connected Components: {len(fg.connected_components())}")
   print(f"Connected Components: {fg.connected_components()}")

5. To get a dictionary of descriptors for a given graph, call descriptors(graph)

.. code-block:: python

   # Produce a list of descriptors
   ig.descriptorsToTxt(ig.descriptors(g), "descriptors_list.txt")

