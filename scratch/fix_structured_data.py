import os
import re
import json

html_files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root or '.system_generated' in root:
        continue
    for f in files_list:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

print(f"Auditing and fixing structured data across {len(html_files)} files...")

updated_files = 0

for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    orig = content

    # Find all ld+json blocks
    def replace_schema(match):
        raw_json = match.group(1).strip()
        try:
            data = json.loads(raw_json)
        except Exception as e:
            print(f"Error decoding JSON in {p}: {e}")
            return match.group(0)

        modified = False

        # Helper recursive cleaner
        def clean_item(item):
            nonlocal modified
            if not isinstance(item, dict):
                return item

            # 1. Fix LocalBusiness & Organization
            if item.get('@type') in ['LocalBusiness', 'TaxiService', 'AutoRental', 'Organization']:
                # Remove fake aggregateRating
                if 'aggregateRating' in item:
                    del item['aggregateRating']
                    modified = True
                # Remove fake review
                if 'review' in item:
                    del item['review']
                    modified = True
                # Fix corrupted priceRange
                if item.get('priceRange') in ['??', '?', '', None]:
                    item['priceRange'] = '₹₹'
                    modified = True
                # Fix address if list
                if isinstance(item.get('address'), list):
                    item['address'] = {
                        "@type": "PostalAddress",
                        "streetAddress": "2/59, Manikandan Nagar, Hasthinapuram, Chrompet",
                        "addressLocality": "Chennai",
                        "addressRegion": "Tamil Nadu",
                        "postalCode": "600044",
                        "addressCountry": "IN"
                    }
                    modified = True
                # Fix HTML entities in description
                if 'description' in item and '&#8377;' in item['description']:
                    item['description'] = item['description'].replace('&#8377;', '₹')
                    modified = True

            # 2. Fix BlogPosting datePublished & dateModified
            if item.get('@type') in ['BlogPosting', 'Article']:
                if item.get('datePublished') == '02 Apr, 2025':
                    item['datePublished'] = '2025-04-02'
                    modified = True
                if item.get('dateModified') == '02 Apr, 2025':
                    item['dateModified'] = '2025-04-02'
                    modified = True

            # 3. Fix BreadcrumbList
            if item.get('@type') == 'BreadcrumbList':
                elements = item.get('itemListElement', [])
                for el in elements:
                    if el.get('position') == 1 and el.get('item') == 'https://needdroptaxi.com':
                        el['item'] = 'https://needdroptaxi.com/'
                        modified = True
                    # Fix /drop-taxi/ 404 in route pages
                    if el.get('position') == 2 and el.get('item') == 'https://needdroptaxi.com/drop-taxi/':
                        el['name'] = 'Outstation Taxi'
                        el['item'] = 'https://needdroptaxi.com/outstation-taxi-service/'
                        modified = True
                    # Normalize any item without trailing slash
                    if isinstance(el.get('item'), str) and el['item'].startswith('https://needdroptaxi.com'):
                        u = el['item']
                        if not u.endswith('/') and not '.' in u.split('/')[-1]:
                            el['item'] = u + '/'
                            modified = True

            # Recursively process children
            for k, v in list(item.items()):
                if isinstance(v, dict):
                    clean_item(v)
                elif isinstance(v, list):
                    for elem in v:
                        if isinstance(elem, dict):
                            clean_item(elem)

            return item

        # Special handling for thank-you-booking
        if 'thank-you-booking' in p and data.get('@type') == 'WebPage':
            # Remove the conflicting fake Service offer
            clean_schema = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": "Booking Confirmed",
                "description": "Thank you for booking with Need Drop Taxi. Your booking request has been received.",
                "url": "https://needdroptaxi.com/thank-you-booking/",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://needdroptaxi.com/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Booking Confirmed",
                            "item": "https://needdroptaxi.com/thank-you-booking/"
                        }
                    ]
                }
            }
            return f'<script type="application/ld+json">{json.dumps(clean_schema, ensure_ascii=False, separators=(",", ":"))}</script>'

        data = clean_item(data)

        if modified:
            return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
        else:
            return match.group(0)

    content = re.sub(
        r'<script\s+type=[\'"]application/ld\+json[\'"]\s*>(.*?)</script>',
        replace_schema,
        content,
        flags=re.DOTALL
    )

    # If trip-fare-calculator doesn't have a BreadcrumbList schema, add it!
    if 'trip-fare-calculator' in p and 'application/ld+json' not in content:
        calculator_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://needdroptaxi.com/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Trip Fare Calculator",
                    "item": "https://needdroptaxi.com/trip-fare-calculator/"
                }
            ]
        }
        schema_tag = f'\n<script type="application/ld+json">{json.dumps(calculator_schema, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        content = content.replace('</head>', f'{schema_tag}</head>', 1)

    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_files += 1
        print(f"Updated schema in: {p}")

print(f"Total files updated for schema: {updated_files}")
