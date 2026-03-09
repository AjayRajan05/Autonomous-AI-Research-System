import json
import requests
from tools.config_loader import load_settings, load_prompts

settings = load_settings()
prompts = load_prompts()


class InsightAgent:

    def run(self, synthesis):

        prompt = prompts["insight_generator"] + "\n\n" + str(synthesis)

        payload = {
            "model": settings["llm"]["model"],
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(settings["llm"]["base_url"], json=payload)

        return json.loads(r.json()["response"])