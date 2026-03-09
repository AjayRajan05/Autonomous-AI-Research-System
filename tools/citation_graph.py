import networkx as nx


class CitationGraph:

    def __init__(self):

        self.graph = nx.DiGraph()

    def add_paper(self, paper):

        title = paper["title"]
        self.graph.add_node(title)

        if "references" in paper:

            for ref in paper["references"]:

                self.graph.add_edge(title, ref)

    def get_neighbors(self, title):

        return list(self.graph.neighbors(title))

    def get_graph(self):

        return self.graph