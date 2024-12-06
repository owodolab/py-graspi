import igraph_testing as ig
import math
import numpy as np

def CC_descriptors(graph,totalBlack, totalWhite):
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
    
    if cc is not None:
        for c in cc:
            if graph.vs['color'][c[0]] == "black":
                countBlack += 1

            if graph.vs['color'][c[0]] == "white":
                countWhite += 1

            if graph.vs[c][0]['color'] == 'black' and 'red' in graph.vs[c]['color']:
                countBlack_Red += 1
                # countBlack_Red_conn += sum(1 for v in c if graph.vs['color'][v] == 'black')
                # QP
                colors = np.array(graph.vs['color'])
                countBlack_Red_conn += np.sum(colors[c] == 'black')
                        
            
            if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
                countWhite_Blue += 1
                # countWhite_Blue_conn += sum(1 for v in c if graph.vs['color'][v] == 'white')
                #QP
                colors = np.array(graph.vs['color'])
                countWhite_Blue_conn += np.sum(colors[c] == 'white')
            # 21% to 7% of runtime

    return countBlack, countWhite, countBlack_Red, countWhite_Blue, round(countBlack_Red_conn / totalBlack,6), round(countWhite_Blue_conn / totalWhite, 6)

'''--------------- Shortest Path Descriptors ---------------'''
def filterGraph_metavertices(graph):
    """
    Filters the graph by keeping only edges between vertices of the same color and metavertices

    Args:
        graph (ig.Graph): The input graph.

    Returns:
        ig.Graph: The filtered graph of vertices of same color and green interface
        ig.Graph: The filtered graph of vertices of same color and blue metavertex
        ig.Graph: The filtered graph of vertices of same color and green metavertex
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


        #QP 

        #call these values once
        weight = graph.es[graph.get_eid(currentNode, toNode)]['weight']
        color_current = graph.vs[currentNode]['color']
        color_toNode = graph.vs[toNode]['color']
        
        if (color_current == color_toNode):
            keptEdges.append(edge)
            keptEdges_blue.append(edge)
            keptEdges_red.append(edge)
            keptWeights.append(weight)
            keptWeights_blue.append(weight)
            keptWeights_red.append(weight)

        

        
        
        if ((color_current == 'green') or (color_toNode == 'green')):
            keptEdges.append(edge)
            keptWeights.append(weight)
        elif ((color_current == 'blue') or (color_toNode == 'blue')):
            keptEdges_blue.append(edge)
            keptWeights_blue.append(weight)
        elif ((color_current == 'red') or (color_toNode == 'red')) :
            keptEdges_red.append(edge)
            keptWeights_red.append(weight)




    filteredGraph_green = graph.subgraph_edges(keptEdges, delete_vertices=False)
    filteredGraph_green.es['weight'] = keptWeights

    fg_blue = graph.subgraph_edges(keptEdges_blue, delete_vertices=False)
    fg_blue.es['weight'] = keptWeights_blue

    fg_red = graph.subgraph_edges(keptEdges_red, delete_vertices=False)
    fg_red.es['weight'] = keptWeights_red

    # filteredGraph_green = graph.subgraph_edges(kept['edges'], delete_vertices=False)
    # filteredGraph_green.es['weight'] = kept['weights']

    # fg_blue = graph.subgraph_edges(kept['edges_blue'], delete_vertices=False)
    # fg_blue.es['weight'] = kept['weights_blue']

    # fg_red = graph.subgraph_edges(kept['edges_red'], delete_vertices=False)
    # fg_red.es['weight'] = kept['weights_red']

    return filteredGraph_green, fg_blue, fg_red

def shortest_path_descriptors(graph,filename,black_vertices,white_vertices, dim, shortest_path_to_red, shortest_path_to_blue):
    fg_green, fg_blue, fg_red = filterGraph_metavertices(graph)
    greenVertex = (graph.vs.select(color = 'green')[0]).index
    redVertex = (graph.vs.select(color = 'red')[0]).index
    blueVertex = (graph.vs.select(color = 'blue')[0]).index


    distances = fg_green.shortest_paths(source=greenVertex, weights=fg_green.es["weight"])[0]

    black_tor_distances = fg_red.shortest_paths(source=redVertex, weights=fg_red.es["weight"])[0]
    white_tor_distances = fg_blue.shortest_paths(source=blueVertex, weights=fg_blue.es["weight"])[0]

    f10_count = 0
    summation = 0
    black_tor = 0
    white_tor = 0

    totalBlacks = len(black_vertices) 
    totalWhite = len(white_vertices)

    filename = filename.split('.txt')[0]
  
    for vertex in black_vertices:
        distance = distances[vertex]
        black_tor_distance = black_tor_distances[vertex]
        straight_path = shortest_path_to_red[vertex]
        
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
            file.write(f'{str(round(distance,6))}\n')
            file.close()

            file = open(f"{filename}_DistanceBlackToRed.txt", 'a')
            file.write(f'{black_tor_distance}\n')
            file.close()

            # check if distance is < 10, if yes, increment counter for DISS_f10_D
            if distance > 0 and distance < 10:
                f10_count += 1
    

    for vertex in white_vertices:
        white_tor_distance = white_tor_distances[vertex]
        straight_path = shortest_path_to_blue[vertex]
        
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


import time
import tracemalloc
def descriptors(graph,filename,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca):
    """
    Generates a dictionary of all graph descriptors.

    Args:
        graph (igraph.Graph): The input graph.
        filename: file used to generate graph

    Returns:
        dict: A dictionary of descriptors and their calculated values.
    """
    dict = {}
    start = time.time()
    tracemalloc.start()
    STAT_n_D = len(black_vertices)
    STAT_n_A = len(white_vertices)
    STAT_CC_D, STAT_CC_A, STAT_CC_D_An, STAT_CC_A_Ca, CT_f_conn_D_An, CT_f_conn_A_Ca = CC_descriptors(graph, STAT_n_D,STAT_n_A)


    # shortest path descriptors
    DISS_f10_D, DISS_wf10_D, CT_f_D_tort1, CT_f_A_tort1 = shortest_path_descriptors(graph,filename, black_vertices,white_vertices, dim, shortest_path_to_red, shortest_path_to_blue)

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
    dict["CT_f_e_conn"] = interface_edge_comp_paths / black_green
    dict["CT_f_conn_D_An"] = CT_f_conn_D_An
    dict["CT_f_conn_A_Ca"] = CT_f_conn_A_Ca
    dict["CT_e_conn"] = interface_edge_comp_paths
    dict["CT_e_D_An"] = black_interface_red
    dict["CT_e_A_Ca"] = white_interface_blue
    dict["CT_n_D_adj_An"] = CT_n_D_adj_An
    dict["CT_n_A_adj_Ca"] = CT_n_A_adj_Ca
    dict["CT_f_D_tort1"] = CT_f_D_tort1
    dict["CT_f_A_tort1"] = CT_f_A_tort1
    stats = tracemalloc.get_traced_memory()
    end = time.time()
    tracemalloc.stop()
    stats = stats[1] - stats[0]
    total_time = end-start
    dict["time"] = total_time
    dict["mem"] = stats

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


