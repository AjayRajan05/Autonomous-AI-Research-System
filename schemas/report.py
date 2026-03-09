"""
Final research report schema.
"""

from pydantic import BaseModel
from typing import List


class ResearchReport(BaseModel):

    query: str

    summary: str

    technologies: List[str]

    key_findings: List[str]

    research_gaps: List[str]

    future_directions: List[str]

    paper_count: int

    sources: List[str]


if __name__ == "__main__":
    report = ResearchReport(
        query="transformers in healthcare",
        summary="Transformers are increasingly used in medical imaging...",
        technologies=["Vision Transformer", "Self Attention"],
        key_findings=["Better accuracy than CNNs"],
        research_gaps=["Limited clinical validation"],
        future_directions=["Multimodal models"],
        paper_count=10,
        sources=["https://arxiv.org/..."]
    )

    print(report.model_dump())