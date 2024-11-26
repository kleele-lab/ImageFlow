#!/bin/bash

# PASS THIS VALUE AS AN ARGUMENT WHEN RUNNING THIS SCRIPT
# See settings_files/example.json for a basic pipeline. 
echo "Attempting to set settings file to: " $1
settings_file=$1


# Prevents the creation of hidden files that break things, this is particularly an issue when running on Macs so remove at your own risk.
export COPY_EXTENDED_ATTRIBUTES_DISABLE=true

# Runs the python that drives your pipeline!
python3 ~/code/driver.py $settings_file