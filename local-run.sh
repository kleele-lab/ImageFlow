#!/bin/bash

# The json settings file defines "pipeline" which will execute. Make sure all paths and steps defined in this file match your dataset and goals before running!
# See settings_files/example.json for a basic pipeline. 
settings_file=~/code/settings_files/Nv3_Day2.json

# Prevents the creation of hidden files that break things, this is particularly an issue when running on Macs so remove at your own risk.
export COPY_EXTENDED_ATTRIBUTES_DISABLE=true


# Runs the python that drives your pipeline!
python3 ~/code/driver.py $settings_file