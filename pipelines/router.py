from agents.planner_agent import PlannerAgent


def route(query):

    planner = PlannerAgent()

    plan = planner.run(query)

    return plan.route, plan