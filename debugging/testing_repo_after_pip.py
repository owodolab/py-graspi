from py_graspi import graph as ig
from py_graspi import descriptors as ds

# filename = "../data/data/data_0.5_2.2_001900.txt"
filename = "../debugging/debugging-tests/data.txt"
graph_data = py_graspi.generateGraph(filename)
ig.visualize(graph_data.graph, graph_data.is_2D)
filtered_graph = ig.filterGraph(graph_data.graph)
py_graspi.visualize(filtered_graph, graph_data.is_2D)
dict_descriptors = ds.compute_descriptors(graph_data, filename)
ds.descriptorsToTxt(dict_descriptors, "debugging-tests/output_descriptors.txt")

#should add following read function into descriptors.py
with open('debugging-tests/output_descriptors.txt', 'r') as file:
    content = file.read()
    print(content)

# print(type(g.is_2D))