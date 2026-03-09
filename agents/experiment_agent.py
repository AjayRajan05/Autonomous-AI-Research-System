#from langchain.chat_models import ChatOpenAI
#from langchain_openai import ChatOpenAI

from langchain_openai import ChatOpenAI

from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Specify your desired Hugging Face model ID
#hf_pipe = pipeline("text-generation", model="gpt2", max_new_tokens=50, truncation = True, max_length=1024)
hf_pipe = pipeline(
    "text-generation", 
    model="microsoft/Phi-3-mini-4k-instruct", 
    trust_remote_code=True,
    max_new_tokens=500,
    device_map="auto"
)
llm = HuggingFacePipeline(pipeline=hf_pipe)

#llm = ChatOpenAI()

def design_experiment(state):

    topic = state["query"]
    

    prompt = f"""
    Write a Python ML experiment using sklearn.

    Task: {topic}

    Requirements:
    - generate synthetic dataset
    - train model
    - print RMSE

    Return only Python code.
    """

    code = llm.invoke(prompt)

    with open("experiments/generated/experiment.py","w") as f:
        f.write(code)

    state["experiment_file"] = "experiments/generated/experiment.py"

    return state