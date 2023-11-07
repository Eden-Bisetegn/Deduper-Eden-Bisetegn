#!/bin/bash

#SBATCH --account=bgmp   ### change this to your actual account for charging
#SBATCH --partition=compute       ### queue to submit to
#SBATCH --job-name=star_align    ### job name
#SBATCH --output=convSAM_%j.out   ### file in which to store job stdout
#SBATCH --error=convSAM_%j.err    ### file in which to store job stderr
#SBATCH --time=3:00:00                ### wall-clock time limit, in minutes
#SBATCH --mem=32G              ### memory limit per node, in MB
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --ntasks-per-node=1     ### number of tasks to launch per node  q
#SBATCH --cpus-per-task=8       ### number of cores for each task
#conda activate samtools

# Convert the SAM file to BAM file format
samtools view -S -b C1_SE_uniqAlign.sam > C1_SE_uniqAlign.out.bam #-S-telles it the input is sam file, #b-tells it the output is bam file
# sort the file
samtools sort C1_SE_uniqAlign.out.bam -o C1_SE_uniqAlign.out.sorted.bam
# index file change to sam 
samtools index C1_SE_uniqAlign.out.sorted.bam
samtools view -h C1_SE_uniqAlign.out.sorted.bam > C1_SE_uniqAlign.out.sorted.sam
