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
                
                # Check for trip calculator
                if any(x in text for x in ['try trip calculator', 'calculate your trip fare', 'trip calculator', 'trip fare calculator']):
                    if 'calculator' in href:
                        if a['href'] != 'https://needdroptaxi.com/trip-fare-calculator/':
                            a['href'] = 'https://needdroptaxi.com/trip-fare-calculator/'
                            changed = True
                            
                # Check for book taxi
                if any(x in text for x in ['book taxi', 'book now', 'book a taxi', 'reserve taxi']):
                    if 'booking' in href or 'book-taxi' in href or 'tally' in href:
                        if a['href'] != 'https://needdroptaxi.com/taxi-booking/':
                            a['href'] = 'https://needdroptaxi.com/taxi-booking/'
                            changed = True

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
