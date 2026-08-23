import re

with open(r"c:\Users\Pathi\Documents\needdroptaxi.com\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the <li> element that has x-on:mouseenter
match = re.search(r'<li x-on:mouseenter="taxiServicesOpen = true".*?</li>', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    # Just find taxiServicesOpen
    idx = content.find("taxiServicesOpen = true")
    if idx != -1:
        start = content.rfind("<li", 0, idx)
        end = content.find("</li>", idx) + 5
        print(content[start:end])
    else:
        print("Not found")
