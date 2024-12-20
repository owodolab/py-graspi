.. _pyGraspiFunctionality:

==============================================
Functionality
==============================================

**py-graspi** is a Python implemented version of GraSPI, which computes a library of descriptors for a segmented microstructure
and computes descriptors that are relevant for organic solar cells performance.

**py-graspi** assumes that input microstructure is segmented into two phases: BLACK and WHITE.
In our application, organic solar cells, BLACK pixels correspond to electron-donating materials,
and WHITE pixels correspond to electron-accepting material - as marked in the figure below.
Three meta-vertices are added to the network:

* BLUE corresponds to cathode,
* RED corresponds to anode,
* GREEN corresponds to the interface.

As graph is being constructed, the meta-vertices are added to the graph. For the
morphology inputed as an array, the BLUE vertex is added to all vertices in the first row,
and RED vertex is added to all vertices corresponding to the last row in the input file.
**py-graspi** reads the colors of the pixels starting from the bottom left corner.
GREEN vertices are added as the graph is constructed, when BLACK pixel has any WHITE
voxel in the neighborhood, two additional edges are added (between BLACK and GREEN, and between WHITE and GREEN).

.. image:: imgs/graphLayout.png
   :width: 600

The package computes two types of descriptors: scalar descriptors and array descriptors.
The scalar descriptors are directed to the standard output, while array descriptors are directed to the corresponding file.
The array descriptors correspond to the shortest distances and are saved to a directory named **descriptors**

**py-graspi** provides multiple functions where a set of descriptors are computed - see the documentation for more details:

:ref:`pyGraspiDescriptors`
