py-graspi Documentation
========================

Welcome to the documentation for **py-graspi**, a library for GraSPI and graph operations using igraph.

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
To install the required dependencies, run:

.. code-block:: bash

   pip install graspi-igraph
   pip install matplotlib

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
   ig.descriptorsToTxt(ig.desciptors(g), "descriptors_list.txt")


