import glob
import re

out_of_range = []
for p in sorted(glob.glob('**/*.html', recursive=True)):
    if 'scratch' in p or '.system_generated' in p or 'email-protection' in p or 'pathi.html' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    # Match content enclosed in double quotes or single quotes accurately
    m = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content="([^"]*)"', c, re.DOTALL)
    if not m:
        m = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=\'([^\']*)\'', c, re.DOTALL)
    if not m:
        m = re.search(r'<meta\s+[^>]*content="([^"]*)"[^>]*name=["\']description["\']', c, re.DOTALL)
    if not m:
        m = re.search(r'<meta\s+[^>]*content=\'([^\']*)\'[^>]*name=["\']description["\']', c, re.DOTALL)
    if m:
        desc = m.group(1)
        l = len(desc)
        if l < 130 or l > 160:
            out_of_range.append((p, l, desc))
    else:
        out_of_range.append((p, 0, 'MISSING'))

print(f"Descriptions out of target range [130-160]: {len(out_of_range)}")
for item in out_of_range:
    print(f"  {item[0]} (length {item[1]}): {item[2]}")
