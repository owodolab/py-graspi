import math
import os

import numpy as np
from py_graspi import graph as ig
from py_graspi import graph_data_class as GraphData
import time
import tracemalloc


def compute_descriptors(graph_data, filename,pixelSize=1):
    """
    This function computes all the descriptors for the graph given and saves them  in a dictionary.

    Args:
        graph_data (GraphData): The graph data.
        filename (str): The file used to generate graphs to compute on.
        pixelsize (float): The pixel size of the graph.

    Returns:
        descriptors_dict: A dictionary containing all the descriptors. The dictionary stores the outputted data in key:value pairs, the unique keys are linked to the associated value.
         The keys of the descriptors are as follow: STAT_n, STAT_e, STAT_n_D, STAT_n_A, STAT_CC_D, STAT_CC_A, STAT_CC_D_An, STAT_CC_A_Ca, ABS_wf_D, ABS_f_D, DISS_f10_D, DISS_wf10_D, CT_f_e_conn, CT_f_conn_D_An, CT_f_conn_A_Ca, CT_e_conn, CT_e_D_An, CT_e_A_Ca, CT_n_D_adj_An, CT_n_A_adj_Ca, CT_f_D_tort1, CT_f_A_tort1.
         For full definitions see the “Descriptors” tab on the Py-Graspi documentation website.
    """

    descriptors_dict = {}

    start = time.time()
    tracemalloc.start()

    STAT_n_D = len(graph_data.black_vertices)
    STAT_n_A = len(graph_data.white_vertices)
    graph_data.STAT_n_D = STAT_n_D
    graph_data.STAT_n_A = STAT_n_A
    graph_data = CC_descriptors(graph_data)

    # shortest path descriptors
    graph_data = shortest_path_descriptors(graph_data, filename, pixelSize)

    descriptors_dict["STAT_n"] =  graph_data.STAT_n_A + graph_data.STAT_n_D
    descriptors_dict["STAT_e"] = graph_data.black_green
    descriptors_dict["STAT_n_D"] = graph_data.STAT_n_D
    descriptors_dict["STAT_n_A"] = graph_data.STAT_n_A
    descriptors_dict["STAT_CC_D"] = graph_data.STAT_CC_D
    descriptors_dict["STAT_CC_A"] = graph_data.STAT_CC_A
    descriptors_dict["STAT_CC_D_An"] = graph_data.STAT_CC_D_An
    descriptors_dict["STAT_CC_A_Ca"] = graph_data.STAT_CC_A_Ca
    descriptors_dict['ABS_wf_D'] = graph_data.ABS_wf_D
    descriptors_dict["ABS_f_D"] = float(graph_data.STAT_n_D / (graph_data.STAT_n_D + graph_data.STAT_n_A))
    descriptors_dict["DISS_f10_D"] = graph_data.DISS_f10_D
    descriptors_dict["DISS_wf10_D"] = graph_data.DISS_wf10_D
    descriptors_dict["CT_f_e_conn"] = float(graph_data.interface_edge_comp_paths / graph_data.black_green)
    descriptors_dict["CT_f_conn_D_An"] = graph_data.CT_f_conn_D_An
    descriptors_dict["CT_f_conn_A_Ca"] = graph_data.CT_f_conn_A_Ca
    descriptors_dict["CT_e_conn"] = graph_data.interface_edge_comp_paths
    descriptors_dict["CT_e_D_An"] = graph_data.black_interface_red
    descriptors_dict["CT_e_A_Ca"] = graph_data.white_interface_blue
    descriptors_dict["CT_n_D_adj_An"] = graph_data.CT_n_D_adj_An
    descriptors_dict["CT_n_A_adj_Ca"] = graph_data.CT_n_A_adj_Ca
    descriptors_dict["CT_f_D_tort1"] = graph_data.CT_f_D_tort1
    descriptors_dict["CT_f_A_tort1"] = graph_data.CT_f_A_tort1

    stats = tracemalloc.get_traced_memory()
    end = time.time()
    tracemalloc.stop()
    stats = stats[1] - stats[0]
    total_time = end - start
    descriptors_dict["time_in_seconds"] = total_time
    descriptors_dict["mem_in_mb"] = stats / (1024 * 1024)

    return descriptors_dict

