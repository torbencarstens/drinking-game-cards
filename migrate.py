import json
import string


with open("tasks_en.json") as input_file:
    tasks = json.load(input_file)

for task in tasks:
    text = "Drink {int: "
    task["text"] = task["text"].replace("Drink {int: ", "Everybody drink {int: ")

with open("tasks_en.json", "w+") as output_file:
    json.dump(tasks, output_file, ensure_ascii=False, indent=2)
