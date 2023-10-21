#!/bin/bash

CONFIG=$1                   # passing configuration file - contains case values
PROJECT_FOLDER=$2           # address of template folder
OUTPUT_PROJECT_FOLDER=$3    # output folder for the resulting templated project

echo ""
echo "Configuration File: " $CONFIG
echo "Project Template Folder: " $PROJECT_FOLDER
echo "Project Output Folder: " $OUTPUT_PROJECT_FOLDER

# if OUTPUT_PROJECT_FOLDER does already ask if overwrite
if [ -d "$OUTPUT_PROJECT_FOLDER" ]; then
    echo "Project Output Folder already exists!"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "Aborted!"
        exit 1
    fi
    # else remove OUTPUT_PROJECT_FOLDER
    rm -rf $OUTPUT_PROJECT_FOLDER
fi

# if PROJECT_FOLDER does not exist stop
if [ ! -d "$PROJECT_FOLDER" ]; then
    echo "Error: Project Template Folder does not exist!"
    echo ""
    exit 1
fi

# replace default configuration file in template repository with the used configuration file
# if CONFIG does not exist stop
if [ ! -f "$CONFIG" ]; then
    echo "Error: Configuration File does not exist!"
    echo ""
    exit 1
fi

# try to jinja2 - if fail stop
if ! command -v jinja2 &> /dev/null
then
    echo "Error: jinja2 could not be found!"
    echo ""
    exit 1
fi

cp -r $PROJECT_FOLDER $OUTPUT_PROJECT_FOLDER
cp $CONFIG $OUTPUT_PROJECT_FOLDER/config.json

# find all 'jinja' templates and set fixed values from the configuration file 
cd $OUTPUT_PROJECT_FOLDER
for filename in $(find . -type f | grep ".j2")
do
    jinja2 $filename config.json -o "${filename%.*}" --format=json # NOTE: last command removes '.j2' (the file type name)
    rm $filename # Template no longer requiered, remove it
done

 chmod +x All* # make scripts executable (Allrun, Allclean, etc.)