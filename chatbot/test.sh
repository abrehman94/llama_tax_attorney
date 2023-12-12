#!/bin/bash

torchrun --nproc_per_node 1 \
    example_chat_interaction.py \
    --ckpt_dir ./models/7B/ \
    --tokenizer_path ./models/tokenizer.model \
    --max_seq_len 512 \
    --max_batch_size 6

    # example_chat_completion.py \
    # example_chat_completion.py \
    # --ckpt_dir llama-2-7b/ \




