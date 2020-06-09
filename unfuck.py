import re
import json

file = "tasks_unfucked.json"

with open(file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# TODO trink verteil
personal_keywords = ['du', 'dir', 'dein', 'dich', 'deine' 'deiner']
personal_regexes = [re.compile(f"\\s{keyword}(\\s|,)")
                    for keyword in personal_keywords]

definitve_personal = ["sms", "whatsapp", "sitznachbar", "wenn du nicht wei", "zungenbrecher"]

def matches_definitve(lowertext: str) -> bool:
    for definitve in definitve_personal:
        if definitve in lowertext:
            task['personal'] = True
            return True
    return False

try:
    for task in tasks:
        text: str = task['text']
        if task['personal']:
            continue

        lowertext = text.lower()

        if "stimmt gleichzeitig" in lowertext or "alle gleichzeitig" in lowertext or "personalpronomen" in lowertext:
            continue

        if matches_definitve(lowertext):
            continue

        for personal_regex in personal_regexes:
            if personal_regex.findall(lowertext):
                abortion = input(f"{task['id']}/{len(tasks)}: {text}")
                if (abortion == ''):
                    print("OK")
                    task['personal'] = True
                print('\n\n\n\n')
                break
except:
    pass

outfile = 'tasks_unfucked.json'
with open(outfile, 'w', encoding='utf-8') as f:
    outcontent = json.dumps(tasks, indent=4, ensure_ascii=False)
    f.write(outcontent)
