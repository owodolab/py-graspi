import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
DEBUG = False
'''---------Function to create edges for graph in specified format --------'''


def graphe_adjList(filename):
    """
    Creates an adjacency list from a given file.

    Args:
        filename (str): The name of the file containing the graph data.

    Returns:
        list: The adjacency list representing the graph.
    """
    adjacency_list = []
    first_order_neighbors = []
    #Opens File
    with open(filename, "r") as file:
        header = file.readline().split()
        vertex_count = int(header[0])
        #loops through all vertices except red and blue meta vertices at the end
        for i in range(vertex_count):
            header = file.readline().split()
            neighbors = []
            #adds all vertex neighbors to current "header" vertex being checked
            #makes sure no edge duplicates exist with prior vertices already checked
            for j in range(2,len(header),3):
                order_neighbor_type = header[j + 2]
                if int(header[j]) < len(adjacency_list):
                    if i not in adjacency_list[int(header[j])]:
                        neighbors.append(int(header[j]))
                else:
                    neighbors.append(int(header[j]))
                #if edge is a first order edge, adds this pairing to a list
                if order_neighbor_type == 'f':
                    first_order_neighbors.append([int(header[j]), i])
            adjacency_list.append(neighbors)

    adjacency_list.append([])
    adjacency_list.append([])
    return adjacency_list, first_order_neighbors


