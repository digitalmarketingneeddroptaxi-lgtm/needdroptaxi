from bs4 import BeautifulSoup
import re

with open(r'outstation-taxi-service\index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

with open(r'scratch\out_price.txt', 'w', encoding='utf-8') as out:
    out.write("--- VISIBLE TEXT ---\n")
    for tag in soup.find_all(['td', 'th', 'p', 'span', 'li', 'div', 'h3']):
        text = tag.get_text(separator=' ', strip=True)
        if 'km' in text.lower() or '?' in text or 'Rs' in text:
            out.write(text + "\n")
            
    out.write("\n--- SCHEMA ---\n")
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            out.write(s.string.strip() + "\n")
