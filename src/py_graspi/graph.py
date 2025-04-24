import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import os
from py_graspi import descriptors as d
from py_graspi import graph_data_class as GraphData

import math
DEBUG = False # debugging mode
DEBUG2 = False   # for green edges
pixelSize = 1
n_flag = 2
# import tortuosity as t


''' data structure for storing info about newly added edges regarding green_vertex'''
class edge_info():
    def __init__(self):
        self.index = None
        self.color = None
        self.order = None
        self.weight = None

'''for updating edge info based on rule '''
'''green vertex can only connect with interface(first order) vertices'''
def store_interface_edges(edges_with_green, index, color, order, weight):
    if index in edges_with_green:
        cur_v = edges_with_green[index]
        if edges_with_green[index].weight > weight * 0.5:     # if previous order is higher than new one
            edges_with_green[index].weight = weight * 0.5     # change it to lower order      

    else:
        newEdge = edge_info()
        newEdge.color = color
        newEdge.index = index
        newEdge.order = order   #order = 1,2,3
        newEdge.weight = weight * 0.5
        
        edges_with_green[index] = newEdge

def generateGraph(file, PERIODICITY = False):
    """
        This function takes in graph data and determines if it’s in .txt or .graphe format in order to represent the graph using an adjacency list and the correct dimensionality.

    Args:
        file (str): The name of the file containing graph data.
        periodicity (bool): Boolean representing if graph has periodic boundary conditions

    Returns:
        This function generates a graph based on the input so the return type depends on the format of graph data that was given.
        See “generateGraphAdj” if in .txt, or “generateGraphGraphe” if in .graphe.
    """
    if os.path.splitext(file)[1] == ".txt":
        return generateGraphAdj(file, PERIODICITY)
    else:
        return generateGraphGraphe(file)

