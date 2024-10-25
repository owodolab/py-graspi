﻿# py-graspi

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from the bottom boundary to all black vertices until the white vertices are met
  -  Graph visualization
  -  Computation of Descriptors

## Installation
First, you'd need to clone the repo by running the following command in your command line:
```
git clone git@github.com:wenqizheng326/graspi_igraph.git
```
**Note: You'd need git installed on your system first**
<br />
<br />
  If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git
<br />
<br />
Next, you'd need to navigate to the cloned repo using terminal. An example would be:
```
cd /path/graspi_igraph
```
First, make sure you're on the memoryFix branch of the repo by running
```
git checkout memoryFix
```
Once navigated to the branch, downloads needed can be found in requirements.txt and can be installed by:
```
pip install -r requirements.txt
```
**Note: you must have Python and pip installed onto your system**
<br />
<br />
  If you do not have Python installed, please visit: https://www.python.org/downloads/
<br />
<br />
  If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/
<br />
<br />
  If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/ 

## Running memory tests
To run memory tests, run the following command in terminal:
```
python main.py n dimension function
```
**Make sure of the following:**
  -  Replace "n" with the size of the graph you want. Note: n should be between 1-1000 for 2D graphs and 1-100 for 3D graphs
  -  Replace "dimension" with 2D or 3D to specify if you want a 2D or 3D graph
  -  Replace "function" with either generate, filter, or shortest_path, to choose which function you want to test memory for
 
<br />**An example of a correct command would be:**
```
python main.py 10 2D generate
```
## Outputs
After running this command, you should see
```
Generating results
```
Followed by the memory usage and runtime results after some time.
<br />
<br />
 The following will print:
```
Completed
```
To know that the tests have been completed
## To Test Algorithms

To **generate graphs**, call the generateGraph(_file_) function which takes in a input-file name
  -  returns a graph
```
ig.generateGraph("2D-testFile/testFile-10-2D.txt")   # utilizing the test file found in 2D-testFiles folder as an example
```

To **filter graphs**, call filterGraph(_graph_) function which takes in a graph object 
  -  can pass a graph generated by generateGraph(_file_)
  -  returns a filtered graph
```
g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
fg = ig.filterGraph(g)
```

To **determine the connected components** of the filtered graph, call connected_components() function
```
print(fg.connected_components())
```
The number of connected components can be found by taking the length of the result produced by the connected_components function 
```
print(len(fg.connected_components())) 
```

The **shortest path** between some meta-vertices to all specified vertices calling the function shortest_path(_fiteredGraph_, _specifiedVertices_, _metaVertex_, _fileName_)
  -  stores the distance of the paths to from the _metaVertex_ to every single _specified Vertices_ in a text file called _fileName_

Example:
  - the example below finds the shortest path between all black vertices to the blue meta-vertex and stores it in the text file, black_to_blue_paths.txt
```
ig.shortest_path(fg,'black','blue',"black_to_blue_paths.txt")    #fg is a filtered graph object
```

### To get list of descriptors

A **descriptors stored in a dictionary** can be found by calling the function descriptors(_graph_)

```
ig.descriptors(g)      # g is a graph object
```
A **list of descriptors in a text file** can be found by calling the function descriptorsToTxt(_dictionary_,_filename_)
```
ig.descriptorsToTxt(dict,"descriptors_list.txt")
```

### To visualize graphs

  -  for 2d graphs, call visual2D(_graph_)
```
g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
ig.visual2D(g)
```
  -  for 3d graphs, call visual3D(_graph_)
```
g = ig.generateGraph("3D-testFile/testFile-10-3D.txt")     # utilizing the test file found in 2D-testFiles folder as an example
ig.visual3D(g)
Finally, the following message will be printed out:
```
