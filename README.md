# graspi_igraph

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from the bottom boundary to all black vertices until the white vertices are met
  -  Graph visualization

## Installation
First, you'd need to make sure you're in a clean environment and clone the repo by running the following command in your command line:
```
git clone git@github.com:owodolab/py-graspi.git
```
**Note: You'd need git installed on your system first**
<br />
<br />
  If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git
<br />
<br />
Next, you'd need to navigate to the cloned repo using terminal. An example would be:
```
cd /path/py-graspi
```
First, make sure you're on the sprint3-subtask5 branch of the repo by running
```
git checkout sprint3-subtask5
```
Once navigated to the branch, access the following directory:
```
cd graspi_igraph
```
Next, the downloads needed can be found in requirements.txt and can be installed by:
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

## Running all 33 morphologies tests
To run the morphologies tests, return to the previous directory of "/py-graspi" by running:
```
cd ..
```
Next, make sure you're on bash first by running:
```
bash
```
Next, run the following:
```
chmod +x run.sh
```
Finally, run the following: 
```
./run.sh
```
## Outputs
After running this command, you should see
```
<Test file name>: passed/failed
```
Followed by the descriptors of the given test files. This will print for all 33 morphologies