def generateGraphAdj(file, PERIODICITY=False):
    """
        This function takes in graph data in the .txt format and constructs the graph with adjacency list representation.
        It also generates additional graph data stored in the graph_data object.
    
    Args:
        file (str): The name of the file containing the graph data.

    Returns:
        graph_data (graph_data_class): The graph data.
    """


    #get edge adjacency list, edge labels list, and boolean to indicate it is's 2D or 3D
    graph_data, green_edges_dic, DarkGreen_dic, LightGreen_dic = adjList(file)
    
    # labels, totalWhite, totalBlack = vertexColors(file)

    f = open(file, 'r')
    line = f.readline()
    line = line.split()
    dimX = int(line[0])
    dimY = int(line[1])


    g = graph_data.graph


    # add color to blue and red metavertices
    g.vs[g.vcount()-2]['color'] = 'blue'
    g.vs[g.vcount()-1]['color'] = 'red'

    shortest_path_to_red = g.distances(source=graph_data.redVertex, weights=g.es['weight'])[0]
    shortest_path_to_blue = g.distances(source=graph_data.blueVertex, weights=g.es['weight'])[0]


    # add wrap around edges and it's edge labels if periodicity boolean is set to True.
    if PERIODICITY:
        for i in range(0, g.vcount() - 2, dimX):
            # first add first neighbor wrap around
            g.add_edge(g.vs[i], g.vs[i + (dimX - 1)])
            g.es[g.ecount() - 1]['label'] = 'f'
            g.es[g.ecount() - 1]['weight'] = 1

            # add diagnol wrap arounds
            if i - 1 >= 0:
                g.add_edge(g.vs[i], g.vs[i - 1])
                g.es[g.ecount() - 1]['label'] = 's'
                g.es[g.ecount() - 1]['weight'] = math.sqrt(2)

            if i + (dimX * 2 - 1) <= dimX * dimY:
                g.add_edge(g.vs[i], g.vs[i + (dimX * 2 - 1)])
                g.es[g.ecount() - 1]['label'] = 's'
                g.es[g.ecount() - 1]['weight'] = math.sqrt(2)


 
    fg_blue, fg_red = filterGraph_blue_red(g)
    redComponent = set(fg_red.subcomponent(graph_data.redVertex, mode="ALL"))
    blueComponent = set(fg_blue.subcomponent(graph_data.blueVertex, mode="ALL"))

    # Add Green Interface and it's color

    if DEBUG:
        black_green_neighbors = []

    # counter for CT_n_D_adj_An
    CT_n_D_adj_An = 0
    # counter for CT_n_A_adj_Ca
    CT_n_A_adj_Ca = 0
    # counter for green black interface edges
    black_green = 0
    # counter for black interface vertices to red
    black_interface_red = 0
    # counter for white interface vertices to blue
    white_interface_blue = 0
    # counter for interface edges for complementary paths
    interface_edge_comp_paths = 0

    edge_count = 0

    white = set()
    black = set()

    vertices = set()

    for edge in g.es:
        edge_count += 1
        source_vertex = edge.source
        target_vertex = edge.target

        source_vertex_color = g.vs[source_vertex]['color']
        target_vertex_color = g.vs[target_vertex]['color']

        # if source_vertex == 30711 or target_vertex == 30711:
        #     print("src color:", source_vertex_color)
        #     print("target color:", target_vertex_color)

        if (source_vertex_color == 'blue' or target_vertex_color == 'blue'):
            if (source_vertex_color == 'blue' and target_vertex_color == 'white') \
                    or (source_vertex_color == 'white' and target_vertex_color == 'blue'):
                CT_n_A_adj_Ca += 1

        if (source_vertex_color == 'red' or target_vertex_color == 'red'):
            if (source_vertex_color == 'red' and target_vertex_color == 'black') \
                    or (source_vertex_color == 'black' and target_vertex_color == 'red'):
                CT_n_D_adj_An += 1

        # Add black/white edges to green interface node.
        if (source_vertex_color == 'black' and target_vertex_color == 'white') \
                or (source_vertex_color == 'white' and target_vertex_color == 'black'):

            if (source_vertex_color == 'black' and source_vertex in redComponent):
                black.add(source_vertex)
                vertices.add(source_vertex)
            if (target_vertex_color == 'black' and target_vertex in redComponent):
                black.add(target_vertex)
                vertices.add(target_vertex)

            if (source_vertex_color == 'white' and source_vertex in blueComponent):
                white.add(source_vertex)
            if (target_vertex_color == 'white' and target_vertex in blueComponent):
                white.add(target_vertex)

            if edge['label'] == 'f':
                # increment count when black and white interface pair, black has path to top (red), white has path to (bottom) blue
                if ((source_vertex_color == 'black' and target_vertex_color == 'white') \
                    and (source_vertex in redComponent and target_vertex in blueComponent)) \
                        or ((source_vertex_color == 'white' and target_vertex_color == 'black') \
                            and (source_vertex in blueComponent and target_vertex in redComponent)):
                    interface_edge_comp_paths += 1

                # increment black_green when black to green edge is added
                black_green += 1

            if DEBUG:
                if source_vertex_color == 'black':
                    black_green_neighbors.append(source_vertex)
                if target_vertex_color == 'black':
                    black_green_neighbors.append(target_vertex)

    edge_count = g.ecount()

    # Add Green Interface and it's color
    g.add_vertices(1)
    g.vs[g.vcount() - 1]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1].index

    g.add_vertices(1)
    g.vs[g.vcount() - 1]['color'] = 'DarkGreen'
    dark_green = g.vs[g.vcount() - 1].index

    g.add_vertices(1)
    g.vs[g.vcount() - 1]['color'] = 'LightGreen'
    light_green = g.vs[g.vcount() - 1].index

    green_edges_to_add = []
    green_edges_labels = []
    green_edges_weights = []

    for i in green_edges_dic:
        green_edges_to_add.append([i, green_vertex])
        green_edges_labels.append("f")  # every edges with green vertex are first order
        green_edges_weights.append(green_edges_dic[i].weight)

    for i in DarkGreen_dic:
        green_edges_to_add.append([i, dark_green])
        green_edges_labels.append("f")  # every edges with green vertex are first order
        green_edges_weights.append(DarkGreen_dic[i].weight)

    for i in LightGreen_dic:
        green_edges_to_add.append([i, light_green])
        green_edges_labels.append("f")  # every edges with green vertex are first order
        green_edges_weights.append(LightGreen_dic[i].weight)

    # add green vertex edges at once (without loop)
    g.add_edges(green_edges_to_add)

    # label, weight set
    g.es[edge_count:]["label"] = green_edges_labels
    g.es[edge_count:]["weight"] = green_edges_weights

    black_interface_red = len(black)  # correct
    white_interface_blue = len(white)  # correct

    # Create graph_data_class object

    # Store vertex attributes
    graph_data.graph = g
    graph_data.black_vertices = black_vertices
    graph_data.white_vertices = white_vertices
    graph_data.black_green = black_green
    graph_data.black_interface_red = black_interface_red
    graph_data.white_interface_blue = white_interface_blue
    graph_data.interface_edge_comp_paths = interface_edge_comp_paths
    graph_data.CT_n_D_adj_An = CT_n_D_adj_An
    graph_data.CT_n_A_adj_Ca = CT_n_A_adj_Ca

    if DEBUG:
        print(g.vs['color'])
        print("Number of nodes: ", g.vcount())
        print("Green vertex neighbors: ", g.neighbors(green_vertex))
        print("Green vertex neighbors LENGTH: ", len(g.neighbors(green_vertex)))
        print("Black/Green Neighbors: ", black_green_neighbors)
        print("Black/Green Neighbors LENGTH: ", len(black_green_neighbors))
        print("Nodes connected to blue: ", g.vs[g.vcount() - 3]['color'], g.neighbors(g.vcount() - 3))
        print("Length: ", len(g.neighbors(g.vcount() - 3)))
        print("Nodes connected to red: ", g.vs[g.vcount() - 2]['color'], g.neighbors(g.vcount() - 2))
        print("Length: ", len(g.neighbors(g.vcount() - 2)))
        # exit()

    if DEBUG2:
        print("new method Green vertex neighbors: ", green_edges_to_add)
        print("new method Green vertex LENGTH: ", len(green_edges_to_add))
        for i in range(len(green_edges_to_add)):
            print("edge: ", green_edges_to_add[i], "label: ", green_edges_labels[i], "weight: ", green_edges_weights[i])

        cnt = 0

        if cnt == len(g.neighbors(green_vertex)):
            print("all vertices stored well!")

    return graph_data


