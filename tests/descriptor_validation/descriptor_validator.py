import sys
import os
import time
import tracemalloc
sys.path.insert(0, os.path.abspath("../../src"))
from py_graspi import descriptors as ds
from py_graspi import graph as ig

def main():
    #Preferences

    targetFileName = 'data_0.5_2.2_001900' # Input file name or naming pattern to search for here
    loop_cnt = 1 # Number of test repetitions

    #Paths
    data_path = os.path.abspath("../../data/2phase/2D-morphologies/data/")  # Adjust data path as necessary
    expected_results_path = os.path.abspath("expected_results/")  # Adjust expected results path as necessary
    test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]

    tolerance = 0.005
    times = []
    mems = []
    time_mem_stats = {}

    for test_file in test_files:
        if targetFileName not in test_file:
            continue
        total_graph_time = 0
        for i in range(loop_cnt):
            tracemalloc.start()
            graph_start = time.time()
            file_path = os.path.join(data_path, test_file + ".txt")
            graph_data = ig.generateGraph(file_path, False)
            _stats = tracemalloc.get_traced_memory()
            graph_end = time.time()
            tracemalloc.stop()
            graph_mem = _stats[1] - _stats[0]
            stats = ds.compute_descriptors(graph_data, file_path)
            total_graph_time += graph_end - graph_start

        print(f"\n{test_file} Results")

        expected_log = os.path.join(expected_results_path, f"{test_file}.log")
        if not os.path.exists(expected_log):
            print(f"Expected result log file not found: {expected_log}")
            continue

        with open(expected_log) as f:
            for line in f:
                stat = line.strip().split(" ")
                try:
                    #if stats.get(stat[0], -1) == int(stat[1]):
                    if abs(stats.get(stat[0], -1) - float(stat[1])) < tolerance:
                        print(f"{stat[0]} passed")
                    elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                        print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
                except ValueError:
                    if abs(stats.get(stat[0], -1) - float(stat[1])) < tolerance:
                        print(f"{stat[0]} passed")
                    elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                        print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
        descriptor_time = stats["time_in_seconds"]
        descriptor_mem = stats["mem_in_mb"]

        times.append(descriptor_time)
        mems.append(descriptor_mem)

        graph_time = total_graph_time / loop_cnt
        print(f"Total time to calculate graph: {graph_time} second(s)")
        print(f"Total time to calculate descriptors: {descriptor_time} second(s)")
        print(f"Peak memory usage for graph generation: {graph_mem} mega bytes")
        print(f"Peak memory usage for descriptor calculation: {descriptor_mem} mega bytes")
        print(stats)
        print("")
        time_mem_stats[test_file] = {"graph_time": graph_time, "descriptor_time": descriptor_time,
                                     "graph_mem": graph_mem, "descriptor_mem": descriptor_mem}

if __name__ == "__main__":
    main()