if (!exists("filename")) filename='default.png'
if (!exists("graphTitle")) graphTitle='Evolution of Twitter Space listeners'

if (!exists("graphStartTime")) graphStartTime = '00:00:00'
if (!exists("graphEndTime")) graphEndTime = '24:00:00'
if (!exists("graphMinimumNumberOfListeners")) graphMinimumNumberOfListeners = 0
if (!exists("graphMaximumNumberOfListeners")) graphMaximumNumberOfListeners = 1000

set term png font "Palatino, 14" size 1280, 720
set output filename

set key autotitle columnhead
set boxwidth 0.5 relative
set datafile separator ","

set ylabel '# of listeners'
set grid

#set xlabel 'minutes'
set xlabel 'Time (CEST)'

set xdata time
set timefmt "%H:%M:%S"
set format x "%H:%M"

set xrange [graphStartTime:graphEndTime]
set yrange [graphMinimumNumberOfListeners:graphMaximumNumberOfListeners]

# do not use the Klammeraffe or underscores
set title graphTitle #

plot 'data.csv' u 4:5 w lines
