# import sys
#
# import igraph_testing as ig
# import seaborn as sns
# import numpy as np
# import matplotlib.pyplot as plt
# from igraph import Graph
# from collections import defaultdict
#
# def find_coords(filename):
#     with open(filename, "r") as file:
#         header = file.readline().split(' ')
#         dimX, dimY = int(header[0]), int(header[1])
#         if len(header) < 3:
#             dimZ = 1
#         else:
#             if int(header[2]) == 0:
#                 dimZ = 1
#             else:
#                 dimZ = int(header[2])
#
#         if dimZ > 1:
#             # dimZ = dimX * dimY
#             is_2d = False
#         coords = [dimX, dimY, dimZ]
#     return coords
#
# def filterGraph(graph):
#     keptEdges = [edge for edge in graph.get_edgelist()
#                  if graph.vs[edge[0]]['color'] == graph.vs[edge[1]]['color']
#                  or 'red' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}
#                  or 'blue' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}]
#
#     return graph.subgraph_edges(keptEdges, delete_vertices=False)
#
#
# def find_tortuosity(g, is_2d, filename):
#     numVertices = g.vcount()
#     redVertex = g.vcount() - 2
#     blackToRedList = []
#     filteredGraph = filterGraph(g)
#     # ig.visualize(filteredGraph, is_2d)
#
#     # Loop through non-meta vertices and find tortuosity based on color
#     for i in range(numVertices - 3):
#         currentVertex = g.vs[i]
#         if currentVertex['color'] == 'black':
#             blackToRedList.append(filteredGraph.get_shortest_path(i, redVertex))
#
#     # print(blackToRedList)
#     #Calculate vertex frequencies
#     vertex_frequency = {i: 0 for i in range(redVertex+1)}
#     # print(vertex_frequency)
#     for path in blackToRedList:
#         for vertex in path:
#             vertex_frequency[vertex] += 1
#
#     vertex_frequency.popitem()
#     vertex_frequency.popitem()
#     # print(vertex_frequency)
#     dimX,dimY,dimZ = coords = find_coords(filename)
#     grid = create_grid(dimX,dimY)
#     # fill_grid_with_dict(grid, vertex_frequency)
#     # print(grid)
#     i = 0
#     for x in range(dimY):
#         for y in range(dimX):
#             grid[x][y] = vertex_frequency[i]
#             i +=1
#     print(grid)
#
#     plt.imshow(grid, cmap="coolwarm", interpolation='nearest')
#     plt.colorbar()
#     plt.title("heatmap")
#     plt.show()
#
#     # testArray = g.shortest_paths()
#     # tortuosityArray = np.array(testArray)
#     # # Create a heatmap using matplotlib
#     # plt.imshow(tortuosityArray, cmap='hot', interpolation='nearest')
#     # plt.colorbar()
#     # plt.title('Shortest Paths Heatmap')
#     # plt.show()
#
#     return g
# '''
#     # Calculate vertex frequencies
#     vertex_frequency = defaultdict(int)
#     for path in blackToRedList:
#         for vertex in path:
#             vertex_frequency[vertex] += 1
#
#     # Get layout coordinates and normalize them
#     layout = g.layout("kk")  # Kamada-Kawai layout for better visualization
#     coords = np.array(layout.coords)
#     min_coords = coords.min(axis=0)
#     max_coords = coords.max(axis=0)
#     norm_coords = (coords - min_coords) / (max_coords - min_coords)
#
#     # Create a heatmap matrix based on vertex frequency
#     resolution = 100  # Increase or decrease this value to adjust granularity
#     heatmap_matrix = np.zeros((resolution, resolution))
#
#     for vertex, freq in vertex_frequency.items():
#         x, y = norm_coords[vertex]
#         x_norm = int(x * (resolution - 1))
#         y_norm = int(y * (resolution - 1))
#         heatmap_matrix[x_norm, y_norm] += freq
#
#     # Plot the heatmap
#     plt.imshow(heatmap_matrix, cmap='hot', interpolation='nearest', origin='lower')
#     plt.colorbar(label='Vertex Frequency')
#     plt.title('Vertex Frequency Heatmap')
#     plt.xlabel('X Coordinates')
#     plt.ylabel('Y Coordinates')
#     plt.show()
#
#     return g
#
# '''
#
# def get_black_nodes(graph):
#     black_nodes = []
#     for node in graph.vs:
#         if node["color"] == "black":
#             black_nodes.append(node)
#     return black_nodes
#
# def create_grid(x_size, y_size):
#     grid = []
#     for y in range(y_size):
#         row = []
#         for x in range(x_size):
#             row.append(0)  # Initialize grid with zeros
#         grid.append(row)
#     return grid

import igraph_testing as ig
import numpy as np
import matplotlib.pyplot as plt
from igraph import Graph
from collections import defaultdict

def find_tortuosity(g, is_2d, filename):
    numVertices = g.vcount()
    redVertex = g.vcount() - 2
    blackToRedList = []
    filteredGraph = filterGraph(g)
    # ig.visualize(filteredGraph, is_2d)

    # Cache to store shortest paths
    shortest_paths_cache = {}

    # Loop through non-meta vertices and find tortuosity based on color
    for i in range(numVertices - 3):
        currentVertex = g.vs[i]
        if currentVertex['color'] == 'black':
            # Check if the red vertex is reachable from the current black node
            if g.are_connected(i, redVertex):
                if i not in shortest_paths_cache:
                    try:
                        path = filteredGraph.get_shortest_path(i, redVertex, output="vpath")
                        shortest_paths_cache[i] = path
                    except Exception as e:
                        print(f"Error finding shortest path from {i} to {redVertex}: {e}")
                blackToRedList.append(shortest_paths_cache[i])

    # Calculate vertex frequencies
    vertex_frequency = {i: 0 for i in range(redVertex + 1)}
    for path in blackToRedList:
        for vertex in path:
            vertex_frequency[vertex] += 1

    vertex_frequency.popitem()
    vertex_frequency.popitem()

    dimX, dimY, dimZ = coords = find_coords(filename)
    grid = create_grid(dimX, dimY)

    i = 0
    for x in range(dimY):
        for y in range(dimX):
            grid[x][y] = vertex_frequency[i]
            i += 1

    plt.imshow(grid, cmap="coolwarm", interpolation='nearest')
    plt.colorbar()
    plt.title("heatmap")
    plt.show()

    return g

def filterGraph(graph):
    keptEdges = [edge for edge in graph.get_edgelist()
                 if graph.vs[edge[0]]['color'] == graph.vs[edge[1]]['color']
                 or 'red' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}
                 or 'blue' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}]
    return graph.subgraph_edges(keptEdges, delete_vertices=False)

def find_coords(filename):
    with open(filename, "r") as file:
        header = file.readline().split(' ')
        dimX, dimY = int(header[0]), int(header[1])
        if len(header) < 3:
            dimZ = 1
        else:
            if int(header[2]) == 0:
                dimZ = 1
            else:
                dimZ = int(header[2])

        if dimZ > 1:
            is_2d = False
        coords = [dimX, dimY, dimZ]
    return coords

def create_grid(x_size, y_size):
    grid = []
    for y in range(y_size):
        row = []
        for x in range(x_size):
            row.append(0)
        grid.append(row)
    return grid
