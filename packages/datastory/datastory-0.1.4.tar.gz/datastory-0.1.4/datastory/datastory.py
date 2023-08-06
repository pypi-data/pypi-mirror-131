import json
import os
import requests
import plotly


class DataStory:

    def __init__(self, name: str):
        self.name = name
        self.views = []

    def header(self, content: str, level: int = 1):
        self.views.append({
            "type": "header",
            "spec": {
                "content": content,
                "level": level
            }
        })

    def markdown(self, md: str):
        self.views.append({
            "type": "markdown",
            "spec": {
                "content": md
            }
        })

    def plotly(self, fig: plotly.graph_objs.Figure):
        self.views.append({
            "type": "plotly",
            "spec": json.loads(fig.to_json())
        })

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "views": [view for view in self.views]
        }


def publish(datastory: DataStory, url: str = os.getenv("DATASTORY_URL", "http://localhost:8080/api/story")) -> str:
    res = requests.post(url, json=datastory.to_dict())
    res.raise_for_status()
    return res.json()["url"]
