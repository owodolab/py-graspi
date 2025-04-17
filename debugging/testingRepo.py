import py_graspi

filename = "../debugging/debugging-tests/data_4_3.txt"
graph_data = py_graspi.generateGraph(filename)
dict_descriptors = py_graspi.descriptors(graph_data, filename)
py_graspi.descriptorsToTxt(dict_descriptors, "debugging-tests/output_descriptors.txt")

#should add following read function into descriptors.py
with open('debugging-tests/output_descriptors.txt', 'r') as file:
    content = file.read()
    print(content)