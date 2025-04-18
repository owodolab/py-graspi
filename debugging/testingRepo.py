import py_graspi
from py_graspi import visualize
from py_graspi.graph_data_class import graph_data_class
# from tests.descriptor_testing import graph_data

# filename = "../data/data/data_0.5_2.2_001900.txt"
filename = "../debugging/debugging-tests/data.txt"
graph_data = py_graspi.generateGraph(filename)
# gr = graph_data_class(graph_data, True)
visualize(graph_data.graph, graph_data.is_2D)
filtered_graph = py_graspi.filterGraph(graph_data.graph)
py_graspi.visualize(filtered_graph, graph_data.is_2D)
dict_descriptors = py_graspi.descriptors(graph_data, filename)
py_graspi.descriptorsToTxt(dict_descriptors, "debugging-tests/output_descriptors.txt")

#should add following read function into descriptors.py
with open('debugging-tests/output_descriptors.txt', 'r') as file:
    content = file.read()
    print(content)

# print(type(g.is_2D))