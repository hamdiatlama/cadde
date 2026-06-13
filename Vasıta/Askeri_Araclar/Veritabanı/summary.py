import json, os

total = 0
files = []
for f in os.listdir("modeller"):
    if f.endswith(".json"):
        with open(os.path.join("modeller", f)) as fh:
            files.append((f, json.load(fh)))

files.sort()
for fn, d in files:
    cnt = len(d["modeller"])
    print(f'{d["marka"]:25s} {cnt:4d} model')
    total += cnt

print(f'---')
print(f'TOPLAM: {len(files)} marka, {total} model')
