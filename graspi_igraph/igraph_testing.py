import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys


'''---------Function to create edges for graph in specified format --------'''
def graphe_adjList(filename):
    adjacency_list = []
    with open(filename, "r") as file:
        header = file.readline().split()
        vertex_count = int(header[0])
        for i in range(vertex_count):
            header = file.readline().split()
            neighbors = []
            for j in range(2,len(header),3):
                if int(header[j]) < len(adjacency_list):
                    if i not in adjacency_list[int(header[j])]:
                        neighbors.append(int(header[j]))
                else:
                    neighbors.append(int(header[j]))
            adjacency_list.append(neighbors)

    adjacency_list.append([])
    adjacency_list.append([])
    
    return adjacency_list

'''------- Labeling the color of the vertices -------'''
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

'''********* Constructing the Graph **********'''

def graphe_generateGraphAdj(file):
    adjacency_list = graphe_adjList(file)
    vertex_colors = graphe_vertexColors(file)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    
    g = ig.Graph(edges, directed=False)
    g.vs["color"] = vertex_colors

    return g

def visual2D(g):
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
        if (graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)
        elif (graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue'):
            keptEdges.append(edge)
        elif (graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red'):
            keptEdges.append(edge)
        elif(graph.vs[currentNode]['color'] == 'green' or graph.vs[toNode]['color'] == 'green'):
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

"""
def main():
    is_2D = True
    correct_input = False
    if sys.argv[2] == '2d':
        is_2D = True
        correct_input = True
    elif sys.argv[2] == '3d':
        is_2D = False
        correct_input = True

    if correct_input == False:
        print("Did not specify if 2d or 3d please try again")
        return 1

    g = generateGraphAdj(sys.argv[1])  # utilizing the test file found in 2D-testFiles folder
    if is_2D:
        visual2D(g)
        filteredGraph = filterGraph(g)
        visual2D(filteredGraph)
        shortest_path(filteredGraph)
    else:
        visual3D(g)
        filteredGraph = filterGraph(g)
        visual3D(filteredGraph)
        shortest_path(filteredGraph)
    print("finished?")

def test():
    is_2D = True
    correct_input = False
    if sys.argv[2] == '2d':
        is_2D = True
        correct_input = True
    elif sys.argv[2] == '3d':
        is_2D = False
        correct_input = True

    if correct_input == False:
        print("Did not specify if 2d or 3d please try again")
        return 1

    g = graphe_generateGraphAdj(sys.argv[1])  # utilizing the test file found in 2D-testFiles folder
    if is_2D:
        visual2D(g)
        filteredGraph = filterGraph(g)
        visual2D(filteredGraph)
        shortest_path(filteredGraph)

if __name__ == '__main__':
    # main()
    test()
"""

g = graphe_generateGraphAdj("tests/2D-testFile/data_4_3.graphe")
visual2D(g)


