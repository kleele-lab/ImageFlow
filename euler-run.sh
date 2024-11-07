#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=4:00:00
#SBATCH --job-name="pipeline"
#SBATCH --mem-per-cpu=1024


# SET THIS VALUE TO THE PIPELINE YOU WANT TO RUN
# See settings_files/example.json for a basic pipeline. 
settings_file=~/code/settings_files/example.json


# Configures the necessary modules, if your pipeline needs any additional modules add them below.
module purge
module load stack/2024-06
module load gcc/12.2.0
module load python/3.9.18

# Prevents the creation of hidden files that break things, this is particularly an issue when running on Macs so remove at your own risk.
export COPY_EXTENDED_ATTRIBUTES_DISABLE=true

# Runs the python that drives your pipeline!
python3 ~/code/driver.py $settings_file