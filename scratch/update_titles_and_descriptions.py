import os
import re

metadata = {
    './index.html': {
        'title': 'Need Drop Taxi - Reliable Taxi Service in Chennai',
        'desc': 'Book affordable one-way drop taxis, outstation cabs, hourly rentals, and airport transfers in Chennai with Need Drop Taxi. 24/7 service & transparent fares.'
    },
    './about/index.html': {
        'title': 'About Us | Need Drop Taxi',
        'desc': "Learn about Need Drop Taxi, Tamil Nadu's trusted provider for one-way drop taxis, outstation trips, local rentals, and airport transfers with 24/7 support."
    },
    './contact/index.html': {
        'title': 'Contact Us | Need Drop Taxi',
        'desc': 'Contact Need Drop Taxi for bookings, rate inquiries, and 24/7 customer support. Call or WhatsApp 08122211865 or email contact@needdroptaxi.com anytime.'
    },
    './privacy-policy/index.html': {
        'title': 'Privacy Policy | Need Drop Taxi',
        'desc': 'Read the Need Drop Taxi Privacy Policy to understand how we collect, use, and protect your personal information during taxi bookings and website visits.'
    },
    './terms-and-conditions/index.html': {
        'title': 'Terms & Conditions | Need Drop Taxi',
        'desc': 'Review the terms and conditions for booking one-way drop taxis, outstation rides, and rental services with Need Drop Taxi. Transparent policies and fares.'
    },
    './trip-fare-calculator/index.html': {
        'title': 'Trip Fare Calculator | Need Drop Taxi',
        'desc': 'Calculate your one-way drop taxi and outstation cab fare instantly with Need Drop Taxi. Transparent per-km pricing with no hidden charges across South India.'
    },
    './taxi-booking/index.html': {
        'title': 'Book Taxi Online | Need Drop Taxi',
        'desc': 'Book your one-way drop taxi, outstation ride, or Chennai airport transfer online with Need Drop Taxi. Instant booking, transparent pricing, and 24/7 support.'
    },
    './thank-you-booking/index.html': {
        'title': 'Booking Confirmed | Need Drop Taxi',
        'desc': 'Thank you for booking with Need Drop Taxi. Your trip request has been received, and our team will contact you shortly to confirm your driver details.'
    },
    './airport-transfer-taxi-service/index.html': {
        'title': 'Airport Transfer Taxi Service | Need Drop Taxi',
        'desc': 'Reliable airport taxi transfers in Chennai. Punctual pickups and drop-offs at Chennai International Airport with professional drivers and clean vehicles.'
    },
    './local-rental-taxi-service/index.html': {
        'title': 'Local Rental Taxi Service | Need Drop Taxi',
        'desc': 'Explore Chennai with our flexible local rental taxi service. Hourly and daily packages available with verified drivers for shopping, meetings, and city tours.'
    },
    './outstation-taxi-service/index.html': {
        'title': 'Outstation Taxi Service | Need Drop Taxi',
        'desc': 'Reliable outstation taxi service from Chennai and across Tamil Nadu. One-way drop taxis and round trips starting at ₹13/km with no hidden charges.'
    },
    './blog/index.html': {
        'title': 'Travel Blog & Guides | Need Drop Taxi',
        'desc': 'Explore the Need Drop Taxi blog for South India travel tips, temple destination guides, road trip itineraries, and practical taxi booking advice.'
    },
    './blog/author/pathi/index.html': {
        'title': 'Pathi - Travel Expert | Need Drop Taxi Blog',
        'desc': 'Explore travel guides and South India transit tips by Pathi, travel expert at Need Drop Taxi. Practical insights for outstation routes and temple tours.'
    },
    './blog/best-places-to-visit-in-kanchipuram-with-need-drop-taxi/index.html': {
        'title': 'Best Places To Visit in Kanchipuram | Travel Guide',
        'desc': 'Explore the top places to visit in Kanchipuram, including historic temples and silk weaving centers. Plan your day trip from Chennai with Need Drop Taxi.'
    },
    './blog/celebrate-diwali-in-your-hometown-with-need-drop-taxi-outstation-rides/index.html': {
        'title': 'Celebrate Diwali with Outstation Rides | Need Drop Taxi',
        'desc': 'Travel stress-free to your hometown this Diwali with Need Drop Taxi outstation rides. Safe, on-time festival travel across Tamil Nadu and Bangalore.'
    },
    './blog/karthigai-deepam-festival-in-tiruvannamalai-with-need-drop-taxi/index.html': {
        'title': 'Karthigai Deepam in Tiruvannamalai | Need Drop Taxi',
        'desc': 'Experience the sacred Karthigai Deepam festival in Tiruvannamalai. Book a comfortable one-way or round-trip outstation taxi with Need Drop Taxi.'
    },
    './blog/top-10-tourist-attractions-to-visit-in-chennai-with-need-drop-taxi/index.html': {
        'title': 'Top 10 Tourist Attractions in Chennai | Travel Guide',
        'desc': "Discover Chennai's top 10 attractions, from Marina Beach to Kapaleeshwarar Temple. Enjoy flexible sightseeing with Need Drop Taxi local hourly rentals."
    },
    './blog/top-10-tourist-attractions-to-visit-in-kanyakumari/index.html': {
        'title': 'Top 10 Tourist Attractions in Kanyakumari | Travel Guide',
        'desc': 'Explore the top 10 attractions in Kanyakumari, from Vivekananda Rock to sunset viewpoints. Plan your coastal journey with Need Drop Taxi outstation cabs.'
    },
    './blog/top-10-tourist-attractions-to-visit-in-rameshwaram/index.html': {
        'title': 'Top 10 Tourist Attractions in Rameshwaram | Travel Guide',
        'desc': 'Discover must-visit sites in Rameshwaram, including Ramanathaswamy Temple, Dhanushkodi, and Pamban Bridge. Travel smoothly with Need Drop Taxi.'
    },
    './blog/why-choose-need-drop-taxi-for-your-chennai-exploration/index.html': {
        'title': 'Why Choose Need Drop Taxi for Chennai Sightseeing',
        'desc': 'Find out why Need Drop Taxi is the best choice for Chennai sightseeing, city commutes, and outstation trips. Transparent pricing and expert local drivers.'
    },
    # 23 Destination Routes
    './drop-taxi/bangalore-to-chennai/index.html': {
        'title': 'Bangalore to Chennai Taxi | One-Way Cab',
        'desc': 'Book Bangalore to Chennai drop taxi service. Fast highway travel along NH48, experienced drivers, doorstep pickup, and one-way rates with zero return fare.'
    },
    './drop-taxi/bangalore-to-coimbatore/index.html': {
        'title': 'Bangalore to Coimbatore Taxi | One-Way Cab',
        'desc': 'Book Bangalore to Coimbatore drop taxi service. Enjoy a smooth Salem-Erode highway journey, clean AC cars, professional drivers, and fair per-km pricing.'
    },
    './drop-taxi/chennai-to-bangalore/index.html': {
        'title': 'Chennai to Bangalore Taxi | One-Way Cab',
        'desc': 'Book Chennai to Bangalore drop taxi for business or leisure. Punctual 24/7 doorstep pickup, well-maintained cabs, and transparent one-way drop fares.'
    },
    './drop-taxi/chennai-to-madurai/index.html': {
        'title': 'Chennai to Madurai Taxi | One-Way Cab',
        'desc': 'Book Chennai to Madurai drop taxi via NH38. Reliable one-way cab service for family, business, or temple trips with transparent fares and no return fee.'
    },
    './drop-taxi/chennai-to-tirupati/index.html': {
        'title': 'Chennai to Tirupati Taxi | One-Way Cab',
        'desc': 'Book Chennai to Tirupati drop taxi for hassle-free temple darshan. Punctual doorstep pickup, clean air-conditioned vehicles, and transparent one-way pricing.'
    },
    './drop-taxi/chennai-to-tiruvannamalai/index.html': {
        'title': 'Chennai to Tiruvannamalai Taxi | One-Way Cab',
        'desc': 'Book Chennai to Tiruvannamalai drop taxi for Girivalam and Arunachaleswarar temple visits. Reliable one-way cab service with 24/7 support & clear fares.'
    },
    './drop-taxi/chennai-to-trichy/index.html': {
        'title': 'Chennai to Trichy Taxi | One-Way Cab',
        'desc': 'Book Chennai to Trichy drop taxi via NH45. Comfortable one-way outstation cab rides for Rockfort, Srirangam, and city travel with no hidden charges.'
    },
    './drop-taxi/coimbatore-to-bangalore/index.html': {
        'title': 'Coimbatore to Bangalore Taxi | One-Way Cab',
        'desc': 'Book Coimbatore to Bangalore drop taxi service. Fast, comfortable interstate travel via NH544/NH44 with professional drivers and transparent one-way pricing.'
    },
    './drop-taxi/kanyakumari-to-madurai/index.html': {
        'title': 'Kanyakumari to Madurai Taxi | One-Way Cab',
        'desc': 'Book Kanyakumari to Madurai drop taxi via NH44. Enjoy smooth highway travel from the southern coast to the temple city with clean cabs and one-way rates.'
    },
    './drop-taxi/kanyakumari-to-rameshwaram/index.html': {
        'title': 'Kanyakumari to Rameshwaram Taxi | One-Way Cab',
        'desc': 'Book Kanyakumari to Rameshwaram drop taxi for scenic coastal temple journeys. Reliable cabs, punctual drivers, and transparent one-way outstation fares.'
    },
    './drop-taxi/madurai-to-chennai/index.html': {
        'title': 'Madurai to Chennai Taxi | One-Way Cab',
        'desc': 'Book Madurai to Chennai drop taxi via NH38. Safe long-distance highway travel, 24/7 service, professional chauffeurs, and transparent one-way drop pricing.'
    },
    './drop-taxi/madurai-to-kanyakumari/index.html': {
        'title': 'Madurai to Kanyakumari Taxi | One-Way Cab',
        'desc': 'Book Madurai to Kanyakumari drop taxi service. Seamless highway trip via Tirunelveli on NH44 with comfortable AC cabs, expert drivers, and one-way fares.'
    },
    './drop-taxi/madurai-to-rameshwaram/index.html': {
        'title': 'Madurai to Rameshwaram Taxi | One-Way Cab',
        'desc': 'Book Madurai to Rameshwaram drop taxi for Ramanathaswamy temple darshan. Pamban bridge route, punctual pickups, clean vehicles, and transparent one-way fares.'
    },
    './drop-taxi/madurai-to-thoothukudi/index.html': {
        'title': 'Madurai to Thoothukudi Taxi | One-Way Cab',
        'desc': 'Book Madurai to Thoothukudi drop taxi via NH38. Fast and convenient one-way cab rides for port, business, or family travel at transparent per-km rates.'
    },
    './drop-taxi/madurai-to-tiruchendur/index.html': {
        'title': 'Madurai to Tiruchendur Taxi | One-Way Cab',
        'desc': 'Book Madurai to Tiruchendur drop taxi for Subramaniya Swamy temple pilgrimage. Prompt pickups, well-maintained cars, and transparent one-way taxi fares.'
    },
    './drop-taxi/madurai-to-tirunelveli/index.html': {
        'title': 'Madurai to Tirunelveli Taxi | One-Way Cab',
        'desc': 'Book Madurai to Tirunelveli drop taxi via NH44. Quick, comfortable rides, professional drivers, and transparent one-way pricing with zero return fare.'
    },
    './drop-taxi/rameshwaram-to-kanyakumari/index.html': {
        'title': 'Rameshwaram to Kanyakumari Taxi | One-Way Cab',
        'desc': 'Book Rameshwaram to Kanyakumari drop taxi. Ideal for South India pilgrimage circuits with courteous drivers, clean vehicles, and transparent one-way fares.'
    },
    './drop-taxi/rameshwaram-to-madurai/index.html': {
        'title': 'Rameshwaram to Madurai Taxi | One-Way Cab',
        'desc': 'Book Rameshwaram to Madurai drop taxi service. Hassle-free post-darshan return travel, punctual pickups, clean vehicles, and transparent per-km rates.'
    },
    './drop-taxi/thoothukudi-to-madurai/index.html': {
        'title': 'Thoothukudi to Madurai Taxi | One-Way Cab',
        'desc': 'Book Thoothukudi to Madurai drop taxi via NH38. Reliable one-way cab service for airport, hospital, and business trips with transparent per-km pricing.'
    },
    './drop-taxi/tiruchendur-to-madurai/index.html': {
        'title': 'Tiruchendur to Madurai Taxi | One-Way Cab',
        'desc': 'Book Tiruchendur to Madurai drop taxi service. Relaxing post-temple journey with courteous drivers, clean air-conditioned cabs, and one-way drop fares.'
    },
    './drop-taxi/tirunelveli-to-madurai/index.html': {
        'title': 'Tirunelveli to Madurai Taxi | One-Way Cab',
        'desc': 'Book Tirunelveli to Madurai drop taxi via NH44. Reliable, on-time one-way cab service with verified drivers, clean cars, and transparent per-km pricing.'
    },
    './drop-taxi/tirupati-to-chennai/index.html': {
        'title': 'Tirupati to Chennai Taxi | One-Way Cab',
        'desc': 'Book Tirupati to Chennai drop taxi after your temple visit. Comfortable one-way cab service, courteous drivers, 24/7 availability, and transparent fares.'
    },
    './drop-taxi/trichy-to-chennai/index.html': {
        'title': 'Trichy to Chennai Taxi | One-Way Cab',
        'desc': 'Book Trichy to Chennai drop taxi via Grand Southern Trunk Rd (NH45). Safe highway travel, clean cabs, punctual service, and affordable one-way drop fares.'
    }
}

