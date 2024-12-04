import sys

import numpy as np


def translate_data(input_file):
    base_filename = input_file[4:-4]
    outputFileName = f"plt/{base_filename}.txt"
    with open(input_file, 'r') as file:
        # Read the file content
        line = file.readline()
        line = file.readline()
        line = line.split()

        #check if 2D of 3D by checking if "Z" exists in the .plt file
        if '"Z"' in line:
            line = file.readline().split()
            numOfVertices = int(line[1][2:-1])
            numOfEdges = int(line[2][2:-1])
            f = str(line[3][2:-1])
            et = str(line[4][3:])
            grid = []
            zCheckgrid = []
            line = file.readline().split()
            zLayer = 0.0
            gridInd = 0
            putIntoZ = True
            z_dim = 1
            for i in range(numOfVertices):
                if (float(line[0]) == 0):
                    grid.append([])
                    zCheckgrid.append([])
                    gridInd += 1
                    if (float(line[2]) != zLayer):
                        # grid.append([])
                        zCheckgrid[gridInd-1].append('\n')
                        z_dim += 1
                        zLayer += 1
                        putIntoZ = False
                numColorOfVertex = int(line[3])
                line = file.readline().split()
                grid[gridInd - 1].append(numColorOfVertex)
                if(putIntoZ):
                    zCheckgrid[gridInd - 1].append(0)
                else:
                    putIntoZ = True
            matrixOfGrid = np.array(grid)
            matrixCheckZ = np.array(zCheckgrid)
            y_dim, x_dim= matrixOfGrid.shape
            y_dim = int(y_dim/z_dim)

            outFile = open(outputFileName, "w")
            outFile.close()
            outFile = open(outputFileName, "a")
            outFile.write(f"{x_dim} {y_dim} {z_dim}")

            # Loop through the matrix
            for i in range(len(grid)):
                outFile.write("\n")
                for j in range(len(grid[i])):
                    # print(f"Element at ({i}, {j}): {grid[i][j]}")
                    if(matrixCheckZ[i][j] == '\n'):
                        outFile.write("\n")
                    outFile.write(f"{grid[i][j]} ")
        else:
            line = file.readline().split()
            numOfVertices = int(line[1][2:-1])
            numOfEdges = int(line[2][2:-1])
            f = str(line[3][2:-1])
            et = str(line[4][3:])
            grid = []
            line = file.readline().split()

            gridInd = 0
            for i in range(numOfVertices):
                if(float(line[0]) == 0):
                    grid.append([])
                    gridInd += 1
                numColorOfVertex = int(line[2])
                line= file.readline().split()
                grid[gridInd-1].append(numColorOfVertex)
            matrixOfGrid = np.array(grid)
            y_dim, x_dim = matrixOfGrid.shape
            outFile = open(outputFileName, "w")
            outFile.close()
            outFile = open(outputFileName, "a")
            outFile.write(f"{x_dim} {y_dim} 0")
            # Loop through the matrix
            for i in range(len(grid)):
                outFile.write("\n")
                for j in range(len(grid[i])):
                    # print(f"Element at ({i}, {j}): {grid[i][j]}")
                    outFile.write(f"{grid[i][j]} ")


# Example usage
# input_file = "plt/5x4x3.plt"  # Replace with your actual input file path
# input_file = "plt/data_4_4.plt"

def main():
    input_file = sys.argv[1]
    translate_data(input_file)

if __name__ == "__main__":
    main()

