import glob
import json
import re

files = sorted(glob.glob('**/*.html', recursive=True))

errors = []
total_schemas = 0

for p in files:
    if 'scratch' in p or '.system_generated' in p or 'email-protection' in p or 'pathi.html' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    for s in scripts:
        total_schemas += 1
        try:
            d = json.loads(s)
        except Exception as e:
            errors.append((p, f"JSON parse error: {e}"))
            continue

        # Check for fake ratings/reviews
        if 'aggregateRating' in d:
            errors.append((p, "Contains aggregateRating"))
        if 'review' in d:
            errors.append((p, "Contains review"))

        # Check priceRange
        if 'priceRange' in d and d['priceRange'] in ['??', '?', '']:
            errors.append((p, f"Invalid priceRange: {d['priceRange']}"))

        # Check dates in BlogPosting
        if d.get('@type') in ['BlogPosting', 'Article']:
            dp = d.get('datePublished', '')
            dm = d.get('dateModified', '')
            if not re.match(r'^\d{4}-\d{2}-\d{2}', dp):
                errors.append((p, f"Invalid datePublished format: {dp}"))
            if not re.match(r'^\d{4}-\d{2}-\d{2}', dm):
                errors.append((p, f"Invalid dateModified format: {dm}"))

        # Check Breadcrumbs
        if d.get('@type') == 'BreadcrumbList':
            for el in d.get('itemListElement', []):
                item = el.get('item', '')
                if not item.startswith('https://'):
                    errors.append((p, f"Breadcrumb item not HTTPS: {item}"))
                if not item.endswith('/'):
                    errors.append((p, f"Breadcrumb item missing trailing slash: {item}"))
                if '/drop-taxi/' in item and item.endswith('/drop-taxi/'):
                    errors.append((p, f"Breadcrumb item points to /drop-taxi/: {item}"))

print(f"Validated {total_schemas} JSON-LD schemas across {len(files)} files.")
print(f"Total validation issues found: {len(errors)}")
for p, err in errors:
    print(f"  {p}: {err}")
