from src import igraph_testing as ig
from src import descriptors
import sys

def main():

    filename = sys.argv[1]
    # dimension = sys.argv[2]
    graph_type = sys.argv[2]
    functionality = sys.argv[3]

    g,is_2D,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca = ig.generateGraph(filename)
    fg = ig.filterGraph(g)


    if functionality == 'visuals':
        g.delete_vertices([64,65,66])
        ig.visualize(g,is_2D)

    if functionality == 'descriptors':
        des = descriptors.descriptors(g, filename, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca)
        print(des)
        # filename = filename.split('/')[-1]
        # descriptors.descriptorsToTxt(des,f"descriptors_{filename}")
    
    if functionality == 'cc':
        print(ig.connectedComponents(g))


if __name__ == '__main__':
    main()



