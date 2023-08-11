tail -n +2 $1 > tables/solverInfo_plot2.dat
sed 's/#//g' tables/solverInfo_plot2.dat > tables/solverInfo_plot.dat
rm tables/solverInfo_plot2.dat

gnuplot plot_residuals
