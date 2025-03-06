# from py_graspi import igraph_testing as ig
# from py_graspi import descriptors as d
import os
import sys

sys.path.append(os.path.abspath('../src'))
import igraph_testing as ig
import descriptors as d


graph_data = ig.generateGraphAdj(sys.argv[1])

dic = d.descriptors(graph_data, sys.argv[1])

for key, value in dic.items():
    print(key, value)
