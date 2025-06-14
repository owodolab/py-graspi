.. _pyGraspiExamples:

==============================================
Example of Usage
==============================================

Getting Started
===========================

**To use the Py-GraSPI package in your project**

.. code-block:: bash

    pip install py-graspi

**To verify that the module has been installed**

.. code-block:: bash

    pip show py-graspi

Ensure you see this output on the terminal when running pip show
    .. image:: imgs/pip_show.png
        :scale: 55%
        :align: center

**For more details, check out the** :doc:`api documentation <api_overview>`.

Simple Example Usage
=====================

Step 1: import the py-graspi package:

.. code-block:: python

    import py_graspi as ig

Step 2: For a given morphology (in Graspi input format), generate graph and calculate descriptors

.. code-block:: python

    filename = "data/data_0.5_2.2_001900.txt"
    graph_data = ig.generateGraph(filename)
    descriptors_dict = ig.compute_descriptors(graph_data, filename)

Step 3: Save descriptors to the file

.. code-block:: python

    outputFile = "example_descriptors.txt"
    ig.descriptorsToTxt(descriptors_dict,outputFile)

Below is the output file generated when calculating the descriptors for the above test data (data_0.5_2.2_001900.txt)
    .. image:: imgs/descriptors.png
        :scale: 60%
        :align: center

Command Line Usage
==================
The user can use Py-GraSPI from the command line. To begin, ensure that the environment is in the src directory.

.. code-block:: bash

    cd src #Starting at the root directory, cd into the src directory

To learn the formatting of the command line arguments, the user is encouraged to run

.. code-block:: bash

    python graph.py

The usage message will provide the list of parameters that can be used. Py-GraSPI accepts input data in two formats: graph and array.

If input file is a .txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If data is structured (e.g., image), the following options are available

.. code-block:: bash

    python graph.py -a <INPUT_FILE.txt> [-s <pixelSize> (default 1)] [-p <{0,1}> (default 0-false)] [-n <{2,3}> (default 2)] #Can use flags

This can be used with both the -p and -n flag, just one of the flags, or none of the flags.

Examples of usage:

.. code-block:: bash

    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -s 1 -p 0 -n 2 #All flags- Pixel size, Periodicity and Phase flags
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -p 0 -n 2 #Periodicity and Phase flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -s 1 -p 0 #Pixel size and Periodicity flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -s 1 #Only pixel size flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -p 1 #Only periodicity flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -n 3 #Only phase flag
    python graph.py -a ../data/2D-testFile/testFile-10-2D.txt #No flag (Pixel size default = 1, Periodicity default = 0, Phase default = 2)

Example output when testing .txt with periodicity flag = 1
    .. image:: imgs/periodicity.png
        :scale: 70%
        :align: center


If input file is a .graphe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If graph is constructed externally data can be inputted in the graph format, for example:

.. code-block:: bash

    python graph.py -g <INPUT_FILE.graphe> #Cannot use flags

Example of usage:

.. code-block:: bash

    python graph.py -g ../data/test_data.graphe

Example output when testing .graphe file
    .. image:: imgs/graphe.png
        :scale: 50%
        :align: center


Flags for command line functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Py-GraSPI requires one mandatory input parameter: **the name of the input file <INPUT_FILE>**. Ensure that filepath is correctly formatted.

Using "../" allows access to files that may not be in the src directory.

The remaining parameters are optional, and have the default values set up, if the parameter is not explicitly provided.

- :code:`-a <INPUT_FILE.txt>` (row-major order): This is the option to input information about structured data. With this assumption, neighborhood of each voxel/pixel can be determined as the graph is constructed.

- :code:`-g <INPUT_FILE.graphe>`: This is the option to input information about the unstructured data. Input file must provide all information about the graph, this means that neighborhood of each vertex in the graph needs to be determined externally. Meta-vertices and the associated edges need to be defines in the input file. When this option is called, GraSPI reads the text file and initializes the set of vertices and edges from the input file, and need to be in agreement with these defined in the package for a given usage case.

- :code:`-s <pixelSize>` (default 1): This option sets the size of the pixel to compute the length of the shortest paths. If unspecified, all results will be outputted in terms of number of pixels, and need to be rescaled for dimensional analysis.

- :code:`-p <{0,1}>` (default 0-false): This option specifies if periodicity on the side faces is to be applied (valid only morphology inputted as the array option -a).

- :code:`-n <{2,3}>` (default 2) (black and white, OR electron-donor and electron-accepting material): This option specifies the number of phases. For three-phase morphology (option -n 3, black, white and grey vertices are read, that correspond to electron-donor, electron-accepting and mixed phase material, respectively).
