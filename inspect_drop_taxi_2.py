import os
file_path = r"c:\Users\Pathi\Documents\needdroptaxi.com\drop-taxi\chennai-to-tirupati\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Look for all 2,410
indices = [i for i in range(len(content)) if content.startswith("2,410", i)]
for idx in indices:
    print(content[max(0, idx-30):min(len(content), idx+30)])
