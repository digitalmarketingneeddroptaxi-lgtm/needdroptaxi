from bs4 import BeautifulSoup

with open(r'outstation-taxi-service\index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

with open(r'scratch\out_price.txt', 'w', encoding='utf-8') as out:
    out.write("--- VISIBLE TEXT ---\n")
    # Instead of just tr, let's find anything with ? or Rs or /km
    import re
    prices = soup.find_all(string=re.compile(r'(?|Rs|\/km)'))
    for p in prices:
        out.write(p.strip() + "\n")
        
    out.write("\n--- SCHEMA ---\n")
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            out.write(s.string.strip() + "\n")
