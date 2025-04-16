# py-graspi
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kkevinmartinezz/kaggle_PyGraspi/3d7bf5df17b015612ab1b8261c63d0bbb00a268f?urlpath=lab%2Ftree%2Fpygraspi-test.ipynb) [![PyPi Package](https://img.shields.io/badge/PyPi-package-blue)](https://pypi.org/project/py-graspi/) [![Go to About](https://img.shields.io/badge/go_to-about-green)](#about) [![go to documentation](https://img.shields.io/badge/go_to-documentation-purple)](https://owodolab.github.io/py-graspi/)



Py-GraSPI (Graph-based Structure Property Identifier) is a Python package designed to compute a comprehensive set of descriptors for segmented microstructures using a graph-based approach. 

Py-GraSPI leverages the igraph library to represent microstructures as graphs, enabling efficient computation of a wide range of descriptors with low computational overhead. Py-GraSPI is the Python implementation of the original GraSPI package, which was developed in C/C++. In addition to descriptor computation, Py-GraSPI offers tools for data conversion across various formats and for post-processing the raw outputs of the graph analysis.

See the documentation attached above in purple for more information.

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from some meta-vertices to all specified vertices
  -  Provide a list of descriptors
  -  Graph visualization


## Getting Started
To install the py-graspi package:
```bash 
pip install py-graspi
```
check out the API: https://owodolab.github.io/py-graspi/api_overview.html

To verify that the module has been installed"

```bash
pip show py-graspi
```

## Simple example of usage

Step 1: import the py-graspi package: 

```python
import py_graspi as ig # check with kevin if possible to import only py_graspi
import graph as ig
import descriptors as d
```

Step 2: For a given morphology (in Graspi input format), generate graph and calculate descriptors

```python
filename = "data_0.5_2.2_001900.txt"
graph_data= ig.generateGraphAdj(filename)
dict = d.descriptors(graph_data, filename)
```

Step 3: Save descriptors to the file 

```python
outputFile = "example_descriptors.txt"
d.descriptorsToTxt(dict,outputFile)
```

## Installation
### Manual Installation of Py-Graspi
Follow these steps to manually install the Py-Graspi package.

1. Clone the project repository by running this command:

   **Note: You must have Git installed on your system**
   ```bash
   git clone https://github.com/owodolab/py-graspi.git
   ```

2. Navigate to the Py-Graspi project directory by running this command:
   ```bash
   cd py-graspi/
   ```

3. Install the py-graspi module from PyPI by running this command:
   **Note: You must have Python and pip installed onto your system**
   ```bash
   pip install -r requirements.txt
   ```
   
4. Now you can create your project using the [Py-Graspi API](https://owodolab.github.io/py-graspi/api_overview.html) or run the high-throughput execution from the command line.
   In the folder py-graspi/tests, you can find the Python file tests.py that shows how to run them.
   To generate the txt files:
   ```bash
   python tests.py txt
   ```
   Or to generate pdf report:
   ```bash
   python tests.py pdf
   ```


## Script mode


Two formats are accepted by the command line script (igraph_testing.py): txt (stores morphology as a vector in the row-wise notation) and graphe (internal graph format), see documentation for more details. The script can be executed with the following options:
  
````
python py_graspi.py -g {total pathname of test file} 
python igraph_testing.py {total pathname of test file}
````
For example:

```
python graph.py -g ../data/test_data.graphe
python graph.py -a ../data/2D-testFile/testFile-10-2D.txt -p 0 -n 2
```
Several other options are available - see the documentation for more details

  
## Short videos for Py-Graspi Installation, Notebook Setup, and Testing via Command Line
Please visit this link: https://drive.google.com/drive/folders/1AECLQXII4kmcBiQuN86RUYXvJG_F9MMq?usp=sharing
### Videos
* **py_graspi_installation**: How to install Py-Graspi and run basic commands.
* **py_graspi_notebook**: How to utilize our prebuilt notebook to run basic commands of Py-Graspi.
* **py_graspi_command_line**: How to print out Py-Graspi's calculations of connected components, descriptors, visualizations of the graph, etc, of provided input files via command line.


# ABOUT
Py-GraSPI (Graph-based Structure Property Identifier) is a Python package designed to compute a comprehensive set of descriptors for segmented microstructures using a graph-based approach. It leverages the igraph library to represent microstructures as graphs, enabling efficient computation of a wide range of descriptors with low computational overhead.
Py-GraSPI is the Python implementation of the original GraSPI package, which was developed in C/C++.
In addition to descriptor computation, Py-GraSPI offers tools for data conversion across various formats and for post-processing the raw outputs of the graph analysis.
