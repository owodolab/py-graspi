import sys
from fileinput import filename

import igraph as ig
import matplotlib.pyplot as plt
from igraph.drawing.plotly.graph import plotly
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

from numpy import character

import descriptors as d
import math
DEBUG = False # debugging mode
DEBUG2 = False   # for green edges
PERIODICITY = True
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
def store_green_edges(v_with_green_vertex, index, color, order, weight):
    if index in v_with_green_vertex:
        cur_v = v_with_green_vertex[index]
        if v_with_green_vertex[index].weight > weight * 0.5:     # if previous order is higher than new one
            v_with_green_vertex[index].weight = weight * 0.5     # change it to lower order      

    else:
        newEdge = edge_info()
        newEdge.color = color
        newEdge.index = index
        newEdge.order = order   #order = 1,2,3
        newEdge.weight = weight * 0.5
        
        v_with_green_vertex[index] = newEdge

'''---------Function to create edges for graph in specified format --------'''


def adjList(fileName):
    """
        Creates an adjacency list from a given file.

        Args:
            filename (str): The name of the file containing the graph data.

        Returns:
            list: The adjacency list representing the graph, lists for first, second, and third, ordered pairs
                  as well as a bool to signal if the graph is a 2D or 3D graph.
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


        import time
        # loadtxt_start = time.time()
        input_data = np.loadtxt(fileName, skiprows=1)
        reshaped_data = input_data.flatten()
        # loadtxt_end = time.time()
        # print("loadtxt time : ", loadtxt_end - loadtxt_start)

        #Loops through input and adds adjacency list of current vertex based on Offsets. Offsets, make it so edges aren't duplicated.
        #Also adds edge labels based on Graspi Documentation

        vertices_with_green_v = {}   # dictionary for storing vertices connected with green vertex


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
                            edge_weights.append(1)

                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 1:
                                if DEBUG2:
                                    print(current_vertex, neighbor_vertex)
                                store_green_edges(vertices_with_green_v, current_vertex, reshaped_data[current_vertex], 1, 1)
                                store_green_edges(vertices_with_green_v, neighbor_vertex, reshaped_data[neighbor_vertex], 1, 1)

                        elif dist == 3:
                            if DEBUG:
                                third_order_pairs.append([min(current_vertex, neighbor_vertex), max(current_vertex, neighbor_vertex)])
                            edge_labels.append("t")
                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 1:
                                edge_weights.append(float(math.sqrt(3) * 0.5))
                            else:
                                edge_weights.append(float(math.sqrt(3)))

                        else:
                            if DEBUG:
                                second_order_pairs.append([min(current_vertex, neighbor_vertex), max(current_vertex, neighbor_vertex)])
                            edge_labels.append("s")
                            if reshaped_data[current_vertex] + reshaped_data[neighbor_vertex] == 1:
                                edge_weights.append(float(math.sqrt(2) * 0.5))
                            else:
                                edge_weights.append(float(math.sqrt(2)))

                        neighbors.append(neighbor_vertex)

                adjacency_list[current_vertex] = neighbors

                #  PERIODIC WRAP-AROUND edges
                if PERIODICITY:
                    # --- X axis wrap-around (row-wise) ---
                    if x == 0:
                        right = current_vertex + (dimX - 1)
                        if DEBUG:
                            first_order_pairs.append([min(current_vertex, right), max(current_vertex, right)])
                        edge_labels.append("f")
                        edge_weights.append(1)

                        if reshaped_data[current_vertex] + reshaped_data[right] == 1:
                            if DEBUG2:
                                print("X-periodicity detected:", current_vertex, right)
                            store_green_edges(vertices_with_green_v, current_vertex, reshaped_data[current_vertex], 1, 1)
                            store_green_edges(vertices_with_green_v, right, reshaped_data[right], 1, 1)

                        neighbors.append(right)

                    # --- Y axis wrap-around (col-wise) ---
                    if not is_2d and y == 0:
                        bottom = current_vertex + dimX * (dimY - 1)
                        if DEBUG:
                            first_order_pairs.append([min(current_vertex, bottom), max(current_vertex, bottom)])
                        edge_labels.append("f")
                        edge_weights.append(1)

                        if reshaped_data[current_vertex] + reshaped_data[bottom] == 1:
                            if DEBUG2:
                                print("Y-periodicity detected:", current_vertex, bottom)
                            store_green_edges(vertices_with_green_v, current_vertex, reshaped_data[current_vertex], 1, 1)
                            store_green_edges(vertices_with_green_v, bottom, reshaped_data[bottom], 1, 1)

                        neighbors.append(bottom)

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
        print("new method Green Edges len : ", len(vertices_with_green_v))

    return adjacency_list, edge_labels, edge_weights, vertex_color, black_vertices, white_vertices, is_2d, redVertex, blueVertex, dim, vertices_with_green_v


def graphe_adjList(filename):
    """
    Creates an adjacency list from a given file.

    Args:
        filename (str): The name of the file containing the graph data.

    Returns:
        list: The adjacency list representing the graph, lists for first, second, and third, ordered pairs
                  as well as a bool to signal if the graph is a 2D or 3D graph.
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

    #only input files that have third order neighbors are 3D input files, this checks for that
    is_2D = False
    if len(third_order_neighbors) <= 0:
        is_2D = True
    return adjacency_list, first_order_neighbors, second_order_neighbors, third_order_neighbors, is_2D


