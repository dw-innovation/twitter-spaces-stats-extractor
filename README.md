# twitter-spaces-stats-extractor
A Python script that uses image detection to extract the number of listeners in a Twitter Spaces based on a screen recording.

## Inspiration
The code's inspiration comes from [here](https://dev.to/video/introduction-to-text-detection-using-opencv-and-pytesseract-3he2).

## Setup
Install [tesseract](https://github.com/tesseract-ocr/tesseract), [pytesseract](https://pypi.org/project/pytesseract/) and [cv2](https://pypi.org/project/opencv-python/).

## Usage
```
./extract <file name of screen recording>
```

## output
The extracted data is stored as a CSV file in ```data.csv```.
In addition, the script generates a graph with gnuplot for every recorded second, stored in ```graphs/```. Note that a few parameters need to be changed manually in ```gnu.plot```:
* xrange
* yrange
* tilte

## The screen recording as source
The screen recording needs to be done on a Desktop browser while the Twitter Space is active. Also, the reocrding needs to be cropped to the essential information, a screenshot is shown here:

<img width="865" alt="Bildschirmfoto 2021-09-16 um 15 29 03" src="https://user-images.githubusercontent.com/5444043/133624480-f1451c42-4f77-41be-9668-68d37aaab039.png">

The number between '+' and 'others' corresponds to the number of listeners.

## Visualisation of the evolution of listeners
The following graphs shows the evolution the listener numbers overtime during the daily newscast of the @tortoise twitter channel, recorded on 2021-09-16 12:30 UTC.

The graph shows that there is a built-up over a minimum of 5 minutes before the curve starts to stabilize. 

![@tortoise Twitter Space 2021-09-16 12_30 UTC](https://user-images.githubusercontent.com/5444043/133624648-317e4d19-174e-4920-b1d1-05fda2998f59.png)
