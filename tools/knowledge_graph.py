"""
Build knowledge graph from extracted research nodes.
"""

import networkx as nx
from schemas.knowledge_node import KnowledgeNode


class KnowledgeGraph:

    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node: KnowledgeNode):

        paper_id = node.paper_id

        self.graph.add_node(paper_id, type="paper")

        for model in node.models:
            self.graph.add_node(model, type="model")
            self.graph.add_edge(paper_id, model, relation="uses")

        for dataset in node.datasets:
            self.graph.add_node(dataset, type="dataset")
            self.graph.add_edge(paper_id, dataset, relation="uses")

    def export_json(self):

        data = nx.node_link_data(self.graph)

        return data


if __name__ == "__main__":

    g = KnowledgeGraph()

    node = KnowledgeNode(
        paper_id="p1",
        claims=["transformers outperform cnn"],
        datasets=["imagenet"],
        models=["vision transformer"],
        metrics={"accuracy": 0.92},
        limitations=[]
    )

    g.add_node(node)

    print(g.export_json())