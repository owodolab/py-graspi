import os
import sys

sys.path.append(os.path.abspath('../src'))
import src.igraph_testing as ig
import src.descriptors as d


(g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
             dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
             CT_n_D_adj_An, CT_n_A_adj_Ca) = ig.generateGraphAdj(sys.argv[1])

dic = d.descriptors(g, sys.argv[1], black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
                dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
                CT_n_D_adj_An, CT_n_A_adj_Ca)

for key, value in dic.items():
    print(key, value)
