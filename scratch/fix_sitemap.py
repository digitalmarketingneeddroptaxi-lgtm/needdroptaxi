import os
import xml.etree.ElementTree as ET

sitemap = r'c:\Users\Pathi\Documents\needdroptaxi.com\sitemap.xml'
tree = ET.parse(sitemap)
root = tree.getroot()
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

to_remove = []
for url in root.findall('ns:url', ns):
    loc = url.find('ns:loc', ns)
    if loc is not None:
        l = loc.text
        # rules for removing
        if 'needdroptaxi.com/needdroptaxi.com' in l or '?' in l or 'author' in l or 'cdn-cgi' in l or l.endswith('.html'):
            to_remove.append(url)
        elif not l.endswith('/') and not l.endswith('.xml') and not l.endswith('.txt'):
            # force trailing slash except for files
            loc.text = l + '/'
            
for url in to_remove:
    root.remove(url)

tree.write(sitemap, encoding='utf-8', xml_declaration=True)
