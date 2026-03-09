import json
import requests
import logging
from schemas.research_plan import ResearchPlan
from tools.config_loader import load_settings, load_prompts

logger = logging.getLogger(__name__)

settings = load_settings()
prompts = load_prompts()


class PlannerAgent:

    def run(self, query: str) -> ResearchPlan:

        prompt = prompts["planner"] + "\n\nQuery:\n" + query

        payload = {
            "model": settings["llm"]["model"],
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(settings["llm"]["base_url"], json=payload)

        text = r.json()["response"]

        data = json.loads(text)

        return ResearchPlan(**data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = PlannerAgent()

    plan = agent.run("transformer models for medical imaging")

    print(plan)