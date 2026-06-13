import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

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

def parse_professions(text, is_health=False):
    if is_health:
        profs = []
        for line in text.split('\n'):
            m = re.match(r'\|\s*\d+\s*\|[^|]*\|[^|]*\|\s*(.+?)\s*\|', line)
            if m:
                items = [x.strip() for x in m.group(1).split(',')]
                for item in items:
                    item = re.sub(r'\([^)]*\)', '', item).strip()
                    if item and len(item) > 2:
                        profs.append(item)
        return profs
    else:
        profs = re.findall(r'\|\s*\d+\s*\|\s*(.+?)\s*\|', text)
        cleaned = []
        for p in profs:
            p = p.strip()
            if p and not p.startswith("#") and not p.startswith("Meslek"):
                cleaned.append(p)
        return cleaned

all_data = []
for emoji, name, fname in CATEGORIES:
    folder = find_folder(emoji, name)
    if not folder:
        continue
    fpath = os.path.join(folder, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    is_health = (name == "Sağlık ve Tıp")
    profs = parse_professions(text, is_health)
    uniq = []
    seen = set()
    for p in profs:
        if p.lower() not in seen:
            seen.add(p.lower())
            uniq.append(p)
    all_data.append((emoji, name, uniq))
    print(f"{name}: {len(uniq)} meslek")

sql = """-- ============================================================
-- MESLEKLER VERiTABANI - PostgreSQL
-- ============================================================

-- Once mevcut veritabanini silip olustur
DROP DATABASE IF EXISTS meslekler;
CREATE DATABASE meslekler;
\\c meslekler;

-- Kategoriler tablosu
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    emoji VARCHAR(10),
    sort_order INT NOT NULL
);

-- Meslekler tablosu
CREATE TABLE professions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE
);

CREATE INDEX idx_professions_category ON professions(category_id);
CREATE INDEX idx_professions_name ON professions(name);

-- Kategorileri ekle
INSERT INTO categories (id, name, emoji, sort_order) VALUES
"""

for i, (emoji, name, _) in enumerate(all_data, 1):
    comma = "," if i < len(all_data) else ";"
    sql += f"    ({i}, '{name}', '{emoji}', {i}){comma}\n"

pid = 1
for cat_id, (emoji, name, profs) in enumerate(all_data, 1):
    for p in profs:
        safe_p = p.replace("'", "''")
        sql += f"INSERT INTO professions (id, name, category_id) VALUES ({pid}, '{safe_p}', {cat_id});\n"
        pid += 1

sql += """
-- Ornek sorgular
-- SELECT * FROM categories ORDER BY sort_order;
-- SELECT p.name FROM professions p JOIN categories c ON p.category_id = c.id WHERE c.id = 1;
-- SELECT * FROM professions WHERE name ILIKE '%muhendis%';
-- SELECT c.name, COUNT(*) FROM professions p JOIN categories c ON p.category_id = c.id GROUP BY c.name;
"""

sql_path = os.path.join(BASE, "web", "veritabani_postgresql.sql")
with open(sql_path, "w", encoding="utf-8") as f:
    f.write(sql)
print(f"\nSQL dosyasi olusturuldu: {sql_path}")
print(f"Toplam: {len(all_data)} kategori, {pid-1} meslek")
