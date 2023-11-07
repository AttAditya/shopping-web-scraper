import os
import json

from modules.search.source import Source

global_agents: list[str] = []
sources: list[Source] = []

with open("data/user-agents", "r") as agents_file:
    global_agents = agents_file.read().split("\n")
    agents_file.close()

for source_filename in os.listdir("data/sources"):
    source_path = f"data/sources/{source_filename}"
    with open(source_path, "r") as source_file:
        source_data = json.load(source_file)
        source_file.close()

        source_data["user_agents"] += global_agents
        sources.append(Source(**source_data))

