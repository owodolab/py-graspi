import sys

from graspi_igraph import filterGraph, vertexColors
import igraph
import matplotlib.pyplot as plt
import igraph_testing as ig
import img_to_txt as translate


def visualize(g):
    layout = g.layout('kk') #drl, kk

    fig, ax = plt.subplots(figsize=(10, 10))

    igraph.plot(g,
                target=ax,
                layout=layout,
                vertex_colors=vertexColors,
                vertex_size=5,
                margin=20)

    # Remove the code that generates the labels for each vertex
    # plt.title("Visualization of White Vertices of Graph")
    plt.show()
def filter_black_vertices(graph):
    """
        Filters the graph by keeping only edges between vertices of the same color {black}.

        Args:
            graph (ig.Graph): The input graph.

        Returns:
            ig.Graph: The filtered graph.
        """
    edgeList = graph.get_edgelist()
    keptEdges = []

    # Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if (graph.vs[currentNode]['color'] == 'black') and (graph.vs[toNode]['color'] == 'black'):
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=True)

    return filteredGraph


def filter_white_vertices(graph):
    """
        Filters the graph by keeping only edges between vertices of the same color {white}.

        Args:
            graph (ig.Graph): The input graph.

        Returns:
            ig.Graph: The filtered graph.
        """
    edgeList = graph.get_edgelist()
    keptEdges = []

    # Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if (graph.vs[currentNode]['color'] == 'white') and (graph.vs[toNode]['color'] == 'white'):
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=True)

    return filteredGraph


def main():
    input_file = sys.argv[1]
    resize_factor = sys.argv[2]
    resize_factor = float(resize_factor)
    translate.img_to_txt(input_file,resize_factor)
    txt_filename = "resized/resized_" +input_file[7:-4]+".txt"
    (g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
     dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
     CT_n_D_adj_An, CT_n_A_adj_Ca) = ig.generateGraphAdj(txt_filename)
    # print("graph created")
    whiteFilteredGraph = filter_white_vertices(g)
    # print("graph filtered")
    visualize(whiteFilteredGraph)
    blackFilteredGraph = filter_black_vertices(g)
    visualize(blackFilteredGraph)


if __name__ == "__main__":
    main()