def generateGraphGraphe(file):
    """
    This function takes in graph data in the .graphe format and constructs the graph with adjacency list representation.
    
    Args:
        file (str): The name of the file containing graph data.

    Returns:
        g (igraph.Graph): The graph representation of the given data
        is_2D (bool): This is true if the graph represents a 2D structure, and false if it represents a 3D
    """
    # gets an adjacency list and first order pairs list from the file input
    graph_data = graphe_adjList(file)
    vertex_colors = adjvertexColors(file)

    # Extract adjacency list from graph object
    adjacency_list = [[] for _ in range(graph_data.graph.vcount())]
    for edge in graph_data.graph.get_edgelist():
        source, target = edge
        adjacency_list[source].append(target)
        adjacency_list[target].append(source)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    # creates graph using Igraph API
    g = ig.Graph(edges, directed=False)
    # adds color label to each vertex
    g.vs["color"] = vertex_colors

    # adds green vertex and its color
    g.add_vertices(1)
    if __debug__:
        print(len(adjacency_list))
        # exit()
    g.vs[len(adjacency_list)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]

    # exists = [0] * (g.vcount() - 3)


    # Loops through all pairings, adds edge between black and white pairings {black-green/white-green}, no multiple edges to same vertex if edge has already been added
    for pair in graph_data.first_order_neighbors:
        source_vertex = pair[0]
        target_vertex = pair[1]

        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white'
                or g.vs[target_vertex]['color'] == 'black') and g.vs[source_vertex]['color'] == 'white':
            # connect both source and target to green meta vertex
            g.add_edge(green_vertex, source_vertex)
            g.add_edge(green_vertex, target_vertex)

    graph_data.graph = g
    return graph_data



