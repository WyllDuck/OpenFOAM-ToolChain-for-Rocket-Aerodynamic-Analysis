tail -n +2 postProcessing/solverInfo1/0/solverInfo.dat > postProcessing/solverInfo1/0/solverInfo_plot2.dat
sed 's/#//g' postProcessing/solverInfo1/0/solverInfo_plot2.dat > postProcessing/solverInfo1/0/solverInfo_plot.dat
rm postProcessing/solverInfo1/0/solverInfo_plot2.dat

gnuplot plot_residuals
