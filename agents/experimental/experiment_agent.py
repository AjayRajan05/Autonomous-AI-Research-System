"""
Run ML experiments on extracted models/datasets.
"""

import logging

logger = logging.getLogger(__name__)


class ExperimentAgent:

    def run(self, nodes):

        results = []

        for n in nodes:

            for model in n.models:

                result = {
                    "model": model,
                    "simulated_score": 0.8
                }

                results.append(result)

        logger.info("Experiments simulated")

        return results