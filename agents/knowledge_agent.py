import json
import requests
from schemas.knowledge_node import KnowledgeNode
from tools.config_loader import load_settings, load_prompts
from memory.vector_store import VectorStore


settings = load_settings()
prompts = load_prompts()


class KnowledgeAgent:

    def __init__(self):
        self.graph = CitationGraph()
        self.vector_store = VectorStore()

    def build(self, papers):

        for paper in papers:

            self.graph.add_paper(paper)

        return self.graph

    def store(self, papers):

        for paper in papers:
            self.vector_store.add_paper(paper)

    def run(self, papers):

        nodes = []

        for p in papers:

            if not p.sections:
                continue

            text = (
                p.sections.get("abstract", "")
                + p.sections.get("methods", "")
                + p.sections.get("results", "")
            )

            prompt = prompts["knowledge_extractor"] + "\n\n" + text

            payload = {
                "model": settings["llm"]["model"],
                "prompt": prompt,
                "stream": False
            }

            r = requests.post(settings["llm"]["base_url"], json=payload)

            data = json.loads(r.json()["response"])

            nodes.append(KnowledgeNode(**data))

        return nodes

    def top_papers(self):

        return sorted(
            self.graph.in_degree,
            key=lambda x: x[1],
            reverse=True
        )[:10]