'''------- Labeling the color of the vertices -------'''

def adjvertexColors(fileName):
    """
    Labels the colors of verti gces based on a given file and on Graspi Documentation.

    Args:
        fileName (str): The name of the file containing the vertex color data.

    Returns:
        list: A list of vertex colors.
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


'''********* Constructing the Graph **********'''
def filterGraph_metavertices(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color and metavertices

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        ig.Graph: The filtered graph.
    """
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

def generateGraphGraphe(file):
    """
    Constructs a graph from an adjacency list and assigns vertex colors.

    Args:
        file (str): The name of the file containing graph data.

    Returns:
        ig.Graph: The constructed graph with assigned vertex colors.
        boolean: a boolean to signal if grpah is 2D or not
    """
    # gets an adjacency list and first order pairs list from the file input
    adjacency_list, first_order_neighbors, second_order_neighbors, third_order_neighbors, is_2d = graphe_adjList(file)
    vertex_colors = adjvertexColors(file)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    # creates graph using Igraph API
    g = ig.Graph(edges, directed=False)
    # adds color label to each vertex
    g.vs["color"] = vertex_colors

    # adds green vertex and its color
    g.add_vertices(1)
    if DEBUG:
        print(len(adjacency_list))
        # exit()
    g.vs[len(adjacency_list)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]

    # exists = [0] * (g.vcount() - 3)


    # Loops through all pairings, adds edge between black and white pairings {black-green/white-green}, no multiple edges to same vertex if edge has already been added
    for pair in first_order_neighbors:
        source_vertex = pair[0]
        target_vertex = pair[1]

        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white'
                or g.vs[target_vertex]['color'] == 'black') and g.vs[source_vertex]['color'] == 'white':
            # connect both source and target to green meta vertex
            g.add_edge(green_vertex, source_vertex)
            g.add_edge(green_vertex, target_vertex)

    # print(test)
    return g, is_2d


