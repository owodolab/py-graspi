import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/py_graspi")))
import graph as ig
import descriptors as d

graph_data = ig.generateGraphAdj(sys.argv[1])

dic = d.compute_descriptors(graph_data, sys.argv[1],float(sys.argv[2]))

for key, value in dic.items():
    print(key, value)