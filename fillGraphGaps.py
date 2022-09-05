import glob
import config
import os
import shutil

def fill():

    fileList = glob.glob(f"{config.graphFolder}/*.png")
    fileList.sort()

    expectedIndex = 0

    for filename in fileList:
        index = int(filename[-8:-4])
        dirname =  os.path.dirname(filename)
        basename = os.path.basename(filename)

        print(filename, index, dirname, basename)

        if index == expectedIndex:
            lastValidFilename = filename

        else:

            # do we miss a file?
            while index != expectedIndex:

                newBasename = "plot%04d" % expectedIndex
                newFilename = os.path.join(dirname, newBasename + '.png')

                print(f"Copying {lastValidFilename} -> {newFilename}")
                shutil.copyfile(lastValidFilename, newFilename)
                expectedIndex += 1

        expectedIndex += 1


if __name__ == '__main__':
    fill()
