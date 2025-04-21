.. _advanced:

==============================================
Advanced
==============================================
The Py-GraSPI package also included scripts with advanced functionality mostly for developers.

User Functionality
==================

Visualize Graphs
~~~~~~~~~~~~~~~~

To visualize graphs, call the visualize(graph_data, is_2D) function.

.. code-block:: python

    # Visualize the graph (2D)
    ig.visualize(graph_data, true)

Running Memory Tests
====================

To run memory tests, run the following command in the terminal:

.. code-block:: bash

    python main.py n dimension function

**Make sure of the following:**

* Replace "n" with the size of the graph you want. **Note:** n should be between 1-1000 for 2D graphs and 1-100 for 3D graphs. Otherwise, the code will timeout.
* Replace "dimension" with 2D or 3D specify if you want a 2D or 3D graph.
* Replace "function" with either generage, filter, or shortest_path to choose which function you want to test memory for.

Example:

.. code-block:: bash

    python main.py 10 2D generate

Translating .plt files to .txt files
========================================

Numerical simulations can be saved using .plt file. Py-GraSPI provides tool to convert the plt file into txt file - following array format, see syntax and the example below:

.. code-block:: bash

    python plt_to_txt.py [pathname]

.. code-block:: bash

    python plt_to_txt.py plt/5x4x3.plt

Translate Image File Into Rescaled .txt File
==========================================================

Py-GraSPI provide also tool to convert black and white image into txt file and rescale it with assumed ratio (provided as fraction, e.g., 0.5). See syntax and the example:

.. code-block:: bash

    python img_to_txt.py {pathname of image file} {Resize calculation amount}

.. code-block:: bash

    python img_to_txt.py ../../data/images/data_0.5_2.2_001900.png 0.15

2D & 3D Morphologies Tests
========================================

To run the 2d and 3d morphologies you will need to setup notebook and pip install the graspi_igraph package.

First you will need to git clone the current repo, and install packages:

.. code-block:: bash

    git clone https://github.com/owodolab/py-graspi.git
    pip install py-graspi
    pip install notebook

Finally, you will be able to use the command:

.. code-block:: bash

    jupyter notebook

This will bring you to the testing files on jupyter.

Navigate to the file **graspi_igraph_notebook.ipynb** under the **notebook** directory.

Running Py-GraSPI on the Library of Morphologies
=========================================

Change folder to py-graspi/tests, generate the executable for the script, and run the code

.. code-block:: bash

    cd tests
    chmod +x run.sh
    ./run.sh <file_type>

Substitute `<file_type>` with either `txt` or `pdf` for the desired output type.

**Example:**

.. code-block:: bash

    ./run.sh txt

After running the command, the automatic report generation will begin.
The following will print when the report generation begins:

.. code-block::

    Generating PDF (If on pdf mode)
    Generating Text Files

Tortuosity HeatMap Visualization
=======================================

In folder tools, you find scrpts to visualize tortuosity:

.. code-block:: bash

    python tortuosity.py {pathname of file}

**Example:**

.. code-block:: bash

    python tortuosity.py ../../data/data/data_0.5_2.2_001900.txt

Jupyter NoteBook to Visualize HeatMap
=========================================

Make sure Jupyter Notebook is installed:

.. code-block:: bash

    pip install jupyter

Run jupyter notebook with following command:

.. code-block:: bash

    jupyter notebook

Open up `tortuosity.ipynb` under the `py_graspi` directory.

Example Visualization
=========================================

This section explains how to visualize a microscopy image by filtering both it's white and black vertices.

Here, the image "mycelium.png" is from the folder py-graspi/data/images.

.. code-block:: bash

    python myceliumTest.py {pathname of image file} {Resize calculation amount}

.. code-block:: bash

    python myceliumTest.py ../../data/images/data_0.5_2.2_001900.png 0.15

This creates a truncated version of the mycelium image (for runtime purposes) and outputs the largest subgraph of the following filtered graphs:
   1. The first one is a white only vertex graph
   2. The second one is a black only vertex graph.
You can interact with the plots to find the appropriate visualization.

Generate API Documentation
==================

In order to generate an API using sphinx, you need to follow the installation of py-graspi:

Install ghp-import in the project root directory:

.. code-block:: bash

   pip install ghp-import

To generate the rst files into the local html, run this command:

.. code-block:: bash

   sphinx-build -b html docs/source docs/build

Ensure that the files have been generated in docs/build.

To push the changes reflected on the html to the gh-pages branch on GitHub, essentially pushing changes to the site, run this command:

.. code-block:: bash

   ghp-import -n -p -f docs/build/

Go to the GitHub repo and verify that the files were pushed to the gh-pages branch

Access and verify the documentation through the following URL: https://owodolab.github.io/py-graspi/.

Update Py-Pi Package
====================

If there are changes made to the to the PyGraspi package locally, these instructions can help push to Py-Pi.

1. To install setuptools, wheel and twine, run this command in terminal:

.. code-block:: bash

   pip install setuptools wheel twine

Ensure that the project already contains setup.py, README.md, _init_.py, LICENSE and other core files.

**Note:** Make sure you update the version number in the setup.py file.

2. Build the distribution files, which creates a dist/ directory containing the .tar.gz and .whl files.

First, CD into project root directory (where setup.py exists). Then, run this command in terminal:

.. code-block:: bash

   python setup.py sdist bdist_wheel

(Optional) It's safe to delete the .tar.gz and .whl file of old versions so that the correct version gets pushed to PyPI

3. Login to PyPI, and retrieve your API token to upload the package using twine.

**Note:** You need to be a manager or owner of the package on PyPI to upload new versions.

4. Use twine to upload the distribution securely by running this command in terminal:

.. code-block:: bash

   twine upload dist/*

When prompted for your API token, retrieve the API token that you can generate from PyPI.

**Note:** The token will not be visible on the terminal for security reasons, so press enter after entering the token.

Verify that the new version has been uploaded successfully at the link https://pypi.org/project/py-graspi/