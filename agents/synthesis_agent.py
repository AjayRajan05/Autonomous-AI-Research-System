import json
import requests
from tools.config_loader import load_settings, load_prompts

settings = load_settings()
prompts = load_prompts()


class SynthesisAgent:

    def run(self, nodes):

        text = "\n".join([str(n.model_dump()) for n in nodes])

        prompt = prompts["synthesizer"] + "\n\n" + text

        payload = {
            "model": settings["llm"]["model"],
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(settings["llm"]["base_url"], json=payload)

        return json.loads(r.json()["response"])