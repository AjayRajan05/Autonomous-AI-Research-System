#from langchain_openai import ChatOpenAI

from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

#hf_pipe = pipeline("text-generation", model="gpt2", max_new_tokens=512, truncation = True, max_length=1024)
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

def generate_report(state):

    query = state["query"]

    #summaries = state["summaries"]
    #evaluation = state["evaluation"]

    summaries = str(state.get("summaries", ""))[-1500:] 
    evaluation = str(state.get("evaluation", ""))[-1000:]

    prompt = f"""
    Write a research report.

    Topic: {query}

    Literature:
    {summaries}

    Results:
    {evaluation}
    """

    report = llm.invoke(prompt)

    state["report"] = report

    return state