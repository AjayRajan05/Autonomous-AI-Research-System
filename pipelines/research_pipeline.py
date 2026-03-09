from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.evaluation_agent import EvaluationAgent
from agents.report_agent import ReportAgent
from memory.vector_store import VectorStore

class ResearchPipeline:

    def __init__(self):

        self.memory = VectorStore()
        self.planner = PlannerAgent()
        self.research = ResearchAgent(self.memory)
        self.evaluator = EvaluationAgent()
        self.reporter = ReportAgent()

    def run(self, query):

        plan = self.planner.plan(query)

        papers = self.research.run(query)

        results = [
            {"model":"LSTM","rmse":2.1},
            {"model":"GNN","rmse":1.8}
        ]

        evaluation = self.evaluator.evaluate(results)

        report = self.reporter.generate(query, papers, results)

        return report