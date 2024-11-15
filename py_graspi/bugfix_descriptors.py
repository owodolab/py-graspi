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

    g,is_2D,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim = ig.generateGraph(filename)
    fg = ig.filterGraph(g)


    if functionality == 'visuals':
        ig.visualize(g,is_2D)

    if functionality == 'descriptors':
        print(descriptors.descriptors(g,filename,black_vertices,white_vertices, black_green, black_interface_red, white_interface_blue, dim))

    
    if functionality == 'cc':
        print(ig.connectedComponents(g))


if __name__ == '__main__':
    main()



