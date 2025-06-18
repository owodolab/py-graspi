# Tortuosity

This directory contains tortuosity computation and visualization tools.
Tortuosity refers to how the curved or twisted the paths between different phases are in given morphologies.
Py-GraSPI leverages this functionality to reflect more complex paths versus more straight and efficient paths. 

## tortuosity.py
This script generates graphs and filters them by the edges phase colors, then, generates 
HeatMaps that help visualize the tortuosity form of the morphology. It filters and shows tortuosities 
from Black to Red (BTR) and White to Blue (WTB).

It takes in the pathname of a file that contains the morphology data. It outputs a pop-up
window with color coded HeatMaps for the tortuosity paths. 

Usage:
```bash 
python tortuosity.py {pathname of file}
```

Example:
```bash
python tortuosity.py ../../data/2phase/2D-morphologies/data/data_0.5_2.2_001900.txt
```

## tortuosity_histogram.py
This script generates graphs and filters them by the edges phase colors, then, generates 
HeatMaps that help visualize the tortuosity form of the morphology. It filters and saves the image file
of tortuosities from Black to Red (BTR) and White to Blue (WTB) for the given morphologies.

It takes in the pathname of a file that contains the morphology data. It saves the image file of 
the tortuosity to the given file pathname. 

## tortuosity_of_multiple_morphologies.ipynb
This notebook generates the tortuosity HeatMaps for given morphologies and displays them in the notebook.
Simply adjust the cell that contains the filename to generate the tortuosity HeatMap for the morphology.

Example: 
```bash
filename = "../../data/2phase/2D-morphologies/data/data_0.5_2.2_001900.txt"
```