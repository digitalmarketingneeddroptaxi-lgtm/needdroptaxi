import json
with open(r'scratch\broken_links.json', 'r') as f:
    data = json.load(f)
print("External Broken Links:")
for e in data.get('external', []):
    print(e)
