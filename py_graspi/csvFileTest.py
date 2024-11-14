import igraph_testing as ig
import time
import tracemalloc
import csv
import os

def writeRow(txt):
    row = []
    finalTotal = 0
    total = 0
    g = ig.lattice(txt)
    for i in range(5):
        start = time.time()
        g=ig.lattice(txt)
        total+=time.time()-start
    total = total/5
    finalTotal +=total
    row.append(total)
    total = 0

    g_filtered = ig.filterGraph(g)
    for i in range(5):
        start = time.time()
        g_filtered = ig.filterGraph(g)
        total+=time.time()-start
    total = total / 5
    finalTotal+=total
    row.append(total)
    total = 0

    for i in range(5):
        start = time.time()
        bfs_paths=ig.shortest_path(g_filtered)
        total+=time.time()-start
    total = total / 5
    finalTotal += total
    row.append(total)
    row.append(finalTotal)
    tracemalloc.start()
    g=ig.lattice(txt)
    g_filtered = ig.filterGraph(g)
    bfs_paths=ig.shortest_path(g_filtered)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = stats[1] - stats[0]
    row.append(stats)
    return row

file_exists = os.path.exists('out.csv')
row = writeRow("2D-testFile/testFile-10-2D.txt")
with open('out.csv', mode='a' if file_exists else 'w', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['creation(s)','filtering(s)','bfs(s)','overall runtime(s)','whole memory usage(byte)'])
    writer.writerow(row)