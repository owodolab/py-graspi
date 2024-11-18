import igraph_testing as ig
import descriptors as ds
import os
import fpdf
import numpy as np
from PIL import Image
import webbrowser
import argparse

current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/descriptors/"
image_path = f"{current_dir}/graspi_igraph/images/"
results_path = f"{current_dir}/graspi_igraph/results/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)]
epsilon = 1e-5

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
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_type", choices=["txt", "pdf"])
    args = parser.parse_args()

    if args.file_type == "txt":
        PDF = False
    else:
        PDF = True

    pdf = None

    if PDF:
        pdf = fpdf.FPDF()
        pdf.set_font("Arial", size=12)
        print("Generating PDF")

    print("Generating Text Files")

    for test_file in test_files:
        print(f"Executing {test_file}")
        if PDF:
            pdf.add_page()

        g, is_2D = ig.generateGraph(data_path + test_file + ".txt")
        stats = ds.descriptors(g)

        if PDF:
            pdf.cell(200, 8, txt=f"{test_file} Results", ln=True, align="L")

        with open(results_path + "descriptors-" + test_file + ".txt", "w") as txt:
            txt.write(f"{test_file} Results\n")
            with open(descriptors_path + "descriptors." + test_file + ".log") as f:
                for line in f:
                    stat = line.strip().split(" ")
                    try:
                        if stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) == int(stat[1]):
                            txt.write(f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}\n")
                            if PDF:
                                pdf.cell(200, 8, txt=f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}", ln=True, align="L")
                        elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                            txt.write(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}\n")
                            if PDF:
                                pdf.cell(200, 8, txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}", ln=True, align="L")
                    except ValueError:
                        if stats.get(stat[0], -1) != -1 and abs(stats.get(stat[0], -1) - float(stat[1])) < epsilon:
                            txt.write(f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}\n")
                            if PDF:
                                pdf.cell(200, 8, txt=f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}", ln=True, align="L")
                        elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                            txt.write(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}\n")
                            if PDF:
                                pdf.cell(200, 8,txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}",ln=True, align="L")
            txt.write(f"{stats}\n")

        if PDF:
            pdf.multi_cell(200, 8, txt=f"{stats}", align="L")
            generate_image(test_file)
            image_file = image_path + test_file + ".png"
            pdf.image(image_file)
    print("Text Files Generated")

    if PDF:
        pdf.output(f"{current_dir}/graspi_igraph/test_results.pdf")
        print("PDF Generated")
        webbrowser.open_new_tab(f"{current_dir}/graspi_igraph/test_results.pdf")

if __name__ == "__main__":
    main()