import sys
from logging import DEBUG

from PIL import Image
import numpy as np
DEBUG = False

def img_to_txt(imageFile, resizeFactor, threshold=127.5):
    """
    Converts an image file into a .txt file, dimensions are multiplied by resizeFactor.

    Args:
        imageFile (string): path of the image file.
        resizeFactor (float): resizeFactor used to multiply X and Y dimensions of imageFile to either truncate or enlarge.
        threshold (float): threshold used for deciding color intensity of what is considered white or black in numpy array of image

    Returns:
        bool_array (numpy Array): numpy array of boolean array which signal if index should be black or white.
        *not really needed is used in function to convert and output resized .txt file of image into the resized directory.
    """
    # Open image file
    image = Image.open(imageFile).convert('L')  # Convert image to grayscale
    numpyData = np.asarray(image)

    dimY = numpyData.shape[0]
    dimX = numpyData.shape[1]

    # Extract base file name from the image path
    partOutfile = imageFile.split("/")[-1].split(".")[0]  # Get filename without extension

    # Resize original image
    new_image = image.resize((int(dimX * resizeFactor), int(dimY * resizeFactor)))
    new_image.save(f"{partOutfile}.png")  # Save resized image with correct name

    image2 = Image.open(f"{partOutfile}.png").convert('L')

    # Process resized image into numpy array
    numpyData2 = np.asarray(image2)
    dimX = numpyData2.shape[1]
    dimY = numpyData2.shape[0]

    # Convert to boolean numpy array using the threshold
    bool_array = numpyData2 > threshold
    print(bool_array)

    # Save the array as a text file
    outfile = f"{partOutfile}.txt"
    with open(outfile, "w") as file:
        file.write(f"{dimX} {dimY}\n")
        for row in bool_array:
            file.write(" ".join(['1' if col else '0' for col in row]) + "\n")

    return bool_array


def main():
    input_file = sys.argv[1]
    resize_factor = sys.argv[2]
    resize_factor = float(resize_factor)
    img_to_txt(input_file, resize_factor)

if __name__ == "__main__":
    main()