from tools.arxiv_tool import search_papers

def research_agent(state):

    query = state["query"]

    papers = search_papers(query)

    summaries = [p["summary"] for p in papers]

    state["papers"] = papers
    state["summaries"] = summaries

    return state