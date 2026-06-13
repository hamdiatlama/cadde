# Karavan & Motorhome - Manuel Model Verileri
import json, os

DATA = {
    "Adria Mobil": [
        {"model": "Matrix 670 SL", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2019},
        {"model": "Supreme 680 SL", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2020},
        {"model": "Compact SP 420", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2018},
        {"model": "Action 361 LT", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
        {"model": "Altea 542 DT", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2016},
        {"model": "Sonik 410 SL", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2019},
    ],
    "Airstream": [
        {"model": "International 25", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2018},
        {"model": "Flying Cloud 23", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
        {"model": "Globetrotter 27", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2019},
        {"model": "Bambi 16", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2020},
        {"model": "Atlas Touring Coach", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2021},
    ],
    "Hymer": [
        {"model": "ML-T 580", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2018},
        {"model": "B-Class SL 540", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2019},
        {"model": "Exsis-i 480", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2017},
        {"model": "Grand Canyon S 820", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2020},
        {"model": "VisionVenture", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2022},
        {"model": "Mercedes Marco Polo", "kasa_tipleri": ["Kamyonet Karavan"], "uretim_baslangic": 2015},
    ],
    "Jayco": [
        {"model": "Alante 27A", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2019},
        {"model": "Greyhawk 29MVP", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2018},
        {"model": "Jay Flight SLX 7", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
        {"model": "White Hawk 28DS", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2019},
    ],
    "Knaus": [
        {"model": "Boxdrive 660", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2018},
        {"model": "Puech", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2020},
        {"model": "Tourer 700", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2019},
        {"model": "Sport 400", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
        {"model": "Südwind 450", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2018},
        {"model": "Tabbert", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2016},
    ],
    "Swift Group": [
        {"model": "Escape 664", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2019},
        {"model": "Segnova", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2020},
        {"model": "Challenger 570", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
    ],
    "Winnebago": [
        {"model": "Solis", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2020},
        {"model": "Travato", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2016},
        {"model": "View", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2015},
        {"model": "Voyage", "kasa_tipleri": ["Motorhome"], "uretim_baslangic": 2018},
        {"model": "Minnie Plus", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2017},
        {"model": "Micro Minnie", "kasa_tipleri": ["Çekme Karavan"], "uretim_baslangic": 2019},
    ],
}

os.makedirs("modeller", exist_ok=True)
combined = []
for brand, models in sorted(DATA.items()):
    dosya_adi = brand.lower().replace(" ","_").replace("ü","u").replace("ö","o").replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g")
    entry = {"marka": brand, "modeller": models, "kaynak": "manuel"}
    with open(f"modeller/{dosya_adi}.json", "w", encoding="utf-8") as fw:
        json.dump(entry, fw, ensure_ascii=False, indent=2)
    combined.append(entry)
    print(f"{brand}: {len(models)} model")
combined.sort(key=lambda x: x["marka"])
with open("tum_modeller.json", "w", encoding="utf-8") as fw:
    json.dump(combined, fw, ensure_ascii=False, indent=2)
print(f"Toplam: {len(combined)} marka, {sum(len(m[\"modeller\"]) for m in combined)} model")
