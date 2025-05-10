#!/bin/bash
#SBATCH -n 8 # Number of cores requested
#SBATCH -t 60  # Runtime in minutes
#SBATCH --mem=64G # Memory in GB
#SBATCH -o combine.out # Stdout logged to this file
#SBATCH -e combine.err # Stderr logged to this file

python combine.py
