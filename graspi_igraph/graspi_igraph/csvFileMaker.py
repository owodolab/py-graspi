from . import igraph_testing as ig
import time 
import tracemalloc
import csv

def functionRuntime(count,function, *argv):
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
    tracemalloc.start()
    function(*argv)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = stats[1] - stats[0]
    
    return stats

def csvMaker(fileName, n, dim, count, graphGen, graphGenPar,graphFilt, graphFiltPar,shortPath, shortPathPar):
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

# fileName = "2D-testFile/testFile-10-2D.txt"
# g = ig.generateGraph(fileName)
# fg = ig.filterGraph(g)

# csvMaker("out.csv",10,2,3,ig.generateGraph,[fileName],ig.filterGraph,[g],ig.shortest_path,[fg]);

# fileName = "2D-testFile/testFile-50-2D.txt"
# g = ig.generateGraph(fileName)
# fg = ig.filterGraph(g)

# csvMaker("out.csv",50,2,3,ig.generateGraph,[fileName],ig.filterGraph,[g],ig.shortest_path,[fg]);

# fileName = "2D-testFile/testFile-100-2D.txt"
# g = ig.generateGraph(fileName)
# fg = ig.filterGraph(g)

# csvMaker("out.csv",100,2,3,ig.generateGraph,[fileName],ig.filterGraph,[g],ig.shortest_path,[fg]);

# fileName = "2D-testFile/testFile-500-2D.txt"
# g = ig.generateGraph(fileName)
# fg = ig.filterGraph(g)

# csvMaker("out.csv",500,2,3,ig.generateGraph,[fileName],ig.filterGraph,[g],ig.shortest_path,[fg]);

# fileName = "2D-testFile/testFile-1000-2D.txt"
# g = ig.generateGraph(fileName)
# fg = ig.filterGraph(g)

# csvMaker("out.csv",1000,2,3,ig.generateGraph,[fileName],ig.filterGraph,[g],ig.shortest_path,[fg]);