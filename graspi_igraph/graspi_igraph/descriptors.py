import igraph_testing as ig

def STAT_n(graph):
    return graph.vcount()-3

def STAT_e(graph):
    edgeList = graph.get_edgelist()
    count = 0

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if(graph.vs[currentNode]['color'] == 'green' or graph.vs[toNode]['color'] == 'green'):
            count += 1

    return count

def STAT_n_D(graph):
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'black':
            count += 1
    
    return count

def STAT_n_A(graph):
    vertices = graph.vcount()
    count = 0;

    for vertex in range(vertices):
        if graph.vs[vertex]['color'] == 'white':
            count += 1
    
    return count

def STAT_CC_D(graph):
    cc = ig.connectedComponents(graph);
    count = 0

    for c in cc:
        if graph.vs['color'][c[0]] == "black":
            count += 1

    return count

def STAT_CC_A(graph):
    cc = ig.connectedComponents(graph);
    count = 0

    for c in cc:
        if graph.vs['color'][c[0]] == "white":
            count += 1

    return count
    
def STAT_CC_D_An(graph):
    cc = ig.connectedComponents(graph);
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'black':
            count += 1
    
    return count

def STAT_CC_A_Ca(graph):
    cc = ig.connectedComponents(graph);
    count = 0;

    for c in cc:
        if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
            count += 1
    
    return count

def ABS_f_D(graph):
    fraction = STAT_n_D(graph) / STAT_n(graph)

    return fraction

def CT_f_conn_D_An(graph):
    fraction = CT_n_D_adj_An(graph) / STAT_n_D(graph)
 
    return fraction

def CT_f_conn_A_Ca(graph):
    fraction = CT_n_A_adj_Ca(graph)/ STAT_n_A(graph)

    return fraction

def CT_n_D_adj_An(graph):
    cc = ig.connectedComponents(graph);
    count = 0
    
    if cc is not None:
        for c in cc:
            if graph.vs[c][0]['color'] == 'black' and 'red' in graph.vs[c]['color']:
                for vertex in c:
                    if graph.vs[vertex]['color'] == 'black':
                        count += 1

    return count

def CT_n_A_adj_Ca(graph):
    cc = ig.connectedComponents(graph);
    count = 0

    if cc is not None:
        for c in cc:
            if graph.vs[c][0]['color'] == 'white' and 'blue' in graph.vs[c]['color']:
                for vertex in c:
                    if graph.vs[vertex]['color'] == 'white':
                        count += 1

    return count

def desciptors(graph):
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
    print(dict)

    return dict


def descriptorsToTxt(dict, fileName):

    f = open(fileName,"x")

    with open(fileName,'a') as f:
        for d in dict:
            f.write(d + " " + str(dict[d]) + '\n')
