import igraph_testing as ig
import descriptors as ds
import os

current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/descriptors/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]

for test_file in test_files:
    g = ig.generateGraph(data_path + test_file + ".txt")
    stats = ds.desciptors(g)

    errorFlag = 0
    with open(descriptors_path + "descriptors." + test_file + ".log") as f:
        for line in f:
            stat = line.strip().split(" ")
            try:
                if stats.get(stat[0], -1) == int(stat[1]):
                    continue
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                    errorFlag = 1
            except ValueError:
                if stats.get(stat[0], -1) == float(stat[1]):
                    continue
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                    errorFlag = 1
    if (errorFlag == 1):
        print(f"{test_file}: failed")
    else:
        print(f"{test_file}: passed")
