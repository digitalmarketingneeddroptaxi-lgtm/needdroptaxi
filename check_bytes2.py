import os

file = r"c:\Users\Pathi\Documents\needdroptaxi.com\privacy-policy\index.html"
with open(file, 'rb') as f:
    content = f.read()

idx = content.find(b"Company")
print("Around Company:", content[idx-15:idx+25])

idx_cp = content.find(b"Copyright")
print("Around Copyright:", content[idx_cp:idx_cp+30])

file2 = r"c:\Users\Pathi\Documents\needdroptaxi.com\terms-and-conditions\index.html"
with open(file2, 'rb') as f:
    content2 = f.read()

idx2_cp = content2.find(b"Copyright")
print("Around Copyright 2:", content2[idx2_cp:idx2_cp+30])
