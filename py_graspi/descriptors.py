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
                colors = np.array(graph.vs['color'])
                countBlack_Red_conn += np.sum(colors[c] == 'black')
                        
            
            if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
                countWhite_Blue += 1
                colors = np.array(graph.vs['color'])
                countWhite_Blue_conn += np.sum(colors[c] == 'white')

    return countBlack, countWhite, countBlack_Red, countWhite_Blue, float(countBlack_Red_conn / totalBlack), \
        float(countWhite_Blue_conn / totalWhite), countBlack_Red_conn, countWhite_Blue_conn

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
    keptEdges_red_unfiltered = []
    keptWeights_red_unfiltered = []

    #Checks edges and keeps only edges that connect to the same colored vertices
    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

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
        
        if((color_current != 'blue') and (color_toNode != 'blue') \
           and (color_current != 'green') and (color_toNode != 'green')):
            keptEdges_red_unfiltered.append(edge)
            keptWeights_red_unfiltered.append(weight)
            


    filteredGraph_green = graph.subgraph_edges(keptEdges, delete_vertices=False)
    filteredGraph_green.es['weight'] = keptWeights

    fg_blue = graph.subgraph_edges(keptEdges_blue, delete_vertices=False)
    fg_blue.es['weight'] = keptWeights_blue

    fg_red = graph.subgraph_edges(keptEdges_red, delete_vertices=False)
    fg_red.es['weight'] = keptWeights_red

    fg_red_unfiltered = graph.subgraph_edges(keptEdges_red_unfiltered, delete_vertices=False)
    fg_red_unfiltered['weight'] = keptWeights_red_unfiltered

    return filteredGraph_green, fg_blue, fg_red, fg_red_unfiltered

def shortest_path_descriptors(graph,filename,black_vertices,white_vertices, dim, shortest_path_to_red, \
                              shortest_path_to_blue,countBlack_Red_conn, countWhite_Blue_conn):
    fg_green, fg_blue, fg_red, fg_red_unfiltered = filterGraph_metavertices(graph)
    greenVertex = (graph.vs.select(color = 'green')[0]).index
    redVertex = (graph.vs.select(color = 'red')[0]).index
    blueVertex = (graph.vs.select(color = 'blue')[0]).index


    distances = fg_green.shortest_paths(source=greenVertex, weights=fg_green.es["weight"])[0]

    black_tor_distances = fg_red.shortest_paths(source=redVertex, weights=fg_red.es["weight"])[0]
    white_tor_distances = fg_blue.shortest_paths(source=blueVertex, weights=fg_blue.es["weight"])[0]

    black_red_unfiltered_distance = fg_red_unfiltered.shortest_paths(source=redVertex, weights=fg_red_unfiltered.es['weight'])[0]

    f10_count = 0
    summation = 0
    black_tor = 0
    white_tor = 0
    total_weighted_black_red = 0

    totalBlacks = len(black_vertices) 
    totalWhite = len(white_vertices)

    filename = filename.split('.txt')[0]

    tort_black_to_red = []
    id_tort_black_to_red = []
    dist_black_to_green = []
    dist_black_to_red = []
    dist_white_to_blue = []
    tort_white_to_blue = []
    id_tort_white_to_blue = []

    d = []
  
    for vertex in black_vertices:
        distance = distances[vertex]
        black_tor_distance = black_tor_distances[vertex]
        straight_path = shortest_path_to_red[vertex]
        black_red = black_red_unfiltered_distance[vertex]
        
        # computing the tor descriptors
        if black_tor_distance != float('inf') and straight_path != float('inf'):
            if straight_path == 0: 
                tor = 1
            else:
                tor = black_tor_distance / straight_path
            tolerance = 1 + (1/dim)
            
            if tor < tolerance:
                tor = 1
                black_tor += 1

            tort_black_to_red.append(f'{float(tor)}\n')
            id_tort_black_to_red.append(f'{vertex} {float(tor)} {float(black_tor_distance)} {float(straight_path)}\n')
    

        if distance != float('inf'):
            dist_black_to_green.append(f'{float(distance)}\n')

            # summation of weight * distance for DISS_wf10_D
            A1=6.265
            B1=-23.0
            C1=17.17

            # check if distance is < 10, if yes, increment counter for DISS_f10_D
            if distance > 0 and distance < 10:
                summation += A1*math.exp(-((distance-B1)/C1)*((distance-B1)/C1))
                f10_count += 1

        if black_tor_distance != float('inf'): 
            dist_black_to_red.append(f'{float(black_tor_distance)}\n')
        
        # computation for ABS_wf_D
        total_weighted_black_red += math.exp(-1.0*(black_red)/100)
    

    for vertex in white_vertices:
        white_tor_distance = white_tor_distances[vertex]
        straight_path = shortest_path_to_blue[vertex]
        
        dist_white_to_blue.append(f'{float(white_tor_distance)}\n')

        if white_tor_distance != float('inf') and straight_path != float('inf'):
            if straight_path == 0:
                tor = 1
            else:
                tor = white_tor_distance / straight_path
            tolerance = 1 + (1/dim)

            if tor < tolerance:
                tor = 1
                white_tor += 1

            tort_white_to_blue.append(f'{float(tor)}\n')
            id_tort_white_to_blue.append(f'{vertex} {float(tor)} {float(white_tor_distance)} {float(straight_path)}\n')

    
    file = open(f"{filename}_TortuosityBlackToRed.txt", 'w')
    file.writelines(tort_black_to_red)
    file.close()

    file = open(f"{filename}_IdTortuosityBlackToRed.txt", 'w')
    file.writelines(id_tort_black_to_red)
    file.close()

    file = open(f"{filename}_DistancesBlackToGreen.txt", 'w')
    file.writelines(dist_black_to_green)
    file.close()

    file = open(f"{filename}_DistancesBlackToRed.txt", 'w')
    file.writelines(dist_black_to_red)
    file.close()

    file = open(f"{filename}_DistancesWhiteToBlue.txt", 'w')
    file.writelines(dist_white_to_blue)
    file.close()

    file = open(f"{filename}_TortuosityWhiteToBlue.txt", 'w')
    file.writelines(tort_white_to_blue)
    file.close()

    file = open(f"{filename}_IdTortuosityWhiteToBlue.txt", 'w')
    file.writelines(id_tort_white_to_blue)
    file.close()

    return float(f10_count / totalBlacks), float(summation / totalBlacks), float(black_tor / countBlack_Red_conn), \
        float(white_tor / countWhite_Blue_conn), float(total_weighted_black_red / (totalBlacks + totalWhite))



