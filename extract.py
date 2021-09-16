#!/usr/bin/env python3

from cv2 import cv2
import pytesseract
import sys
import re
import os
import time
import datetime
import statistics

# maximum increase if listener number wrt to total listeners
maximumListenerIncrease = 0.3 # 10%

# movie file is cmdline argument
inputPath = sys.argv[1]

# output file is 2. cmdline argument
outputPath = "out.csv"
if len(sys.argv) > 2:
    outputPath = sys.argv[2]

# start output and write header
outputFile = open(outputPath, 'w')
header = "frame, seconds, minutes, time, listeners\n"
outputFile.write(header)

# When was the file recorded?
creationTime = os.stat(outputPath).st_birthtime
creationDatetime = datetime.datetime.fromtimestamp(creationTime)
print(f"Creation time: {creationDatetime}")

# setup capture
vidcap = cv2.VideoCapture(inputPath)

# get framerate
fps = vidcap.get(cv2.CAP_PROP_FPS)
print(f"Frame rate: {fps} fps")

# store previous number of listeners here
averageNumberOfListeners = 0

listenerEvolution = []

# get first frame
success,frame = vidcap.read()
framenbr = 0

while success:

    # next frame
    framenbr += 1

    # get next frame
    success,frame = vidcap.read()
        
    # break if we are at the end
    if not success:
        break

    # update every second
    if framenbr % int(10*fps) == 0:
        
        # change to grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # resize
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

        #cv2.imshow("Resized image", gray)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # text extraction
        data = pytesseract.image_to_string(gray, lang='eng', config='--psm 3').lower()

        # relevant part
        extractedLines = re.findall(r'(\d+) others', data)

        if len(extractedLines) == 0:
            print(f"No extracted lines. Skipping.")
            #cv2.imshow("Resized image", gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            continue

        extracted = extractedLines[0]

        # use last 3 charcters, first one it is interpreted as '4'
        numberOfListeners = int(extracted[-3:])

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

        outputFile.write(csvLine + '\n')
        outputFile.flush()




  