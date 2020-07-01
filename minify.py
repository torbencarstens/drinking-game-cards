import json
import os
import re

for file in os.listdir("."):
    locale = re.findall(r"tasks_(\w{2}).json", file)
    if locale:
        with open(f"tasks_{locale[0]}.json") as input_file:
           tasks = json.load(input_file)
        with open(f"minified_{locale[0]}.json", "w+") as output_file:
            json.dump(tasks, output_file, ensure_ascii=False)

