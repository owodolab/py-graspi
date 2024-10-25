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
    #ig.visual2D(g, 'graph')

    print(f"{test_file} Results")

    with open(descriptors_path + "descriptors." + test_file + ".log") as f:
        for line in f:
            stat = line.strip().split(" ")
            try:
                if stats.get(stat[0], -1) == int(stat[1]):
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
            except ValueError:
                if stats.get(stat[0], -1) == float(stat[1]):
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
    print(stats)
    print("")
