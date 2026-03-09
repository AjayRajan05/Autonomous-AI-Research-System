"""
Paper schema.

Defines the structure of an academic paper in the system.
All retrieval agents must convert API responses into this model.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class Paper(BaseModel):
    """
    Standardized representation of an academic paper.
    """

    id: str = Field(..., description="Unique identifier (arxiv id / semantic scholar id)")
    title: str
    authors: List[str]
    year: int
    abstract: str
    url: str
    pdf_url: Optional[str] = None

    source: str = Field(
        ...,
        description="Source of paper: arxiv | semantic_scholar | pubmed"
    )

    sections: Optional[Dict[str, str]] = None
    embedding: Optional[List[float]] = None


if __name__ == "__main__":
    # Quick test
    paper = Paper(
        id="123",
        title="Transformer Models for Medical Imaging",
        authors=["Alice", "Bob"],
        year=2024,
        abstract="This paper studies...",
        url="https://example.com",
        pdf_url="https://example.com/paper.pdf",
        source="arxiv"
    )

    print(paper.model_dump())