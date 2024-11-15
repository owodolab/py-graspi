# from . 
import igraph_testing as ig
# import py_graspi as ig
import math

def STAT_n(graph):
    """
    Calculates the number of vertices in the graph, excluding three specific nodes.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of vertices minus three.
    """
    return graph.vcount()-3

def STAT_e(graph):
    """
    Counts the edges connected to at least one 'green' vertex (interface edges).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of edges where at least one endpoint has the color 'green'.
    """
    edgeList = graph.get_edgelist()
    count = 0

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        # check if the edge is connected the interface
        if(graph.vs[currentNode]['color'] == 'green' or graph.vs[toNode]['color'] == 'green'):
            # check if the endpoints of the edges are either green or black
            if(graph.vs[currentNode]['color'] == 'green' and graph.vs[toNode] == 'black') or (graph.vs[currentNode]['color'] == 'black' and graph.vs[toNode]['color'] == 'green'):
                # increment the edge count
                count += 1

    return count

def STAT_n_color(graph):
    """
    Counts the number of vertices colored 'white'.
    Counts the number of vertices colored 'black'.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of vertices with the color 'black'.
        int: The number of vertices with the color 'white'.
    """
    vertices = graph.vcount()
    countBlack = 0
    countWhite = 0

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'black':
            countBlack += 1
        if graph.vs[vertex]['color'] == 'white':
            countWhite += 1
    
    return countBlack, countWhite


def ABS_f_D(graph):
    """
    Calculates the fraction of 'black' vertices out of the total vertices minus three (accounts for red, green, and blue vertices).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        float: The fraction of 'black' vertices.
    """
    fraction = STAT_n_color(graph)[0] / STAT_n(graph)

    return round(fraction,6)

def CC_descriptors(graph):
    """
    Counts the connected components that contain at least one 'black' vertex.
    Counts the connected components that contain at least one 'white' vertex.
    Counts the connected components containing 'black' vertices and 'red' vertex (top).
    Counts the connected components containing 'white' vertices and 'blue' vertex (bottom).
    Calculates the fraction of 'black' vertices in specific connected components with red and black vertices (top).
    Calculates the fraction of 'white' vertices in connected components with 'white' and 'blue' vertices (bottom).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of connected components with at least one 'black' vertex.
        int: The number of connected components with at least one 'white' vertex.
        int: The number of connected components with 'black' and 'red' vertices (top).
        int: The number of connected components with 'white' and 'blue' vertices (bottom).
        float: The fraction of 'black' vertices in connected components with 'black' vertices (top).
        float: The fraction of 'white' vertices in specific connected components (bottom).
    """
    cc = ig.connectedComponents(graph);
    countBlack = 0
    countWhite = 0
    countBlack_Red = 0
    countWhite_Blue = 0
    countBlack_Red_conn = 0
    countWhite_Blue_conn = 0

    totalBlack, totalWhite = STAT_n_color(graph)
    
    if cc is not None:
        for c in cc:
            if graph.vs['color'][c[0]] == "black":
                countBlack += 1

            if graph.vs['color'][c[0]] == "white":
                countWhite += 1

            if graph.vs[c][0]['color'] == 'black' and 'red' in graph.vs[c]['color']:
                countBlack_Red += 1
                countBlack_Red_conn += sum(1 for v in c if graph.vs['color'][v] == 'black')
                        
            
            if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
                countWhite_Blue += 1
                countWhite_Blue_conn += sum(1 for v in c if graph.vs['color'][v] == 'white')


    return countBlack, countWhite, countBlack_Red, countWhite_Blue, round(countBlack_Red_conn / totalBlack,6), round(countWhite_Blue_conn / totalWhite, 6)


