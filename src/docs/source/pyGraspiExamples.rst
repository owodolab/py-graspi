.. _pyGraspiExamples:

==============================================
Example of Usage
==============================================

**Py-GraSPI** can be a command line tool. Make sure to install all requirements with:

.. code-block:: bash

    pip install -r requirements.txt

Get the List of Descriptors
===========================

A **descriptor stored in a dictionary** can be found by calling the function descriptors(graph)

.. code-block:: bash

    ig.descriptors(g)      # g is a graph object

A **list of descriptors** in a **text file** can be found by calling the function descriptorsToTxt(dictionary,filename)

.. code-block:: bash

    ig.descriptorsToTxt(dict,"descriptors_list.txt")

Visualize Graphs
================

For 2D graphs, call visual2D(graph)

.. code-block:: bash

    g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
    ig.visual2D(g)

For 3D graphs, call visual3D(graph)

.. code-block:: bash

    g = ig.generateGraph("3D-testFile/testFile-10-3D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
    ig.visual3D(g)

