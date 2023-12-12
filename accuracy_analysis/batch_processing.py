from typing import List, Optional
import fire
from llama import Llama, Dialog

import time
import select
import sys
import csv
import pickle

def build_generator(    
                    ckpt_dir: str,
                    tokenizer_path: str,
                    max_seq_len: int = 512,
                    max_batch_size: int = 8,
                ):

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    return generator

def get_response(
                    generator, 
                    dialogs,
                    temperature: float = 0.6,
                    top_p: float = 0.9,
                    max_gen_len: Optional[int] = None,
    ):
    results = generator.chat_completion(
            dialogs,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
    return results 

def read_data( test_data ):
    reasoning = []
    numerical = []

    with open(test_data, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            ans = row[2].lower()
            if ans == 'entailment' or ans == 'contradiction':
                reasoning.append( row )
            else:
                numerical.append( row )
    return reasoning, numerical

def processing_reasoning_batch( reasoning, generator, temperature ):
    # construct a batch into a dialog 
    batch = reasoning 
    dialogs: List[Dialog] = []
    sys_prompt = 'Please answer by performing statutory reasoning step by step to determine if last statement in query is entailed or contradicted according to the statutes of tax law. Answer in one word.'
    for b in batch:
        query = b[0] + '\n' + b[1]
        dialogs.append( [{"role": "system", "content": sys_prompt},{"role": "user", "content": query}] )

    # run batch through the model 
    results = get_response( generator, dialogs, temperature ) 
    
    query = []
    mans = []
    aans = []
    i = 0
    for d,r in zip(dialogs,results):
        # print("-"*20)
        # print("Query: {}".format(d[1]['content']))
        # print("Answer: {}".format(r['generation']['content']))
        # print("Acutal: {}".format(batch[i][2]))
        query.append( d[1]['content'] )
        mans.append( r['generation']['content'] )
        aans.append( batch[i][2] )
        i += 1
    return query, mans, aans

def processing_numerical_batch( numerical, generator ):
    # construct a batch into a dialog 
    batch = numerical 
    dialogs: List[Dialog] = []
    sys_prompt = 'Please calculate tax applicable in given context. Do not show steps. Give numerical answer after tag total tax: '
    for b in batch:
        query = b[0] + '\n' + b[1]
        dialogs.append( [{"role": "system", "content": sys_prompt},{"role": "user", "content": query}] )

    # run batch through the model 
    results = get_response( generator, dialogs ) 
    
    query = []
    mans = []
    aans = []
    i = 0
    for d,r in zip(dialogs,results):
        # print("-"*20)
        # print("Query: {}".format(d[1]['content']))
        # print("Answer: {}".format(r['generation']['content']))
        # print("Acutal: {}".format(batch[i][2]))
        query.append( d[1]['content'] )
        mans.append( r['generation']['content'] )
        aans.append( batch[i][2] )
        i += 1
    return query, mans, aans

def save_obj( pickle_file_path, obj  ):
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(obj, file)

def main( 
    test_data,

    ckpt_dir: str,
    tokenizer_path: str,
    base, 
    temprature,
        ):

    reasoning, numerical = read_data( test_data )
    print("{} for reasoning questions and {} numerical".format(len(reasoning), len(numerical)))
    
    generator = build_generator(ckpt_dir, tokenizer_path)
    
    if True: 
        bsize = 8
        query = []
        mans = []
        aans = []

        for i in range(0,len(reasoning),bsize):

            batch = reasoning[i:i+bsize]

            queryo, manso, aanso = processing_reasoning_batch( batch, generator, temperature=float(temprature) ) 

            query.extend( queryo )
            mans.extend( manso )
            aans.extend( aanso )

            print("Done with {} of {}".format(i,len(reasoning)), end='\r')

        save_obj( base+'/queries.pkl', query )
        save_obj( base+'/model_ans.pkl', mans )
        save_obj( base+'/actual_ans.pkl',aans )
        
    # save the mans and aans as pickle dumps 
    
    if True: 
        # generate numerical reasoning results  
        bsize = 8
        query = []
        mans = []
        aans = []

        for i in range(0,len(numerical),bsize):
            batch = numerical[i:i+bsize]
            queryo, manso, aanso = processing_numerical_batch( batch, generator ) 
            query.extend( queryo )
            mans.extend( manso )
            aans.extend( aanso )
            print("Done with {} of {}".format(i,len(reasoning)), end='\r')
        
        base = base + '/numerical'
        save_obj( base+'/queries.pkl', query )
        save_obj( base+'/model_ans.pkl', mans )
        save_obj( base+'/actual_ans.pkl',aans )

if __name__ == "__main__":
    fire.Fire(main)

