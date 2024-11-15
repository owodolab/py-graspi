import igraph_testing as ig
import descriptors as ds
import os
import fpdf
import numpy as np
from PIL import Image, ImageOps
import webbrowser
import argparse
import matplotlib.pyplot as plt

current_dir = os.getcwd()
data_path = f"{current_dir}/graspi_igraph/data/"
descriptors_path = f"{current_dir}/graspi_igraph/descriptors/"
image_path = f"{current_dir}/graspi_igraph/images/"
hist_path = f"{current_dir}/graspi_igraph/histograms/"
results_path = f"{current_dir}/graspi_igraph/results/"
test_files = [os.path.splitext(file)[0] for file in os.listdir(data_path)][:1]
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

def generate_histogram(data, filename, title, labelX, labelY, color):
    plt.hist(data, color=color)
    plt.title(title)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.savefig(hist_path + filename + ".png", format="png")
    plt.close()
    return hist_path + filename + ".png"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_type", choices=["txt", "pdf"])
    parser.add_argument("--testing", default="output", required=False)
    args = parser.parse_args()

    if args.file_type == "txt":
        PDF = False
    else:
        PDF = True

    if args.testing == "test":
        TEST = True
    else:
        TEST = False

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

        g, is_2D = ig.generateGraph(data_path + test_file + ".txt")
        stats = ds.descriptors(g)

        if PDF:
            pdf.cell(200, 8, txt=f"Morphology: {test_file}", ln=True, align="L")

        if PDF:
            #pdf.multi_cell(200, 8, txt=f"{stats}", align="L")
            generate_image(test_file)
            image_file = image_path + test_file + ".png"
            pdf.image(image_file, h=15, w=60)

        with open(results_path + "descriptors-" + test_file + ".txt", "w") as txt:
            txt.write(f"Morphology: {test_file}\n")
            if TEST:
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
            else:
                for stat in stats:
                    txt.write(f"{stat} {stats[stat]}")
                    if PDF:
                        pdf.cell(40, 8, txt=f"{stat} {stats[stat]}", ln=True, align="L")

                if PDF:
                    data1 = [0,0,0,1,1,1,2,2,2,3,3,3,4,4,4]
                    hist1 = generate_histogram(data1, test_file+"1", "Placeholder", "Placeholder", "Placeholder", "Blue")
                    pdf.image(hist1, x=70, y=0, h=54, w=72)

                    data2 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
                    hist2 = generate_histogram(data2, test_file + "2", "Placeholder", "Placeholder", "Placeholder","Red")
                    pdf.image(hist2, x=140, y=0, h=54, w=72)

                    data3 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
                    hist3 = generate_histogram(data3, test_file + "3", "Placeholder", "Placeholder", "Placeholder","Green")
                    pdf.image(hist3, x=70, y=50, h=54, w=72)

                    data4 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
                    hist4 = generate_histogram(data4, test_file + "4", "Placeholder", "Placeholder", "Placeholder","Blue")
                    pdf.image(hist4, x=140, y=50, h=54, w=72)

                    data5 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
                    hist5 = generate_histogram(data5, test_file + "5", "Placeholder", "Placeholder", "Placeholder","Red")
                    pdf.image(hist5, x=70, y=100, h=54, w=72)

                    data6 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
                    hist6 = generate_histogram(data6, test_file + "6", "Placeholder", "Placeholder", "Placeholder","Green")
                    pdf.image(hist6, x=140, y=100, h=54, w=72)


    print("Text Files Generated")

    if PDF:
        pdf.output(f"{current_dir}/graspi_igraph/test_results.pdf")
        print("PDF Generated")
        webbrowser.open_new_tab(f"{current_dir}/graspi_igraph/test_results.pdf")

if __name__ == "__main__":
    main()