import sys

from numpy.matlib import empty
from seaborn import heatmap

import igraph_testing as ig
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from igraph import Graph
from collections import defaultdict

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
            # dimZ = dimX * dimY
            is_2d = False
        coords = [dimX, dimY, dimZ]
    return coords

def filterGraph(graph):
    keptEdges = [edge for edge in graph.get_edgelist()
                 if graph.vs[edge[0]]['color'] == graph.vs[edge[1]]['color']
                 or 'red' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}
                 or 'blue' in {graph.vs[edge[0]]['color'], graph.vs[edge[1]]['color']}]

    return graph.subgraph_edges(keptEdges, delete_vertices=False)


def find_tortuosity(g, is_2d, filename):
    numVertices = g.vcount()
    redVertex = g.vcount() - 2
    blackToRedList = []
    filteredGraph = filterGraph(g)
    # ig.visualize(filteredGraph, is_2d)
    idOfPixelIn1DArray, tort = read_file_and_extract_numbers(filename)
    # # Loop through non-meta vertices and find tortuosity based on color
    # for i in range(numVertices - 3):
    #     currentVertex = g.vs[i]
    #     if currentVertex['color'] == 'black':
    #         blackToRedList.append(filteredGraph.get_shortest_path(i, redVertex))


    # print(blackToRedList)
    #Calculate vertex frequencies
    vertex_frequency = [0] * numVertices
    for i in range(len(idOfPixelIn1DArray)):
        vertex_frequency[idOfPixelIn1DArray[i]] = tort[i]


    # for path in blackToRedList:
    #     for vertex in path:
    #         vertex_frequency[vertex] += 1
    # print(vertex_frequency)
    #
    # # Remove the last three entries
    # vertex_frequency = vertex_frequency[:-3]
    vertex_frequency = vertex_frequency[:-3]
    dimX,dimY,dimZ = coords = find_coords(filename)
    # Reshape the 1D array back into a 2D array
    # You'll need to know the original shape (e.g., 3x3)
    data_2d = np.array(vertex_frequency).reshape(dimY, dimX)

    # Create the heatmap
    plt.imshow(data_2d, cmap='hot', interpolation='nearest')
    plt.colorbar()  # Add a colorbar to show the values
    plt.show()

# Define the function to read the file and extract the numbers
def read_file_and_extract_numbers(base_filename):
    base_filename = base_filename[5:-4]
    file_path = f"distances/{base_filename}-IdTortuosityBlackToRed.txt"
    idOfPixelIn1DArray = []
    tort = []

    # Open the file in read mode
    with open(file_path, "r") as file:
        # Read each line in the file
        for line in file:
            # Split the line into a list of strings
            parts = line.split()
            # Extract the first and second numbers and convert them to appropriate types
            first_number = int(parts[0])
            second_number = float(parts[1])
            # Append the numbers to their respective lists
            idOfPixelIn1DArray.append(first_number)
            tort.append(second_number)

    return idOfPixelIn1DArray, tort

