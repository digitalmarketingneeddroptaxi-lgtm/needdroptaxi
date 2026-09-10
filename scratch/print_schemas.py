import os
import re
import json

files_to_check = [
    './index.html',
    './about/index.html',
    './airport-transfer-taxi-service/index.html',
    './local-rental-taxi-service/index.html',
    './outstation-taxi-service/index.html',
    './taxi-booking/index.html',
    './thank-you-booking/index.html',
    './contact/index.html',
    './blog/index.html',
    './blog/author/pathi/index.html',
    './blog/top-10-tourist-attractions-to-visit-in-kanyakumari/index.html',
    './drop-taxi/chennai-to-bangalore/index.html'
]

for p in files_to_check:
    print(f"\n========================================\nFILE: {p}\n========================================")
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    for idx, s in enumerate(scripts):
        print(f"--- Schema #{idx+1} ---")
        try:
            d = json.loads(s.strip())
            print(json.dumps(d, indent=2))
        except Exception as e:
            print("ERROR parsing:", e)
