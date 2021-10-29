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

set xrange ["21:50:00":"23:00:00"]
set yrange [0:1100]

#set style data histogram
#set style fill solid

set title 'Evolution of listeners: Deutschlandfunk Twitter Space 2021-09-26 22 CEST'

plot 'data.csv' u 4:5 w lines
