import re
import json

file = "tasks_unfucked.json"

with open(file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# TODO trink verteil
keywords = ['hand', 'knie', 'bein', 'küssen', 'kuschel', 'schlägt',
            'streichel', 'schlag auf', 'kneif', 'Backpfeife', 'tauscht', 'Nimm das Getränk']
regexes = [re.compile(f"\\s{keyword}(\\s|,)") for keyword in keywords]

#TODO Getränkt
excempts = [it.lower() for it in ['dein Knie mit deiner Stirn', 'die Hand heben', 'Handtasche','Wer sich als Letzter', 'Bilder auf deinem Handy', 'Schreibe jemandem den Satz', 'Getränkt','Kuschelrock', 'ob beim Furz nicht', 'Lieber ohne Beine', 'Handwerk', 'handstand', 'Handy', 'Handball', 'die luft an', "beinhalte", "Stimmt alle", "Hand trinken", "Links trinken", 'nur die linke Hand benutzen', 'Letzter auf dem Boden kniet', 'Kuscheltier', 'Verstecke etwas in deiner geschlossenen Faust']]


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


outfile = 'tasks_unfucked.json'
with open(outfile, 'w', encoding='utf-8') as f:
    outcontent = json.dumps(tasks, indent=4, ensure_ascii=False)
    f.write(outcontent)
    f.write('\n')
