import igraph_testing as ig
import descriptors as ds
import os
import fpdf
import numpy as np
from PIL import Image
import webbrowser
import argparse

current_dir = os.getcwd()
data_path = f"{current_dir}/py_graspi/data/"
descriptors_path = f"{current_dir}/py_graspi/descriptors/"
expected_distances_path = f"{current_dir}/py_graspi/distances/"
results_path = f"{current_dir}/py_graspi/comparisons/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path) if os.path.splitext(file)[0].count("_") > 3]
epsilon = 1e-5


def file_checker(file1, file2, is_idTor):
    idTor_comparison = []
    distance_comparison = []

    with open(file1,'r') as f1, open(file2, 'r') as f2:
        f1_line = f1.readline()
        f2_line = f2.readline()

        f1_line = f1_line.split()
        f2_line = f2_line.split()

        for x in range(len(f1_line)):
            if is_idTor == True:
                if float(f1_line[0]) == float(f2_line[0]):
                    if abs(float(f1_line[-1]) - float(f2_line[-1])) > epsilon or abs(float(f2_line[-2]) - float(f1_line[-2])) > epsilon or abs(float(f2_line[1]) - float(f1_line[1])) > epsilon:
                        idTor_comparison.append(f'{float(f1_line[0])} Expected: {float(f1_line[1])} {float(f1_line[-2])} {float(f1_line[-1])} Actual: {float(f2_line[1])} {float(f2_line[-2])} {float(f2_line[-1])}\n')
        
            else:
                if abs(float(f1_line[0]) - float(f2_line[0])) > epsilon: 
                    distance_comparison.append(f'Line: {x+1} Expected: {float(f1_line[0])} Actual: {float(f2_line[0])}\n')

        
    # filename = file2.split('_',-1)
    filename = file1.rsplit('.',1)[0]
    filename = filename.rsplit('/',1)[1]


    if len(idTor_comparison) != 0 or len(distance_comparison) != 0:
    
        file = open(f"{results_path + filename}_comparison.txt",'w')
        if len(idTor_comparison) != 0:
            file.writelines(idTor_comparison)
        else:
            file.writelines(distance_comparison)
        file.close()


def main():
    for test_file in test_files:
        filename, distanceType = test_file.rsplit('_',1)
        expectedFile = data_path + test_file + ".txt"
        file = f'{expected_distances_path + filename}-{distanceType}.txt' 
        is_idTor = (distanceType[:2] == 'Id')

        file_checker(expectedFile, file, is_idTor)


if __name__ == '__main__':
    main()