import os
import json
from bs4 import BeautifulSoup

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

# 1. Fix schema pricing in index.html and others
for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            changed = False
            
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    script_changed = False
                    
                    if isinstance(data, dict):
                        if data.get('@type') == 'LocalBusiness':
                            if 'description' in data and '13/km' in data['description']:
                                data['description'] = data['description'].replace('13/km', '14/km')
                                script_changed = True
                            if 'hasOfferCatalog' in data:
                                for item in data['hasOfferCatalog'].get('itemListElement', []):
                                    offer = item.get('itemOffered', {})
                                    if offer.get('name') == 'Outstation Taxi Service' and item.get('price') == '13':
                                        item['price'] = '14'
                                        script_changed = True
                                    if offer.get('name') == 'Airport Transfer Taxi Service' and item.get('price') == '13':
                                        item['price'] = '14'
                                        script_changed = True

                    if script_changed:
                        script.string = json.dumps(data, separators=(',', ':'))
                        changed = True
                except Exception as e:
                    pass

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                    
# 2. Fix broken links
with open(os.path.join(root, 'scratch', 'broken_links.json'), 'r') as f:
    broken_data = json.load(f)

# Group internal broken links by source file
files_to_fix = {}
for source, target in broken_data.get('internal', []):
    if source not in files_to_fix:
        files_to_fix[source] = []
    files_to_fix[source].append(target)
    
for source, target in broken_data.get('external', []):
    if source not in files_to_fix:
        files_to_fix[source] = []
    files_to_fix[source].append(target)

for rel_filepath, targets in files_to_fix.items():
    filepath = os.path.join(root, rel_filepath)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        changed = False
        for a in soup.find_all('a'):
            href = a.get('href')
            if href in targets:
                if 'twitter.com' in href:
                    a['href'] = 'https://x.com/' # fallback
                else:
                    a['href'] = '/blog/'
                changed = True
                
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
