import igraph_testing as ig
import descriptors as ds
import os

# Define paths to data and descriptors directories
current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/descriptors/"

# Extract the list of test file names without extensions
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]

for test_file in test_files:
    """
    Generates a graph from a test file, calculates its descriptors, and compares them to expected values.

    Each graph's descriptors are validated against a corresponding log file. If any discrepancies are found,
    the test is marked as failed; otherwise, it is marked as passed.
    """
    g = ig.generateGraph(data_path + test_file + ".txt")
    stats = ds.desciptors(g)
    #ig.visual2D(g, 'graph')

    print(f"{test_file} Results")

<<<<<<< Updated upstream
=======
    errorFlag = 0  # Flag to track if any errors are found

    # Open and read the log file containing expected descriptor values
>>>>>>> Stashed changes
    with open(descriptors_path + "descriptors." + test_file + ".log") as f:
        for line in f:
            stat = line.strip().split(" ")

            # Compare calculated descriptors with expected values
            try:
                if stats.get(stat[0], -1) == int(stat[1]):
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
            except ValueError:
                if stats.get(stat[0], -1) == float(stat[1]):
                    print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
<<<<<<< Updated upstream
                    print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
    print(stats)
    print("")
=======
                    errorFlag = 1

    # Print the result of the test based on the error flag
    if errorFlag == 1:
        print(f"{test_file}: failed")
    else:
        print(f"{test_file}: passed")
>>>>>>> Stashed changes
