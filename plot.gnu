set term pdf font "Palatino"
set output 'graph.pdf'
set key autotitle columnhead
set datafile separator ","
set xlabel 'minutes'
set ylabel '# of listeners'
set grid

set title 'Evolution of listeners: Fact or Cap 2021-09-20 11 CEST'

plot 'out.csv' u 3:5 w lines
