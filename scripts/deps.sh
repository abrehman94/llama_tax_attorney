#!/bin/bash

# set -x 

eval "$(/data2/ar/anaconda3/bin/conda shell.$(basename $SHELL) hook)"

env_name=chatbot
conda create -n "$env_name" python=3.8
conda activate "$env_name"
conda install -c conda-forge cudatoolkit=11.4 cudnn=8.6 -y

python3 -m pip install -U pip setuptools
python3 -m pip install \
        llama-recipes \
        transformers \
        datasets \
        accelerate \
        sentencepiece \
        protobuf=="3.20" \
        py7zr \
        scipy \
        peft \
        bitsandbytes \
        fire \
        torch_tb_profiler


