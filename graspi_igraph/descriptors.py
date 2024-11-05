from . import igraph_testing as ig
# import igraph_testing as ig

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
        # neighbor of green, only with only blacks and if first neighbor
        if(graph.vs[currentNode]['color'] == 'green' or graph.vs[toNode]['color'] == 'green'):
            if(graph.vs[currentNode]['color'] == 'green' and graph.vs[toNode] == 'black') or (graph.vs[currentNode]['color'] == 'black' and graph.vs[toNode]['color'] == 'green'):
                count += 1

    return count

def STAT_n_D(graph):
    """
    Counts the number of vertices colored 'black'.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of vertices with the color 'black'.
    """
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'black':
            count += 1
    
    return count

def STAT_n_A(graph):
    """
    Counts the number of vertices colored 'white'.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of vertices with the color 'white'.
    """
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'white':
            count += 1
    
    return count

def STAT_CC_D(graph):
    """
    Counts the connected components that contain at least one 'black' vertex.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of connected components with at least one 'black' vertex.
    """
    cc = ig.connectedComponents(graph);
    count = 0

    for c in cc:
        if graph.vs['color'][c[0]] == "black":
            count += 1

    return count

def STAT_CC_A(graph):
    """
    Counts the connected components that contain at least one 'white' vertex.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of connected components with at least one 'white' vertex.
    """
    cc = ig.connectedComponents(graph);
    count = 0

    for c in cc:
        if graph.vs['color'][c[0]] == "white":
            count += 1

    return count
    
def STAT_CC_D_An(graph):
    """
    Counts the connected components containing 'black' vertices and 'red' vertex (top).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of connected components with 'black' and 'red' vertices (top).
    """
    cc = ig.connectedComponents(graph);
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'black' and 'red' in graph.vs[c]['color']:
            count += 1
    
    return count

def STAT_CC_A_Ca(graph):
    """
    Counts the connected components containing 'white' vertices and 'blue' vertex (bottom).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of connected components with 'white' and 'blue' vertices (bottom).
    """
    cc = ig.connectedComponents(graph);
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
            count += 1
    
    return count

def ABS_f_D(graph):
    """
    Calculates the fraction of 'black' vertices out of the total vertices minus three (accounts for red, green, and blue vertices).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        float: The fraction of 'black' vertices.
    """
    fraction = STAT_n_D(graph) / STAT_n(graph)

    return round(fraction,6)

def CT_f_conn_D_An(graph):
    """
    Calculates the fraction of 'black' vertices in specific connected components with red and black vertices (top).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        float: The fraction of 'black' vertices in connected components with 'black' vertices (top).
    """
    cc = ig.connectedComponents(graph);
    count = 0
    
    if cc is not None:
        for c in cc:
            if graph.vs[c][0]['color'] == 'black' and 'red' in graph.vs[c]['color']:
                for vertex in c:
                    if graph.vs[vertex]['color'] == 'black':
                        count += 1

    fraction = count / STAT_n_D(graph)
 
    return round(fraction,6)

def CT_f_conn_A_Ca(graph):
    """
    Calculates the fraction of 'white' vertices in connected components with 'white' and 'blue' vertices (bottom).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        float: The fraction of 'white' vertices in specific connected components (bottom).
    """
    cc = ig.connectedComponents(graph);
    count = 0

    if cc is not None:
        for c in cc:
            if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
                for vertex in c:
                    if graph.vs[vertex]['color'] == 'white':
                        count += 1

    fraction = count / STAT_n_A(graph)

    return round(fraction,6)

def CT_n_D_adj_An(graph):
    """
    Counts number of 'black' vertices in direct contact with the 'red' vertex (top).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of 'black' vertices direct contact with the 'red' vertex (top).
    """
    edgeList = graph.get_edgelist()
    count = 0

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if(graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red'):
            if(graph.vs[currentNode]['color'] == 'red' and graph.vs[toNode] == 'black') or (graph.vs[currentNode]['color'] == 'black' and graph.vs[toNode]['color'] == 'red'):
                count += 1

    return count

def CT_n_A_adj_Ca(graph):
    """
    Counts number of 'white' vertices in direct contact with the 'blue' vertex (bottom).

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        int: The number of 'white' vertices direct contact with the 'blue' vertex (bottom).
    """
    
    edgeList = graph.get_edgelist()
    count = 0

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]

        if(graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue'):
            if(graph.vs[currentNode]['color'] == 'blue' and graph.vs[toNode] == 'white') or (graph.vs[currentNode]['color'] == 'white' and graph.vs[toNode]['color'] == 'blue'):
                count += 1

    

    return count

def descriptors(graph):
    """
    Generates a dictionary of all graph descriptors.

    Args:
        graph (igraph.Graph): The input graph.

    Returns:
        dict: A dictionary of descriptors and their calculated values.
    """
    dict = {}
    dict["STAT_n"] =  STAT_n(graph)
    dict["STAT_e"] = STAT_e(graph)
    dict["STAT_n_D"] = STAT_n_D(graph)
    dict["STAT_n_A"] = STAT_n_A(graph)
    dict["STAT_CC_D"] = STAT_CC_D(graph)
    dict["STAT_CC_A"] = STAT_CC_A(graph)
    dict["STAT_CC_D_An"] = STAT_CC_D_An(graph)
    dict["STAT_CC_A_Ca"] = STAT_CC_A_Ca(graph)
    dict["ABS_f_D"] = ABS_f_D(graph)
    dict["CT_f_conn_D_An"] = CT_f_conn_D_An(graph)
    dict["CT_f_conn_A_Ca"] = CT_f_conn_A_Ca(graph)
    dict["CT_n_D_adj_An"] = CT_n_D_adj_An(graph)
    dict["CT_n_A_adj_Ca"] = CT_n_A_adj_Ca(graph)

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

