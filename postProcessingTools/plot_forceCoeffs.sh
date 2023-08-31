mkdir -p tables

touch tables/forceCoeffs_plot.dat
gnuplot plot_forceCoeffs &

(
    trap printout SIGINT
    printout() {
        echo ""
        exit
    }
    while :
    do
        tail -n +13 $1 | sed -e '/Time/ s/#//g' > tables/forceCoeffs_plot.dat
        sleep 30
    done
)

echo "Finishing script"
