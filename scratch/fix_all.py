import os
import re
from bs4 import BeautifulSoup
import json

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

# 1. Fix _redirects
redirects_path = os.path.join(root, '_redirects')
if os.path.exists(redirects_path):
    with open(redirects_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(redirects_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if '/taxi-booking/*' in line or '/trip-fare-calculator/*' in line:
                continue # remove loop rules
            f.write(line)
            
# 2. Iterate through all html files
for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Simple string replacements for malformed URLs
            html = html.replace('needdroptaxi.com/needdroptaxi.com/', 'needdroptaxi.com/')
            html = html.replace('needdroptaxi.com/needdroptaxi.com', 'needdroptaxi.com')
            html = html.replace('../trip-fare-calculator/', '/trip-fare-calculator/')
            html = html.replace('../trip-fare-calculator', '/trip-fare-calculator/')
            html = html.replace('needdroptaxi.com/trip-fare-calculator', 'https://needdroptaxi.com/trip-fare-calculator')
            html = html.replace('https://https://', 'https://')
            
            soup = BeautifulSoup(html, 'html.parser')
            changed = False
            
            # Fix CTA buttons to point to /trip-fare-calculator/ and /taxi-booking/
            for a in soup.find_all('a'):
                href = a.get('href')
                if not href:
                    continue
                text = a.get_text(strip=True).lower()
                
                # Fix Trip Calculator buttons
                if 'try trip calculator' in text or 'calculate your trip fare' in text or 'trip calculator' in text:
                    if not href.startswith('#') and 'calculator' in href.lower():
                        a['href'] = '/trip-fare-calculator/'
                        changed = True
                
                # Fix Book Taxi buttons
                if text in ['book taxi', 'book now', 'book a taxi', 'reserve taxi']:
                    if not href.startswith('#') and 'tally.so' not in href: # Only fix non-external ones that aren't anchors
                        if 'booking' in href.lower() or 'book-taxi' in href.lower():
                            a['href'] = '/taxi-booking/'
                            changed = True
                elif text in ['book taxi', 'book now', 'book a taxi', 'reserve taxi'] and ('booking' in href.lower() or 'tally.so' in href.lower()):
                    a['href'] = '/taxi-booking/'
                    changed = True
                    
                # Ensure tally links point to /taxi-booking/ unless it's a specific instruction not to break it
                # The instruction says "Make sure all Book Taxi buttons ... point to /taxi-booking/".
                if href.startswith('https://tally.so/r/'):
                     a['href'] = '/taxi-booking/'
                     changed = True

                # Replace old HTTrack URLs or broken blog links if needed
                if href == '/top-10-tourist-attractions-to-visit-in-chennai-with-need-drop-taxi/':
                    a['href'] = '/blog/' # fallback or leave it
                    changed = True

            # Fix canonicals
            can = soup.find('link', rel='canonical')
            if can:
                # remove duplicated needdroptaxi.com if any
                can_href = can.get('href')
                if 'needdroptaxi.com/needdroptaxi.com' in can_href:
                    can['href'] = can_href.replace('needdroptaxi.com/needdroptaxi.com', 'needdroptaxi.com')
                    changed = True

            # Schema fixes
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    script_changed = False
                    
                    if isinstance(data, dict):
                        # Fix LocalBusiness Schema
                        if data.get('@type') == 'LocalBusiness':
                            if 'description' in data and '13/km' in data['description']:
                                data['description'] = data['description'].replace('13/km', '14/km')
                                script_changed = True
                            if 'hasOfferCatalog' in data:
                                for item in data['hasOfferCatalog'].get('itemListElement', []):
                                    offer = item.get('itemOffered', {})
                                    if offer.get('name') == 'Hatchback Outstation Service':
                                        item['price'] = "14"
                                        script_changed = True
                                    elif offer.get('name') == 'Sedan Outstation Service':
                                        item['price'] = "14"
                                        script_changed = True
                                    elif offer.get('name') == 'SUV Outstation Service':
                                        item['price'] = "19"
                                        script_changed = True
                        
                        # Fix FAQPage Schema
                        if data.get('@type') == 'FAQPage':
                            for entity in data.get('mainEntity', []):
                                ans = entity.get('acceptedAnswer', {}).get('text', '')
                                if '13/km' in ans:
                                    ans = ans.replace('13/km', '14/km')
                                    ans = ans.replace('18/km', '19/km')
                                    entity['acceptedAnswer']['text'] = ans
                                    script_changed = True
                                if '100 km' in ans:
                                    ans = ans.replace('100 km', '130 km')
                                    entity['acceptedAnswer']['text'] = ans
                                    script_changed = True

                    if script_changed:
                        script.string = json.dumps(data, separators=(',', ':'))
                        changed = True
                except:
                    pass

            # Update if changed
            if changed or True:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