'''---------Function to create edges for graph in specified format --------'''
def adjList(fileName):
    """
        This function creates an adjacency list based on the graph data provided. An adjacency list represents a set of edges in the graph. It also generates additional
        graph data stored in the graph_data object.
        It also counts the vertices connected to interface edges.

        Args:
            filename (str): The name of the file containing the graph data.

        Returns:
            graph_data (graph_data_class): The graph data.
            edges_with_green({vertex : edge_info}dictionary): Storing edges connected with green vertex
)
    """
    adjacency_list = {}
    if DEBUG:
        first_order_pairs = []
        second_order_pairs = []
        third_order_pairs = []

    edge_labels = []
    edge_weights = []
    black_vertices = []
    white_vertices = []

    redVertex = None
    blueVertex = None

    is_2d = True
    with open(fileName, "r") as file:
        header = file.readline().strip().split(' ')
        dimX, dimY = int(header[0]), int(header[1])
        dim = dimY
        if len(header) < 3:
            dimZ = 1
        else:
            if int(header[2]) == 0:
                dimZ = 1
            else:
                dimZ = int(header[2])

        if dimZ > 1:
            # dimZ = dimX * dimY
            is_2d = False
            dim = dimZ
        offsets = [(-1, -1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1), (-1,-1,-1), (-1,0,-1), (0,-1,-1), (1,-1,-1),
                   (1,0,-1), (1,-1,0)]

        vertex_color = [""] * (dimX * dimY * dimZ)


        input_data = np.loadtxt(fileName, skiprows=1)
        reshaped_data = input_data.flatten()

        #Loops through input and adds adjacency list of current vertex based on Offsets. Offsets, make it so edges aren't duplicated.
        #Also adds edge labels based on Graspi Documentation

        edges_with_green = {}   # dictionary for storing vertices connected with green vertex
        edges_with_LightGreen = {}
        edges_with_DarkGreen = {}

    for z in range(dimZ):
        for y in range(dimY):
            for x in range(dimX):
                current_vertex = z * dimY * dimX + y * dimX + x
                if reshaped_data[current_vertex] == 1:
                    vertex_color[current_vertex] = 'white'
                    white_vertices.append(current_vertex)
                elif reshaped_data[current_vertex] == 0:
                    vertex_color[current_vertex] = 'black'
                    black_vertices.append(current_vertex)

                neighbors = []

                for i in range(len(offsets)):
                    dx, dy, dz = offsets[i]
                    dist = dx**2 + dy**2 + dz**2
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < dimX and 0 <= ny < dimY and 0 <= nz < dimZ:
                        neighbor_vertex = nz * dimY * dimX + ny * dimX + nx

                        if dist == 1:
                            if DEBUG:
                                first_order_pairs.append([min(current_vertex, neighbor_vertex), max(current_vertex, neighbor_vertex)])
                            edge_labels.append("f")
                            edge_weights.append(1*pixelSize)

                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 1: # interface edges
                                if DEBUG2:
                                    print(current_vertex, neighbor_vertex)
                                store_interface_edges(edges_with_green, current_vertex, reshaped_data[current_vertex], 1, 1)
                                store_interface_edges(edges_with_green, neighbor_vertex, reshaped_data[neighbor_vertex], 1, 1)

                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 3: # gray-white interface
                                if DEBUG2:
                                    print(current_vertex, neighbor_vertex)
                                store_interface_edges(edges_with_LightGreen, current_vertex, reshaped_data[current_vertex], 1, 1)
                                store_interface_edges(edges_with_LightGreen, neighbor_vertex, reshaped_data[neighbor_vertex], 1, 1)

                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 4: # gray-black interface
                                if DEBUG2:
                                    print(current_vertex, neighbor_vertex)
                                store_interface_edges(edges_with_DarkGreen, current_vertex, reshaped_data[current_vertex], 1, 1)
                                store_interface_edges(edges_with_DarkGreen, neighbor_vertex, reshaped_data[neighbor_vertex], 1, 1)

                        elif dist == 3:
                            if DEBUG:
                                third_order_pairs.append([min(current_vertex, neighbor_vertex), max(current_vertex, neighbor_vertex)])
                            edge_labels.append("t")
                            edge_weights.append(float(math.sqrt(3))*pixelSize)

                        else:
                            if DEBUG:
                                second_order_pairs.append([min(current_vertex, neighbor_vertex), max(current_vertex, neighbor_vertex)])
                            edge_labels.append("s")
                            edge_weights.append(float(math.sqrt(2))*pixelSize)
                        neighbors.append(neighbor_vertex)
                adjacency_list[current_vertex] = neighbors


    if not is_2d:
        # add edges to Blue Node for 3D
        adjacency_list[dimZ * dimY * dimX] = []
        blueVertex = dimZ * dimY * dimX
        for y in range(dimY):
            for x in range(dimX):
                vertex_index = y * dimX + x
                adjacency_list[dimZ * dimY * dimX].append(vertex_index)
                edge_labels.append("s")
                edge_weights.append(0)

        #add edges to Red Node for 3D
        adjacency_list[dimZ * dimY * dimX + 1] = []
        redVertex = dimZ * dimY * dimX + 1
        for y in range(dimY):
            for x in range(dimX):
                vertex_index = (dimZ - 1) * (dimY * dimX) + y * dimX + x
                adjacency_list[dimZ * dimY * dimX + 1].append(vertex_index)
                edge_labels.append("s")
                edge_weights.append(0)

    elif is_2d:
        # add edges to Blue Node for 2D
        adjacency_list[dimZ * dimY * dimX] = []
        blueVertex = dimZ * dimY * dimX
        for z in range(dimZ):
            for x in range(dimX):
                vertex_index = z * (dimY * dimX) + x
                adjacency_list[dimZ * dimY * dimX].append(vertex_index)
                edge_labels.append("s")
                edge_weights.append(0)

        #add edges to Red Node for 2D
        adjacency_list[dimZ * dimY * dimX + 1] = []
        redVertex = dimZ * dimY * dimX + 1
        for z in range(dimZ):
            for x in range(dimX):
                vertex_index = z * (dimY * dimX) + (dimY - 1) * dimX + x
                adjacency_list[dimZ * dimY * dimX + 1].append(vertex_index)
                edge_labels.append("s")
                edge_weights.append(0)

    edges_dict = {v: [n for n in neighbors] for v, neighbors in adjacency_list.items()}
    g = ig.Graph.ListDict(edges=edges_dict, directed=False)
    g.vs["color"] = vertex_color
    g.es['label'] = edge_labels
    g.es['weight'] = edge_weights

    graph_data = GraphData.graph_data_class(graph=g, is_2D=is_2d)

    # Store vertex attributes
    graph_data.graph = g
    graph_data.is_2D = is_2d
    graph_data.black_vertices = black_vertices
    graph_data.white_vertices = white_vertices
    graph_data.dim = dim
    graph_data.redVertex = redVertex
    graph_data.blueVertex = blueVertex

    if redVertex is not None and blueVertex is not None:
        graph_data.compute_shortest_paths(red_vertex=redVertex, blue_vertex=blueVertex)

    if DEBUG:
        print("Adjacency List: ", adjacency_list)
        print("Adjacency List LENGTH: ", len(adjacency_list))
        print("First Order Pairs: ", first_order_pairs)
        print("First Order Pairs LENGTH: ", len(first_order_pairs))
        print("Second Order Pairs: ", second_order_pairs)
        print("Second Order Pairs LENGTH: ", len(second_order_pairs))
        print("Third Order Pairs: ", third_order_pairs)
        print("Third Order Pairs LENGTH: ", len(third_order_pairs))
        print("Blue Node neighbors: ", adjacency_list[dimZ * dimY * dimX])
        print("Red Node neighbors: ", adjacency_list[dimZ * dimY * dimX + 1])
        # exit()
    if DEBUG2:
        print("new method Green Edges len : ", len(edges_with_green))

    # return adjacency_list, edge_labels, edge_weights, vertex_color, black_vertices, white_vertices, is_2d, redVertex, blueVertex, dim, edges_with_green
    return graph_data, edges_with_green, edges_with_DarkGreen, edges_with_LightGreen


