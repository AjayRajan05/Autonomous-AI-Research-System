"""
Structured knowledge extracted from a paper.
"""

from pydantic import BaseModel
from typing import List, Dict


class KnowledgeNode(BaseModel):

    paper_id: str

    claims: List[str]

    datasets: List[str]

    models: List[str]

    metrics: Dict[str, float]

    limitations: List[str]


if __name__ == "__main__":
    node = KnowledgeNode(
        paper_id="123",
        claims=["Transformers outperform CNNs"],
        datasets=["ImageNet", "ChestX-ray14"],
        models=["Vision Transformer"],
        metrics={"accuracy": 0.92},
        limitations=["Small dataset", "High compute cost"]
    )

    print(node.model_dump())