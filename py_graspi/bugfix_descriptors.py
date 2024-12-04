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

    g,is_2D,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca = ig.generateGraph(filename)
    fg = ig.filterGraph(g)


    if functionality == 'visuals':
        g = g.subgraph_edges([(0, 1), (0, 1), (2, 3), (2, 3), (3, 4), (4, 5), (6, 7), (6, 7), (7, 8), (7, 8), (2, 8), (2, 8), (4, 10), (12, 13), (12, 13), (13, 14), (13, 14), (14, 15), (14, 15), (9, 15), (9, 15), (15, 16), (15, 16), (18, 19), (18, 19), (14, 20), (14, 20), (20, 21), (20, 21), (15, 21), (15, 21), (24, 25), (24, 25), (21, 27), (21, 27), (27, 28), (27, 28), (30, 31), (30, 31), (32, 33), (32, 33), (27, 33), (27, 33), (33, 34), (33, 34), (28, 34), (28, 34), (34, 35), (34, 35)], delete_vertices=False)
        g.delete_vertices([36,37,38])
        ig.visualize(g,is_2D)

    if functionality == 'descriptors':
        print(descriptors.descriptors(g,filename,black_vertices,white_vertices, black_green, black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca))

    
    if functionality == 'cc':
        print(ig.connectedComponents(g))


if __name__ == '__main__':
    main()



