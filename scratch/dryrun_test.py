import os, re, json, urllib.request, urllib.error

SITE_ROOT      = r'c:\Users\Pathi\Documents\needdroptaxi.com'
SITE_BASE_URL  = 'https://needdroptaxi.com'
WEBHOOK_URL    = 'https://ozvvhracfdhjeawlwfkp.supabase.co/functions/v1/cms-webhook'
WEBHOOK_SECRET = 'whsec_91add28850537f36ae4f88a033e7449f249dae5a98f6bb57'

with open(os.path.join(SITE_ROOT, 'index.html'), encoding='utf-8', errors='ignore') as f:
    html = f.read()

import re
pat = re.compile(r'src=["\']([^"\']+\.(webp|png|jpg|svg))["\']', re.IGNORECASE)
srcs = list(dict.fromkeys(m.group(1) for m in pat.finditer(html) if not m.group(1).startswith('data:')))[:3]

for src in srcs:
    url = (SITE_BASE_URL + src) if src.startswith('/') else src
    print('Testing:', url)
    payload = json.dumps({'imageUrl': url, 'source': 'needdroptaxi'}).encode()
    req = urllib.request.Request(WEBHOOK_URL, data=payload,
          headers={'Content-Type': 'application/json', 'x-webhook-secret': WEBHOOK_SECRET}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            print('  HTTP', resp.status, body[:400])
    except urllib.error.HTTPError as e:
        print('  HTTP', e.code, e.read().decode()[:400])
    except Exception as ex:
        print('  ERROR:', ex)
    print()