def graphe_adjList(filename):
    """
    This function creates the adjacency list for graph data given in .graphe format, it categorizes neighbors of vertices into first, second, and third order.
    This function is called inside the “generateGraphGraphe” function to help create the necessary information to generate the final graph.

    Args:
        filename (str): The name of the file containing the graph data.

    Returns:
        graph_data (graph_data_class): The graph data containing graph, is_2D, first_order_neighbors, second_order_neighbors, and third_order_neighbors attributes
    """

    adjacency_list = []
    first_order_neighbors = []
    second_order_neighbors = []
    third_order_neighbors = []
    # Opens File
    with open(filename, "r") as file:
        header = file.readline().split()
        vertex_count = int(header[0])
        # loops through all vertices except red and blue meta vertices at the end
        for i in range(vertex_count):
            header = file.readline().split()
            neighbors = []
            # adds all vertex neighbors to current "header" vertex being checked
            # makes sure no edge duplicates exist with prior vertices already checked
            for j in range(2, len(header), 3):
                order_neighbor_type = header[j + 2]
                if int(header[j]) < len(adjacency_list):
                    if i not in adjacency_list[int(header[j])]:
                        neighbors.append(int(header[j]))
                else:
                    neighbors.append(int(header[j]))
                # adds order neighbor type depending on what input states, it is located 2 indices after the node number
                if order_neighbor_type == 'f':
                    first_order_neighbors.append([int(header[j]), i])
                elif order_neighbor_type == 's':
                    second_order_neighbors.append([int(header[j]), i])
                elif order_neighbor_type == 't':
                    third_order_neighbors.append([int(header[j]), i])
            adjacency_list.append(neighbors)

    #Adds empty lists for Red and Blue nodes since input should have already added any nodes that belong to them, this removes duplicate edges (no cycles)
    adjacency_list.append([])
    adjacency_list.append([])

    # the only input files that have third order neighbors are 3D input files, this checks for that
    is_2D = False
    if len(third_order_neighbors) <= 0:
        is_2D = True

    edges_dict = {v: neighbors for v, neighbors in enumerate(adjacency_list)}
    g = ig.Graph.ListDict(edges=edges_dict, directed=False)

    # Create graph_data_class object
    graph_data = GraphData.graph_data_class(graph=g, is_2D=is_2D)
    graph_data.is_2D = is_2D
    graph_data.first_order_neighbors = first_order_neighbors
    graph_data.second_order_neighbors = second_order_neighbors
    graph_data.third_order_neighbors = third_order_neighbors

    return graph_data


