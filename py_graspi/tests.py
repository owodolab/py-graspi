import igraph_testing as ig
import descriptors as ds
import os
import fpdf
import numpy as np
from PIL import Image, ImageOps
import webbrowser
import argparse
import matplotlib.pyplot as plt
import math

current_dir = os.getcwd()
data_path = f"{current_dir}/py_graspi/data/"
descriptors_path = f"{current_dir}/py_graspi/descriptors/"
image_path = f"{current_dir}/py_graspi/images/"
hist_path = f"{current_dir}/py_graspi/histograms/"
results_path = f"{current_dir}/py_graspi/results/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path) if os.path.splitext(file)[0].count("_") == 3]
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
    outline_image = ImageOps.expand(bw_image, border=1, fill="black")
    outline_image.save(image_path + filename + ".png")

def generate_histogram(data, bins, filename, title, labelX, labelY, color):
    plt.hist(data, color=color, bins=bins)
    plt.title(title)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.xticks(ticks=np.arange(start=min(data[0]),
                               step=np.ptp(data[0]) / bins,
                               stop=np.max(data[0]) + 1), rotation=90)
    plt.savefig(hist_path + filename + ".png", format="png")
    plt.close()
    return hist_path + filename + ".png"

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
        pdf.set_font("Arial", size=10)
        print("Generating PDF")

    print("Generating Text Files")

    for test_file in test_files:
        print(f"Executing {test_file}")
        if PDF:
            pdf.add_page()

        g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca = ig.generateGraph(data_path + test_file + ".txt")
        print(f"{test_file} Graph Generated")
        stats = ds.descriptors(g,data_path + test_file + ".txt",black_vertices,white_vertices, black_green,black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca)
        print(f"{test_file} Descriptors Generated")

        if PDF:
            pdf.cell(200, 8, txt=f"Morphology: {test_file}", ln=True, align="L")

        if PDF:
            #pdf.multi_cell(200, 8, txt=f"{stats}", align="L")
            generate_image(test_file)
            image_file = image_path + test_file + ".png"
            pdf.image(image_file, h=15, w=60)

        with open(results_path + "descriptors-" + test_file + ".txt", "w") as txt:
            txt.write(f"Morphology: {test_file}\n")

            #with open(descriptors_path + "descriptors." + test_file + ".log") as f:
                #for line in f:
                    #stat = line.strip().split(" ")
                    #try:
                        #if stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) == int(stat[1]):
                            #txt.write(f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}\n")
                            #if PDF:
                                #pdf.cell(200, 8, txt=f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}", ln=True, align="L")
                        #elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != int(stat[1]):
                            #txt.write(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}\n")
                            #if PDF:
                                #pdf.cell(200, 8, txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}", ln=True, align="L")
                    #except ValueError:
                        #if stats.get(stat[0], -1) != -1 and abs(stats.get(stat[0], -1) - float(stat[1])) < epsilon:
                            #txt.write(f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}\n")
                            #if PDF:
                                #pdf.cell(200, 8, txt=f"{stat[0]} passed - {stats.get(stat[0])} is the same as expected {stat[1]}", ln=True, align="L")
                        #elif stats.get(stat[0], -1) != -1 and stats.get(stat[0], -1) != float(stat[1]):
                            #txt.write(f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}\n")
                            #if PDF:
                                #pdf.cell(200, 8,txt=f"{stat[0]} failed - {stats.get(stat[0])} is not the same as expected {stat[1]}",ln=True, align="L")

            for stat in stats:
                txt.write(f"{stat} {stats[stat]}")
                if PDF:
                    pdf.cell(40, 8, txt=f"{stat} {stats[stat]}", ln=True, align="L")

            print(f"{test_file} Text File Generated")

            if PDF:
                with open(data_path + test_file + "_DistancesWhiteToBlue.txt", "r") as f:
                    data1 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                    hist1 = generate_histogram([data1], 25, test_file + "1", "Distance from A to Ca", "Distance","Instances", "Blue")
                    pdf.image(hist1, x=70, y=0, h=54, w=72)

                with open(data_path + test_file + "_DistanceBlackToRed.txt", "r") as f:
                    data2 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                    hist2 = generate_histogram([data2], 10, test_file + "2", "Distance from D to Am", "Distance","Instances", "Red")
                    pdf.image(hist2, x=140, y=0, h=54, w=72)

                hist3 = generate_histogram([data1, data2], 25, test_file + "3", "Path Balance", "Distance", "Instances",["Blue", "Red"])
                pdf.image(hist3, x=70, y=70, h=54, w=72)

                with open(data_path + test_file + "_DistanceBlackToGreen.txt", "r") as f:
                    data4 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                    hist4 = generate_histogram([data4], 10, test_file + "4", "Distance from D to Int", "Distance","Instances", "Blue")
                    pdf.image(hist4, x=140, y=70, h=54, w=72)

                with open(data_path + test_file + "_TortuosityBlackToRed.txt", "r") as f:
                    data5 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                    hist5 = generate_histogram([data5], 25, test_file + "5", "Tortuosity of D-paths to An", "Tortuosity","Instances", "Red")
                    pdf.image(hist5, x=70, y=140, h=54, w=72)

                with open(data_path + test_file + "_TortuosityWhiteToBlue.txt", "r") as f:
                    data6 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                    hist6 = generate_histogram([data6], 25, test_file + "6", "Tortuosity of A-paths to Ca", "Tortuosity","Instances", "Green")
                    pdf.image(hist6, x=140, y=140, h=54, w=72)

                print(f"{test_file} PDF Generated")


    print("Text Files Generated")

    if PDF:
        pdf.output(f"{current_dir}/py_graspi/test_results.pdf")
        print("PDF Generated")
        webbrowser.open_new_tab(f"{current_dir}/py_graspi/test_results.pdf")

if __name__ == "__main__":
    main()