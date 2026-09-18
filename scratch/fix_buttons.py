import os
from bs4 import BeautifulSoup

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            changed = False
            
            for a in soup.find_all('a'):
                href = a.get('href')
                if not href: continue
                text = a.get_text(strip=True).lower()
                
                if 'try trip calculator' in text or 'calculate your trip fare' in text or 'trip calculator' in text or 'trip fare calculator' in text:
                    if href == '/trip-fare-calculator/' or href == 'https://needdroptaxi.com/trip-fare-calculator/':
                        a['href'] = 'https://needdroptaxi.com/trip-fare-calculator/'
                        changed = True
                        
                if text in ['book taxi', 'book now', 'book a taxi', 'reserve taxi', 'book taxi now']:
                    if href == '/taxi-booking/' or href == 'https://needdroptaxi.com/taxi-booking/':
                        a['href'] = 'https://needdroptaxi.com/taxi-booking/'
                        changed = True

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
