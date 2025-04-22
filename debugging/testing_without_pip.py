import os
import sys

sys.path.append(os.path.abspath('../src/'))
from py_graspi import graph as ig
from py_graspi import descriptors as ds



filename = "../debugging/debugging-tests/data.txt"

graphData = ig.generateGraph(filename)
descriptors_dict = ds.compute_descriptors(graphData, filename)
ds.descriptorsToTxt(descriptors_dict, "debugging-tests/test_output.txt")
ds.readDescriptorsFromTxt("debugging-tests/test_output.txt")