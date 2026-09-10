import json
import re

for p in ['./index.html', './about/index.html', './airport-transfer-taxi-service/index.html', './outstation-taxi-service/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    print(f"\n========================================\n{p}\n========================================")
    for idx, s in enumerate(scripts):
        try:
            d = json.loads(s.strip())
            print(f"--- Schema {idx+1}: {d.get('@type')} ---")
            # print top-level keys
            print("Keys:", list(d.keys()))
            if 'aggregateRating' in d:
                print("aggregateRating:", d['aggregateRating'])
            if 'review' in d:
                print("review count:", len(d['review']))
            # print full json
            print(json.dumps(d, indent=2)[:1500])
        except Exception as e:
            print(f"Error: {e}")