'''------- Labeling the color of the vertices -------'''

def adjvertexColors(fileName):
    """
        This function assigns each vertex a color label based on the data in the specified file and returns a list where each index corresponds to a vertex's color.
    Args:
        fileName (str): The name of the file containing the vertex color data.

    Returns:
        labels (list): This list contains color labels (‘black’, ‘white’, ‘red’, or ‘blue’) for each vertex or metavertex in the graph.
    """
    labels = []
    with open(fileName, 'r') as file:
        line = file.readline().split()
        vertex_count = int(line[0])
        for i in range(vertex_count + 2):
            line = file.readline().split()
            char = line[1]
            if char == '1':
                labels.append('white')
            elif char == '0':
                labels.append('black')
            elif char == '10':
                labels.append('blue')
            elif char == '20':
                labels.append('red')

    return labels






def visualize(graph, is_2D):
    """
       This function shows a visualization of the given graph in either 2D or 3D depending on the is_2D boolean.

       Args:
            graph (igraph.Graph): The given graph to visualize.
            is_2D (bool): This is true if the graph represents a 2D structure, and false if it represents a 3D
       
       Returns:
           This function does not return a value, it performs an action by outputting the visualization of the given graph using plt.
       """
    g = graph
    if is_2D:
        layout = g.layout('fr')
        # fig, ax = plt.subplots()
        # ax.invert_yaxis() # reverse starting point of graph (vertex 0)
        fig, ax = plt.subplots(figsize=(10, 10))

        ig.plot(g, target=ax, layout=layout, vertex_size=15, margin=5)

        ''' ---- generate the labels of each vertex value ---- '''
        for i, (x, y) in enumerate(layout):
            g.vs['label'] = [i for i in range(len(g.vs))]
            ax.text(
                x, y - 0.2,
                g.vs['label'][i],
                fontsize=10,
                color='black',
                ha='right',  # Horizontal alignment
                va='top',  # Vertical alignment
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.3)
            )

        plt.show()
    else:
        """
            Visualizes the graph in 3D.

            Args:
                g (ig.Graph): The input graph to visualize.

            Returns:
                None
            """
        edges = g.get_edgelist()
        num_vertices = len(g.vs)
        grid_size = int(np.ceil(num_vertices ** (1 / 3)))

        # Generate 3D coordinates (layout) for the vertices
        x, y, z = np.meshgrid(range(grid_size), range(grid_size), range(grid_size))
        coords = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T[:num_vertices]  # Ensure coords match the number of vertices

        # Plot the graph in 3D using matplotlib
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        color = g.vs['color']

        # Plot vertices
        ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=color, s=100)

        # Plot edges
        for e in edges:
            start, end = e
            ax.plot([coords[start][0], coords[end][0]],
                    [coords[start][1], coords[end][1]],
                    [coords[start][2], coords[end][2]], 'black')

        # Add labels to the vertices
        for i, (x, y, z) in enumerate(coords):
            ax.text(x, y, z, str(i), color='black')

        plt.show()