def filterGraph_blue_red(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color and metavertices

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        ig.Graph: The filtered graph.
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

    return fg_blue, fg_red, keptEdges_blue, keptEdges_red

def generateGraphAdj(file):
    """
        Creates an adjacency list from a given file.

        Args:
            filename (str): The name of the file containing the graph data.

        Returns:
            graph: the graph that holds all the edges and vertices based on file input
            boolean: returns  a boolean to signal if graph is 2D or not
        """

    import time
    const_adj_start = time.time()

    #get edge adjacency list, edge labels list, and boolean to indicate it is's 2D or 3D
    edges, edge_labels, edge_weights, vertex_color, black_vertices, white_vertices, is_2D, \
        redVertex, blueVertex, dim, greenv_dic = adjList(file)
    
    const_adj_end = time.time()     
    const_adj_time = const_adj_end - const_adj_start

    if DEBUG:
        print("PART #1 time : ",const_adj_time)    

    # labels, totalWhite, totalBlack = vertexColors(file)
    f = open(file, 'r')
    line = f.readline()
    line = line.split()
    dimX = int(line[0])
    dimY = int(line[1])
    dimZ = int(line[2])

    # print("xyz:", dimX, dimY, dimZ)
    g = ig.Graph.ListDict(edges=edges, directed=False)
    color_dict = {0:"black", 1:"white"}
    g.vs["color"] = vertex_color

    # g.vs["color"] = vertex_color
    g.es['label'] = edge_labels
    g.es['weight'] = edge_weights

    # add color to blue and red metavertices
    g.vs[g.vcount()-2]['color'] = 'blue'
    g.vs[g.vcount()-1]['color'] = 'red'

    # shortest_start = time.time()
    shortest_path_to_red = g.shortest_paths(source = redVertex, weights = g.es['weight'])[0]    #different point 1
    shortest_path_to_blue = g.shortest_paths(source = blueVertex,weights = g.es['weight'])[0]

    # shortest_end = time.time()     
    # shortest_time = shortest_end - shortest_start

    # print("shortest time : ", shortest_time)    

    others_start = time.time()    



    # filter_start = time.time()
    fg_blue, fg_red, keptEdges_blue, keptEdges_red = filterGraph_blue_red(g)   # different point 2
    redComponent = set(fg_red.subcomponent(redVertex, mode="ALL"))
    blueComponent = set(fg_blue.subcomponent(blueVertex, mode="ALL"))
    # filter_end = time.time()
    # filter_time = filter_end - filter_start

    # print("filter time (in PART #2):", filter_time)
    


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

    edges_index_start = 0
    extra_edges = 0
    edge_count = 0
    edges_to_add_set = set()

    white = set()
    black = set()

    vertices = set()
    others_end = time.time()     
    others_time = others_end - others_start

    if DEBUG:
        print("PART #2 time : ",others_time)    

    loop_start = time.time()

    # for edge in keptEdges_red:
    #     source_vertex = edge.source
    #     target_vertex = edge.target

    #     source_vertex_color = g.vs[source_vertex]['color']
    #     target_vertex_color = g.vs[target_vertex]['color']


        #all edge traversal
        #Add black/white edges to green interface node.
    for edge in g.es[edges_index_start:]:
        edge_count += 1
        source_vertex = edge.source
        target_vertex = edge.target

        source_vertex_color = g.vs[source_vertex]['color']
        target_vertex_color = g.vs[target_vertex]['color']

        if(source_vertex_color == 'blue' or target_vertex_color == 'blue'):
            if(source_vertex_color == 'blue' and target_vertex_color == 'white') \
                or (source_vertex_color == 'white' and target_vertex_color == 'blue'):
                CT_n_A_adj_Ca += 1

        if(source_vertex_color == 'red' or target_vertex_color == 'red'):
            if(source_vertex_color == 'red' and target_vertex_color == 'black') \
                or (source_vertex_color == 'black' and target_vertex_color == 'red'):
                CT_n_D_adj_An += 1

        #Add black/white edges to green interface node.
        if (source_vertex_color == 'black' and target_vertex_color == 'white') \
            or (source_vertex_color == 'white' and target_vertex_color == 'black'):

            if (source_vertex_color == 'black' and source_vertex in redComponent):
                black.add(source_vertex)
                vertices.add(source_vertex)
            if(target_vertex_color == 'black' and target_vertex in redComponent):
                black.add(target_vertex)
                vertices.add(target_vertex)
            
            if (source_vertex_color == 'white' and source_vertex in blueComponent):
                white.add(source_vertex)
            if (target_vertex_color == 'white' and target_vertex in blueComponent):
                white.add(target_vertex)

            
            if edge['label'] == 'f':
                # increment count when black and white interface pair, black has path to top (red), white has path to (bottom) blue
                if ((source_vertex_color == 'black' and target_vertex_color == 'white') \
                    and (source_vertex in redComponent and target_vertex in blueComponent))\
                        or ((source_vertex_color == 'white' and target_vertex_color == 'black') \
                            and (source_vertex in blueComponent and target_vertex in redComponent)):
                    interface_edge_comp_paths += 1
                

                # increment black_green when black to green edge is added
                black_green += 1 #useless?


            if DEBUG:
                if source_vertex_color == 'black':
                    black_green_neighbors.append(source_vertex)
            if DEBUG:
                if target_vertex_color == 'black':
                    black_green_neighbors.append(target_vertex)

    starting_index = g.ecount()


    #Add Green Interface and it's color
    g.add_vertices(1)
    g.vs[g.vcount()-1]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1].index

    green_edges_to_add = []
    green_edges_labels = []
    green_edges_weights = []

    for i in greenv_dic:
        green_edges_to_add.append([i, green_vertex])
        green_edges_labels.append("f")  #every edges with green vertex are first order 
        green_edges_weights.append(greenv_dic[i].weight)

    # add green vertex edges at once (without loop) 
    g.add_edges(green_edges_to_add)

    # label, weight set
    g.es[starting_index:]["label"] = green_edges_labels
    g.es[starting_index:]["weight"] = green_edges_weights    


    black_interface_red = len(black)
    white_interface_blue = len(white)

    loop_end = time.time()     
    loop_time = loop_end - loop_start

    if DEBUG:
        print("PART #3 time : ",loop_time)    


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
        print("previous method Green vertex neighbors: ", g.neighbors(green_vertex))
        print("previous method Green vertex neighbors LENGTH: ", len(g.neighbors(green_vertex)))
        print("new method Green vertex neighbors: ", green_edges_to_add)
        print("new method Green vertex LENGTH: ", len(green_edges_to_add))
        for i in range(len(green_edges_to_add)):
            print ("edge: ", green_edges_to_add[i], "label: ", green_edges_labels[i], "weight: ", green_edges_weights[i])

        cnt = 0
                
        if cnt == len(g.neighbors(green_vertex)):
            print("all vertices stored well!")


    return g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, \
        dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca


