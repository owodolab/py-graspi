import random

def testFileMaker(num,depth,textFileName):
    f = open(textFileName,"x")

    with open(textFileName,'a') as f:

        f.write(str(num)+" "+str(num)+ " "+str(depth)+"\n")

        for layer in range(depth):
            for x in range(num):
                for y in range((num-1)):
                    if x < num/2:
                        f.write("0" + " ")
                    else:
                        f.write("1" + " ")

                if x < num/2:
                    f.write("0" + "\n")
                else:
                    f.write("1" + "\n")

    f.close()

    return "success"
