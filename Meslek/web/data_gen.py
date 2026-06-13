import os, re, json, sys
sys.stdout.reconfigure = lambda encoding='utf-8', errors='replace': None

BASE = r"C:\Users\Hamdi Atlama\Downloads\Veri Tabanıları\Meslek"

CATEGORIES = [
    ("🏥", "Sağlık ve Tıp", "meslek_tablosu.md"),
    ("🏗️", "Mühendislik ve Teknik", "tablo.md"),
    ("💻", "Bilişim ve Teknoloji", "tablo.md"),
    ("📚", "Eğitim ve Akademi", "tablo.md"),
    ("⚖️", "Hukuk ve Adalet", "tablo.md"),
    ("💰", "İş ve Finans", "tablo.md"),
    ("🎨", "Sanat, Medya ve Eğlence", "tablo.md"),
    ("🏭", "Sanayi ve Üretim", "tablo.md"),
    ("🌾", "Tarım ve Hayvancılık", "tablo.md"),
    ("🍽️", "Gıda ve İçecek", "tablo.md"),
    ("🚚", "Ulaşım ve Lojistik", "tablo.md"),
    ("🏛️", "Kamu ve Yönetim", "tablo.md"),
    ("🛍️", "Perakende ve Satış", "tablo.md"),
    ("🏗️", "İnşaat ve Yapı", "tablo.md"),
    ("🧹", "Hizmet ve Bakım", "tablo.md"),
    ("💼", "Danışmanlık ve Profesyonel Hizmetler", "tablo.md"),
]

def find_folder(emoji, name):
    for d in os.listdir(BASE):
        dpath = os.path.join(BASE, d)
        if os.path.isdir(dpath) and (emoji in d or name[:8] in d):
            return dpath
    return None

def generate_data():
    all_categories = []
    all_professions = []
    pid = 1

    for cat_id, (emoji, name, fname) in enumerate(CATEGORIES, 1):
        all_categories.append({"id": cat_id, "name": name, "emoji": emoji, "sort_order": cat_id})
        folder = find_folder(emoji, name)
        if not folder:
            continue
        fpath = os.path.join(folder, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        if name == "Sağlık ve Tıp":
            seen = set()
            for line in text.split('\n'):
                m = re.match(r'\|\s*\d+\s*\|[^|]*\|[^|]*\|\s*(.+?)\s*\|', line)
                if m:
                    items = [x.strip() for x in m.group(1).split(',')]
                    for item in items:
                        item = re.sub(r'\([^)]*\)', '', item).strip()
                        if item and len(item) > 2 and item.lower() not in seen:
                            seen.add(item.lower())
                            all_professions.append({"id": pid, "name": item, "category_id": cat_id})
                            pid += 1
        else:
            profs = re.findall(r'\|\s*\d+\s*\|\s*(.+?)\s*\|', text)
            for p in profs:
                p = p.strip()
                if p and not p.startswith("#") and not p.startswith("Meslek"):
                    all_professions.append({"id": pid, "name": p, "category_id": cat_id})
                    pid += 1

    out = {"categories": all_categories, "professions": all_professions}
    out_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"data.json olusturuldu: {len(all_categories)} kategori, {len(all_professions)} meslek")

if __name__ == "__main__":
    generate_data()
