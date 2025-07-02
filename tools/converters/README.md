# Converters

This directory contains tools to convert between different data formats.

### img_to_graph.py
This tool converts png images to graph based representation of the morphology. It also offers 
the option to resize the image, with the outputted image going into a resized folder in this directory.

Usage:
```bash
python img_to_graph.py {pathname of image file} {Resize calculation amount}
```
Example:
```bash
python img_to_graph.py ../../data/2phase/2D-morphologies/images/data_0.5_2.2_001900.png 0.15
```
### img_to_txt.py
This tool converts png images to text based representation of the morphology. It also offers
the option to resize the image, with the outputted image going into a resized folder in this directory. 

Usage: 
```bash
python img_to_txt.py {pathname of image file} {Resize calculation amount}
```
Example:
```bash
python img_to_txt.py ../../data/2phase/2D-morphologies/data/images/data_0.5_2.2_001900.png 0.15
```
### plt_to_txt.py
This tools converts plt images to text based representation of the morphology. 

Usage: 
```bash
python plt_to_txt.py [pathname]
```
Example:
```bash
python plt_to_txt.py plt/5x4x3.plt
```
