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
            "spec": fig.to_json()
        })

    def to_json(self) -> str:
        data = {
            "name": self.name,
            "views": [view for view in self.views]
        }
        return json.dumps(data)


def publish(datastory: DataStory, url: str = os.getenv("DATASTORY_URL", "http://localhost:8080/api/story")) -> str:
    res = requests.post(url, data=datastory.to_json())
    res.raise_for_status()
    return res.json()["url"]