for file_path, data in metadata.items():
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        continue
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    new_title = data['title']
    new_desc = data['desc']
    
    # Replace <title>
    content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content, count=1, flags=re.DOTALL)
    
    # Replace <meta name="description" content="...">
    if re.search(r'<meta\s+name=[\'"]description[\'"]', content):
        content = re.sub(
            r'<meta\s+name=[\'"]description[\'"]\s+content=[\'"].*?[\'"]',
            f'<meta name="description" content="{new_desc}"',
            content,
            count=1,
            flags=re.DOTALL
        )
    elif re.search(r'<meta\s+content=[\'"].*?[\'"]\s+name=[\'"]description[\'"]', content):
        content = re.sub(
            r'<meta\s+content=[\'"].*?[\'"]\s+name=[\'"]description[\'"]',
            f'<meta name="description" content="{new_desc}"',
            content,
            count=1,
            flags=re.DOTALL
        )
    
    # Also update Open Graph & Twitter meta tags if present
    content = re.sub(
        r'<meta\s+property=[\'"]og:title[\'"]\s+content=[\'"].*?[\'"]',
        f'<meta property="og:title" content="{new_title}"',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<meta\s+property=[\'"]og:description[\'"]\s+content=[\'"].*?[\'"]',
        f'<meta property="og:description" content="{new_desc}"',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<meta\s+name=[\'"]twitter:title[\'"]\s+content=[\'"].*?[\'"]',
        f'<meta name="twitter:title" content="{new_title}"',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<meta\s+name=[\'"]twitter:description[\'"]\s+content=[\'"].*?[\'"]',
        f'<meta name="twitter:description" content="{new_desc}"',
        content,
        flags=re.DOTALL
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {file_path} -> Title ({len(new_title)}): {new_title} | Desc ({len(new_desc)}): {new_desc[:40]}...")

print(f"\nSuccessfully updated {len(metadata)} pages.")
