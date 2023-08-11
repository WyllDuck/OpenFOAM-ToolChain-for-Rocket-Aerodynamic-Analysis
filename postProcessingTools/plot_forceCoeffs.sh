tail -n +13 $1 > tables/forceCoeffs_plot2.dat
sed 's/#//g' tables/forceCoeffs_plot2.dat > tables/forceCoeffs_plot.dat
rm tables/forceCoeffs_plot2.dat

gnuplot plot_forceCoeffs
