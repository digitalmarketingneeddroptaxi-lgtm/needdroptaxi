import re

files = ['index.html', r'outstation-taxi-service\index.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        print(f"\n--- {f} ---")
        links = re.findall(r'href="([^"]+)"', content)
        for l in set(links):
            if 'needdroptaxi' in l or 'calculator' in l or 'taxi-booking' in l:
                print(f"HREF: {l}")
        srcs = re.findall(r'src="([^"]+)"', content)
        for s in set(srcs):
            if 'needdroptaxi' in s or 'mockup' in s:
                print(f"SRC: {s}")
