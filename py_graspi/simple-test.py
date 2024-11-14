from . import igraph_testing as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import descriptors
import sys

def main():

    filename = sys.argv[1]
    # # dimension = sys.argv[2]
    # graph_type = sys.argv[2]
    # functionality = sys.argv[3]

    g,is_2D = ig.generateGraph(filename)
    descript = descriptors.descriptors(g)
    expected = [65536,1634,32713,32823,2,1,1,1,0.499161,0.870266,1.0,512,512]
    i = 0

    for d in descript:
        if descript[d] != expected[i]:
            print(f"The computed descriptors was not what was expected. Failed on Discriptor: {d} Expected: {descript[d]} Computed: {expected[i]} :( ")
            return
        i += 1

    print(f"All the computed descriptors are the same as expected values :) ")
    
    


if __name__ == '__main__':
    main()
    