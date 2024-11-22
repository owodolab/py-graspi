import combined_with as ig
import new_descriptors as ds
import os
import time

current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/p1descriptors/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]
epsilon=1e-5
for test_file in test_files:
    if 'morph' not in test_file:
        continue
    if '2x' not in test_file:
        continue
    # g = ig.generateGraph(data_path + test_file + ".txt")
    import time
    graph_start = time.time()
    g,is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca= ig.generateGraph(data_path + test_file + ".txt")
    graph_end = time.time()
    stats = ds.descriptors(g, test_file, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca)
    #ig.visual2D(g, 'graph')

    print(f"{test_file} Results")

    with open(descriptors_path + "p1descriptors." + test_file + ".log") as f:
        for line in f:
            stat = line.strip().split(" ")
            try:
                # if stats.get(stat[0], -1) == int(stat[1]):
                if abs(stats.get(stat[0], -1) - float(stat[1])) < epsilon:
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
            except ValueError:
                if abs(stats.get(stat[0], -1) - float(stat[1])) < epsilon:
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
    time = stats["time"]
    mem = stats["mem"]
    graph_time = graph_end-graph_start
    print(f"Total time to calculate graph: {graph_time} second(s)")
    print(f"Total time to calculate descriptors: {time} second(s)")
    print(f"Peak memory usage for descriptor calculation: {mem} bytes")
    print(stats)
    print("")