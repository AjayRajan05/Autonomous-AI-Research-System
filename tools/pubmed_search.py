"""
Search PubMed for biomedical papers.
"""

from Bio import Entrez
from typing import List
import logging

from schemas.paper import Paper

logger = logging.getLogger(__name__)

Entrez.email = "research_agent@example.com"


def search(query: str, limit: int = 10) -> List[Paper]:

    logger.info(f"Searching PubMed: {query}")

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=limit
    )

    record = Entrez.read(handle)

    ids = record["IdList"]

    papers = []

    if not ids:
        return papers

    fetch = Entrez.efetch(
        db="pubmed",
        id=",".join(ids),
        retmode="xml"
    )

    data = Entrez.read(fetch)

    for article in data["PubmedArticle"]:

        article_data = article["MedlineCitation"]["Article"]

        title = article_data.get("ArticleTitle", "")

        abstract = ""
        if "Abstract" in article_data:
            abstract = " ".join(article_data["Abstract"]["AbstractText"])

        authors = []
        for a in article_data.get("AuthorList", []):
            if "LastName" in a:
                authors.append(a["LastName"])

        year = 0
        if "Journal" in article_data:
            year = article_data["Journal"]["JournalIssue"]["PubDate"].get("Year", 0)

        paper = Paper(
            id=article["MedlineCitation"]["PMID"],
            title=title,
            authors=authors,
            year=int(year) if year else 0,
            abstract=abstract,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']}/",
            pdf_url=None,
            source="pubmed"
        )

        papers.append(paper)

    return papers