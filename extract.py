#!/usr/bin/env python3

from cv2 import cv2
import pytesseract
import sys
import re
import os
import time
import datetime
import statistics

def extractMacCSV(samplingIntervalInSeconds, creationDatetime, outputCSVFilename):

    # maximum increase if listener number wrt to total listeners
    maximumListenerIncrease = 1 # 100%

    # movie file is cmdline argument
    inputPath = sys.argv[1]

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
        if framenbr % int(samplingIntervalInSeconds*fps) == 0:
            
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
            extractedLines = re.findall(r'(\d+k?) others', data)

            # skip if no result could be found
            if len(extractedLines) == 0:
                print(f"No extracted lines. Skipping.")
                #cv2.imshow("Resized image", gray)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                continue

            # get relevant part
            extracted = extractedLines[0]

            # determine factor - it'S 1000 if there is a 'k' at the end
            factor = 1
            if extracted[-1] == 'k':
                factor = 1000
                extracted = extracted[:-1] # loose last 'k'


            # use last 3 charcters, first one it is interpreted as '4'
            numberOfListeners = int(extracted[-3:]) * factor

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
            #print(data)

            outputFile.write(csvLine + '\n')
            outputFile.flush()


def extractiPhoneCSV(samplingIntervalInSeconds, creationTime, outputCSVFilename):

    # maximum increase if listener number wrt to total listeners
    maximumListenerIncrease = 1 # 100%



    # movie file is cmdline argument
    inputPath = sys.argv[1]

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
        if framenbr % int(samplingIntervalInSeconds*fps) == 0:
            
            # change to grey scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # resize
            gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

            #cv2.imshow("Resized image", gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            # text extraction
            data = pytesseract.image_to_string(gray, lang='eng', config='--psm 3').lower()

            # default exaction
            extracted = None

            # split OCR result into lines
            dataLines = data.split('\n')

            # go though each extracted line
            for dataLine in dataLines:

                #print(dataLine)

                # search for relevant parts
                extractedGroups = re.findall(r'(\d+k?) (?:others|weitere)', dataLine)

                #print(extractedGroups)
                #print("************")

                # if we found something
                if len(extractedGroups) > 0:
                    extracted = extractedGroups[0]
                    break
                else:
                    continue

            # skip if no data could be found
            if extracted is None:
                    # skip if no result could be found
                    print(f"No extracted data. Skipping.")
                    continue

            # determine factor - it'S 1000 if there is a 'k' at the end
            factor = 1
            if extracted[-1] == 'k':
                factor = 1000
                extracted = extracted[:-1] # loose last 'k'


            # use last 3 charcters, first one it is interpreted as '4'
            #numberOfListeners = int(extracted[-3:]) * factor
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
            #print(data)

            outputFile.write(csvLine + '\n')
            outputFile.flush()

if __name__ == '__main__':

    # sampling interval in seconds
    samplingIntervalInSeconds = 5

    # When was the file recorded?
    #creationTime = os.stat(outputPath).st_birthtime
    #creationDatetime = datetime.datetime.fromtimestamp(creationTime)
    #creationDatetime = datetime.datetime(year=2021, month=9, day=26, hour=21, minute=56, second=00)
    #extractMacCSV(samplingIntervalInSeconds, creationDatetime, 'mac.csv')
    
    
    creationDatetime = datetime.datetime(year=2021, month=9, day=26, hour=22, minute=47, second=18)
    extractiPhoneCSV(samplingIntervalInSeconds, creationDatetime, 'iPhone.csv')

  