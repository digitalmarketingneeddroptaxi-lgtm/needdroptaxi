import os

related_links = {
    'blog/best-places-to-visit-in-kanchipuram-with-need-drop-taxi/index.html': [
        ('/blog/why-choose-need-drop-taxi-for-your-chennai-exploration/', 'Why Choose Need Drop Taxi for Chennai Exploration'),
        ('/blog/top-10-tourist-attractions-to-visit-in-chennai-with-need-drop-taxi/', 'Top 10 Tourist Attractions in Chennai'),
        ('/outstation-taxi-service/', 'Outstation Taxi Service in Tamil Nadu'),
        ('/trip-fare-calculator/', 'Calculate Trip Fares Instantly')
    ],
    'blog/celebrate-diwali-in-your-hometown-with-need-drop-taxi-outstation-rides/index.html': [
        ('/blog/karthigai-deepam-festival-in-tiruvannamalai-with-need-drop-taxi/', 'Karthigai Deepam Festival in Tiruvannamalai'),
        ('/drop-taxi/bangalore-to-chennai/', 'Bangalore to Chennai Drop Taxi'),
        ('/outstation-taxi-service/', 'Comfortable Outstation Rides'),
        ('/trip-fare-calculator/', 'Calculate Festival Trip Fare')
    ],
    'blog/karthigai-deepam-festival-in-tiruvannamalai-with-need-drop-taxi/index.html': [
        ('/drop-taxi/chennai-to-tiruvannamalai/', 'Chennai to Tiruvannamalai Drop Taxi'),
        ('/blog/celebrate-diwali-in-your-hometown-with-need-drop-taxi-outstation-rides/', 'Diwali Outstation Festival Rides'),
        ('/blog/top-10-tourist-attractions-to-visit-in-rameshwaram/', 'Top 10 Attractions in Rameshwaram'),
        ('/trip-fare-calculator/', 'Trip Fare Calculator')
    ],
    'blog/top-10-tourist-attractions-to-visit-in-chennai-with-need-drop-taxi/index.html': [
        ('/blog/why-choose-need-drop-taxi-for-your-chennai-exploration/', 'Why Choose Need Drop Taxi for Chennai Exploration'),
        ('/blog/best-places-to-visit-in-kanchipuram-with-need-drop-taxi/', 'Best Places to Visit in Kanchipuram'),
        ('/local-rental-taxi-service/', 'Hourly Local Rental Taxi Service'),
        ('/airport-transfer-taxi-service/', 'Chennai Airport Transfer Taxi')
    ],
    'blog/top-10-tourist-attractions-to-visit-in-kanyakumari/index.html': [
        ('/blog/top-10-tourist-attractions-to-visit-in-rameshwaram/', 'Top 10 Tourist Attractions in Rameshwaram'),
        ('/drop-taxi/madurai-to-kanyakumari/', 'Madurai to Kanyakumari Taxi'),
        ('/drop-taxi/kanyakumari-to-rameshwaram/', 'Kanyakumari to Rameshwaram Taxi'),
        ('/trip-fare-calculator/', 'Trip Fare Calculator')
    ],
    'blog/top-10-tourist-attractions-to-visit-in-rameshwaram/index.html': [
        ('/blog/top-10-tourist-attractions-to-visit-in-kanyakumari/', 'Top 10 Tourist Attractions in Kanyakumari'),
        ('/drop-taxi/madurai-to-rameshwaram/', 'Madurai to Rameshwaram Taxi'),
        ('/drop-taxi/rameshwaram-to-madurai/', 'Rameshwaram to Madurai Taxi'),
        ('/trip-fare-calculator/', 'Trip Fare Calculator')
    ],
    'blog/why-choose-need-drop-taxi-for-your-chennai-exploration/index.html': [
        ('/blog/top-10-tourist-attractions-to-visit-in-chennai-with-need-drop-taxi/', 'Top 10 Tourist Attractions in Chennai'),
        ('/blog/best-places-to-visit-in-kanchipuram-with-need-drop-taxi/', 'Best Places to Visit in Kanchipuram'),
        ('/local-rental-taxi-service/', 'Local Rental Taxi Service'),
        ('/trip-fare-calculator/', 'Estimate Your Trip Fare')
    ]
}

for file_path, links in related_links.items():
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if 'Related Travel Guides' in content:
        print(f"Already has related guides: {file_path}")
        continue

    # Build HTML block
    cards_html = '\n'.join([
        f'      <li class="p-3 bg-white rounded-lg shadow-sm border border-gray-200 hover:border-yellow-400 transition-colors">'
        f'<a href="{url}" class="text-blue-700 font-semibold hover:underline flex items-center gap-2">'
        f'<span class="text-yellow-500">?</span> {anchor}</a></li>'
        for url, anchor in links
    ])

    block = f'''
    <section class="not-prose my-10 p-6 bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-2xl shadow-sm">
      <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <span>?</span> Related Travel Guides &amp; Popular Routes
      </h3>
      <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3 list-none p-0 m-0">
{cards_html}
      </ul>
    </section>
'''

    # Insert before </article>
    if '</article>' in content:
        content = content.replace('</article>', f'{block}\n</article>', 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Related Guides to: {file_path}")
    else:
        print(f"Warning: </article> not found in {file_path}")

print("Done updating related guides.")
