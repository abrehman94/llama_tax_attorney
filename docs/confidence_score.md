# How to determine confidence score each response? 

## References 

  * [LLMs for Multi-Modal Knowledge Extraction and Analysis in Intelligence/Safety-Critical Applications](https://arxiv.org/pdf/2312.03088.pdf)
  * [Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs](https://arxiv.org/pdf/2306.13063.pdf)

## What can we do in this short time? 
  
  * use consistency based confidence score 
    * vary temprature - to get 5 different respones
      * % of same responses is confidence 

## Possible ways 
  
  * model logits 
    * use model embeddings to calculate confidence score 
      * more instrusive but not applicable in case of closed source models 
  * Asking the model 
    * determining the response from model response 
      * consistency - among multiple respones - is an indicator of confidence 
      * explicit textual response of confidence from the model - not ususally reliable - models tend to be overconfident 
      * second paper proposes a hybrid of the two approaches 

    * vanilla verbalized confidence
      * prompt giving definition of confidence 
    * Chain-of-Thought-based verbalized confidence
      * asking it to 'think step by step' - seems to improve the confidence score 
    * multi-step Verbalized confidence
    * Top-K verbalized confidence

## Details 
### Asking the model 
  
  principally two ways 
    * textual reponse from the model 
    * consistency among multiple reponses 


  Response Ranking and LLM-Based uncertainty estimates (see [29]) –
  some investigation has occurred in evaluating the extent to which an
  LLM is capable of assessing its own uncertainty by way of prompting
  the LLM to include such information in its response (for example:
  “provide your confidence between 0-100% in the response”). In the
  case of verbalized confidence (where the LLM is supposed to explicitly state confidence in its response), LLMs tend to be overconfident;
  however using other prompting strategies such as ‘Top-K’ (ranking
  the top K answers), or Chain-of-Thought (asking for the explicit
  reasoning process that lead to an answer) seems to improve the outcomes.