def descriptors(graph,filename,black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, \
                dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca):
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
    STAT_CC_D, STAT_CC_A, STAT_CC_D_An, STAT_CC_A_Ca, CT_f_conn_D_An, CT_f_conn_A_Ca, countBlack_Red_conn, \
        countWhite_Blue_conn = CC_descriptors(graph, STAT_n_D,STAT_n_A)


    # shortest path descriptors
    DISS_f10_D, DISS_wf10_D, CT_f_D_tort1, CT_f_A_tort1, ABS_wf_D \
        = shortest_path_descriptors(graph,filename, black_vertices,white_vertices, dim, shortest_path_to_red, \
                                    shortest_path_to_blue, countBlack_Red_conn, countWhite_Blue_conn)

    dict["STAT_n"] =  STAT_n_A + STAT_n_D
    dict["STAT_e"] = black_green
    dict["STAT_n_D"] = STAT_n_D
    dict["STAT_n_A"] = STAT_n_A
    dict["STAT_CC_D"] = STAT_CC_D
    dict["STAT_CC_A"] = STAT_CC_A
    dict["STAT_CC_D_An"] = STAT_CC_D_An
    dict["STAT_CC_A_Ca"] = STAT_CC_A_Ca
    dict['ABS_wf_D'] = ABS_wf_D
    dict["ABS_f_D"] = float(STAT_n_D / (STAT_n_D + STAT_n_A))
    dict["DISS_f10_D"] = DISS_f10_D
    dict["DISS_wf10_D"] = DISS_wf10_D
    dict["CT_f_e_conn"] = float(interface_edge_comp_paths / black_green)
    dict["CT_f_conn_D_An"] = CT_f_conn_D_An
    dict["CT_f_conn_A_Ca"] = CT_f_conn_A_Ca
    dict["CT_e_conn"] = interface_edge_comp_paths
    dict["CT_e_D_An"] = black_interface_red
    dict["CT_e_A_Ca"] = white_interface_blue
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

    with open(fileName,'w') as f:
        for d in dict:
            f.write(d + " " + str(float(dict[d])) + '\n')



