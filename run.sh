#!/bin/bash
GLOBAL_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $GLOBAL_DIR
mkdir -p run

# Execute Openfoam Simulation
function execute_openfoam_sim
{
    now=$(date --iso-8601=seconds)
    logFile="$GLOBAL_DIR/log.$1"
    pathDir="$GLOBAL_DIR/run/$1"
    
    echo '================================================'
    echo "[${now}] Logfile for $scriptName:  $logFile" 2>&1 | tee $logFile
    echo "Starting Next Simulation
         pathDir: $pathDir
    "  2>&1 | tee $logFile
    
    # Instructions To Follow - Execute Simulation and Go Back To General Directory
    mv "$GLOBAL_DIR/todo/$1" "$pathDir"
    cd $pathDir
    
    chmod +x All* # ensure that script are executable
    ./Allclean # clean previous work
    ./Allrun
    cd $GLOBAL_DIR # back to general directory to possibily execute more simulations
    
    echo "Simulation Ended."  2>&1 | tee $logFile
}


# Initial Loop Conditions
found=false

while IFS= read -r line;
do
    line=$(echo $line|tr -d '\n')
    
    if [ $line = 'end' ]; then
        echo "Termination"
        break
    fi
    
    # Output Next Simulation 2 Run
    if $found; then
        
        # Recursive Call to Function
		./run.sh $1 $line
        
        break
    fi
    
    # Find the input word
    if [ $2 = $line ]; then
        execute_openfoam_sim $line
        found=true
    fi
    
done < $1