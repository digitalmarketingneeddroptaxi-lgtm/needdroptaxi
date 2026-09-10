import os
import re

routes = [
    'bangalore-to-chennai',
    'bangalore-to-coimbatore',
    'chennai-to-bangalore',
    'chennai-to-madurai',
    'chennai-to-tirupati',
    'chennai-to-tiruvannamalai',
    'chennai-to-trichy',
    'coimbatore-to-bangalore',
    'kanyakumari-to-madurai',
    'kanyakumari-to-rameshwaram',
    'madurai-to-chennai',
    'madurai-to-kanyakumari',
    'madurai-to-rameshwaram',
    'madurai-to-thoothukudi',
    'madurai-to-tiruchendur',
    'madurai-to-tirunelveli',
    'rameshwaram-to-kanyakumari',
    'rameshwaram-to-madurai',
    'thoothukudi-to-madurai',
    'tiruchendur-to-madurai',
    'tirunelveli-to-madurai',
    'tirupati-to-chennai',
    'trichy-to-chennai'
]

html_files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root or '.system_generated' in root:
        continue
    for f in files_list:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

print(f"Fixing internal links across {len(html_files)} files...")

updated_count = 0

for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    orig = content

    # 1. Fix /../ in links
    content = re.sub(r'href=[\'"]/+\.\./*[\'"]', 'href="/"', content)

    # 2. Fix /author/pathi/ -> /blog/author/pathi/
    content = re.sub(r'href=[\'"]/author/pathi/*[\'"]', 'href="/blog/author/pathi/"', content)

    # 3. Fix all 23 routes without /drop-taxi/ prefix
    for r in routes:
        # Match href="/route/" or href="/route" but NOT href="/drop-taxi/route"
        # We can use negative lookbehind or replace exact pattern
        content = re.sub(r'href=[\'"]/' + re.escape(r) + r'/?[\'"]', f'href="/drop-taxi/{r}/"', content)

    # 4. Contextual cross-linking:
    # A) In blog posts, add contextual links if not present
    if 'blog/top-10-tourist-attractions-to-visit-in-kanyakumari' in p:
        if '/drop-taxi/madurai-to-kanyakumari/' not in content:
            content = content.replace(
                'Plan your perfect trip with Need Drop Taxi.',
                'Plan your journey with our <a href="/drop-taxi/madurai-to-kanyakumari/" class="text-blue-600 underline hover:text-blue-800">Madurai to Kanyakumari taxi</a> or explore the coastal route via <a href="/drop-taxi/kanyakumari-to-rameshwaram/" class="text-blue-600 underline hover:text-blue-800">Kanyakumari to Rameshwaram taxi</a>. You can also estimate your trip fare instantly with our <a href="/trip-fare-calculator/" class="text-blue-600 underline hover:text-blue-800">Trip Fare Calculator</a>.'
            )

    if 'blog/top-10-tourist-attractions-to-visit-in-rameshwaram' in p:
        if '/drop-taxi/madurai-to-rameshwaram/' not in content:
            content = content.replace(
                'Plan your journey with Need Drop Taxi to make the most of your visit.',
                'Plan your trip with our reliable <a href="/drop-taxi/madurai-to-rameshwaram/" class="text-blue-600 underline hover:text-blue-800">Madurai to Rameshwaram taxi</a> or return conveniently with our <a href="/drop-taxi/rameshwaram-to-madurai/" class="text-blue-600 underline hover:text-blue-800">Rameshwaram to Madurai drop taxi</a>. Check transparent pricing using our <a href="/trip-fare-calculator/" class="text-blue-600 underline hover:text-blue-800">Trip Fare Calculator</a>.'
            )

    if 'blog/karthigai-deepam-festival-in-tiruvannamalai' in p:
        if '/drop-taxi/chennai-to-tiruvannamalai/' not in content:
            content = content.replace(
                'Book your ride today with Need Drop Taxi',
                'Book your ride today with our <a href="/drop-taxi/chennai-to-tiruvannamalai/" class="text-blue-600 underline hover:text-blue-800">Chennai to Tiruvannamalai drop taxi</a> or learn about our comprehensive <a href="/outstation-taxi-service/" class="text-blue-600 underline hover:text-blue-800">Outstation Taxi Service</a>. Plan ahead using our <a href="/trip-fare-calculator/" class="text-blue-600 underline hover:text-blue-800">Trip Fare Calculator</a>'
            )

    if 'blog/top-10-tourist-attractions-to-visit-in-chennai' in p:
        if '/airport-transfer-taxi-service/' not in content:
            content = content.replace(
                'using Need Drop Taxi.',
                'using Need Drop Taxi. Arriving by flight? Book our prompt <a href="/airport-transfer-taxi-service/" class="text-blue-600 underline hover:text-blue-800">Airport Transfer Taxi Service</a> or reserve a city ride with our <a href="/local-rental-taxi-service/" class="text-blue-600 underline hover:text-blue-800">Local Rental Taxi Service</a>.'
            )

    # B) In destination pages, link back to related guides
    if p.endswith('drop-taxi/madurai-to-rameshwaram/index.html') or p.endswith('drop-taxi/rameshwaram-to-madurai/index.html'):
        if '/blog/top-10-tourist-attractions-to-visit-in-rameshwaram/' not in content:
            callout = '<div class="my-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r text-gray-800"><strong>Travel Guide:</strong> Planning your pilgrimage? Read our curated guide on the <a href="/blog/top-10-tourist-attractions-to-visit-in-rameshwaram/" class="text-blue-600 underline hover:text-blue-800">Top 10 Tourist Attractions to Visit in Rameshwaram</a>.</div>'
            # insert before popular routes section
            content = content.replace('<section class="py-16 bg-gradient-to-t', callout + '\n<section class="py-16 bg-gradient-to-t', 1)

    if p.endswith('drop-taxi/madurai-to-kanyakumari/index.html') or p.endswith('drop-taxi/kanyakumari-to-madurai/index.html'):
        if '/blog/top-10-tourist-attractions-to-visit-in-kanyakumari/' not in content:
            callout = '<div class="my-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r text-gray-800"><strong>Travel Guide:</strong> Exploring the southern tip of India? Check out our <a href="/blog/top-10-tourist-attractions-to-visit-in-kanyakumari/" class="text-blue-600 underline hover:text-blue-800">Top 10 Tourist Attractions in Kanyakumari Guide</a>.</div>'
            content = content.replace('<section class="py-16 bg-gradient-to-t', callout + '\n<section class="py-16 bg-gradient-to-t', 1)

    if p.endswith('drop-taxi/chennai-to-tiruvannamalai/index.html'):
        if '/blog/karthigai-deepam-festival-in-tiruvannamalai-with-need-drop-taxi/' not in content:
            callout = '<div class="my-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r text-gray-800"><strong>Festival Guide:</strong> Visiting for Girivalam or festival darshan? Read our guide on <a href="/blog/karthigai-deepam-festival-in-tiruvannamalai-with-need-drop-taxi/" class="text-blue-600 underline hover:text-blue-800">Experiencing Karthigai Deepam in Tiruvannamalai</a>.</div>'
            content = content.replace('<section class="py-16 bg-gradient-to-t', callout + '\n<section class="py-16 bg-gradient-to-t', 1)

    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1
        print(f"Updated internal links in: {p}")

print(f"\nInternal links updated in {updated_count} files.")
