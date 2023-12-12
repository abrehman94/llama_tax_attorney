import pickle
import fire
import re
import torch

def load_pickle(f):
    with open(f, 'rb') as f:
        return pickle.load(f)

def is_prefix( string, prefix ):
    r = re.compile(prefix+'.*')
    if re.match(r, string):
        return True
    return False    

def preprocess_text( data ):
    data = str( data )
    data = data.replace("\\r\\n"," ")
    data = data.replace(","," ")
    data = data.replace("."," ")
    data = data.replace('"'," ")
    data = data.replace("'"," ")
    data = data.lower()
    data = data.split(" ")
    data = [ d for d in data if len(d) > 0 ]
    data = data[0]
    # data = " ".join(data)
    return data

def postprocess( base, query, mans, aans ):
    
    query = load_pickle( base + '/' + query ) 
    mans = load_pickle( base + '/' + mans ) 
    aans = load_pickle( base + '/' + aans ) 
    
    results = []

    for m,a in zip(mans,aans):
        #m = preprocess_text( m )
        a = preprocess_text( a )

        if is_prefix(m, 'entail') and is_prefix(a, 'entail'):
            results.append( 1 )
        elif is_prefix(m, 'contra') and is_prefix(a, 'contra'):
            results.append( 1 )
        else:
            results.append( 0 )
        print("-"*20)
        print( m )
        print( a )

    print("accuracy {} %".format(sum(results)*100/len(results)))

if __name__ == "__main__":
    fire.Fire(postprocess)

