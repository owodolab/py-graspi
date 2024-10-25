import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys


'''---------Function to create edges for graph in specified format --------'''
def graphe_adjList(filename):
    adjacency_list = {}
    with open(filename, "r") as file:
        header = file.readline().split()
        vertex_count = int(header[0])
        # print(vertex_count)
        for i in range(vertex_count):
            header = file.readline().split()
            vertex_count = header
            # print(vertex_count)
            j = 2
            current_node = header[0]
            neighbors = []
            while j in range(len(header)):
                neighbor_node = header[j]
                # print(current_node)
                neighbors.append(neighbor_node)
                j += 3
            adjacency_list[current_node] = neighbors
        for i in range(2):
            header = file.readline().split()
            vertex_count = header
            # print(vertex_count)
            j = 2
            current_node = header[0]
            neighbors = []
            while j < len(header):
                neighbor_node = header[j]
                # print(current_node)
                neighbors.append(neighbor_node)
                j += 3
            adjacency_list[current_node] = neighbors
    return adjacency_list



def adjList(fileName):
    adjacency_list = {}
    dimX = dimY = dimZ = 0

    with open(fileName, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY, dimZ = int(header[0]), int(header[1]), int(header[2])

        offsets = [(-1, -1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, -1, 0)]

        for z in range(dimZ):
            for y in range(dimY):
                for x in range(dimX):
                    current_vertex = x * dimY * dimZ + y * dimZ + z
                    neighbors = []

                    for dx, dy, dz in offsets:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < dimX and 0 <= ny < dimY and 0 <= nz < dimZ:
                            neighbor_vertex = nx * dimY * dimZ + ny * dimZ + nz
                            neighbors.append(neighbor_vertex)

                    adjacency_list[current_vertex] = neighbors

    adjacency_list[dimZ * dimY * dimX] = list(range(dimX))
    adjacency_list[dimZ * dimY * dimX + 1] = [i + dimX * (dimY - 1) for i in range(dimX)]
    # green_vertex = adjacency_list[dimZ * dimY * dimX + 2]


    return adjacency_list


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

def graphe_vertexColors(fileName):
    labels = []
    with open(fileName, 'r') as file:
        line = file.readline().split()
        vertex_count = int(line[0])
        for i in range(vertex_count):
            line = file.readline().split()
            char = line[1]
            if char == '1':
                labels.append('white')
            elif char == '0':
                labels.append('black')

        # lines = file.readlines()
        # for line in lines[1:]:
        #     for char in line[1]:
        #         if char == '1':
        #             labels.append('white')
        #         elif char == '0':
        #             labels.append('black')


    return labels

'''********* Constructing the Graph **********'''

def generateGraphAdj(file):
    edges = adjList(file)
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
    for i in range(g.ecount()):
        current_edge = g.es[i]
        source_vertex = current_edge.source
        target_vertex = current_edge.target
        if(g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white'):
            '''connect both source and target to green meta vertex'''
            g.add_edge(green_vertex, source_vertex)
            g.add_edge(green_vertex, target_vertex)
    return g

def graphe_generateGraphAdj(file):
    edges = graphe_adjList(file)
    labels = graphe_vertexColors(file)

    f = open(file, 'r')
    line = f.readline()
    line = line.split()

    g = ig.Graph.ListDict(edges=edges, directed=False)
    g.vs["color"] = labels
    print(len(edges))
    g.vs[len(edges) - 2]['color'] = 'blue'
    g.vs[len(edges) - 1]['color'] = 'red'

    g.add_vertices(1)
    g.vs[len(edges)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]
    for i in range(g.ecount()):
        current_edge = g.es[i]
        source_vertex = current_edge.source
        target_vertex = current_edge.target
        if(g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white'):
            '''connect both source and target to green meta vertex'''
            g.add_edge(green_vertex, source_vertex)
            g.add_edge(green_vertex, target_vertex)
    return g
'''Add green interface node'''

def visual2D(g):
    layout = g.layout('reingold_tilford')
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