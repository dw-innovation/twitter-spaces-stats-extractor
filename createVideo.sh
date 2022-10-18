#!/bin/bash
ffmpeg -r 1 -f image2 -s 1280x720 -start_number 180 -i graphs/plot%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p graph.mp4
