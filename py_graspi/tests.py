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
import tortuosity_histogram as t

current_dir = os.getcwd()
data_path = f"{current_dir}/py_graspi/data/"
descriptors_path = f"{current_dir}/py_graspi/descriptors/"
image_path = f"{current_dir}/py_graspi/images/"
hist_path = f"{current_dir}/py_graspi/histograms/"
results_path = f"{current_dir}/py_graspi/results/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path) if os.path.splitext(file)[0].count("_") == 3]
epsilon = 1e-5

"""
Generates the black and white images of each morphology.
"""
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

"""
Generates the histograms of each descriptor data for distances and tortuosity.
"""
def generate_histogram(data, bins, filename, title, labelX, labelY, color, start, step, stop):
    if title == "Path Balance":
        plt.hist(data, color=color, bins=bins, label=["White pixels to bottom","Black pixels to top"])
        plt.legend(fontsize=20)
    else:
        plt.hist(data, color=color, bins=bins)
    plt.title(title, fontsize=20)
    plt.xlabel(labelX, fontsize=20)
    plt.ylabel(labelY, fontsize=20)
    plt.xlim(start, stop)
    plt.xticks(ticks=np.arange(start=start, step=step, stop=stop), rotation=90, fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig(hist_path + filename + ".png", format="png")
    plt.close()
    return hist_path + filename + ".png"

"""
Main function that generates the txt and pdf files of the report.
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_type", choices=["txt", "pdf"])
    args = parser.parse_args()

    """
    Checks if the user wants to generate the txt files or the pdf.
    """
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

    """
    Generates the txt files and pdf for each of the 33 morphology descriptors.
    """
    for test_file in test_files:
        print(f"Executing {test_file}")
        if PDF:
            pdf.add_page()

        if PDF:
            pdf.cell(200, 8, txt=f"Morphology: {test_file}", ln=True, align="L")

        if PDF:
            generate_image(test_file)
            image_file = image_path + test_file + ".png"
            pdf.image(image_file, h=15, w=60)

        """
        Generates the graph for each of the morphology descriptors
        """
        g, is_2D, black_vertices, white_vertices, black_green, black_interface_red, white_interface_blue, dim, interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca = ig.generateGraph(
            data_path + test_file + ".txt")
        print(f"{test_file} Graph Generated")

        """
        Checks if txt files already exists. 
        If they exist and the user requests the pdf, it will only regenerate the pdf.
        txt must be selected to regenerate the txt files.
        """
        if os.path.exists(results_path + "descriptors-" + test_file + ".txt") and PDF:
            with open(results_path + "descriptors-" + test_file + ".txt", "r") as txt:
                next(txt)
                for line in txt.readlines():
                    pdf.cell(40, 8, txt=line, ln=True, align="L")
        else:
            stats = ds.descriptors(g, data_path + test_file + ".txt", black_vertices, white_vertices, black_green,
                                   black_interface_red, white_interface_blue, dim, interface_edge_comp_paths,
                                   shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca)
            print(f"{test_file} Descriptors Generated")
            with open(results_path + "descriptors-" + test_file + ".txt", "w") as txt:
                txt.write(f"Morphology: {test_file}\n")

                for stat in stats:
                    txt.write(f"{stat} {stats[stat]}\n")
                    if PDF:
                        pdf.cell(40, 8, txt=f"{stat} {stats[stat]}", ln=True, align="L")

                print(f"{test_file} Text File Generated")

        """
        Generates and adds in the descriptor histograms to the pdf
        """
        if PDF:
            with open(data_path + test_file + "_DistancesWhiteToBlue.txt", "r") as f:
                data1 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                hist1 = generate_histogram([data1], 25, test_file + "1", "Distance from A to Ca", "Distance","Instances", "Blue", 0, 50, 250)
                pdf.image(hist1, x=80, y=10, w=60)

            with open(data_path + test_file + "_DistanceBlackToRed.txt", "r") as f:
                data2 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                hist2 = generate_histogram([data2], 20, test_file + "2", "Distance from D to Am", "Distance","Instances", "Red", 0, 20, 200)
                pdf.image(hist2, x=142, y=10, w=60)

            hist3 = generate_histogram([data1, data2], 25, test_file + "3", "Path Balance", "Distance", "Instances",["Blue", "Red"], 0, 50, 250)
            pdf.image(hist3, x=80, y=60, w=60)

            with open(data_path + test_file + "_DistanceBlackToGreen.txt", "r") as f:
                data4 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                hist4 = generate_histogram([data4], 12, test_file + "4", "Distance from D to Int", "Distance","Instances", "Green", 0, 10, 60)
                pdf.image(hist4, x=142, y=60, w=60)

            with open(data_path + test_file + "_TortuosityBlackToRed.txt", "r") as f:
                data5 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                hist5 = generate_histogram([data5], 25, test_file + "5", "Tortuosity of D-paths to An", "Tortuosity","Instances", "Red", 1, 0.1, 1.5)
                pdf.image(hist5, x=80, y=110, w=60)

            with open(data_path + test_file + "_TortuosityWhiteToBlue.txt", "r") as f:
                data6 = [float(line.strip()) for line in f if not math.isinf(float(line.strip()))]
                hist6 = generate_histogram([data6], 25, test_file + "6", "Tortuosity of A-paths to Ca", "Tortuosity","Instances", "Blue", 1, 0.1, 1.5)
                pdf.image(hist6, x=142, y=110, w=60)

            """
            Generates the heat map of tortuosity between black and red, and white to blue
            """
            heat1 = t.find_BTR_tortuosity(g, is_2D, test_file + ".txt", hist_path + test_file + "7.png", "Tortuosity of D-paths to An")
            pdf.image(hist_path + test_file + "7.png", x=80, y=160, w=60)

            heat2 = t.find_WTB_tortuosity(g, is_2D, test_file + ".txt", hist_path + test_file + "8.png","Tortuosity of A-paths to Ca")
            pdf.image(hist_path + test_file + "8.png", x=142, y=160, w=60)


            print(f"{test_file} PDF Generated")


    print("Text Files Generated")

    """
    Outputs the generated pdf to the user.
    """
    if PDF:
        pdf.output(f"{current_dir}/py_graspi/test_results.pdf")
        print("PDF Generated")
        webbrowser.open_new_tab(f"{current_dir}/py_graspi/test_results.pdf")

if __name__ == "__main__":
    main()