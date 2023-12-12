# SARA_v3 Dataset 

  Statutory Reasoning Assessment Dataset 

  [Paper Describing Dataset](https://ceur-ws.org/Vol-2645/paper5.pdf)
  [Dataset tar.gz](https://nlp.jhu.edu/law/sara_v3/)
  
  Dataset 
    statutes.txt  
      Statutes are the set of rules.   

    train.tsv     
    test.tsv      
     tab seperated file of context, question and answer  

     answer can be 
      numerical value 
      entailment / conflict - boolean answer  

  Court Corpus of 1.7M US Federal Court Cases 
    
  [case.law 157 MB zip file](https://archive.data.jhu.edu/dataset.xhtml?persistentId=doi:10.7281/T1/N1X6I4)


## How this dataset can be used? 

  train the Llama on 
    court corpus of 1.7M cases 
    sara dataset 
      statues 
      train data - context, question, answer 
  
### Statues 

  Let's start with this! 

  Single text document which need to be fed to the model line by line? 

  statues - 258 lines - 4,375 words 
  
### Context, Question, Answer  
 
 train - 256 examples  
 test - 120 examples 

### Court Corpus 

  Let's leave it for the last if time permits 

  It's also a single text document - but very large! ~700 MB 




