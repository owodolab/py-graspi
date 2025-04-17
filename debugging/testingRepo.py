import py_graspi
from py_graspi import visualize
from py_graspi.graph_data_class import graph_data_class
# from tests.descriptor_testing import graph_data

filename = "../debugging/debugging-tests/data_4_3.txt"
graph_data = py_graspi.generateGraphAdj(filename)
g = graph_data_class(graph_data, True)

dict_descriptors = py_graspi.descriptors(graph_data, filename)
py_graspi.descriptorsToTxt(dict_descriptors, "debugging-tests/output_descriptors.txt")
py_graspi.visualize(g.graph, True)

#should add following read function into descriptors.py
with open('debugging-tests/output_descriptors.txt', 'r') as file:
    content = file.read()
    print(content)

# print(type(g.is_2D))