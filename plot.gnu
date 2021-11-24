if (!exists("filename")) filename='default.png'

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

set xrange ["14:00:00":"14:40:00"]
set yrange [0:30]

#set style data histogram
#set style fill solid

# do not use the Klammeraffe or underscores
set title 'Evolution of listeners: dw environment Twitter Space 2021-11-12 13 CEST'

plot 'data.csv' u 4:5 w lines
