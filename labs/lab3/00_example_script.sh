#!/bin/bash

#The name of the job is test_job
#SBATCH -J test_job

#The job requires 1 compute node
#SBATCH -N 1

#The job requires 1 task per node
#SBATCH --ntasks-per-node=1

#The maximum walltime of the job is 5 minutes
#SBATCH -t 00:05:00

#SBATCH --mem=5G

#If you keep the next two lines, you will get an e-mail notification
#whenever something happens to your job (it starts running, completes or fails)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@here.com

#Keep this line if you need a GPU for your job
#SBATCH --partition=gpu

#Indicates that you need one GPU node
#SBATCH --gres=gpu:tesla:1

#Commands to execute go below

#Load Python
module load python/3.6.3/CUDA-9.0

#Activate your environment
source activate mtcourse

#Display Sockeye's help message
sockeye-train --help
