import sys
from logging import DEBUG

from PIL import Image
import numpy as np
DEBUG = False

def img_to_txt(imageFile, resizeFactor, threshold=127.5):
    """
        translates an image to a truncated .txt file
        Args:
            imageFile (string): image file path
            resizeFactor (float): resize factor
            threshold (float): threshold for image conversion
        Returns:
            bool_array: boolean array with true or false of truncated image.
            Read README to find out the path of the new resized .txt file
        """
    # Open image file
    image = Image.open(imageFile).convert('L')  # Convert image to grayscale
    # Turn image into a numpy array
    numpyData = np.asarray(image)

    # Initialize x and y axis of image
    dimY = numpyData.shape[0]
    dimX = numpyData.shape[1]

    # Resize original image into a new image file
    partOutfile = imageFile[7:-4]
    new_image = image.resize((int(dimX * resizeFactor), int(dimY * resizeFactor)))
    new_image.save(f"resized/resized_{partOutfile}_{resizeFactor}x.png")
    image2 = Image.open(f"resized/resized_{partOutfile}_{resizeFactor}x.png").convert('L')
    if DEBUG:
        print(image2.format)
        print(image2.size)
        print(image2.mode)

    # Turn new image into an array and find the Rows and Columns of new image
    numpyData2 = np.asarray(image2)
    dimX = numpyData2.shape[1]
    dimY = numpyData2.shape[0]

    # Convert to boolean numpy array using the threshold
    bool_array = numpyData2 > threshold
    print(bool_array)
    # Set up output file for new txt file that will be created from the newly shrunken image
    outfile = f"resized/resized_{partOutfile}_{resizeFactor}x.txt"
    with open(outfile, "w") as file:
        file.write(f"{dimX} {dimY}\n")

        # Loop through new image array and write out into the new file
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