import sys

import numpy
from PIL import Image
from numpy.ma.core import asarray

DEBUG = False

def img_to_txt(imageFile, resizeFactor):
    #open image file
    image = Image.open(imageFile)
    #turn image into a numpy Array
    numpyData = asarray(image)

    #initialize x and y axis of image
    dimY = numpyData.shape[0]
    dimX = numpyData.shape[1]

   #resize original image into a new image file
    partOutfile = imageFile[7:-4]
    new_image = image.resize((int(dimX * resizeFactor), int(dimY * resizeFactor)))
    new_image.save(f"resized/resized_{partOutfile}.png")
    image2 = Image.open(f"resized/resized_{partOutfile}.png")
    if DEBUG:
        print(image2.format)
        print(image2.size)
        print(image2.mode)
    #turn new image into an array and find the Rows and Columns of new image
    numpyData2 = asarray(image2)
    dimX = numpyData2.shape[1]
    dimY = numpyData2.shape[0]

    #set up output file for new txt file that will be created from the newly shrunken image
    outfile = f"resized/resized_{partOutfile}.txt"
    file = open(outfile, "w")
    file.write(f"{dimX} {dimY}")

    #loop through newimage array and write out into the new file
    for rows in numpyData2:
        file.write("\n")
        for cols in rows:
            if(cols == True):
                file.write("1 ")
            else:
                file.write("0 ")

    return

def main():
    input_file = sys.argv[1]
    resize_factor = sys.argv[2]
    resize_factor = float(resize_factor)
    img_to_txt(input_file, resize_factor)

if __name__ == "__main__":
    main()