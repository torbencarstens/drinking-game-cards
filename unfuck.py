import json

file = "tasks_unfucked.json"

with open(file, 'r') as f:
    tasks = json.load(f)

# TODO trink verteil
personal_keywords = ['du', 'dir', 'dein', 'dich']


try:
    for task in tasks:
        text: str = task['text']
        if task['personal']:
            continue

        if "Zungenbrecher" in text or "wenn du nicht wei" in text.lower():
            task['personal'] = True
            continue

        for personal_keyword in personal_keywords:
            if personal_keyword in text.lower():
                abortion = input(text)
                if (abortion == ''):
                    print("OK")
                    task['personal'] = True
                print('\n\n\n\n')
                break
except:
    pass

outfile = 'tasks_unfucked.json'
with open(outfile, 'w') as f:
    json.dump(tasks, f, indent=4)
