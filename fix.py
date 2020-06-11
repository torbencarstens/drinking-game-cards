import re
import json

file = "tasks.json"

with open(file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# TODO trink verteil
keywords = ['bis zum ende']
regexes = [re.compile(f"\\s{keyword}(\\s|,)") for keyword in keywords]

# TODO Getränkt
excempts = [it.lower() for it in []]


def is_excempt(lowertext: str) -> bool:
    for excempt in excempts:
        if excempt in lowertext:
            return True
    return False


try:
    with open('checkme.txt', 'w', encoding='utf-8') as f:
        for task in tasks:
            text: str = task['text']
            lowertext = text.lower()


except BaseException as e:
    print(e)


outfile = 'tasks.json'
with open(outfile, 'w', encoding='utf-8') as f:
    outcontent = json.dumps(tasks, indent=4, ensure_ascii=False)
    f.write(outcontent)
    f.write('\n')
