#!/usr/bin/env python3

from cv2 import cv2
import pytesseract
import sys
import re
import os
import time
import datetime
import statistics


def extractCSV2Graph(samplingIntervalInSeconds, creationTime, inputPath, outputCSVFilename):

    # maximum increase if listener number wrt to total listeners
    maximumListenerIncrease = 1 # 100%


    # start output and write header
    outputFile = open(outputCSVFilename, 'w')
    header = "frame, seconds, minutes, time, listeners\n"
    outputFile.write(header)

    # When was the file recorded?
    print(f"Creation time: {creationDatetime}")

    # setup capture
    vidcap = cv2.VideoCapture(inputPath)

    # get framerate
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print(f"Frame rate: {fps} fps")

    # store previous number of listeners here
    averageNumberOfListeners = 0

    # store results here
    listenerEvolution = []

    # get first frame
    success,frame = vidcap.read()
    framenbr = 0

    # count lines written out to csv file
    csvLineCounter = -1

    while success:

        # next frame
        framenbr += 1

        # get next frame
        success,frame = vidcap.read()
            
        # break if we are at the end
        if not success:
            break

        # update every <samplingIntervalInSeconds>
        if framenbr % int(samplingIntervalInSeconds*fps) == 0:
            
            # update csvLine Counter
            csvLineCounter += 1

            # change to grey scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # resize
            gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

            # text extraction
            data = pytesseract.image_to_string(gray, lang='eng', config='--psm 3').lower()

            # default exaction
            extracted = None

            # split OCR result into lines
            dataLines = data.split('\n')

            # go though each extracted line
            for dataLine in dataLines:

                # search for relevant parts
                extractedGroups = re.findall(r'(\d+k?) (?:others|weitere)', dataLine)

                # if we found something
                if len(extractedGroups) > 0:
                    extracted = extractedGroups[0]
                    break
                else:
                    # go to next line
                    continue

            # skip frame if no data could be found
            if extracted is None:
                    # skip if no result could be found
                    print(f"No extracted data inf frame. Skipping.")
                    continue

            # determine factor - it'S 1000 if there is a 'k' at the end
            factor = 1
            if extracted[-1] == 'k':
                factor = 1000
                extracted = extracted[:-1] # loose last 'k'


            # use last 3 charcters, first one it is interpreted as '4'
            #numberOfListeners = int(extracted[-3:]) * factor
            
            # convert to number of listeners
            numberOfListeners = int(extracted) * factor

            # store in evolution of the listenerEvolution
            listenerEvolution.append(numberOfListeners)

            # keep last 20 values
            if len(listenerEvolution) > 20:
                listenerEvolution = listenerEvolution[-20:]

            
            # median
            median = statistics.median(listenerEvolution)

            # is the increase too large - > ignore, as this is an OCR problem
            if  abs(numberOfListeners - median) > median * maximumListenerIncrease:
                print(f"change in number too large. Skipping")
                print(f"extracted: {extracted}")
                print(f"numberOfListeners: {numberOfListeners}")
                print(f"median: {median}")
                continue

            # relative time
            relTimeSec = framenbr/fps
            relTimeMin = relTimeSec/60

            # absolute time
            frameDatetime = creationDatetime + datetime.timedelta(seconds=relTimeSec)
            frameTimeString = frameDatetime.strftime("%H:%M:%S ")

            # prints als CSV line
            csvLine = f"{framenbr}, {relTimeSec}, {relTimeMin}, {frameTimeString}, {numberOfListeners}"
            print(csvLine)
 
            # store in file
            outputFile.write(csvLine + '\n')
            outputFile.flush()

            # create graph of current csv with gnuplot
            os.system("gnuplot -e \"filename='%s/plot%04d.png'\" plot.gnu" % (graphFolder, csvLineCounter))

if __name__ == '__main__':

    # sampling interval in seconds
    samplingIntervalInSeconds = 1

    # folder, in whoch gnuplot stores all the graphs
    graphFolder = "graphs"

    # movie file is cmdline argument
    inputPath = sys.argv[1]

    # When was the file recorded?
    #creationTime = os.stat(outputPath).st_birthtime
    #creationDatetime = datetime.datetime.fromtimestamp(creationTime)

    # Mac Stay or Leave
    #creationDatetime = datetime.datetime(year=2021, month=10, day=19, hour=13, minute=1, second=19)
    #extractCSV2Graph(samplingIntervalInSeconds, creationDatetime, inputPath, 'data.csv')

    # iPhone DLF
    #creationDatetime = datetime.datetime(year=2021, month=9, day=26, hour=22, minute=47, second=18)
    #extractCSV2Graph(samplingIntervalInSeconds, creationDatetime, inputPath, 'iPhone.csv')

    # Mac DLF
    creationDatetime = datetime.datetime(year=2021, month=11, day=4, hour=12, minute=1, second=2)
    extractCSV2Graph(samplingIntervalInSeconds, creationDatetime, inputPath, 'data.csv')
  