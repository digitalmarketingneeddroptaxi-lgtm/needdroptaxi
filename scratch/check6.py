import codecs
with codecs.open('scan_results.txt', 'r', 'utf-16le', errors='ignore') as f:
    for line in f:
        if 'index.html' in line or 'BROKEN_INTERNAL_LINK' in line:
            print(line.strip().encode('ascii', 'ignore').decode('ascii'))
