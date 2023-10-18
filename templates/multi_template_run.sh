#!/bin/bash
mkdir -p ../todo

./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA0_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma0.6_AoA0_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma0.6_AoA0_R5_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.0_AoA0_R1_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.0_AoA0_R1_rhoPimpleFoam
./template_run.sh ~/openfoam-data/WARR_thermal_simulation/configs/config_Ma1.0_AoA0_R5_rhoPimpleFoam.json rhoPimpleFoamSubsonic ~/openfoam-data/sphereCases/todo/Ma1.0_AoA0_R5_rhoPimpleFoam