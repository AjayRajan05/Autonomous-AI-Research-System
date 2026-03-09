import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:

    def __init__(self):

        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("papers")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_paper(self, paper):

        embedding = self.model.encode(paper["abstract"]).tolist()

        self.collection.add(
            documents=[paper["abstract"]],
            embeddings=[embedding],
            ids=[paper["title"]]
        )

    def search(self, query):

        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        return results