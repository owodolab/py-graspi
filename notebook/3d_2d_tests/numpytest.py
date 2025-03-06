import numpy as np
import os

current_dir = os.getcwd()
fileName = f"{current_dir}/graspi_igraph/data/testFile-100-2D.txt"
with open(fileName, "r") as file:
    header = file.readline().split(' ')
    dimX, dimY = int(header[0]), int(header[1])
    dim = dimY
    array = np.loadtxt(fileName, skiprows=1)
    print(len(array))
    print(len(array[0]))
print(array) 