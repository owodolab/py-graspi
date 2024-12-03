import sys
import numpy as np
import matplotlib.pyplot as plt
import igraph_testing as ig
import os

current_dir = os.getcwd()

def find_coords(filename):
    with open(f"{current_dir}/py_graspi/data/{filename}", "r") as file:
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


def find_BTR_tortuosity(g, is_2d, filename, output, title):
    numVertices = g.vcount()
    redVertex = g.vcount() - 2
    blackToRedList = []
    filteredGraph = filterGraph(g)
    idOfPixelIn1DArray, tort = read_BTR_file_and_extract_numbers(filename)
    #Calculate vertex frequencies
    vertex_frequency = [0] * numVertices
    for i in range(len(idOfPixelIn1DArray)):
        vertex_frequency[idOfPixelIn1DArray[i]] = tort[i]

    vertex_frequency = vertex_frequency[:-3]
    dimX,dimY,dimZ = coords = find_coords(filename)
    data_2d = np.array(vertex_frequency).reshape(dimY, dimX)

    # Create the heatmap
    plt.rcParams.update({'font.size': 20})
    plt.title("Black to Red Tortuosity HeatMap")
    plt.imshow(data_2d, cmap='hot', interpolation='nearest')
    plt.colorbar()  # Add a colorbar to show the values
    plt.title(title, y=2, fontsize=20)
    plt.savefig(output)
    plt.close()

def find_WTB_tortuosity(g, is_2d, filename, output, title):
    numVertices = g.vcount()
    blueVertex = g.vcount() - 1
    whiteToBlueList = []
    filteredGraph = filterGraph(g)
    idOfPixelIn1DArray, tort = read_WTB_file_and_extract_numbers(filename)
    #Calculate vertex frequencies
    vertex_frequency = [0] * numVertices
    for i in range(len(idOfPixelIn1DArray)):
        vertex_frequency[idOfPixelIn1DArray[i]] = tort[i]

    vertex_frequency = vertex_frequency[:-3]
    dimX,dimY,dimZ = coords = find_coords(filename)
    data_2d = np.array(vertex_frequency).reshape(dimY, dimX)

    # Create the heatmap
    plt.rcParams.update({'font.size': 20})
    plt.title("White to Blue Tortuosity HeatMap")
    plt.imshow(data_2d, cmap='hot', interpolation='nearest')
    plt.colorbar()  # Add a colorbar to show the values
    plt.title(title, y=2, fontsize=20)
    plt.savefig(output)
    plt.close()

# Define the function to read the file and extract the numbers
def read_BTR_file_and_extract_numbers(base_filename):
    base_filename = base_filename[5:-4]
    file_path = f"{current_dir}/py_graspi/data/data_{base_filename}_IdTortuosityBlackToRed.txt"
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

def read_WTB_file_and_extract_numbers(base_filename):
    base_filename = base_filename[5:-4]
    file_path = f"{current_dir}/py_graspi/data/data_{base_filename}_IdTortuosityWhiteToBlue.txt"
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