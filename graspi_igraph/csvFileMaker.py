from . import igraph_testing as ig
import time 
import tracemalloc
import csv

def functionRuntime(count,function, *argv):
    """
    Measures the average runtime of a function over a specified number of executions.

    Args:
        count (int): The number of times to execute the function.
        function (Callable): The function to measure the runtime for.
        *argv: Arguments to be passed to the function.

    Returns:
        float: The average execution time in seconds across the `count` executions.
    """
    totaltime = 0
    
    for x in range(count):
        startTime = time.time()
        function(*argv)
        endTime = time.time()
        timeTaken = endTime - startTime
        totaltime += timeTaken

    avgExecution = totaltime / count

    return avgExecution

def functionMemory(function, *argv):
    """
    Measures the peak memory usage of a function during its execution.

    Args:
        function (Callable): The function to measure memory usage for.
        *argv: Arguments to be passed to the function.

    Returns:
        int: The memory used in bytes during the function's execution.
    """
    tracemalloc.start()
    function(*argv)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = stats[1] - stats[0]
    
    return stats

def csvMaker(fileName, n, dim, count, graphGen, graphGenPar,graphFilt, graphFiltPar,shortPath, shortPathPar):
    """
    Runs multiple graph-related functions, records their runtime and memory usage,
    and stores the results in a CSV file.

    Args:
        fileName (str): The name of the CSV file to write results to.
        n (int): The base size parameter of the graph.
        dim (int): The dimension to compute the total nodes as n^dim.
        count (int): The number of times to run each function for benchmarking.
        graphGen (Callable): Function to generate a graph.
        graphGenPar (tuple): Parameters for the graph generation function.
        graphFilt (Callable): Function to filter the graph.
        graphFiltPar (tuple): Parameters for the graph filtering function.
        shortPath (Callable): Function to compute the shortest path in the graph.
        shortPathPar (tuple): Parameters for the shortest path function.

    Returns:
        None: The function writes results to the specified CSV file.
    """
    row = [n,(n**dim)]
    totalTime = 0
    totalMem = 0

    graphGenRuntime = functionRuntime(count,graphGen,*graphGenPar)
    graphFiltRuntime = functionRuntime(count,graphFilt,*graphFiltPar)
    shortPathRuntime = functionRuntime(count,shortPath,*shortPathPar)

    totalTime = graphGenRuntime + graphFiltRuntime + shortPathRuntime
    totalTime = round(totalTime,20)
    
    graphGenMem = functionMemory(graphGen,*graphGenPar)
    graphFiltMem = functionMemory(graphFilt,*graphFiltPar)
    shortPathMem = functionMemory(shortPath,*shortPathPar)

    totalMem = graphGenMem + graphFiltMem + shortPathMem
    totalMem = round(totalMem,20)

    row.append(graphGenRuntime)
    row.append(graphFiltRuntime)
    row.append(shortPathRuntime)
    row.append(totalTime)
    row.append(graphGenMem)
    row.append(graphFiltMem)
    row.append(shortPathMem)
    row.append(totalMem)

    with open(fileName, 'a', newline = "\n") as file:
        writer = csv.writer(file)
        writer.writerow(row)
