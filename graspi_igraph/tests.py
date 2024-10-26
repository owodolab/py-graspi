import igraph_testing as ig
import descriptors as ds
import os
import fpdf
import numpy as np
from PIL import Image
import webbrowser

current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/descriptors/"
image_path = f"{current_dir}/graspi_igraph/images/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]

pdf = fpdf.FPDF()
pdf.set_font("Arial", size=12)

def generate_image(filename):
    file_path = data_path + filename + ".txt"
    matrix = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            row = []
            line = line.strip().split(" ")
            for char in line:
                row.append(int(char))
            matrix.append(row)
    matrix_array = np.array(matrix, dtype=np.uint8)
    image = Image.fromarray(matrix_array * 255, mode="L")
    bw_image = image.convert("1")
    bw_image.save(image_path + filename + ".png")

for test_file in test_files:
    pdf.add_page()
    g = ig.generateGraph(data_path + test_file + ".txt")
    stats = ds.desciptors(g)
    #ig.visual2D(g, 'graph')

    pdf.cell(200, 10, txt=f"{test_file} Results", ln=True, align="L")
    #print(f"{test_file} Results")

    with open(descriptors_path + "descriptors." + test_file + ".log") as f:
        for line in f:
            stat = line.strip().split(" ")
            try:
                if stats.get(stat[0], -1) == int(stat[1]):
                    pdf.cell(200, 10, txt=f"{stat[0]} passed", ln=True, align="L")
                    #print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                    pdf.cell(200, 10, txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}", ln=True, align="L")
                    #print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
            except ValueError:
                if stats.get(stat[0], -1) == float(stat[1]):
                    pdf.cell(200, 10, txt=f"{stat[0]} passed", ln=True, align="L")
                    #print(f"{stat[0]} passed")
                elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                    pdf.cell(200, 10,
                             txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}",
                             ln=True, align="L")
                    #print(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}")
    #print(stats)
    #print("")
    pdf.cell(200, 10, txt=f"{stats}", ln=True, align="L")

    generate_image(test_file)
    image_file = image_path + test_file + ".png"
    pdf.image(image_file)

pdf.output("test_results.pdf")
webbrowser.open_new_tab(f"{current_dir}/graspi_igraph/test_results.pdf")
