"""
Semantic Scholar search tool.

Fetches academic papers using Semantic Scholar API
and converts them into Paper schema objects.
"""

import logging
import requests
from typing import List

from schemas.paper import Paper


logger = logging.getLogger(__name__)

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search(query: str, limit: int = 10) -> List[Paper]:
    """
    Search Semantic Scholar papers.

    Args:
        query: search query
        limit: number of papers to return

    Returns:
        List[Paper]
    """

    logger.info(f"Searching Semantic Scholar for query: {query}")

    params = {
        "query": query,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,openAccessPdf,url"
    }

    papers: List[Paper] = []

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        for item in data.get("data", []):

            authors = []
            for a in item.get("authors", []):
                if "name" in a:
                    authors.append(a["name"])

            pdf_url = None
            if item.get("openAccessPdf"):
                pdf_url = item["openAccessPdf"].get("url")

            paper = Paper(
                id=item.get("paperId"),
                title=item.get("title", ""),
                authors=authors,
                year=item.get("year") or 0,
                abstract=item.get("abstract") or "",
                url=item.get("url") or "",
                pdf_url=pdf_url,
                source="semantic_scholar"
            )

            papers.append(paper)

    except Exception as e:
        logger.error(f"Semantic Scholar search failed: {e}")

    logger.info(f"Semantic Scholar returned {len(papers)} papers")

    return papers


if __name__ == "__main__":
    """
    Standalone testing.
    """

    logging.basicConfig(level=logging.INFO)

    query = "transformer models medical imaging"

    results = search(query, limit=5)

    for paper in results:
        print("\n---")
        print("Title:", paper.title)
        print("Authors:", paper.authors)
        print("Year:", paper.year)
        print("PDF:", paper.pdf_url)