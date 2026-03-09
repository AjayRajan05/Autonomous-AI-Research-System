from tools.arxiv_search import search_arxiv

class ExplorationAgent:

    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def explore(self, seed_papers):

        explored_titles = set()
        all_papers = []

        frontier = seed_papers

        for depth in range(self.max_depth):

            new_frontier = []

            for paper in frontier:

                title = paper["title"]

                if title in explored_titles:
                    continue

                explored_titles.add(title)
                all_papers.append(paper)

                query = title

                related = search_arxiv(query)

                for r in related:
                    if r["title"] not in explored_titles:
                        new_frontier.append(r)

            frontier = new_frontier

        return all_papers