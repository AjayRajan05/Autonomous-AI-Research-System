from graphs.research_graph import build_graph

graph = build_graph()

state = {
    "query":"traffic prediction using machine learning"
}

result = graph.invoke(state)

print(result["report"])