import os
import glob
import re
import json

blog_files = glob.glob('blog/**/*.html', recursive=True)
for p in sorted(blog_files):
    p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    scripts = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>', c, re.DOTALL)
    print(f"\n========================================\n{p}\n========================================")
    for idx, s in enumerate(scripts):
        try:
            d = json.loads(s.strip())
            print(f"Schema {idx+1}: {d.get('@type')}")
            # Check keys
            if d.get('@type') in ['BlogPosting', 'Article']:
                for k in ['headline', 'description', 'image', 'datePublished', 'dateModified', 'author', 'publisher']:
                    val = d.get(k)
                    print(f"  {k}: {type(val)} = {str(val)[:60]}")
            elif d.get('@type') == 'BreadcrumbList':
                print("  Breadcrumb elements:")
                for el in d.get('itemListElement', []):
                    print(f"    {el.get('position')}: {el.get('name')} -> {el.get('item')}")
            else:
                print(f"  Type: {d.get('@type')}")
        except Exception as e:
            print("  Error:", e)
