#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=4:00:00
#SBATCH --job-name="pipeline"
#SBATCH --mem-per-cpu=1024
#SBATCH --error=error.txt


# The json settings file defines "pipeline" which will execute, nothing else will be run
#   example params provides options you may choose to set in your pipeline
settings_file=~/code/settings_files/Nv3_Day2.json

# Prevents the creation of hidden files that break things
export COPY_EXTENDED_ATTRIBUTES_DISABLE=true

# Configures the necessary modules
module purge
module load stack/2024-06
module load gcc/12.2.0
module load python/3.9.18


################################################################
# If your workflow requires additional modules, add them below #
################################################################




# Runs the python that drives your pipeline!
python3 ~/code/driver.py $settings_file