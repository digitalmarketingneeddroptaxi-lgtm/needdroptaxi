import json, re

for p in ['taxi-booking/index.html', 'thank-you-booking/index.html', 'trip-fare-calculator/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    print(f"\n==============================\n{p} ({len(scripts)} schemas)")
    for s in scripts:
        print(s.strip())
