#!/bin/bash

CONFIG=$1                   # passing configuration file - contains case values
PROJECT_FOLDER=$2           # address of template folder
OUTPUT_PROJECT_FOLDER=$3    # output folder for the resulting templated project

echo "Configuration File: " $CONFIG
echo "Project Template Folder: " $PROJECT_FOLDER
echo "Project Output Folder: " $OUTPUT_PROJECT_FOLDER

# copy template in 'run' folder and change directory
cp -r $PROJECT_FOLDER ../run/$OUTPUT_PROJECT_FOLDER

# replace default configuration file in template repository with the used configuration file
cp $CONFIG ../run/$OUTPUT_PROJECT_FOLDER/config.yaml

# find all 'jinja' templates and set fixed values from the configuration file 
cd ../run/$OUTPUT_PROJECT_FOLDER
for filename in $(find . -type f | grep ".j2")
do
    jinja2 $filename config.yaml -o "${filename%.*}" # NOTE: last command removes '.j2' (the file type name)
    rm $filename # Template no longer requiered, remove it
done