def CT_n(graph):
    """
    Counts number of 'white' vertices in direct contact with the 'blue' vertex (bottom).
    Counts number of 'black' vertices in direct contact with the 'red' vertex (top).

    Args:
        graph (igraph.Graph): The input graph.

    Returns multiple values:
        int: The number of 'white' vertices direct contact with the 'blue' vertex (bottom).
        int: The number of 'black' vertices direct contact with the 'red' vertex (top).
    """
    
    edgeList = graph.get_edgelist()
    countWhite = 0
    countBlack = 0

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if(graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue'):
            if(graph.vs[currentNode]['color'] == 'blue' and graph.vs[toNode] == 'white') or (graph.vs[currentNode]['color'] == 'white' and graph.vs[toNode]['color'] == 'blue'):
                countWhite += 1

        if(graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red'):
            if(graph.vs[currentNode]['color'] == 'red' and graph.vs[toNode] == 'black') or (graph.vs[currentNode]['color'] == 'black' and graph.vs[toNode]['color'] == 'red'):
                countBlack += 1

    return countBlack, countWhite

'''--------------- Shortest Path Descriptors ---------------'''
'''
def filterGraph_Metavertices(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color and metavertices

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
        elif ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')):
            keptEdges.append(edge)
        elif ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges, delete_vertices=False)

    return filteredGraph
'''
def filterGraph_metavertices(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color and metavertices

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        ig.Graph: The filtered graph.
    """
    edgeList = graph.get_edgelist()
    keptEdges = []
    keptWeights = []
    keptEdges_blue = []
    keptWeights_blue = []
    keptEdges_red = []
    keptWeights_red= []

    #Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if (graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)
            keptEdges_blue.append(edge)
            keptEdges_red.append(edge)
            keptWeights.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

        if ((graph.vs[currentNode]['color'] == 'green') or (graph.vs[toNode]['color'] == 'green')):
            keptEdges.append(edge)
            keptWeights.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
        elif ((graph.vs[currentNode]['color'] == 'blue') or (graph.vs[toNode]['color'] == 'blue')):
            keptEdges_blue.append(edge)
            keptWeights_blue.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])
        elif ((graph.vs[currentNode]['color'] == 'red') or (graph.vs[toNode]['color'] == 'red')) :
            keptEdges_red.append(edge)
            keptWeights_red.append(graph.es[graph.get_eid(currentNode, toNode)]['weight'])

    filteredGraph_green = graph.subgraph_edges(keptEdges, delete_vertices=False)
    filteredGraph_green.es['weight'] = keptWeights

    fg_blue = graph.subgraph_edges(keptEdges_blue, delete_vertices=False)
    fg_blue.es['weight'] = keptWeights_blue

    fg_red = graph.subgraph_edges(keptEdges_red, delete_vertices=False)
    fg_red.es['weight'] = keptWeights_red

    return filteredGraph_green, fg_blue, fg_red

'''
# def shortest_path_descriptors(graph, is_2d, filename):
#     vertices = graph.vcount()
#     edgeList = graph.get_edgelist()
#     f10_count = 0
#     summation = 0
#     tor_black = 0
#     tor_white = 0
#     blackToTop = 0

#     #get metavertices
#     greenVertex = (graph.vs.select(color = 'green')[0]).index
#     redVertex = (graph.vs.select(color = 'red')[0]).index
#     blueVertex = (graph.vs.select(color = 'blue')[0]).index
    
#     totalBlacks, totalWhites = STAT_n_color(graph)
#     fg = filterGraph_Metavertices(graph)

#     # get red and blue connected components
#     redComponent = set(fg.subcomponent(redVertex, mode="ALL"))
#     blueComponent = set(fg.subcomponent(blueVertex, mode="ALL"))
#     greenComponent = set(graph.subcomponent(greenVertex, mode="ALL"))

#     # get esp_val 
#     with open(filename, "r") as file:
#         header = file.readline().split(' ')
#         if is_2d:
#             esp_val = int(header[1])
#         else:
#             if len(header) == 3:
#                 esp_val = int(header[-1])

#     for vertex in range(vertices):
#         color = graph.vs[vertex]['color']

#         # check if vertex is black
#         if color == 'black':

#             # computation of weighted summation for DISS_wf10_D
#             if vertex in greenComponent:
#                 distance = len(graph.get_shortest_paths(vertex,greenVertex, output="vpath"))
#                 print(distance)
#                 weight = math.exp(-(distance / 10))
#                 summation += (weight*distance)

#                 # number of black vertices for DISS_f10_D
#                 if distance < 10:
#                     f10_count += 1

#                 file0 = open("DistancesBlackToGreen", 'a')
#                 file0.write(f'{vertex}: {distance} \n')
#                 file0.close

#             if vertex in redComponent:
#                 # compute the weighted distance from any black to red via black
#                 distance = len(fg.get_shortest_paths(vertex,redVertex, output="vpath"))
#                 weight = math.exp(-(distance / 10))

#                 file1 = open("DistancesBlackToRed.txt", 'a')
#                 # writing to DistancesBlackToRed
#                 file1.write(str(weight*distance) + '\n')
#                 file1.close()

#                 # computation for TortuosityBlackToRed
#                 delt_h = len(graph.get_shortest_paths(vertex,redVertex, output="vpath"))
#                 d = len(fg.get_shortest_paths(vertex,redVertex, output="vpath"))
#                 t = (d/delt_h) 
#                 tolerance = 1 + (1/esp_val)

#                 # write to TortuosityBlackToRed
#                 file3 = open("TortuosityBlackToRed.txt", 'a')
#                 file3.write(str(t) + '\n')
#                 file3.close()
                
#                 if t < tolerance:
#                     tor_black += 1

            

#         # check if vertex is white
#         if color == 'white' and vertex in blueComponent:
#             # compute the weighted distance from any white to blue via white
#             distance = len(fg.get_shortest_paths(vertex,blueVertex, output="vpath"))
#             weight = math.exp(-(distance / 10))
            
#             # writing to DistancesBlackToRed
#             file2 = open("DistancesWhiteToBlue.txt", 'a')
#             file2.write(str(weight*distance) + '\n')
#             file2.close()

#             # computation for TortuosityWhiteToBlue
#             delt_h = len(graph.get_shortest_paths(vertex,blueVertex, output="vpath"))
#             d = len(fg.get_shortest_paths(vertex,blueVertex, output="vpath"))
#             t = (d/delt_h) 
#             tolerance = 1 + (1/esp_val)

#             # write to TortuosityWhiteToBlue
#             file4 = open("TortuosityWhiteToBlue.txt", "a")
#             file4.write(str(t) + '\n')
#             file4.close()
            
#             if t < tolerance:
#                 tor_white += 1

#     for edge in edgeList:
#         currentNode = edge[0]
#         toNode = edge[1]

#         # check its a vertex connected to the green vertex
#         if currentNode == greenVertex or toNode == greenVertex:
#             # checking to see if the vertex is black and if there is a path to the top
#             if (graph.vs['color'][currentNode] == 'black' and currentNode in redComponent) or (graph.vs['color'][toNode] == 'black' and toNode in redComponent):
#                 blackToTop += 1

#     return blackToTop, f10_count / totalBlacks, summation / totalBlacks, tor_black / totalBlacks, tor_white / totalWhites
'''

def DISS(graph,filename,black_vertices,white_vertices, dim):
    fg_green, fg_blue, fg_red = filterGraph_metavertices(graph)
    greenVertex = (graph.vs.select(color = 'green')[0]).index
    redVertex = (graph.vs.select(color = 'red')[0]).index
    blueVertex = (graph.vs.select(color = 'blue')[0]).index


    distances = fg_green.shortest_paths(source=greenVertex, weights=fg_green.es["weight"])[0]

    black_tor_distances = fg_red.shortest_paths(source=redVertex, weights=fg_red.es["weight"])[0]
    white_tor_distances = fg_blue.shortest_paths(source=blueVertex, weights=fg_blue.es["weight"])[0]

    straight_paths = graph.shortest_paths(source=redVertex, weights=graph.es["weight"])[0]
    
    f10_count = 0
    summation = 0
    black_tor = 0
    white_tor = 0

    totalBlacks = len(black_vertices) 
    totalWhite = len(white_vertices)
    print(f'dim: {dim}')
    for vertex in black_vertices:
        distance = distances[vertex]
        black_tor_distance = black_tor_distances[vertex]
        straight_path = straight_paths[vertex]
        
        if black_tor_distance != float('inf') and straight_path != float('inf'):
            tor = black_tor_distance / straight_path
            tolerance = 1 + (1/dim)

            file = open(f"{filename}_TortuosityBlackToRed.txt", 'a')
            file.write(f'{tor}\n')
            file.close()

            file = open(f"{filename}_IdTortuosityBlackToRed.txt",'a')
            file.write(f'{vertex} {tor} {black_tor_distance} {straight_path}\n')
            file.close()

            if tor < tolerance:
                black_tor += 1

        if distance != float('inf'):
            # summation of weight * distance for DISS_wf10_D
            A1=6.265
            B1=-23.0
            C1=17.17
            
            summation += A1*math.exp(-((distance-B1)/C1)*((distance-B1)/C1))

            file = open(f"{filename}_DistanceBlackToGreen.txt", 'a')
            file.write(f'{str(distance)}\n')
            file.close()

            file = open(f"{filename}_DistanceBlackToRed.txt", 'a')
            file.write(f'{black_tor_distance}\n')
            file.close()

            # check if distance is < 10, if yes, increment counter for DISS_f10_D
            if distance > 0 and distance < 10:
                f10_count += 1
    

    straight_paths = graph.shortest_paths(source=blueVertex, weights=graph.es["weight"])[0]
    for vertex in white_vertices:
        white_tor_distance = white_tor_distances[vertex]
        straight_path = straight_paths[vertex]
        
        file = open(f"{filename}_DistancesWhiteToBlue.txt",'a')
        file.write(f'{white_tor_distance}\n')
        file.close()

        if white_tor_distance != float('inf') and straight_path != float('inf'):
            tor = white_tor_distance / straight_path
            tolerance = 1 + (1/dim)

            file = open(f"{filename}_TortuosityWhiteToBlue.txt",'a')
            file.write(f'{tor}\n')
            file.close()

            file = open(f"{filename}_IdTortuosityWhiteToBlue.txt",'a')
            file.write(f'{vertex} {tor} {white_tor_distance} {straight_path}\n')
            file.close()

            if tor < tolerance:
                white_tor += 1
    
        

    return f10_count / totalBlacks, summation / totalBlacks, black_tor / totalBlacks, white_tor / totalWhite



def descriptors(graph,filename,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim):
    """
    Generates a dictionary of all graph descriptors.

    Args:
        graph (igraph.Graph): The input graph.
        filename: file used to generate graph

    Returns:
        dict: A dictionary of descriptors and their calculated values.
    """
    dict = {}

    STAT_n_D = len(black_vertices)
    STAT_n_A = len(white_vertices)
    STAT_CC_D, STAT_CC_A, STAT_CC_D_An, STAT_CC_A_Ca, CT_f_conn_D_An, CT_f_conn_A_Ca = CC_descriptors(graph)
    CT_n_D_adj_An, CT_n_A_adj_Ca = CT_n(graph)

    # shortest path descriptors

    DISS_f10_D, DISS_wf10_D, CT_f_D_tort1, CT_f_A_tort1= DISS(graph,filename, black_vertices,white_vertices, dim)

    dict["STAT_n"] =  STAT_n_A + STAT_n_D
    dict["STAT_e"] = black_green
    dict["STAT_n_D"] = STAT_n_D
    dict["STAT_n_A"] = STAT_n_A
    dict["STAT_CC_D"] = STAT_CC_D
    dict["STAT_CC_A"] = STAT_CC_A
    dict["STAT_CC_D_An"] = STAT_CC_D_An
    dict["STAT_CC_A_Ca"] = STAT_CC_A_Ca
    dict["ABS_f_D"] = STAT_n_D / (STAT_n_D + STAT_n_A)
    dict["DISS_f10_D"] = DISS_f10_D
    dict["DISS_wf10_D"] = DISS_wf10_D
    dict["CT_e_D_An"] = black_interface_red
    dict["CT_e_A_Ca"] = white_interface_blue
    dict["CT_f_conn_D_An"] = CT_f_conn_D_An
    dict["CT_f_conn_A_Ca"] = CT_f_conn_A_Ca
    dict["CT_n_D_adj_An"] = CT_n_D_adj_An
    dict["CT_n_A_adj_Ca"] = CT_n_A_adj_Ca
    dict["CT_f_D_tort1"] = CT_f_D_tort1
    dict["CT_f_A_tort1"] = CT_f_A_tort1

    return dict


def descriptorsToTxt(dict, fileName):
    """
    Writes graph descriptors to a text file.

    Args:
        dict (dict): The dictionary of descriptors.
        fileName (str): The name of the file to write to.

    Returns:
        None
    """

    f = open(fileName,"x")

    with open(fileName,'a') as f:
        for d in dict:
            f.write(d + " " + str(dict[d]) + '\n')



