import sys
import os
import time
import tracemalloc
sys.path.insert(0, os.path.abspath("../../src"))
from py_graspi import descriptors as ds
from py_graspi import graph as ig
'''
This script generates descriptors for given morphologies and compares against expected value logs with a 0.05 tolerance. 
To use this script from the command line, run 'python descriptor_validator.py all' to test all files in the given data_path against 
all the expected value logs in the given expected_results_path. To run a single test, run 'python descriptor_validator.py [name of file]'. 
For example, to run trial_17, run 'python descriptor_validator.py trial_17'. If no file arguments are provided, the script will default to all. 
'''
def main():
    # Paths
    #targetFileName = 'data_0.5_2.2_001900'
    #data_path = os.path.abspath("../../data/2phase/2D-morphologies/data/")

    # Paths
    data_path = os.path.abspath("test_file")  # Folder containing all .txt test files
    expected_results_path = os.path.abspath("expected_results/")

    # CLI handling
    if len(sys.argv) > 1:
        # user gave: python descriptor_validator.py trial_17
        arg = sys.argv[1]

        if arg.lower() == "all":
            targetFileName = "ALL"
        else:
            targetFileName = arg
    else:
        # default: if no arguments, run all tests
        targetFileName = "ALL"

    loop_cnt = 1  # Number of test repetitions

    # Get all files from preset data_path
    all_files = [
        os.path.splitext(file)[0]
        for file in os.listdir(data_path)
        if file.endswith(".txt")
    ]

    # Choose whether to run all files or a target file based on CLI input
    if targetFileName == "ALL":
        test_files = all_files
    else:
        test_files = [targetFileName]

    tolerance = 0.05

    for test_file in test_files:
        print("Testing " + test_file)
        times = []
        mems = []
        time_mem_stats = {}

        total_graph_time = 0
        for i in range(loop_cnt):
            tracemalloc.start()
            graph_start = time.time()
            file_path = os.path.join(data_path, test_file + ".txt")
            print("Generating graph for " + test_file)
            graph_data = ig.generateGraph(file_path, False) #changed to 3 to signal 3 phase
            _stats = tracemalloc.get_traced_memory()
            graph_end = time.time()
            tracemalloc.stop()
            graph_mem = _stats[1] - _stats[0]
            print("Computing descriptors for " + test_file)
            stats = ds.compute_descriptors(graph_data, file_path, 1,3)  #changed to 3 to signal 3 phase
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
                    if stats.get(stat[0], -1) == int(stat[1]):
                    #if abs(stats.get(stat[0], -1) - float(stat[1])) < tolerance:
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
        print(f"Total time to calculate graph: {graph_time:.2f} second(s)")
        print(f"Total time to calculate descriptors: {descriptor_time:.2f} second(s)")
        print(f"Peak memory usage for graph generation: {graph_mem / (1024 * 1024):.2f} MB")
        print(f"Peak memory usage for descriptor calculation: {descriptor_mem:.2f} MB")
        print(stats)
        print("")
        time_mem_stats[test_file] = {"graph_time": graph_time, "descriptor_time": descriptor_time,
                                     "graph_mem": graph_mem, "descriptor_mem": descriptor_mem}

if __name__ == "__main__":
    main()