mkdir -p tables

HEADER=$(head -n 2 $1 | tail -n +2)

array=()
for file in $HEADER
do
    if [[ $file == *"initial"* ]]; then
        array+="$file "
    fi
done

echo "plotting ..."
for elem in $array
do
    echo $elem
done

jinja2 plot_residuals.j2 -o plot_residuals -D columns="$array"

touch tables/solverInfo_plot.dat
gnuplot plot_residuals &

(
    trap printout SIGINT
    printout() {
        echo ""
        exit
    }
    while :
    do
        tail -n +2 $1 | sed -e '/Time/ s/#//g' > tables/solverInfo_plot.dat
        sleep 30
    done
)

echo "Finishing script"
