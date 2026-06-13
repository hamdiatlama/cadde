import json, os
for f in sorted(os.listdir("modeller")):
    if f.endswith(".json"):
        with open(os.path.join("modeller", f)) as fh:
            data = json.load(fh)
        print(f'{data["marka"]}: {len(data["modeller"])} model')
