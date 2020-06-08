import json

with open("tasks.json") as input_file:
    tasks = json.load(input_file)

with open("minified.json", "w+") as output_file:
    json.dump(tasks, output_file, ensure_ascii=False)
