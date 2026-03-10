from agents.planner_agent import PlannerAgent
from pipelines.literature_pipeline import LiteraturePipeline
from pipelines.datascience_pipeline import DatasciencePipeline
from memory.session_memory import SessionMemory


class Router:
    
    def __init__(self, memory: SessionMemory):
        self.memory = memory
    
    def route(self, mode: str):
        """Route to appropriate pipeline based on mode"""
        if mode == "literature":
            return LiteraturePipeline()
        elif mode == "datascience":
            return DatasciencePipeline()
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'literature' or 'datascience'")


def route(query):
    """Legacy function for backward compatibility"""
    planner = PlannerAgent()
    plan = planner.run(query)
    return plan.route, plan