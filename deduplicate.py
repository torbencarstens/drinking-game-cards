import json
from collections import Counter

with open("tasks.json") as input_file:
    tasks = json.load(input_file)

deduplicated = {}
to_delete = []
for task in tasks:
    if task["text"] in deduplicated.keys():
        to_delete.append(task["id"])
        continue
    deduplicated[task["text"]] = task
    deduplicated[task["text"]]["count"] = sum([t["count"] for t in tasks if t["text"] == task["text"]])


with open("tasks.json", "w+") as output_file:
    json.dump(list(deduplicated.values()), output_file, ensure_ascii=False, indent=2)