def generateGraph(file):
    """
    Generates graph based on file input.

    Args:
        file (str): The name of the file containing graph data.

    Returns:
        Generated graph based on input
    """
    if os.path.splitext(file)[1] == ".txt":
        return generateGraphAdj(file)
    else:
        return generateGraphGraphe(file)


def visualize(graph, is_2D):
    """
       Creates a visualization from the given graph

       Args:
           graph (ig.Graph): The graph to visualize
           is_2D (bool): A boolean to signal if the graph is 2D or not

       Returns:
           NONE: but outputs visualization of graph.
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


'''********* Filtering the Graph **********'''

def filterGraph(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color.

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        ig.Graph: The filtered graph.
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


'''**************** Connected Components *******************'''


def connectedComponents(graph):
    """
    Identifies the connected components of the filtered graph.

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        list: A list of connected components.
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


def main():
    if sys.argv[1] == "-p":
        # global PERIODICITY
        # PERIODICITY = True
        if sys.argv[2] == "-g":
            g, is_2D = generateGraphGraphe(sys.argv[3])  # utilizing the test file found in 2D-testFiles folder
            visualize(g, is_2D)
            filteredGraph = filterGraph(g)
            visualize(filteredGraph, is_2D)

            if DEBUG:
                dic = d.descriptors(g)
                print(connectedComponents(filteredGraph))
                for key, value in dic.items():
                    print(key, value)

        elif sys.argv[1] != "-g":
            (g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
             dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
             CT_n_D_adj_An, CT_n_A_adj_Ca)= generateGraphAdj(sys.argv[2])  # utilizing the test file found in 2D-testFiles folder
            visualize(g, is_2D)
            filteredGraph = filterGraph(g)
            visualize(filteredGraph, is_2D)

            if DEBUG:
                dic = d.descriptors(g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
                dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
                CT_n_D_adj_An, CT_n_A_adj_Ca)
                print(connectedComponents(filteredGraph))
                for key, value in dic.items():
                    print(key, value)

        else:
            if sys.argv[1] == "-g":
                g, is_2D = generateGraphGraphe(sys.argv[2])  # utilizing the test file found in 2D-testFiles folder
                visualize(g, is_2D)
                filteredGraph = filterGraph(g)
                visualize(filteredGraph, is_2D)
                if DEBUG:
                    print(connectedComponents(filteredGraph))
                    dic = d.descriptors(g)
                    print(connectedComponents(filteredGraph))
                    for key, value in dic.items():
                        print(key, value)
    else:
        if sys.argv[1] == "-g":
            g, is_2D = generateGraphGraphe(sys.argv[2])  # utilizing the test file found in 2D-testFiles folder
            visualize(g, is_2D)
            filteredGraph = filterGraph(g)
            visualize(filteredGraph, is_2D)
            if DEBUG:
                print(connectedComponents(filteredGraph))
                dic = d.descriptors(g)
                print(connectedComponents(filteredGraph))
                for key, value in dic.items():
                    print(key, value)


        elif sys.argv[1] != "-g":
            (g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue,
             dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue,
             CT_n_D_adj_An, CT_n_A_adj_Ca) = generateGraphAdj(sys.argv[1])  # utilizing the test file found in 2D-testFiles folder
            visualize(g, is_2D)
            filteredGraph = filterGraph(g)
            visualize(filteredGraph, is_2D)

            if DEBUG:
                dic = d.descriptors(g)
                print(connectedComponents(filteredGraph))
                for key, value in dic.items():
                    print(key, value)
            if DEBUG:
                dic = d.descriptors(g)
                print(connectedComponents(filteredGraph))
                for key, value in dic.items():
                    print(key, value)



if __name__ == '__main__':
    main()
