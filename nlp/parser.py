import re
import json
from collections import defaultdict

REFREGEX = re.compile(r'(. ?Reg. ?[0-9]+[0-9]+)(,?\.? ?[sS](chedule)?\.? [0-9]+)+( \([0-9]+\))?\.|([\s\r\n])?([0-9]{4},) (c. ?[0-9]+)(, Sched. [A-Z0-9]+?)?(, s. [0-9]+)?( \([0-9, ]+\))?( - [0-9]{2}\/[0-9]{2}\/[0-9]{4})?(\.|;|)?')

BULLETREGEX = re.compile(r'^([0-9]+\.?)?([0-9]+\.?-?[0-9]+?\.?)?(\s?\([0-9]\))?(\([a-z]+\.?([0-9]+)?\))?\s')

with open('data/laws_raw.json', 'r+') as f:
    laws = json.load(f)

# extract refset
refset = set()

for law in laws.keys():
    refset = refset.union(
        [match.group().rstrip(r'[\.:;,]$').strip() for match in re.finditer(REFREGEX, ' '.join([c['text'] for c in laws[law]['content']]))])

ref_to_id = dict(
    zip(refset, [f'Ref{n}' for n in range(1, len(refset) + 1)])
)

id_to_ref = dict([(v, k) for k, v in ref_to_id.items()])

parsed = defaultdict(lambda: {})

for law in laws:
    parsed[law]['url'] = laws[law]['url']
    parsed[law]['content'] = []
    for c in laws[law]['content']:
        text = c['text']
        refs = [match.group().rstrip(r'[\.:;,]$').strip()
                for match in re.finditer(REFREGEX, text)]
            
        for ref in sorted(refs, key=len, reverse=True):
            try:
                text = text.replace(ref, ref_to_id[ref])
            except KeyError:
                text = text
        
        bullet = [match.group().rstrip(r'[\.:;,]$').strip() for match in re.finditer(BULLETREGEX, text)] 
        
        text = re.sub(BULLETREGEX, '',  text).strip()
        
        c['norm'] = text
        c['bullet'] = bullet
        parsed[law]['content'].append(c)

with open('data/parsed.json', 'w') as f:
    json.dump(laws, f)
