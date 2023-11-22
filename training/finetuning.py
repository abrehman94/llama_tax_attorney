import torch
from llama_recipes.utils.dataset_utils import get_preprocessed_dataset
from llama_recipes.configs.datasets import samsum_dataset

from transformers import LlamaForCausalLM, LlamaTokenizer
from transformers import TrainerCallback
from transformers import default_data_collator, Trainer, TrainingArguments

from contextlib import nullcontext


model_id="../../llama/models-hf/"

def check_model(model, tokenizer):
    eval_prompt = """
    Summarize this dialog:
    A: Hi Tom, are you busy tomorrow’s afternoon?
    B: I’m pretty sure I am. What’s up?
    A: Can you go with me to the animal shelter?.
    B: What do you want to do?
    A: I want to get a puppy for my son.
    B: That will make him so happy.
    A: Yeah, we’ve discussed it many times. I think he’s ready now.
    B: That’s good. Raising a dog is a tough issue. Like having a baby ;-) 
    A: I'll get him one of those little dogs.
    B: One that won't grow up too big;-)
    A: And eat too much;-))
    B: Do you know which one he would like?
    A: Oh, yes, I took him there last Monday. He showed me one that he really liked.
    B: I bet you had to drag him away.
    A: He wanted to take it home right away ;-).
    B: I wonder what he'll name it.
    A: He said he’d name it after his dead hamster – Lemmy  - he's  a great Motorhead fan :-)))
    ---
    Summary:
    """
    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
    model.eval()
    with torch.no_grad():
        print(tokenizer.decode(model.generate(**model_input, max_new_tokens=100)[0], skip_special_tokens=True))

def prepare_for_train(model):
    model.train()

    def create_peft_config(model):
        from peft import (
            get_peft_model,
            LoraConfig,
            TaskType,
            prepare_model_for_int8_training,
        )

        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=8,
            lora_alpha=32,
            lora_dropout=0.05,
            target_modules = ["q_proj", "v_proj"]
        )

        # prepare int-8 model for training
        model = prepare_model_for_int8_training(model)
        model = get_peft_model(model, peft_config)
        model.print_trainable_parameters()
        return model, peft_config

    # create peft config
    model, lora_config = create_peft_config(model) 
    return model, lora_config

def get_profiler():
    profiler = nullcontext()
    return profiler

if __name__ == "__main__":

    enable_profiler = False
    output_dir = "tmp/llama-output" 

    if True:
    # if False:
        tokenizer = LlamaTokenizer.from_pretrained(model_id)
        model = LlamaForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16)

    train_dataset = get_preprocessed_dataset(tokenizer, samsum_dataset, 'train')

    check_model( model, tokenizer )

    model, lora_config = prepare_for_train( model )

    config = {
        'lora_config': lora_config,
        'learning_rate': 1e-4,
        'num_train_epochs': 1,
        'gradient_accumulation_steps': 2,
        'per_device_train_batch_size': 2,
        'gradient_checkpointing': False,
    }

    profiler = get_profiler()

    # Define training args
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        bf16=False,  # Use BF16 if available
        # logging strategies
        logging_dir=f"{output_dir}/logs",
        logging_strategy="steps",
        logging_steps=10,
        save_strategy="no",
        optim="adamw_torch_fused",
        max_steps=total_steps if enable_profiler else -1,
        **{k:v for k,v in config.items() if k != 'lora_config'}
    )

    with profiler:
        # Create Trainer instance
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=default_data_collator,
            callbacks=[profiler_callback] if enable_profiler else [],
        )

        # Start training
        trainer.train()
    model.save_pretrained(output_dir)

    check_model( model, tokenizer )