def adjList(fileName):
    adjacency_list = {}
    first_order_pairs = []
    second_order_pairs = []
    third_order_pairs = []
    is_2d = True
    with open(fileName, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY = int(header[0]), int(header[1])
        if len(header) < 3:
            dimZ = 1
        else:
            if int(header[2]) == 0:
                dimZ = 1
            else:
                dimZ = int(header[2])

        if dimZ == 0 or dimZ == 1:
            dimZ = 1
        else:
            dimZ = dimX * dimY
            is_2d = False
        offsets = [(-1, -1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1), (-1,-1,-1), (-1,0,-1), (0,-1,-1), (1,-1,-1)]

        for z in range(dimZ):
            for y in range(dimY):
                for x in range(dimX):
                    current_vertex = z * dimY * dimX + y * dimX + x
                    neighbors = []
                    for dx, dy, dz in offsets:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < dimX and 0 <= ny < dimY and 0 <= nz < dimZ:
                            neighbor_vertex = nz * dimY * dimX + ny * dimX + nx
                            if (dx, dy, dz) == offsets[1] or (dx, dy, dz) == offsets[2] or (dx, dy, dz) == offsets[3]:
                                first_order_pairs.append([current_vertex, neighbor_vertex])
                            elif (dx, dy, dz) == offsets[4] or (dx, dy, dz) == offsets[5] or (dx, dy, dz) == offsets[6] or (dx, dy, dz) == offsets[7]:
                                third_order_pairs.append([current_vertex, neighbor_vertex])
                            else:
                                second_order_pairs.append([current_vertex, neighbor_vertex])
                            neighbors.append(neighbor_vertex)
                    adjacency_list[current_vertex] = neighbors

    adjacency_list[dimZ * dimY * dimX] = list(range(dimX))
    adjacency_list[dimZ * dimY * dimX + 1] = [i + dimX * (dimY - 1) for i in range(dimX)]
    if DEBUG:
        # print("Adjacency List: ", adjacency_list)
        print("Adjacency List LENGTH: ", len(adjacency_list))
        # print("First Order Pairs: ", first_order_pairs)
        print("First Order Pairs LENGTH: ", len(first_order_pairs))
        # print("Second Order Pairs: ", second_order_pairs)
        print("Second Order Pairs LENGTH: ", len(second_order_pairs))
        # print("Third Order Pairs: ", third_order_pairs)
        print("Third Order Pairs LENGTH: ", len(third_order_pairs))
        #exit()
    return adjacency_list, first_order_pairs, is_2d

'''------- Labeling the color of the vertices -------'''

def adjvertexColors(fileName):
    """
    Labels the colors of vertices based on a given file.

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


def vertexColors(fileName):
    """
    Labels the colors of vertices based on a given file.

    Args:
        fileName (str): The name of the file containing the vertex color data.

    Returns:
        list: A list of vertex colors.
    """
    labels = []
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            for char in line:
                if char == '1':
                    labels.append('white')
                elif char == '0':
                    labels.append('black')

    return labels

'''Adding Labels'''
def edgeLabels(g, first_order_pairs):
    order_pair_label = []

    edges = g.es
    for edge in edges:
        if [edge.source, edge.target] in first_order_pairs or [edge.target, edge.source] in first_order_pairs:
            order_pair_label.append('f')
        else:
            order_pair_label.append('s')
    return order_pair_label

'''********* Constructing the Graph **********'''


def generateGraphGraphe(file):

    """
    Constructs a graph from an adjacency list and assigns vertex colors.

    Args:
        file (str): The name of the file containing graph data.

    Returns:
        ig.Graph: The constructed graph with assigned vertex colors.
    """
    #gets an adjacency list and first order pairs list from the file input
    adjacency_list, first_order_neighbors = graphe_adjList(file)
    vertex_colors = adjvertexColors(file)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    #creates graph using Igraph API
    g = ig.Graph(edges, directed=False)
    #adds color label to each vertex
    g.vs["color"] = vertex_colors

    #adds green vertex and its color
    g.add_vertices(1)
    g.vs[len(adjacency_list)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]

    exists = [0] * (g.vcount()-3)
    #For loop makes sure all black and white pairings are labeled black as first and white as second in pairing
    for pair in first_order_neighbors:
        if g.vs[pair[0]]['color'] == 'white' and g.vs[pair[1]]['color'] == 'black':
            temp = pair[0]
            pair[0] = pair[1]
            pair[1] = temp

    # test = []
    #Loops through all pairings, adds edge between black and white pairings {black-green/white-green}, no multiple edges to same vertex if edge has already been added
    for pair in first_order_neighbors:
        source_vertex = pair[0]
        target_vertex = pair[1]

        if g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white':
            #connect both source and target to green meta vertex
            if exists[pair[0]] == 0:
                g.add_edge(green_vertex, source_vertex)
                exists[pair[0]] += 1
                # test.append(pair[0])

            if exists[pair[1]] == 0:
                g.add_edge(green_vertex, target_vertex)
                exists[pair[1]] += 1
                # test.append(pair[1])

    # print(test)
    return g


def generateGraphAdj(file):
    """
    Generates Graph using an adjacency list.

    Args:
        file (str): The name of the file containing graph data.

    Returns:
        Generated graph using an adjacency list.
    """
    edges, first_order_pairs, is_2D = adjList(file)
    labels = vertexColors(file)
    f = open(file, 'r')
    line = f.readline()
    line = line.split()
    dimX = line[0]
    dimY = line[1]
    g = ig.Graph.ListDict(edges=edges, directed=False)
    g.vs["color"] = labels
    g.es['label'] = edgeLabels(g, first_order_pairs)

    # add wrap around edges.
    # for i in range(0, g.vcount() - 2, int(dimX)):
    #     #first add first neighbor wrap around
    #     g.add_edge(g.vs[i], g.vs[i + (int(dimX) - 1)])
    #     edge_index_f = g.get_eid(g.vs[i], g.vs[i + (int(dimX) - 1)])
    #     g.es[edge_index_f]['label'] = 'f'
    
    #     #only add one wrap around since other wouldn't exist in this case
    #     if i == 0:
    #         g.add_edge(g.vs[i], g.vs[int(dimX)-1 + int(dimX)])
    #         edge_index_s = g.get_eid(g.vs[i], g.vs[int(dimX)-1 + int(dimX)])
    #         g.es[edge_index_s]['label'] = 's'
    
    #     elif i + int(dimX) >= g.vcount()-2:
    #         g.add_edge(g.vs[i], g.vs[i -1])
    
    #     #add diagnol wrap arounds
    #     else:
    #         g.add_edge(g.vs[i], g.vs[i+ int(dimX) - 1 + int(dimX)])
    #         edge_index1 = g.get_eid(g.vs[i], g.vs[i+ int(dimX) - 1 + int(dimX)])
    #         g.es[edge_index1]['label'] = 's'
    #         g.add_edge(g.vs[i], g.vs[i - 1])
    #         edge_index2 = g.get_eid(g.vs[i], g.vs[i - 1])
    #         g.es[edge_index2]['label'] = 's'

    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    g.vs[int(line[0]) * int(line[1]) + 1]['color'] = 'red'

    g.add_vertices(1)
    g.vs[int(line[0]) * int(line[1]) + 2]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]

    if DEBUG:
        black_green_neighbors = []

 
    for edge in g.es:
        source_vertex = edge.source
        target_vertex = edge.target
        if edge['label'] == 'f':
            if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white') or (
                    g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):

                g.add_edge(green_vertex, source_vertex)
                if DEBUG:
                    if g.vs[source_vertex]['color'] == 'black':
                        black_green_neighbors.append(source_vertex)

                if DEBUG:
                    if g.vs[target_vertex]['color'] == 'black':
                        black_green_neighbors.append(target_vertex)
                g.add_edge(green_vertex, target_vertex)

    if DEBUG:
        # print(g.vs['color'])
        print("Number of nodes: ", g.vcount())
        # print("Green vertex neighbors: ", g.neighbors(green_vertex))
        print("Green vertex neighbors LENGTH: ", len(g.neighbors(green_vertex)))
        # print("Black/Green Neighbors: ", black_green_neighbors)
        print("Black/Green Neighbors LENGTH: ", len(black_green_neighbors))
        # print("Nodes connected to blue: ", g.vs[g.vcount()-3]['color'], g.neighbors(g.vcount()-3))
        print("Length: ", len(g.neighbors(g.vcount()-3)))
        # print("Nodes connected to red: ", g.vs[g.vcount()-2]['color'],g.neighbors(g.vcount()-2))
        print("Length: ", len(g.neighbors(g.vcount()-2)))
        # exit()
    return g, is_2D

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

def visual2D(g, type):
    """
    Visualizes the graph in 2D.

    Args:
        g (ig.Graph): The input graph to visualize.
        type (str): The layout type ('graph' or 'grid').

    Returns:
        None
    """
    if type == 'graph':
        layout = g.layout('fr')
    else:
        layout = g.layout('grid')
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


def visual3D(g):
    """
    Visualizes the graph in 3D.

    Args:
        g (ig.Graph): The input graph to visualize.

    Returns:
        None
    """
    edges = g.get_edgelist()
    num_vertices = len(g.vs)
    grid_size = int(np.round(num_vertices ** (1 / 3)))

    # Generate 3D coordinates (layout) for the vertices
    x, y, z = np.meshgrid(range(grid_size), range(grid_size), range(grid_size))
    coords = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

    # Plot the graph in 3D using matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot vertices
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=g.vs['color'], s=100)

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
    redVertex = None;
    blueVertex = None;
    blackCCList = []
    whiteCCList = []
    # print(len(cc))

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


'''********* Shortest Path **********'''


def shortest_path(graph, vertices, toVertex, fileName):
    """
    Finds the shortest paths from vertices to a target vertex and writes them to a file.

    Args:
        graph (ig.Graph): The input graph.
        vertices (str): The source vertex color.
        toVertex (str): The target vertex color.
        fileName (str): The name of the output file.

    Returns:
        dict: A dictionary of shortest paths.
    """
    numVertices = graph.vcount()
    ccp = graph.connected_components()
    listOfShortestPaths = {}
    vertex = numVertices;

    if toVertex == 'blue':
        vertex = numVertices - 2
    elif toVertex == 'red':
        vertex = numVertices - 1

    f = open(fileName, "x")

    with open(fileName, 'a') as f:
        for c in ccp:
            if graph.vs[c][0]['color'] == vertices or graph.vs[c][0]['color'] == toVertex:
                for x in c:
                    if graph.vs[x]['color'] == vertices or graph.vs[x]['color'] == toVertex:
                        listOfShortestPaths[x] = graph.get_shortest_paths(x, vertex, output="vpath")[0]
                        f.write(str(x) + ": " + str(
                            len(graph.get_shortest_paths(x, vertex, output="vpath")[0]) - 1) + '\n');

    return listOfShortestPaths
