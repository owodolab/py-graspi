from calendar import firstweekday
from logging import DEBUG
from os.path import exists

import igraph as ig
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys


DEBUG = True
from fontTools.merge.util import first

'''Returns an adjacency list of a .txt file in the form of a dict.'''
def adjList(fileName):
    adjacency_list = {}
    first_order_pairs = []
    second_order_pairs = []
    is_2d = True
    with open(fileName, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY, dimZ = int(header[0]), int(header[1]), int(header[2])
        if dimZ == 0 or dimZ == 1:
            dimz = 1
        else:
            dimZ = dimX * dimY
            is_2d = False
        offsets = [(-1, -1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, -1, 0)]
        for z in range(dimZ):
            for x in range(dimX):
                for y in range(dimY):
                    current_vertex = x * dimY * dimZ + y * dimZ + z
                    neighbors = []
                    for dx, dy, dz in offsets:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < dimX and 0 <= ny < dimY and 0 <= nz < dimZ:

                            neighbor_vertex = nx * dimY * dimZ + ny * dimZ + nz
                            if (dx, dy, dz) == offsets[1] or (dx, dy, dz) == offsets[2] or (dx, dy, dz) == offsets[3]:
                                first_order_pairs.append([current_vertex, neighbor_vertex])

                            neighbors.append(neighbor_vertex)

                    adjacency_list[current_vertex] = neighbors

                # print(neighbors)
                # exit()
    adjacency_list[dimZ * dimY * dimX] = list(range(dimX))
    adjacency_list[dimZ * dimY * dimX + 1] = [i + dimX * (dimY - 1) for i in range(dimX)]
    if DEBUG:
        print("Adjacency List: ", adjacency_list)
        print("Adjacency List LENGTH: ", len(adjacency_list))
        print("First Order Pairs: ", first_order_pairs)
        print("First Order Pairs LENGTH: ", len(first_order_pairs))
        #exit()
    return adjacency_list, first_order_pairs, is_2d
'''------- Labeling the color of the vertices -------'''
def vertexColors(fileName):
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
'''********* Constructing the Graph **********'''
def generateGraphAdj(file):
    edges, first_order_pairs, is_2D = adjList(file)
    labels = vertexColors(file)
    f = open(file, 'r')
    line = f.readline()
    line = line.split()
    g = ig.Graph.ListDict(edges=edges, directed=False)
    g.vs["color"] = labels
    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    g.vs[int(line[0]) * int(line[1]) + 1]['color'] = 'red'

    g.add_vertices(1)
    g.vs[int(line[0]) * int(line[1]) + 2]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]
    exists = []
    edge_list = g.get_edgelist()
    for edge in edge_list:
        if edge in first_order_pairs:
            g.es[edge[0]][edge[1]]['label'] = 'f'

    for pair in first_order_pairs:
        source_vertex = pair[0]
        target_vertex = pair[1]
        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white') or (
                g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):
            if [source_vertex, target_vertex] in first_order_pairs or [target_vertex, source_vertex] in first_order_pairs:
                if source_vertex not in exists:
                    g.add_edge(green_vertex, source_vertex)
                    exists.append(source_vertex)
                if target_vertex not in exists:
                    g.add_edge(green_vertex, target_vertex)
                    exists.append(target_vertex)
    if DEBUG:
        print("Number of nodes: ", g.vcount())
        print("Green vertex neighbors: ", g.neighbors(green_vertex))
        print("Green vertex neighbors LENGTH: " ,len(g.neighbors(green_vertex)))
        exit()
    return g, is_2D


'''---------Function to create edges for graph in specified format --------'''

'''Takes in filename and reads given .graphe file.
    Creates an adjacency list of each vertex with no duplicates (this makes it so graph does not have cycles).
    Also creates a "first_order_neighbors" list, this list returns the pairing of first order neighbors which is used
    later when checking for nodes to connect to the green interface node. (only first order neighbors are allowed to connect to the green interface) '''
'''RETURNS: [Adjacency list, first_order_neighbors list]'''

def graphe_adjList(filename):
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

'''------- Labeling the color of the vertices-------'''
def graphe_vertexColors(fileName):
    labels = []
    with open(fileName, 'r') as file:
        line = file.readline().split()
        vertex_count = int(line[0])
        for i in range(vertex_count+2):
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

'''********* Constructing the Graph for .graphe files **********'''

'''Creates graph and adds green interface node to black and white First Order vertices that share an edge.
    RETURNS: graph created'''
def graphe_generateGraphAdj(file):
    #gets an adjacency list and first order pairs list from the file input
    adjacency_list, first_order_neighbors = graphe_adjList(file)
    vertex_colors = graphe_vertexColors(file)

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

def visual2D(g):
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
    edgeList = graph.get_edgelist()
    keptEdges = []

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if graph.vs[currentNode]['color'] == graph.vs[toNode]['color']:
            keptEdges.append(edge)
        elif graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue':
            keptEdges.append(edge)
        elif graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red':
            keptEdges.append(edge)
        elif graph.vs[currentNode]['color'] == 'green' or graph.vs[toNode]['color'] == 'green':
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=False)

    return filteredGraph


'''********* Shortest Path **********'''

def shortest_path(graph):
    numVertices = graph.vcount()
    ccp = graph.connected_components()
    listOfShortestPaths = {}
    greenVertex = numVertices - 1

    for c in ccp:
        if graph.vs[c]['color'] == 'black':
            for x in c:
                if graph.vs[x]['color'] == 'black' or graph.vs[x]['color'] == 'green':
                    listOfShortestPaths[x] = graph.get_shortest_paths(greenVertex, x, output="vpath")[0]

    return listOfShortestPaths

'''Returns file is a 2D or 3D file (needed for visualization)'''
def check_if_correct_input(file_type):
    is_2D_index = 3

    if file_type != "g":
        is_2D_index = 2

    is_2D = True
    correct_input = False
    if sys.argv[is_2D_index] == '2d':
        is_2D = True
        correct_input = True
    elif sys.argv[is_2D_index] == '3d':
        is_2D = False
        correct_input = True

    if not correct_input:
        print("Did not specify if 2d or 3d please try again")
        return 1
    return is_2D

''''runs functions for visualizing, filtering, and finding shortest_paths for 2D inputs'''
def for_2D_graphs(graph):
    visual2D(graph)
    filteredGraph = filterGraph(graph)
    visual2D(filteredGraph)
    shortest_path(filteredGraph)

''''runs functions for visualizing, filtering, and finding shortest_paths for 3D inputs'''

def for_3D_graphs(graph):
    visual3D(graph)
    filteredGraph = filterGraph(graph)
    visual3D(filteredGraph)
    shortest_path(filteredGraph)

def main():
    # print(sys.argv[2])
    # exit()
    if sys.argv[1] == "g":
        # is_2D = check_if_correct_input('g')
        g, is_2D = graphe_generateGraphAdj(sys.argv[2])  # utilizing the test file found in 2D-testFiles folder
        if is_2D:
            for_2D_graphs(g)
        else:
            for_3D_graphs(g)
    elif sys.argv[1] != "g":
        #is_2D = check_if_correct_input(1)
        g, is_2D = generateGraphAdj(sys.argv[1])  # utilizing the test file found in 2D-testFiles folder
        if is_2D:
            for_2D_graphs(g)
        else:
            for_3D_graphs(g)

if __name__ == '__main__':
    main()




