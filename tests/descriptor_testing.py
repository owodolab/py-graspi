import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import src.graph as ig
import src.descriptors as d


graph_data = ig.generateGraphAdj(sys.argv[1])

dic = d.descriptors(graph_data, sys.argv[1])

for key, value in dic.items():
    print(key, value)