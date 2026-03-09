import logging
from tools.arxiv_search import search as arxiv_search
from tools.semantic_scholar import search as ss_search
from rapidfuzz import fuzz
from schemas.paper import Paper


logger = logging.getLogger(__name__)


class RetrievalAgent:

    def run(self, plan):

        papers = []

        for q in plan.search_queries:

            papers += arxiv_search(q, 5)
            papers += ss_search(q, 5)

        unique = []

        for p in papers:
            unique[p.title.lower()] = p
        
            duplicate = False

            for u in unique:
                score = fuzz.ratio(
                    paper["title"].lower(),
                    u["title"].lower()
                )

                if score > 90:
                    duplicate = True
                    break

            if not duplicate:
                unique.append(paper)

        return list(unique.values())[:plan.max_papers]
  