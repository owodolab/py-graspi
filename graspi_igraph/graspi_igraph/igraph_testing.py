import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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
def adjVertexColors(fileName):
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
def generateGraph(file):
    adjacency_list = graphe_adjList(file)
    vertex_colors = vertexColors(file)

    edges = [(i, neighbor) for i, neighbors in enumerate(adjacency_list) for neighbor in neighbors]
    
    g = ig.Graph(edges, directed=False)
    g.vs["color"] = vertex_colors
    g.add_vertices(1)

    g.vs[len(adjacency_list)]['color'] = 'green'
    green_vertex = g.vs[g.vcount() - 1]
    exists = []

    for i in range(g.ecount()):
        current_edge = g.es[i]
        source_vertex = current_edge.source
        target_vertex = current_edge.target
        if (g.vs[source_vertex]['color'] == 'black' and g.vs[target_vertex]['color'] == 'white'):
            '''connect both source and target to green meta vertex'''
            if exists.count([green_vertex, source_vertex]) == 0:
                g.add_edge(green_vertex, source_vertex)
            if exists.count([green_vertex, target_vertex]) == 0:
                g.add_edge(green_vertex, target_vertex)
            exists.append([green_vertex, source_vertex])
            exists.append([green_vertex, target_vertex])
        if(g.vs[source_vertex]['color'] == 'white' and g.vs[target_vertex]['color'] == 'black'):
            '''connect both source and target to green meta vertex'''
            if exists.count([green_vertex, source_vertex]) == 0:
                g.add_edge(green_vertex, source_vertex)
            if exists.count([green_vertex, target_vertex]) == 0:
                g.add_edge(green_vertex, target_vertex)
            exists.append([green_vertex, source_vertex])
            exists.append([green_vertex, target_vertex])

    return g

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

    return g

def visual2D(g,type):
    if type == 'graph' :
        layout = g.layout('fr')  
    else:
        layout = g.layout('grid')  
    # fig, ax = plt.subplots()
    # ax.invert_yaxis() # reverse starting point of graph (vertex 0)
    fig,ax = plt.subplots(figsize=(10, 10))

    ig.plot(g, target=ax, layout=layout,vertex_size=15,margin=5)

    ''' ---- generate the labels of each vertex value ---- '''
    for i, (x, y) in enumerate(layout):
        g.vs['label']=[i for i in range(len(g.vs))]
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
    grid_size = int(np.round(num_vertices ** (1/3)))  

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
        if(graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)
   
    filteredGraph = graph.subgraph_edges(keptEdges,delete_vertices = True)

    return filteredGraph

'''**************** Connected Components *******************'''
def connectedComponents(graph):
    vertices = graph.vcount()
    edgeList = set(graph.get_edgelist())
    fg = filterGraph(graph)
    cc = fg.connected_components()
    redVertex = None;
    blueVertex = None;
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

    blackCCList = [c for c in cc if fg.vs[c[0]]['color'] == 'black']
    whiteCCList = [c for c in cc if fg.vs[c[0]]['color'] == 'white']

    for c in blackCCList:
        passedRed = False
        passedBlue = False
        for vertex in c:
            if not passedRed:
                if (vertex,redVertex) in edgeList or (redVertex,vertex) in edgeList:
                    c.append(redVertex)
                    passedRed = True
            if not passedBlue:
                if (vertex,blueVertex) in edgeList or (blueVertex,vertex) in edgeList:
                    c.append(blueVertex)
                    passedBlue = True
            if passedBlue and passedRed:
                break

    for c in whiteCCList:
        passedRed = False
        passedBlue = False
        for vertex in c:
            if not passedRed:
                if (vertex,redVertex) in edgeList or (redVertex,vertex) in edgeList:
                    c.append(redVertex)
                    passedRed = True
            if not passedBlue:
                if (vertex,blueVertex) in edgeList or (blueVertex,vertex) in edgeList:
                    c.append(blueVertex)
                    passedBlue = True
            if passedBlue and passedRed:
                break

    connected_comp = whiteCCList + blackCCList

    return connected_comp

'''********* Shortest Path **********'''
def shortest_path(graph,vertices,toVertex,fileName):
    numVertices = graph.vcount()
    ccp = graph.connected_components()
    listOfShortestPaths = {}
    vertex = numVertices;
    
    if toVertex == 'blue' :
        vertex = numVertices-2
    elif toVertex == 'red':
        vertex = numVertices-1

    f = open(fileName,"x")

    with open(fileName,'a') as f:
        for c in ccp:
            if graph.vs[c][0]['color'] == vertices or graph.vs[c][0]['color'] == toVertex:
                for x in c:
                    if graph.vs[x]['color'] == vertices or graph.vs[x]['color'] == toVertex:
                        listOfShortestPaths[x] = graph.get_shortest_paths(x,vertex,output="vpath")[0]
                        f.write(str(x) + ": " + str(len(graph.get_shortest_paths(x,vertex,output="vpath")[0]) - 1) + '\n');

    return listOfShortestPaths


