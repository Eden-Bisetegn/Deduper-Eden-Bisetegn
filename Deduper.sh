#!/bin/bash

#SBATCH --account=bgmp   ### change this to your actual account for charging
#SBATCH --partition=bgmp       ### queue to submit to
#SBATCH --job-name=deduper    ### job name
#SBATCH --output=deduper_%j.out   ### file in which to store job stdout
#SBATCH --error=deduper_%j.err    ### file in which to store job stderr
#SBATCH --time=3:00:00                ### wall-clock time limit, in minutes
#SBATCH --mem=32G              ### memory limit per node, in MB
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --ntasks-per-node=1     ### number of tasks to launch per node  q
#SBATCH --cpus-per-task=8       ### number of cores for each task

/usr/bin/time ./Bisetegn_deduper.py -u STL96.txt -f C1_SE_uniqAlign.out.sorted.sam -o C1_SE_uniqAligndeduped.out.sam

#test run
#./Bisetegn_deduper.py -u STL96.txt -f test.sam -o test.out.sam