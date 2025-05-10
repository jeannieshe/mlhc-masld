#!/bin/bash
#SBATCH -n 4 # Number of cores requested
#SBATCH -t 60  # Runtime in minutes
#SBATCH --mem=64G # Memory in GB
#SBATCH -o dia.out # Stdout logged to this file
#SBATCH -e dia.err # Stderr logged to this file

python dia.py
