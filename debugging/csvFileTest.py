from src import igraph_testing as ig
import time
import tracemalloc
import csv
import os

def writeRow(txt):
    """
    Measures and records the time and memory usage of graph creation, filtering, and pathfinding.

    This function benchmarks the following operations:
    1. Creates a lattice graph.
    2. Filters the graph.
    3. Finds the shortest paths using BFS on the filtered graph.
    Each operation is repeated 5 times, and the average time is recorded.
    Additionally, the memory usage for all operations is measured.

    Args:
        txt (str): The file path to the graph specification used for the lattice generation.

    Returns:
        list: A list containing the following metrics:
            - Average creation time (seconds)
            - Average filtering time (seconds)
            - Average BFS time (seconds)
            - Overall runtime (seconds)
            - Total memory usage (bytes)
    """
    row = []
    finalTotal = 0
    total = 0

    # Create the lattice graph and measure the average creation time
    g = ig.lattice(txt)
    for _ in range(5):
        start = time.time()
        g = ig.lattice(txt)
        total += time.time() - start
    total = total / 5
    finalTotal += total
    row.append(total)
    total = 0

    # Filter the graph and measure the average filtering time
    g_filtered = ig.filterGraph(g)
    for _ in range(5):
        start = time.time()
        g_filtered = ig.filterGraph(g)
        total += time.time() - start
    total = total / 5
    finalTotal += total
    row.append(total)
    total = 0

    # Find the shortest paths using BFS and measure the average time
    for _ in range(5):
        start = time.time()
        bfs_paths = ig.shortest_path(g_filtered)
        total += time.time() - start
    total = total / 5
    finalTotal += total
    row.append(total)

    # Append the total runtime to the row
    row.append(finalTotal)

    # Measure memory usage for all operations
    tracemalloc.start()
    g = ig.lattice(txt)
    g_filtered = ig.filterGraph(g)
    bfs_paths = ig.shortest_path(g_filtered)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_usage = stats[1] - stats[0]
    row.append(memory_usage)

    return row

# Check if the output CSV file already exists
file_exists = os.path.exists('out.csv')

# Write the benchmark results to the CSV file
row = writeRow("2D-testFile/testFile-10-2D.txt")
with open('out.csv', mode='a' if file_exists else 'w', newline='') as file:
    writer = csv.writer(file)

    # If the file doesn't exist, write the header row
    if not file_exists:
        writer.writerow(['creation(s)', 'filtering(s)', 'bfs(s)',
                         'overall runtime(s)', 'whole memory usage(byte)'])

    # Write the data row with the benchmark results
    writer.writerow(row)
