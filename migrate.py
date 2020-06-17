import json
import string


with open("tasks.json") as input_file:
    tasks = json.load(input_file)

for task in tasks:
    replacement_variables = string.ascii_lowercase[8:8 + task.get("text").count("{int}")]
    task["variables"] = {}

    for rv in replacement_variables:
        task["text"] = task.get("text").replace("{int}", f"{{int: {rv}}}", 1)
        task["variables"][rv] = "ANY"

with open("tasks.json", "w+") as output_file:
    json.dump(tasks, output_file, ensure_ascii=False, indent=2)