'''**************** Connected Components *******************'''


def connectedComponents(graph):
    """
        This function identifies the connected components of a filtered graph and returns lists that contain the vertices that are part of the connected components.
        It filters based on ‘black’ vertices that connect to the ‘red’ metavertex and ‘white’ vertices that connect to the ‘blue’ metavertex.

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        connected_comp (list): The list will contain a list or several lists, depending on how many connected components there are. Each list contains the vertices that are part of the connected component.
    """
    vertices = graph.vcount()
    edgeList = set(graph.get_edgelist())
    fg = filterGraph(graph)
    cc = fg.connected_components()
    redVertex = None
    blueVertex = None
    blackCCList = []
    whiteCCList = []

    for vertex in range(vertices - 1, -1, -1):
        color = graph.vs[vertex]['color']
        if color == 'blue':
            blueVertex = vertex
        elif color == 'red':
            redVertex = vertex
        if blueVertex is not None and redVertex is not None:
            break

    blackCCList = [c for c in cc if graph.vs[c[0]]['color'] == 'black']
    whiteCCList = [c for c in cc if graph.vs[c[0]]['color'] == 'white']

    for c in blackCCList:
        passedRed = False
        passedBlue = False
        for vertex in c:
            if not passedRed:
                if (vertex, redVertex) in edgeList or (redVertex, vertex) in edgeList:
                    c.append(redVertex)
                    passedRed = True
            if not passedBlue:
                if (vertex, blueVertex) in edgeList or (blueVertex, vertex) in edgeList:
                    c.append(blueVertex)
                    passedBlue = True
            if passedBlue and passedRed:
                break

    for c in whiteCCList:
        passedRed = False
        passedBlue = False
        for vertex in c:
            if not passedRed:
                if (vertex, redVertex) in edgeList or (redVertex, vertex) in edgeList:
                    c.append(redVertex)
                    passedRed = True
            if not passedBlue:
                if (vertex, blueVertex) in edgeList or (blueVertex, vertex) in edgeList:
                    c.append(blueVertex)
                    passedBlue = True
            if passedBlue and passedRed:
                break

    connected_comp = whiteCCList + blackCCList

    return connected_comp


'''********* Filtering the Graph **********'''

def filterGraph(graph):
    """
        This function returns a subgraph that is created by filtering the given graph to only contain edges that connect vertices of the same color.
    Args:
        graph (ig.Graph): The input graph.

    Returns:
        filteredGraph (igraph.Graph): The filtered graph with only edges between the same color vertices.
    """
    edgeList = graph.get_edgelist()
    keptEdges = []

    #Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if (graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=False)

    return filteredGraph


'''********* Constructing the Graph **********'''
def filterGraph_metavertices(graph):
    """
        This function filters the given graph into two subgraphs, one that contains all the edges that connect vertices of the same color or involve the ‘blue’/cathode metavertex,
        and one that contains all the edges that connect the vertices of the same color or involve the ‘red’/anode metavertex.
    Args:
        graph (ig.Graph): The input graph.

    Returns:
        fg_blue (igraph.Graph): This is a subgraph that only contains the edges that either connect vertices of the same color or involve a ‘blue’ vertex.
        fg_red (igraph.Graph): This is a subgraph that only contains the edges that either connect vertices of the same color or involve a ‘red’ vertex.    """
    edgeList = graph.get_edgelist()
    keptEdges_blue = []
    keptWeights_blue = []
    keptEdges_red = []
    keptWeights_red= []

    #Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if (graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges_blue.append(edge)
            keptEdges_red.append(edge)
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

        if ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges_blue.append(edge)
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
        elif ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')) :
            keptEdges_red.append(edge)
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

    fg_blue = graph.subgraph_edges(keptEdges_blue, delete_vertices=False)
    fg_blue.es['weight'] = keptWeights_blue

    fg_red = graph.subgraph_edges(keptEdges_red, delete_vertices=False)
    fg_red.es['weight'] = keptWeights_red

    return fg_blue, fg_red


