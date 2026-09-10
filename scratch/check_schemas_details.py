import json
import re

for p in ['./index.html', './about/index.html', './airport-transfer-taxi-service/index.html', './outstation-taxi-service/index.html', './local-rental-taxi-service/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    print(f"=== {p} ({len(scripts)} schemas) ===")
    for idx, s in enumerate(scripts):
        try:
            d = json.loads(s.strip())
            print(f"Schema {idx+1}: {d.get('@type')}")
            print(json.dumps(d, indent=2))
        except Exception as e:
            print(f"Schema {idx+1} Error: {e}\nRaw: {s}")
