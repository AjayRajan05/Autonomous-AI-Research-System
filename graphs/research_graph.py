from langgraph.graph import StateGraph

from agents.research_agent import research_agent
from agents.experiment_agent import design_experiment
from agents.executor_agent import execute_experiment
from agents.evaluator_agent import evaluate
from agents.reflection_agent import reflect
from agents.report_agent import generate_report


def build_graph():

    graph = StateGraph(dict)

    graph.add_node("research", research_agent)
    graph.add_node("design", design_experiment)
    graph.add_node("execute", execute_experiment)
    graph.add_node("evaluate", evaluate)
    graph.add_node("reflect", reflect)
    graph.add_node("report", generate_report)

    graph.set_entry_point("research")

    graph.add_edge("research","design")
    graph.add_edge("design","execute")
    graph.add_edge("execute","evaluate")
    graph.add_edge("evaluate","reflect")
    graph.add_edge("reflect","report")

    return graph.compile()