def filterGraph_blue_red(graph):
    """
        This function filters the given graph into two subgraphs, one that contains all the edges that connect vertices of the same color or involve the ‘blue’ cathode metavertex,
        and one that contains all the edges that connect the vertices of the same color or involve the ‘red’ anode metavertex.
    Args:
        graph (ig.Graph): The input graph.

    Returns:
        fg_blue (igraph.Graph): This is a subgraph that only contains the edges that either connect vertices of the same color or involve a ‘blue’ metavertex.
        fg_red (igraph.Graph): This is a subgraph that only contains the edges that either connect vertices of the same color or involve a ‘red’ metavertex.    
    """
    
    edgeList = graph.get_edgelist()
    keptEdges_blue = []
    keptWeights_blue = []
    keptEdges_red = []
    keptWeights_red= []

    #Checks edges and keeps only edges that connect to the same colored vertices
    #improvement point 4: graph.vs[toNode]['color'] caching? (make a blue_list)
      
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if (graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges_blue.append(edge)
            keptEdges_red.append(edge)
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

        if ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges_blue.append(edge)
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
        
        if ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')):
            keptEdges_red.append(edge)
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

    fg_blue = graph.subgraph_edges(keptEdges_blue, delete_vertices=False)
    fg_blue.es['weight'] = keptWeights_blue

    fg_red = graph.subgraph_edges(keptEdges_red, delete_vertices=False)
    fg_red.es['weight'] = keptWeights_red

    return fg_blue, fg_red


def main():
    global PERIODICITY, n_flag, pixelSize
    PERIODICITY = False
    n_flag = 2
    pixelSize = 1  # Default pixel size

    # Validate and parse command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python graph.py -a <INPUT_FILE.txt> [-s <pixelSize>] [-p <{0,1}>] [-n <{2,3}>] OR -g <INPUT_FILE.graphe>")
        return

    # Handle structured data
    if sys.argv[1] == "-a":
        filename = sys.argv[2]
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "-p":
                if i + 1 < len(sys.argv):
                    if sys.argv[i + 1] == "1":
                        PERIODICITY = True
                    elif sys.argv[i + 1] == "0":
                        PERIODICITY = False
                    else:
                        print("Invalid argument for -p. Use 0 or 1.")
                        return
                    i += 2
                else:
                    print("Missing value for -p flag.")
                    return
            elif sys.argv[i] == "-n":
                if i + 1 < len(sys.argv):
                    if sys.argv[i + 1] == "2":
                        n_flag = 2
                    elif sys.argv[i + 1] == "3":
                        print("3 Phase not yet implemented.")
                        return
                    else:
                        print("Invalid argument for -n. Use 2 or 3.")
                        return
                    i += 2
                else:
                    print("Missing value for -n flag.")
                    return
            elif sys.argv[i] == "-s":
                if i + 1 < len(sys.argv):
                    try:
                        pixelSize = float(sys.argv[i + 1])
                    except ValueError:
                        print("Invalid pixel size. Must be a number.")
                        return
                    i += 2
                else:
                    print("Missing value for -s flag.")
                    return
            else:
                print(f"Unknown argument: {sys.argv[i]}")
                return

        graph_data = generateGraphAdj(filename, PERIODICITY)

    # Handle unstructured data
    elif sys.argv[1] == "-g":
        if len(sys.argv) > 3 and any(flag in sys.argv for flag in ["-p", "-n", "-s"]):
            print("Error: -p, -n, and -s flags cannot be used with -g. Only -a supports them.")
            return
        if len(sys.argv) != 3:
            print("Usage: python graph.py -g <INPUT_FILE.graphe>")
            return
        graph_data = generateGraphGraphe(sys.argv[2])

    else:
        print("Usage: python graph.py -a <INPUT_FILE.txt> [-s <pixelSize>] [-p <{0,1}>] [-n <{2,3}>] OR -g <INPUT_FILE.graphe>")
        return

    # Visualize and filter the graph
    visualize(graph_data.graph, graph_data.is_2D)
    filteredGraph = filterGraph(graph_data.graph)
    visualize(filteredGraph, graph_data.is_2D)

    # Debug info
    if DEBUG:
        dic = d.descriptors(graph_data.graph, sys.argv[2], pixelSize)
        print(connectedComponents(filteredGraph))
        for key, value in dic.items():
            print(key, value)

if __name__ == '__main__':
    main()
