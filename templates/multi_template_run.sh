#!/bin/bash
mkdir -p ../todo

./template_run.sh config.json rhoCentralFoam /data/OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis/todo/Ma2.3_AoA16_R1_rhoCentralFoam
# Add more lines to generate additional templates