#Marked for improvement. This function should return bool - the status of the writing process.
def descriptorsToTxt(descriptors_dict, fileName):
    """
    This function writes a dictionary of descriptors to the specified text file.

    Args:
        descriptors_dict (dict): The dictionary of descriptors.
        fileName (str): The name of the file to write to.

    Returns:
        None
    """

    with open(fileName,'w') as f:
        for d in descriptors_dict:
            f.write(d + " " + str(float(descriptors_dict[d])) + '\n')

def readDescriptorsFromTxt(fileName):
    """
        This function reads a text file and returns a dictionary of descriptors to standard output.

        Args:
            fileName (str): The name of the file to read from.

        Returns:
            None
        """
    with open(fileName, 'r') as file:
        content = file.read()
        print(content)

def printDescriptors(dict):
    """
    This function prints descriptors to standard output.

    Args:
        dict (dict): The dictionary of descriptors.

    Returns:
        None, but standard outputs descriptors.
    """
    for key, value in dict.items():
        print(key, value)

def CC_descriptors(graph_data):
    """
    This function computes the connected component descriptors that correspond to the following descriptors:
    STAT_CC_D, STAT_CC_A, STAT_CC_D_An, STAT_CC_A_Ca, CT_f_conn_D_An, CT_f_conn_A_Ca, countBlack_Red_conn, and countWhite_Blue_conn.
    Auxiliary quantities such as, ‘countBlack_Red_conn’ and ‘countWhite_Blue_conn’ are only used to compute CT_f_conn_D_An and CT_f_conn_A_Ca.

    Args:
        graph_data (graph_data_class): The input graph object.

    Returns:
        graph_data (graph_data_class): The updated graph object.
    """
    graph = graph_data.graph
    totalWhite = graph_data.STAT_n_A
    totalBlack = graph_data.STAT_n_D

    cc = ig.connectedComponents(graph)
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

    graph_data.STAT_CC_D = countBlack
    graph_data.STAT_CC_A = countWhite
    graph_data.STAT_CC_D_An = countBlack_Red
    graph_data.STAT_CC_A_Ca = countWhite_Blue
    if totalBlack != 0:
        graph_data.CT_f_conn_D_An = float(countBlack_Red_conn / totalBlack)
    if totalWhite != 0:
        graph_data.CT_f_conn_A_Ca = float(countWhite_Blue_conn / totalWhite)
    graph_data.countBlack_Red_conn = countBlack_Red_conn
    graph_data.countWhite_Blue_conn = countWhite_Blue_conn

    return graph_data


