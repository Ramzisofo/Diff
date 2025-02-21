#!/bin/bash -l
#SBATCH --job-name="darTraj"
#SBATCH --account="emshare"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ramzi.dakhmouche@empa.ch
#SBATCH --time=5:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal
#SBATCH --constraint=gpu
#SBATCH --hint=nomultithread

cd ..
cd ..
uenv start prgenv-gnu/24.11:v1 --view=default
source ./pytorch-env/bin/activate
cd Diff
cd diffusion


python diff.py
