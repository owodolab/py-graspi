import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
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
    # edge_test = g.es[4]
    # print(g.ecount())
    # source_vertex = edge_test.source
    # target_vertex = edge_test.target
    # print(g.vs[source_vertex]["color"], g.vs[target_vertex]["color"])
    print(g.ecount())
    exists = []
    for i in range(g.ecount()):
        current_edge = g.es[i]
        source_vertex = current_edge.source
        target_vertex = current_edge.target
        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white') or (
                g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):
            '''connect both source and target to green meta vertex'''
            if exists.count([green_vertex, source_vertex]) == 0:
                g.add_edge(green_vertex, source_vertex)
            if exists.count([green_vertex, target_vertex]) == 0:
                g.add_edge(green_vertex, target_vertex)
            exists.append([green_vertex, source_vertex])
            exists.append([green_vertex, target_vertex])
    print(g.ecount())
    return g


'''---------Function to create edges for graph in specified format --------'''

def graphe_adjList(filename):
    adjacency_list = []
    first_order_neighbors = []
    with open(filename, "r") as file:
        header = file.readline().split()
        vertex_count = int(header[0])
        for i in range(vertex_count):
            header = file.readline().split()
            neighbors = []
            for j in range(2,len(header),3):
                order_neighbor = header[j + 2]
                if int(header[j]) < len(adjacency_list):
                    if i not in adjacency_list[int(header[j])]:
                        neighbors.append(int(header[j]))
                        if order_neighbor == 'f':
                            first_order_neighbors.append([int(header[j]), i])

                else:
                    neighbors.append(int(header[j]))
                    if order_neighbor == 'f':
                        first_order_neighbors.append([int(header[j]), i])
            adjacency_list.append(neighbors)

    adjacency_list.append([])
    adjacency_list.append([])
    # print(first_order_neighbors)
    # exit()
    return adjacency_list, first_order_neighbors

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
    adj_firstOrders = graphe_adjList(file)
    adjacency_list = adj_firstOrders[0]
    first_order_neighbors = adj_firstOrders[1]
    vertex_colors = graphe_vertexColors(file)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    
    g = ig.Graph(edges, directed=False)
    g.vs["color"] = vertex_colors
    g.add_vertices(1)
    # print(len(adjacency_list))

    # exit()
    g.vs[len(adjacency_list)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]
    exists = []
    for i in range(len(first_order_neighbors)):
        current_edge = first_order_neighbors[i]
        source_vertex = first_order_neighbors[i][0]
        target_vertex = first_order_neighbors[i][1]
        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white') or (g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):
            '''connect both source and target to green meta vertex'''
            if exists.count([green_vertex, source_vertex]) ==0:
                g.add_edge(green_vertex, source_vertex)
            if exists.count([green_vertex, target_vertex]) == 0:
                g.add_edge(green_vertex, target_vertex)
            exists.append([green_vertex, source_vertex])
            exists.append([green_vertex, target_vertex])
    print(g.get_edgelist())
    # for i in range(g.ecount()):
    #     current_edge = g.es[i]
    #     source_vertex = current_edge.source
    #     target_vertex = current_edge.target
    #     if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white') or (g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):
    #         '''connect both source and target to green meta vertex'''
    #         if exists.count([green_vertex, source_vertex]) ==0:
    #             g.add_edge(green_vertex, source_vertex)
    #         if exists.count([green_vertex, target_vertex]) == 0:
    #             g.add_edge(green_vertex, target_vertex)
    #         exists.append([green_vertex, source_vertex])
    #         exists.append([green_vertex, target_vertex])
    # print(g.get_edgelist())
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




