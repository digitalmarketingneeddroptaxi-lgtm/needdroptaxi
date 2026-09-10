import os
import re
import json

html_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

for p in sorted(html_files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    if not scripts:
        print(f"[NO SCHEMA] {p}")
    for idx, s in enumerate(scripts):
        try:
            data = json.loads(s.strip())
            stype = data.get('@type')
            # Look for errors:
            # 1. Invalid @context
            ctx = data.get('@context')
            if ctx not in ['https://schema.org', 'http://schema.org']:
                print(f"[{p}] Invalid @context: {ctx}")
            # 2. Check types
            if stype == 'LocalBusiness' or stype == 'TaxiService':
                # check address, priceRange, telephone, name, geo, openingHours
                pass
            # 3. Check for malformed URLs inside schema
            s_str = json.dumps(data)
            if '/needdroptaxi.com/' in s_str:
                print(f"[{p}] Schema contains /needdroptaxi.com/: {stype}")
            if 'http://needdroptaxi.com' in s_str:
                print(f"[{p}] Schema contains http://: {stype}")
            if 'www.needdroptaxi.com' in s_str:
                print(f"[{p}] Schema contains www.: {stype}")
            if '../../' in s_str:
                print(f"[{p}] Schema contains relative ../../: {stype}")
            
            # 4. Check BlogPosting / Article
            if stype in ['BlogPosting', 'Article']:
                author = data.get('author')
                publisher = data.get('publisher')
                datePub = data.get('datePublished')
                headline = data.get('headline')
                image = data.get('image')
                if not author or not publisher or not datePub or not headline:
                    print(f"[{p}] BlogPosting missing required fields: author={bool(author)}, pub={bool(publisher)}, date={bool(datePub)}, headline={bool(headline)}")
                if isinstance(author, dict) and author.get('@type') not in ['Person', 'Organization']:
                    print(f"[{p}] Invalid author type: {author}")
                if isinstance(publisher, dict) and publisher.get('@type') != 'Organization':
                    print(f"[{p}] Invalid publisher type: {publisher}")
            
            # 5. Check BreadcrumbList
            if stype == 'BreadcrumbList':
                items = data.get('itemListElement', [])
                for it in items:
                    if 'item' not in it or '@id' in it and 'item' not in it:
                        print(f"[{p}] Breadcrumb missing item: {it}")
                    if isinstance(it.get('item'), str) and not it['item'].startswith('http'):
                        print(f"[{p}] Breadcrumb item relative URL: {it['item']}")
        except Exception as e:
            print(f"[{p}] JSON decode error: {e}")
