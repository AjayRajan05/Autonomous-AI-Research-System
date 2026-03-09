class EvaluationAgent:

    def evaluate(self, results):

        best = min(results, key=lambda x: x["rmse"])

        return {
            "best_model": best["model"],
            "rmse": best["rmse"]
        }