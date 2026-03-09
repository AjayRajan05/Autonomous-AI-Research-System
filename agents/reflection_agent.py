#from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline


#hf_pipe = pipeline("text-generation", model="gpt2", max_new_tokens=50, truncation = True, max_length=1024)
#hf_pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
hf_pipe = pipeline(
    "text-generation", 
    model="microsoft/Phi-3-mini-4k-instruct", 
    trust_remote_code=True,
    max_new_tokens=500,
    device_map="auto"
)
llm = HuggingFacePipeline(pipeline=hf_pipe)

#llm = ChatOpenAI()

def reflect(state):

    results = state["experiment_output"]

    prompt = f"""
    Analyze this experiment result.

    {results}

    Suggest improvements to the model.
    """

    reflection = llm.invoke(prompt)

    state["reflection"] = reflection

    return state