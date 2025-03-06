import os
import sys

sys.path.append(os.path.abspath('../src'))

import src.igraph_testing as ig
import src.descriptors

def main():

    filename = sys.argv[1]
    # # dimension = sys.argv[2]
    # graph_type = sys.argv[2]
    # functionality = sys.argv[3]

    g,is_2D,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca = ig.generateGraph(filename)
    descript = src.descriptors.descriptors(g, filename, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca)
    expected = [65536,1634,32713,32823,2,1,1,1,0.4991607666015625,0.42716962675388986,0.23717581433983226,0.7821297429620563,0.870266,1.0,1278,1278,1634,512,512,0.8437318497233516,0.7345154312524754]
    i = 0

    for d in descript:
        if descript[d] != expected[i]:
            print(f"The computed descriptors was not what was expected. Failed on Discriptor: {d} Expected: {descript[d]} Computed: {expected[i]} :( ")
            return
        i += 1

    print(f"All the computed descriptors are the same as expected values :) ")
    
    


if __name__ == '__main__':
    main()
    