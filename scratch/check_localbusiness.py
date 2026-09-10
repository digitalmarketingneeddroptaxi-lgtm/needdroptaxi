import json
import re

for p in ['./index.html', './airport-transfer-taxi-service/index.html', './outstation-taxi-service/index.html', './local-rental-taxi-service/index.html', './about/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    print(f"\n========================================\n{p}\n========================================")
    for idx, s in enumerate(scripts):
        try:
            d = json.loads(s.strip())
            print(f"--- Schema {idx+1}: {d.get('@type')} ---")
            if d.get('@type') == 'LocalBusiness':
                print("Address:", d.get('address'))
                print("Geo:", d.get('geo'))
                print("PriceRange:", d.get('priceRange'))
                print("OpeningHours:", d.get('openingHours'))
        except Exception as e:
            print(f"Error: {e}")
