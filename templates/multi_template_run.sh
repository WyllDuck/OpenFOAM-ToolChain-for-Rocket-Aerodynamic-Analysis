#!/bin/bash
mkdir -p ../todo


./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA0_R1_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA8_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA8_R1_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA16_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA16_R1_rhoCentralFoam

./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA0_R5_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA8_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA8_R5_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma0.6_AoA16_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma0.6_AoA16_R5_rhoCentralFoam

./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA0_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA0_R1_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA8_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA8_R1_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA16_R1_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA16_R1_rhoCentralFoam

./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA0_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA0_R5_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA8_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA8_R5_rhoCentralFoam
./template_run.sh /data/WARR_thermal_simulation/configs/config_Ma1.0_AoA16_R5_rhoCentralFoam.json rhoCentralFoamSubsonic /data/sphereCases/todo/Ma1.0_AoA16_R5_rhoCentralFoam