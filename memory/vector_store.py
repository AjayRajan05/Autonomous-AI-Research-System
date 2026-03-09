from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.index = faiss.IndexFlatL2(384)

    def add_documents(self, docs):

        embeddings = self.model.encode(docs)
        self.index.add(np.array(embeddings))

        self.texts.extend(docs)

    def search(self, query, k=3):

        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, k)

        return [self.texts[i] for i in indices[0]]
