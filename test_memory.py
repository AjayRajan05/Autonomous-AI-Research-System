from memory.vector_store import VectorStore

store = VectorStore()

store.add_documents([
    "Graph neural networks for traffic prediction",
    "Transformer models for time series forecasting"
])

print(store.search("traffic models"))