def shortest_path_descriptors(graph_data, filename,pixelSize=1):
    """
        This function computes descriptors related to shortest paths with vertex and metavertex colorations that correspond to the following descriptors:
        DISS_f10_D, DISS_wf10_D, CT_f_D_tort1, CT_f_A_tort1 and ABS_wf_D.
        The inputs countBlack_Red_conn and countWhite_Blue_conn are stored in the graph_data_class object generated by the ‘CC_descriptors’ function.

        Args:
            graph_data (graph_data_class): The graph data object.
            filename (str): Base filename for output text files storing the results.
            pixelSize(float): The pixel size of the graph in pixels.

        Returns:
            graph_data (graph_data_class): The updated graph data object with shortest path descriptors
        """
    graph = graph_data.graph
    black_vertices = graph_data.black_vertices
    white_vertices = graph_data.white_vertices
    dim = graph_data.dim
    countBlack_Red_conn = graph_data.countBlack_Red_conn
    countWhite_Blue_conn = graph_data.countWhite_Blue_conn
    shortest_path_to_red = graph_data.shortest_path_to_red
    shortest_path_to_blue = graph_data.shortest_path_to_blue

    fg_green, fg_blue, fg_red, fg_red_unfiltered = filterGraph_metavertices(graph)
    greenVertex = (graph.vs.select(color = 'green')[0]).index
    redVertex = (graph.vs.select(color = 'red')[0]).index
    blueVertex = (graph.vs.select(color = 'blue')[0]).index

    distances = fg_green.shortest_paths(source=greenVertex, weights=fg_green.es["weight"])[0]

    black_tor_distances = fg_red.shortest_paths(source=redVertex, weights=fg_red.es["weight"])[0]
    white_tor_distances = fg_blue.shortest_paths(source=blueVertex, weights=fg_blue.es["weight"])[0]

    black_red_unfiltered_distance = \
    fg_red_unfiltered.shortest_paths(source=redVertex, weights=fg_red_unfiltered.es['weight'])[0]

    # Apply pixelSize only where needed
    distances = [d * pixelSize for d in distances]  # For DISS_f10_D and DISS_wf10_D
    black_red_unfiltered_distance = [d * pixelSize for d in black_red_unfiltered_distance]  # For ABS_wf_D

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
            tolerance = 1 + (1 / dim)

            if tor < tolerance:
                tor = 1
                black_tor += 1

            tort_black_to_red.append(f'{float(tor)}\n')
            id_tort_black_to_red.append(f'{vertex} {float(tor)} {float(black_tor_distance)} {float(straight_path)}\n')

        if distance != float('inf'):
            dist_black_to_green.append(f'{float(distance)}\n')

            # summation of weight * distance for DISS_wf10_D
            A1 = 6.265
            B1 = -23.0
            C1 = 17.17

            # check if distance is < 10, if yes, increment counter for DISS_f10_D
            if distance > 0 and distance < 10:
                summation += A1 * math.exp(-((distance - B1) / C1) * ((distance - B1) / C1))
                f10_count += 1

        if black_tor_distance != float('inf'):
            dist_black_to_red.append(f'{float(black_tor_distance)}\n')

        # computation for ABS_wf_D
        total_weighted_black_red += math.exp(-1.0 * (black_red) / 100)

    for vertex in white_vertices:
        white_tor_distance = white_tor_distances[vertex]
        straight_path = shortest_path_to_blue[vertex]

        dist_white_to_blue.append(f'{float(white_tor_distance)}\n')

        if white_tor_distance != float('inf') and straight_path != float('inf'):
            if straight_path == 0:
                tor = 1
            else:
                tor = white_tor_distance / straight_path
            tolerance = 1 + (1 / dim)

            if tor < tolerance:
                tor = 1
                white_tor += 1

            tort_white_to_blue.append(f'{float(tor)}\n')
            id_tort_white_to_blue.append(f'{vertex} {float(tor)} {float(white_tor_distance)} {float(straight_path)}\n')

    filename = os.path.basename(filename)
    os.makedirs("test_results", exist_ok=True)
    file = open(f"./test_results/{filename}_TortuosityBlackToRed.txt", 'w')
    file.writelines(tort_black_to_red)
    file.close()

    file = open(f"./test_results/{filename}_IdTortuosityBlackToRed.txt", 'w')
    file.writelines(id_tort_black_to_red)
    file.close()

    file = open(f"./test_results/{filename}_DistancesBlackToGreen.txt", 'w')
    file.writelines(dist_black_to_green)
    file.close()

    file = open(f"./test_results/{filename}_DistancesBlackToRed.txt", 'w')
    file.writelines(dist_black_to_red)
    file.close()

    file = open(f"./test_results/{filename}_DistancesWhiteToBlue.txt", 'w')
    file.writelines(dist_white_to_blue)
    file.close()

    file = open(f"./test_results/{filename}_TortuosityWhiteToBlue.txt", 'w')
    file.writelines(tort_white_to_blue)
    file.close()

    file = open(f"./test_results/{filename}_IdTortuosityWhiteToBlue.txt", 'w')
    file.writelines(id_tort_white_to_blue)
    file.close()
    if totalBlacks != 0:
        graph_data.DISS_f10_D = float(f10_count / totalBlacks)
        graph_data.DISS_wf10_D = float(summation / totalBlacks)
    if countBlack_Red_conn != 0:
        graph_data.CT_f_D_tort1 = float(black_tor / countBlack_Red_conn)
    if countWhite_Blue_conn != 0:
       graph_data.CT_f_A_tort1 = float(white_tor / countWhite_Blue_conn)
    if totalBlacks + totalWhite != 0:
        graph_data.ABS_wf_D = float(total_weighted_black_red / (totalBlacks + totalWhite))
    return graph_data

'''--------------- Shortest Path Descriptors ---------------'''

def filterGraph_metavertices(graph):

    """
    This function filters a graph by only keeping the edges that connect vertices of the same color and metavertices.

    Args:
        graph (ig.Graph): The input graph.
        
    Returns:
        ig.Graph: The filtered graph of vertices of the same color and green metavertex.
        ig.Graph: The filtered graph of vertices of the same color and blue metavertex.
        ig.Graph: The filtered graph of vertices of the same color and green metavertex.
        ig.Graph: The filtered graph of vertices of the same color and red metavertex.

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