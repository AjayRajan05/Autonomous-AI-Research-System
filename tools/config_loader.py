"""
Configuration loader for the AI research platform.
"""

import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "configs"


def load_settings():
    """
    Load system settings YAML.
    """
    path = CONFIG_DIR / "settings.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_prompts():
    """
    Load prompt templates YAML.
    """
    path = CONFIG_DIR / "prompts.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    settings = load_settings()
    prompts = load_prompts()

    print("Settings loaded:")
    print(settings)

    print("\nPrompts loaded:")
    print(prompts.keys())