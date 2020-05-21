import pickle
import json
from law import Law
from scorer import Scorer

scorer = Scorer()

laws = pickle.load(open('data/law_objects.p', 'rb'))

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
    output.append({name: sections})

with open('data/laws.json', 'w') as f:
    json.dump(output, f)
