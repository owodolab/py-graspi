.. _pyGraspiExamples:

==============================================
Example of Usage
==============================================

Getting Started
===========================

**Testing Py-Graspi Online**

Follow these steps to explore the capabilities of Py-Graspi using an online Jupyter Notebook environment like Google Colab.

**To run an existing test notebook**

1. Open Google Colab.
2. Click the GitHub tab, and paste the following link: https://github.com/owodolab/py-graspi/blob/dev/tests/pip_install_descriptors_example.ipynb
3. Since this is an existing notebook, you can run each code block to view the output.

**To create your own notebook and use the Py-GraSPI package**

1. Open Google Colab.
2. In the notebook, install Py-Graspi by running the following command:

.. code-block:: bash

    !pip install py-graspi

3. Import the py-graspi package by running this command in the notebook:

.. code-block:: bash

    import py_graspi as ig

Command Line Usage
==================
The user can use Py-GraSPI from the command line. To begin, ensure that the environment is in the src directory.

.. code-block:: bash

    cd src #Starting at the root directory, cd into the src directory

To learn the formatting of the command line arguments, the user is encouraged to run

.. code-block:: bash

    python graph.py

The usage message will provide the list of parameters that can be used. Py-GraSPI accepts input data in two formats: graph and array.

If graph is constructed externally data can be inputted in the graph format, for example:

.. code-block:: bash

    python graph.py -g <INPUT_FILE.graphe> #Cannot use flags

Example of usage:

.. code-block:: bash

    python graph.py -g ../data/test_data.graphe

If data is structured (e.g., image), the following options are available

.. code-block:: bash

    python graph.py -a <INPUT_FILE.txt> -p <{0,1}> (default 0-false) -n <{2,3}> (default 2) #Can use flags

This can be used with both the -p and -n flag, just one of the flags, or none of the flags.

Examples of usage:

.. code-block:: bash

    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -p 0 -n 2 #Both flags
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -p 1 #Only periodicity flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -n 3 #Only phase flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt #No flag

Py-GraSPI requires one one mandatory input parameter: the name of the input file <INPUT_FILE>. Ensure that filepath is correctly formatted.
Using "../" allows access to files that may not be in the src directory.

The remaining parameters are optional, and have the default values set up, if the parameter is not explicitly provided.

- -a <INPUT_FILE.txt> (row-major order) this is the option to input information about structured data. With this assumption, neighborhood of each voxel/pixel can be determined as the graph is constructed.

- -g <INPUT_FILE.graphe> this is the option to input information about the unstructured data. Input file must provide all information about the graph, this means that neighborhood of each vertex in the graph needs to be determined externally. Meta-vertices and the associated edges need to be defines in the input file. When this option is called, GraSPI reads the text file and initializes the set of vertices and edges from the input file, and need to be in agreement with these defined in the package for a given usage case.

- -p <{0,1}> (default 0-false) this option specifies if periodicity on the side faces is to be applied (valid only morphology inputted as the array option -a).

- -n <{2,3}> default 2 (black and white, electron-donor and electron accepting material) – this option specifies the number of phases. For three-phase morphology (option -n 3, black, white and grey vertices are read, that correspond to electron-donor, electron-accepting and mixed phase material, respectively).

User Functionality
==================

Get the List of Descriptors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **descriptor stored in a dictionary** can be found by calling the function descriptors(graph)

.. code-block:: bash

    ig.descriptors(g)      # g is a graph object

A **list of descriptors** in a **text file** can be found by calling the function descriptorsToTxt(dictionary,filename)

.. code-block:: bash

    ig.descriptorsToTxt(dict,"descriptors_list.txt")

Visualize Graphs
~~~~~~~~~~~~~~~~

For 2D graphs, call visual2D(graph)

.. code-block:: bash

    g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
    ig.visual2D(g)

For 3D graphs, call visual3D(graph)

.. code-block:: bash

    g = ig.generateGraph("3D-testFile/testFile-10-3D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
    ig.visual3D(g)

