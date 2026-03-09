"""
Evaluate experiment results.
"""

import logging

logger = logging.getLogger(__name__)


class EvaluationAgent:

    def run(self, experiment_results, nodes):

        summary = {}

        for r in experiment_results:

            model = r["model"]

            if model not in summary:
                summary[model] = []

            summary[model].append(r["simulated_score"])

        avg = {
            m: sum(v) / len(v)
            for m, v in summary.items()
        }

        logger.info("Evaluation completed")

        return avg
    