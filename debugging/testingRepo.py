import py_graspi
from py_graspi import visualize
from py_graspi.graph_data_class import graph_data_class
# from tests.descriptor_testing import graph_data

filename = "../data/data/data_0.5_2.2_001900.txt"
graph_data = py_graspi.generateGraph(filename)
g = graph_data_class(graph_data, True)
print(g)
print(type(g.is_2D))
if True == g.is_2D:
    print("This is what we want")
# exit()

py_graspi.shortest_path_descriptors(g.graph, filename, g.black_interface_red, g.white_interface_blue)
dict_descriptors = py_graspi.descriptors(graph_data, filename)
py_graspi.descriptorsToTxt(dict_descriptors, "debugging-tests/output_descriptors.txt")
py_graspi.visualize(g.graph, g.is_2D)

#should add following read function into descriptors.py
with open('debugging-tests/output_descriptors.txt', 'r') as file:
    content = file.read()
    print(content)

# print(type(g.is_2D))