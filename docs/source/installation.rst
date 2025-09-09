.. _installation:

==============================================
Installation
==============================================


Simple Usage of Py-Graspi package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To install the py-graspi package, run this command in terminal

.. code-block:: bash

    pip install py-graspi

To verify that the module has been installed

.. code-block:: bash

    pip show py-graspi

Ensure you see this output on the terminal when running pip show
    .. image:: imgs/pip_show.png
        :scale: 55%
        :align: center

To utilize the package, import the Py-Graspi package to your python project:

.. code-block:: python

    import py_graspi as ig

Manual Installation for Py-Graspi source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to manually install the Py-Graspi package.

1. Clone the project repository by running this command:

Note: You must have Git installed on your system

.. code-block:: bash

   git clone https://github.com/owodolab/py-graspi.git


2. Navigate to the Py-Graspi project directory by running this command:

.. code-block:: bash

   cd py-graspi/

3. Install the modules required to utilize Py-Graspi algorithms

Note: You must have pip installed onto your system

.. code-block:: bash

   pip install -r requirements.txt

4. Now you can create your project using the Py-Graspi API or run the high-throughput execution from the command line.

In the folder py-graspi/tests, you can find the Python file generate_report.py that generates information about data.

Note: You must have Python installed onto your system. Below examples assume user is in the tests directory.


    a. To generate the txt files:

    .. code-block:: bash

        python generate_report.py txt

    b. Or to generate pdf report:

    .. code-block:: bash

        python generate_report.py pdf


Jupyter Notebook for Py-Graspi source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the project repository by running this command:

Note: You must have Git installed on your system

.. code-block:: bash

   git clone https://github.com/owodolab/py-graspi.git

2. Navigate to the Py-Graspi project directory by running this command:

Note: You must have pip installed on your system

.. code-block:: bash

   cd py-graspi/

3. Install the modules required to utilize Py-Graspi algorithms:

Note: You must have Python installed on your system

.. code-block:: bash

   pip install -r requirements.txt

4. Install jupyter notebook by running this command:

.. code-block:: bash

   pip install notebook

5. Now, open the package in Jupyter Notebook for testing by running this command:

.. code-block:: bash

   jupyter notebook

A localhost jupyter notebook should open with the same directories and files as the py-graspi package.


