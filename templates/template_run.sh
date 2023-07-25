#!/bin/bash

CONFIG=$1                   # passing configuration file - contains case values
PROJECT_FOLDER=$2           # address of template folder
OUTPUT_PROJECT_FOLDER=$3    # output folder for the resulting templated project

echo "Configuration File: " $CONFIG
echo "Project Template Folder: " $PROJECT_FOLDER
echo "Project Output Folder: " $OUTPUT_PROJECT_FOLDER

# copy template in 'run' folder and change directory
cp -r $PROJECT_FOLDER ../run/$OUTPUT_PROJECT_FOLDER
cd ../run/$OUTPUT_PROJECT_FOLDER

# find all 'jinja' templates and set fixed values from the configuration file 
for filename in $(find . -type f | grep ".j2")
do
    jinja2 $filename $CONFIG -o "${filename%.*}" # NOTE: last command removes '.j2' (the file type name)
done

# replace default configuration file in template repository with the used configuration file
cp $CONFIG config.yaml
