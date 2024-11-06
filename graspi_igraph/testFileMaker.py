import random

def testFileMaker(num, depth, textFileName):
    """
    Creates a text file containing a structured grid of binary values based on the given parameters.

    Args:
        num (int): The number of rows and columns (grid size).
        depth (int): The number of layers to generate.
        textFileName (str): The name of the output text file.

    Returns:
        str: "success" if the file is created successfully.
    """
    # Create the file, raising an error if it already exists.
    f = open(textFileName, "x")

    with open(textFileName, 'a') as f:
        # Write the header with the grid dimensions and depth.
        f.write(f"{num} {num} {depth}\n")

        # Generate the grid for each layer.
        for layer in range(depth):
            for x in range(num):
                for y in range(num - 1):
                    if x < num / 2:
                        f.write("0 ")
                    else:
                        f.write("1 ")

                # Write the final value of each row and move to the next line.
                if x < num / 2:
                    f.write("0\n")
                else:
                    f.write("1\n")

    # Close the file and return success.
    f.close()

    return "success"

def run_test_file_maker():
    testFileMaker(4, 1, "t.txt")

if __name__ == "__main__":
    run_test_file_maker()
