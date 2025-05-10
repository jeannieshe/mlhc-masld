#!/bin/bash
#SBATCH -n 8 # Number of cores requested
#SBATCH -t 60  # Runtime in minutes
#SBATCH --mem=64G # Memory in GB
#SBATCH -o clean_med.out # Stdout logged to this file
#SBATCH -e clean_med.err # Stderr logged to this file


python clean_med.py
