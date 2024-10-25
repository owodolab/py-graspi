import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

'''---------Function to create adjacency list for graph in specified format --------'''
def adjList(fileName):
    adjacency_list = {}
    dimX = dimY = 0

    with open(fileName, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY = int(header[0]), int(header[1])

        offsets = [(-1, -1), (-1, 0), (0, -1), (1, -1)]


        for y in range(dimY):
            for x in range(dimX):
                current_vertex = y * dimX + x
                neighbors = []

                for dx, dy in offsets:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < dimX and 0 <= ny < dimY:
                        neighbor_vertex = ny * dimX + nx
                        neighbors.append(neighbor_vertex)

                adjacency_list[current_vertex] = neighbors

    adjacency_list[dimY * dimX] = list(range(dimX))
    adjacency_list[dimY * dimX + 1] = [i + dimX * (dimY - 1) for i in range(dimX)]

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
def generateGraph(file):
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
def visual2D(g):
    layout = g.layout('reingold_tilford')
    fig, ax = plt.subplots()
    # ax.invert_yaxis() # reverse starting point of graph (vertex 0)

    ig.plot(g, target=ax, layout=layout,vertex_size=25,margin=5)

    ''' ---- generate the labels of each vertex value ---- '''
    for i, (x, y) in enumerate(layout):
        g.vs['label']=[i for i in range(len(g.vs))]
        ax.text(
            x, y - 0.2,
            g.vs['label'][i],
            fontsize=12,
            color='black',
            ha='right',  # Horizontal alignment
            va='top'  # Vertical alignment
        )

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
        # elif(graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue'):
        #     keptEdges.append(edge)
        # elif(graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red'):
        #     keptEdges.append(edge)
   
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
