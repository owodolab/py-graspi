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
git@github.com:owodolab/py-graspi.git
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
Once navigated to the branch, move to this branch of the repo using the following:
```
git branch Card#108-Create-Automated-PDF-Report
```
Once on the correct branch, access the "graspi_igraph" directory by using the following:
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
./run.sh <file_type>
```
Substitute <file_type> with either txt or pdf for the desired output type.
## 33 Morphologies Output
After running the command, the automatic report generation will begin. 
<br />
<br /> 
The following will print when the report generation begins:
```
Generating PDF (If on pdf mode)
Generating Text Files
```
As the script is running, the following will print for which microstructure it is on
```
Executing <test_file>
```
After a few minutes, the following will print once the report has been created
```
Text Files Generated
PDF Generated (If on pdf mode)
```
## Viewing 33 Morphologies Output
For text files, navigate to the results directory by using the following command:
```
cd graspi_igraph/results
```
Use the following command to view the list of text files generated:
```
ls
```
To view the result in each file, run the following command:
```
cat <result_file_name>
```
Replace <result_file_name> with any of the files outputted by "ls"
<br />
<br />
If using pdf mode, the pdf should automattically open upon completion.
<br />
<br />
If the pdf does not automatically pop up, use the following commands:
### On Windows
```
start graspi_igraph/test_results.pdf
```
### On MacOS
```
open graspi_igraph/test_results.pdf
```
### On Linux
```
evince graspi_igraph/test_results.pdf
```
If evince is not installed, run this first:
```
sudo apt install evince
```
