#!/bin/bash

source ./config.sh

TRANSFORM=`python3 -c "import transformers;print('/'.join(transformers.__file__.split('/')[:-1])+'/models/llama/convert_llama_weights_to_hf.py')"`
echo $TRANSFORM

mkdir -p $base/models-hf/
python3 ${TRANSFORM} --input_dir $base/models/ --model_size 7B --output_dir $base/models-hf/ 



