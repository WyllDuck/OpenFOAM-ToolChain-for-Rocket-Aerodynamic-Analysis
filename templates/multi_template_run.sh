#!/bin/bash
mkdir -p ../todo

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma4.63_AoA0_R1_rhoPimpleFoam.json rhoPimpleFoamTransonic ~/openfoam-data/sphereCases/todo/Ma4.63_AoA0_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma4.63_AoA0_R5_rhoPimpleFoam.json rhoPimpleFoamTransonic ~/openfoam-data/sphereCases/todo/Ma4.63_AoA0_R5_rhoPimpleFoam

#############################################################################################################

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA0_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA0_R5_rhoPimpleFoam

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA8_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA8_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA8_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA8_R5_rhoPimpleFoam

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA16_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA16_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA16_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA16_R5_rhoPimpleFoam

#############################################################################################################

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA0_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA0_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA0_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA0_R5_rhoPimpleFoam

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA8_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA8_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA8_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA8_R5_rhoPimpleFoam

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA16_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA16_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA16_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA16_R5_rhoPimpleFoam

#############################################################################################################

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma4.63_AoA16_R6_rhoCentralFoam.json rhoCentralFoam ~/openfoam-data/sphereCases/todo/Ma4.63_AoA16_R6_rhoCentralFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma2.3_AoA8_R6_rhoPimpleFoam.json rhoPimpleFoamTransonic ~/openfoam-data/sphereCases/todo/Ma2.3_AoA8_R6_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.5_AoA0_R6_rhoPimpleFoam.json rhoPimpleFoamTransonic ~/openfoam-data/sphereCases/todo/Ma1.5_AoA0_R6_rhoPimpleFoam