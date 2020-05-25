import pickle
import json
from law import Law
from scorer import Scorer

scorer = Scorer()

with open('data/parsed.json', 'r+') as f:
    parsed = json.load(f)

laws = dict()

for name, items in parsed.items():
    laws[name] = Law(name, items['url'], items['content'])

output = []

for name, law in laws.items():
    print(name)
    sections = []

    for i, titles in law.table_of_content.items():
        
        text = law.get_section(int(i))
        if text != '':
            d = titles.copy()
            d['text'] = text
            d['flesh_score'] = scorer.FleschScore(text)

            sections.append(d)
    output.append({'title': name, 'sections': sections})

with open('data/laws.json', 'w') as f:
    json.dump(output, f)
