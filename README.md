# twitter-spaces-stats-extractor
A Python script that uses image detection to extract the number of listeners in a Twitter Spaces based on a screen recording. It also creates a folder with graphs (one for each second of the recording) which can be assembled into a movie using a second script.

## Inspiration
The code's inspiration comes from [here](https://dev.to/video/introduction-to-text-detection-using-opencv-and-pytesseract-3he2).

## Setup
Install [tesseract](https://github.com/tesseract-ocr/tesseract), [pytesseract](https://pypi.org/project/pytesseract/) and [cv2](https://pypi.org/project/opencv-python/).

In oder to create movie, you need to install [ffmpeg](https://ffmpeg.org).

**Tip**: If you are on a Mac, I recommend to use [Homebrew](https://brew.sh/index_de) to install ```tesseract```and ```ffmpeg```.

## Usage

### Configuration
Before starting the script, open up ```config.py```to specify a few useful parameters. The latter are explained in file.


### Extracting the data
Then extract the data using
```
./extract <file name of screen recording>
```
on the command line.

The results are stored in ```data.csv```, while the created graphs are stored in ```graphs/```(unless you have changed to corresponding parameter in ```config.py```.

### Creating the movie
You can assemble the graph images into a movie by executing

```./createVideo.sh```

again on the command line (that's the *Terminal* program on the Mac).


## The screen recording as source
The screen recording needs to be done on a Desktop browser while the Twitter Space is active. Also, the recording needs to be cropped to the essential information, a screenshot is shown here:

<img width="865" alt="Bildschirmfoto 2021-09-16 um 15 29 03" src="https://user-images.githubusercontent.com/5444043/133624480-f1451c42-4f77-41be-9668-68d37aaab039.png">

The number between '+' and 'others' corresponds to the number of listeners.

## Visualisation of the evolution of listeners
The following graphs shows the evolution the listener numbers over time during the daily newscast of the @tortoise twitter channel, recorded on 2021-09-16 12:30 UTC.

The graph shows that there is a built-up over a minimum of 5 minutes before the curve starts to stabilize. 

![@tortoise Twitter Space 2021-09-16 12_30 UTC](https://user-images.githubusercontent.com/5444043/133624648-317e4d19-174e-4920-b1d1-05fda2998f59.png)
