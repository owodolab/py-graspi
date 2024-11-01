import igraph_testing as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import descriptors
import sys

def main():

    filename = sys.argv[1]
    # dimension = sys.argv[2]
    graph_type = sys.argv[2]
    functionality = sys.argv[3]

    g,is_2D = ig.generateGraph(filename)
    fg = ig.filterGraph(g)


    if functionality == 'visuals':
        if is_2D == True:
            if graph_type == 'g':
                ig.visual2D(g,'graph')
                print("Plot displayed.")
            if graph_type == 'fg':
                ig.visual2D(fg,'filtered')
                print("Plot displayed.")
        else:
            if graph_type == 'g':
                ig.visual3D(g)
            if graph_type == 'fg':
                ig.visual3D(fg)

    if functionality == 'descriptors':
        print(descriptors.desciptors(g))

    
    if functionality == 'cc':
        print(ig.connectedComponents(g))


if __name__ == '__main__':
    main()



