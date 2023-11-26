#!/bin/bash

get_real_path() {
    script_path=$(dirname $1)
    script_path=$(realpath $script_path)
}
if [[ $0 != $BASH_SOURCE ]]; then
    get_real_path $BASH_SOURCE
else
    get_real_path $0
fi
cd $script_path

# Ref: https://github.com/SgfdDttt/sara
wget https://nlp.jhu.edu/law/sara_v3/sara_v3.tar.gz

# uncompress data
tar -xzvf sara_v3.tar.gz

# create splits
cd sara_v3
python3 $script_path/code/make_text_dataset.py

