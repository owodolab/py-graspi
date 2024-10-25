import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

'''---------Function to create edges for graph in specified format --------'''
def edge(fileName):
    line = []
    n = ""
    d = ""
    dimension = 0
    with open(fileName,'r') as file:
        line = file.readline()
        splitLine = line.split()
        numBottomLayers = int(splitLine[2])
        numBottomRowVertices = int(splitLine[0])
        for i in line:
            if i != ' ':
                n += i
            elif i == ' ':
                break
        for i in reversed(line):
            if i != ' ' and i != '\n':
                d += i
            elif i == ' ':
                break
            
        dimension = int(d[::-1])
  
    num = int(n)
    edge = []
    secondToLastRow = num**2 - num
    offset = 0
    blueVertex = num**2
    redVertex = num**2 + 1
    topOffset = (num**2) - num


    for x in range(numBottomLayers):
        offset = x * numBottomLayers
        for i in range(numBottomRowVertices):
            edge.append([blueVertex,i+offset])

    for x in range(numBottomLayers):
        offset = x * numBottomLayers
        
        for i in range(numBottomRowVertices):
            edge.append([redVertex,i+offset+topOffset])

    for z in range(dimension):
        offset = z * (num**2)
        for y in range(num**2):
            if z < (dimension - 1):
                edge.append([y+offset,(y+offset+(num**2))])


        for x in range(0,secondToLastRow,num):
            x_num = x + num + offset
            x_offset = x+offset

            edge.append([x_offset,x_num])
            edge.append([x_offset,x_num+1])
            edge.append([x_offset,(x_offset+1)])

            for i in range(1,num):
                xi = x+i+offset
                edge.append([xi,(xi+num)])
                edge.append([(xi),(xi+(num-1))]) # right to left diagonals

                if i < num-1:
                    edge.append([xi,xi+1+num]) # left to right diagonals bottom row
                    edge.append([xi,xi+1]) # horizontal except first column
                    if x == secondToLastRow - num:
                        edge.append([secondToLastRow+i+offset,secondToLastRow+offset+i+1]) # horizontal last row except first column
            
    edge.append([(secondToLastRow+offset),(secondToLastRow+1+offset)]) # horizontal last row first column

    return edge

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
    edges = edge(file)
    labels = vertexColors(file)

    f = open(file,'r')
    line = f.readline()
    line = line.split()
    
    g = ig.Graph(n = int(line[0])*int(line[1]),edges=edges, directed=False, vertex_attrs={'color':labels})
    g.vs[int(line[0])*int(line[1])]['color'] = 'blue'
    g.vs[int(line[0])*int(line[1])+1]['color'] = 'red'

    return g

def visual2D(g,type):
    if type == 'graph' :
        layout = g.layout('reingold_tilford')  
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


