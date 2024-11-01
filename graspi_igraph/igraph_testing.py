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
                # if edge is a first order edge, adds this pairing to a list
                if order_neighbor_type == 'f':
                    first_order_neighbors.append([int(header[j]), i])
                elif order_neighbor_type == 's':
                    second_order_neighbors.append([int(header[j]), i])
                elif order_neighbor_type == 't':
                    third_order_neighbors.append([int(header[j]), i])
            adjacency_list.append(neighbors)

    adjacency_list.append([])
    adjacency_list.append([])
    is_2D = False
    if len(third_order_neighbors) <= 0:
        is_2D = True
    return adjacency_list, first_order_neighbors, second_order_neighbors, third_order_neighbors, is_2D
    
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

def edgeLabels(g, first_order_pairs, second_order_pairs, third_order_pairs):
    """
        Creates a edge label list from a given graph.

        Args:
            graph (igraph): The name of the graph containing graph data such as edges and vertices.
            first_order_pairs (list): A list of tuples containing the first order pairings.
            second_order_pairs (list): A list of tuples containing the second order pairings.
            third_order_pairs (list): A list of tuples containing the third order pairings.

        Returns:
            order_pair_label (list): returns a list containing the correct label ordering for the edges in the graph.
        """
    order_pair_label = []

    edges = g.es
    for edge in edges:
        if [edge.source, edge.target] in first_order_pairs or [edge.target, edge.source] in first_order_pairs:
            order_pair_label.append('f')
        elif [edge.source, edge.target] in first_order_pairs or [edge.target, edge.source] in second_order_pairs:
            order_pair_label.append('s')
        elif [edge.source, edge.target] in first_order_pairs or [edge.target, edge.source] in third_order_pairs:
            order_pair_label.append('t')
    return order_pair_label


'''********* Constructing the Graph **********'''


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
    vertex_colors = graphe_vertexColors(file)

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

    exists = [0] * (g.vcount() - 3)
    # For loop makes sure all black and white pairings are labeled black as first and white as second in pairing
    for pair in first_order_neighbors:
        if g.vs[pair[0]]['color'] == 'white' and g.vs[pair[1]]['color'] == 'black':
            temp = pair[0]
            pair[0] = pair[1]
            pair[1] = temp


    # Loops through all pairings, adds edge between black and white pairings {black-green/white-green}, no multiple edges to same vertex if edge has already been added
    for pair in first_order_neighbors:
        source_vertex = pair[0]
        target_vertex = pair[1]

        if g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white':
            # connect both source and target to green meta vertex
            if exists[pair[0]] == 0:
                g.add_edge(green_vertex, source_vertex)
                exists[pair[0]] += 1
            if exists[pair[1]] == 0:
                g.add_edge(green_vertex, target_vertex)
                exists[pair[1]] += 1


    # print(test)
    return g, is_2d


def generateGraphAdj(file):
    """
        Creates an adjacency list from a given file.

        Args:
            filename (str): The name of the file containing the graph data.

        Returns:
            graph: the graph that holds all the edges and vertices based on file input
            boolean: returns  a boolean to signal if graph is 2D or not
        """
    edges, first_order_pairs, second_order_pairs, third_order_pairs, blue_neighbors, red_neighbors, is_2D = adjList(file)
    labels = vertexColors(file)
    f = open(file, 'r')
    line = f.readline()
    line = line.split()
    dimX = line[0]
    dimY = line[1]
    g = ig.Graph.ListDict(edges=edges, directed=False)
    g.vs["color"] = labels
    g.es['label'] = edgeLabels(g, first_order_pairs, second_order_pairs, third_order_pairs)

    # add wrap around edges if periodicity boolean is set to True.
    if PERIODICITY:
        for i in range(0, g.vcount() - 2, int(dimX)):
            # first add first neighbor wrap around
            g.add_edge(g.vs[i], g.vs[i + (int(dimX) - 1)])
            edge_index_f = g.get_eid(g.vs[i], g.vs[i + (int(dimX) - 1)])
            g.es[edge_index_f]['label'] = 'f'

            # only add one wrap around since other wouldn't exist in this case
            if i == 0:
                g.add_edge(g.vs[i], g.vs[int(dimX) - 1 + int(dimX)])
                edge_index_s = g.get_eid(g.vs[i], g.vs[int(dimX) - 1 + int(dimX)])
                g.es[edge_index_s]['label'] = 's'

            elif i + int(dimX) >= g.vcount() - 2:
                g.add_edge(g.vs[i], g.vs[i - 1])

            # add diagnol wrap arounds
            else:
                g.add_edge(g.vs[i], g.vs[i + int(dimX) - 1 + int(dimX)])
                edge_index1 = g.get_eid(g.vs[i], g.vs[i + int(dimX) - 1 + int(dimX)])
                g.es[edge_index1]['label'] = 's'
                g.add_edge(g.vs[i], g.vs[i - 1])
                edge_index2 = g.get_eid(g.vs[i], g.vs[i - 1])
                g.es[edge_index2]['label'] = 's'

    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    blue_vertex =  g.vs[int(line[0]) * int(line[1])]
    g.vs[int(line[0]) * int(line[1]) + 1]['color'] = 'red'
    red_vertex = g.vs[int(line[0]) * int(line[1]) + 1]
    for i in blue_neighbors:
        g.add_edge(blue_vertex, g.vs[i])
    for i in red_neighbors:
        g.add_edge(red_vertex, g.vs[i])

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
        print(g.vs['color'])
        print("Number of nodes: ", g.vcount())
        print("Green vertex neighbors: ", g.neighbors(green_vertex))
        print("Green vertex neighbors LENGTH: ", len(g.neighbors(green_vertex)))
        print("Black/Green Neighbors: ", black_green_neighbors)
        print("Black/Green Neighbors LENGTH: ", len(black_green_neighbors))
        print("Nodes connected to blue: ", g.vs[g.vcount()-3]['color'], g.neighbors(g.vcount()-3))
        print("Length: ", len(g.neighbors(g.vcount()-3)))
        print("Nodes connected to red: ", g.vs[g.vcount()-2]['color'],g.neighbors(g.vcount()-2))
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

def visualize(graph,is_2D):
    """
       Creates a visualization from the given graph

       Args:
           graph (ig.Graph): The graph to visualize
           is_2D (bool): A boolean to signal if the graph is 2D or not

       Returns:
           NONE: but outputs visualization of graph.
       """
    g= graph
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
        grid_size = int(np.round(num_vertices ** (1 / 3)))

        # Generate 3D coordinates (layout) for the vertices
        x, y, z = np.meshgrid(range(grid_size), range(grid_size), range(grid_size))
        coords = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

        # Plot the graph in 3D using matplotlib
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        color = []
        for vertex in range(g.vcount()):
            color.append(str(g.vs[vertex]['color']))
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
