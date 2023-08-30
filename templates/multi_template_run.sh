#!/bin/bash
mkdir -p ../todo

./template_run.sh /mnt/e/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R0_rhoCentralFoam.json rhoCentralFoam ../todo/Ma2.3_AoA8_R0_rhoCentralFoam
./template_run.sh /mnt/e/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R1_rhoCentralFoam.json rhoCentralFoam ../todo/Ma2.3_AoA8_R1_rhoCentralFoam
./template_run.sh /mnt/e/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R2_rhoCentralFoam.json rhoCentralFoam ../todo/Ma2.3_AoA8_R2_rhoCentralFoam
./template_run.sh /mnt/e/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R3_rhoCentralFoam.json rhoCentralFoam ../todo/Ma2.3_AoA8_R3_rhoCentralFoam
./template_run.sh /mnt/e/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R4_rhoCentralFoam.json rhoCentralFoam ../todo/Ma2.3_AoA8_R4_rhoCentralFoam