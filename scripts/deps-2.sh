#!/bin/bash


python3 -m pip install venv 
python3 -m pip install -U pip setuptools
python3 -m pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 -e .
python3 -m pip install llama-recipes transformers datasets accelerate sentencepiece protobuf==3.20 py7zr scipy peft bitsandbytes fire torch_tb_profiler ipywidgets

exit 0


