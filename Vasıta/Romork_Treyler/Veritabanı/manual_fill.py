# Römork & Treyler - Manuel Model Verileri
# Bu dosyayı çalıştırmak için: python manual_fill.py

import json, os

DATA = {
    "Böckmann": [
        {"model": "Timber 2000", "kasa_tipleri": ["Araba Römorku"], "uretim_baslangic": 2018},
        {"model": "Timber 2700", "kasa_tipleri": ["Araba Römorku"], "uretim_baslangic": 2019},
        {"model": "Timber 3200", "kasa_tipleri": ["Araba Römorku"], "uretim_baslangic": 2020},
        {"model": "Alpin", "kasa_tipleri": ["Motorsiklet Römorku"], "uretim_baslangic": 2019},
        {"model": "Topline", "kasa_tipleri": ["Kapalı Römork"], "uretim_baslangic": 2017},
        {"model": "TipLine", "kasa_tipleri": ["Damperli Römork"], "uretim_baslangic": 2018},
        {"model": "Pony", "kasa_tipleri": ["Mini Römork"], "uretim_baslangic": 2016},
    ],
    "Derman Treyler": [
        {"model": "Dorito", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2018},
        {"model": "Dorise", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2019},
        {"model": "Dokum", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2018},
        {"model": "Doreks", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2020},
        {"model": "Doreks Mega", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2021},
        {"model": "Dokum Flat", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2020},
        {"model": "Dokum Step", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2021},
    ],
    "Fliegl": [
        {"model": "ASW 271", "kasa_tipleri": ["Tarım Römorku"], "uretim_baslangic": 2016},
        {"model": "ASS 260", "kasa_tipleri": ["Tarım Römorku"], "uretim_baslangic": 2017},
        {"model": "Tandem", "kasa_tipleri": ["Tarım Römorku"], "uretim_baslangic": 2015},
        {"model": "Tridem", "kasa_tipleri": ["Tarım Römorku"], "uretim_baslangic": 2016},
        {"model": "Container", "kasa_tipleri": ["Konteyner"], "uretim_baslangic": 2018},
        {"model": "Flatbed", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2017},
    ],
    "Kaksan": [
        {"model": "Tanker", "kasa_tipleri": ["Tank"], "uretim_baslangic": 2015},
        {"model": "Silobas", "kasa_tipleri": ["Silobas"], "uretim_baslangic": 2015},
        {"model": "Flatbed", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2016},
        {"model": "Konteyner", "kasa_tipleri": ["Konteyner"], "uretim_baslangic": 2015},
        {"model": "Dorse", "kasa_tipleri": ["Yarı Römork"], "uretim_baslangic": 2015},
        {"model": "Lowbed", "kasa_tipleri": ["Düşük Yataklı"], "uretim_baslangic": 2016},
    ],
    "Krone": [
        {"model": "Cool Liner", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2016},
        {"model": "Dry Liner", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2016},
        {"model": "Mega Liner", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2017},
        {"model": "Tautliner", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2015},
        {"model": "Platform", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2015},
        {"model": "Flatbed", "kasa_tipleri": ["Kamyonet Römork"], "uretim_baslangic": 2015},
        {"model": "Sattelit", "kasa_tipleri": ["Yarı Römork"], "uretim_baslangic": 2018},
        {"model": "Tipper", "kasa_tipleri": ["Damperli"], "uretim_baslangic": 2016},
    ],
    "Kögel": [
        {"model": "Cool", "kasa_tipleri": ["Soğutmalı Treyler"], "uretim_baslangic": 2015},
        {"model": "Dry", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2016},
        {"model": "Curtain", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2015},
        {"model": "Mega", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2017},
        {"model": "Flat", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2016},
        {"model": "Container Chassis", "kasa_tipleri": ["Konteyner"], "uretim_baslangic": 2015},
        {"model": "Tank", "kasa_tipleri": ["Tank"], "uretim_baslangic": 2016},
    ],
    "OMSAN": [
        {"model": "Perdeli Dorse", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2016},
        {"model": "Kapalı Dorse", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2016},
        {"model": "Platform Dorse", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2017},
        {"model": "Tenteli Dorse", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2017},
        {"model": "Soğutmalı Dorse", "kasa_tipleri": ["Soğutmalı Treyler"], "uretim_baslangic": 2018},
        {"model": "Lowbed", "kasa_tipleri": ["Düşük Yataklı"], "uretim_baslangic": 2018},
    ],
    "Schmitz Cargobull": [
        {"model": "S.CS", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2016},
        {"model": "S.KO", "kasa_tipleri": ["Soğutmalı Treyler"], "uretim_baslangic": 2016},
        {"model": "S.BO", "kasa_tipleri": ["Kapalı Treyler"], "uretim_baslangic": 2017},
        {"model": "S.DS", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2018},
        {"model": "S.MG", "kasa_tipleri": ["Platform"], "uretim_baslangic": 2017},
        {"model": "EcoFLEX", "kasa_tipleri": ["Perde Treyler"], "uretim_baslangic": 2020},
        {"model": "S.KOe", "kasa_tipleri": ["Elektrikli Soğutmalı"], "uretim_baslangic": 2022},
    ],
}

os.makedirs("modeller", exist_ok=True)
combined = []
for brand, models in sorted(DATA.items()):
    dosya_adi = brand.lower().replace(" ","_").replace("ü","u").replace("ö","o").replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g")
    entry = {"marka": brand, "modeller": models, "kaynak": "manuel"}
    with open(f"modeller/{dosya_adi}.json", "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    combined.append(entry)
    print(f"{brand}: {len(models)} model")
combined.sort(key=lambda x: x["marka"])
with open("tum_modeller.json", "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)
print(f"Toplam: {len(combined)} marka, {sum(len(m[\"modeller\"]) for m in combined)} model")
