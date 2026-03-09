"""
Simple web search using DuckDuckGo API.
"""

import requests
import logging

logger = logging.getLogger(__name__)


def search(query: str, limit: int = 5):

    url = "https://api.duckduckgo.com/"

    params = {
        "q": query,
        "format": "json"
    }

    r = requests.get(url, params=params)

    data = r.json()

    results = []

    for topic in data.get("RelatedTopics", [])[:limit]:

        if "Text" in topic:
            results.append({
                "title": topic["Text"],
                "url": topic.get("FirstURL")
            })

    return results