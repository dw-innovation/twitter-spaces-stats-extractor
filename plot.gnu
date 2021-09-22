set term png font "Palatino, 14" size 1280, 720
set output 'graph.png'

set key autotitle columnhead
set boxwidth 0.5 relative
set datafile separator ","
set xlabel 'minutes'
set ylabel '# of listeners'
set grid
#set style data histogram
#set style fill solid

set title 'Evolution of listeners: Fact or Cap 2021-09-20 11 CEST'

plot 'out.csv' u 3:5 w lines
