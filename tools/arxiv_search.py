"""
arXiv paper search tool.

Responsible for retrieving academic papers from arXiv
and converting them into standardized Paper objects.
"""

import arxiv
import logging
from typing import List

from schemas.paper import Paper


logger = logging.getLogger(__name__)


def search(query: str, max_results: int = 10) -> List[Paper]:
    """
    Search arXiv for academic papers.

    Args:
        query: research query
        max_results: maximum papers to fetch

    Returns:
        List[Paper]
    """

    logger.info(f"Searching arXiv for query: {query}")

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers: List[Paper] = []

    try:
        for result in search.results():

            paper = Paper(
                id=result.entry_id.split("/")[-1],
                title=result.title,
                authors=[author.name for author in result.authors],
                year=result.published.year,
                abstract=result.summary,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                source="arxiv"
            )

            papers.append(paper)

    except Exception as e:
        logger.error(f"arXiv search failed: {e}")

    logger.info(f"arXiv returned {len(papers)} papers")

    return papers


if __name__ == "__main__":
    """
    Standalone test.
    """

    logging.basicConfig(level=logging.INFO)

    query = "transformer models medical imaging"

    results = search(query, max_results=5)

    for paper in results:
        print("\n---")
        print(paper.title)
        print(paper.authors)
        print(paper.year)
        print(paper.pdf_url)