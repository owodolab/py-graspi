import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import graph as ig
import descriptors as d


graph_data = ig.generateGraphAdj(sys.argv[1])

descriptors_dict = d.descriptors(graph_data, sys.argv[1])

for key, value in descriptors_dict.items():
    print(key, value)