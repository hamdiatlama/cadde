# Elektrikli Scooter & Bisiklet - Manuel Model Verileri
import json, os

DATA = {
    "Dualtron": [
        {"model": "Thunder", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2019},
        {"model": "Storm", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "Spider", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "Eagle Pro", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2021},
        {"model": "X Limited", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2021},
    ],
    "Giant": [
        {"model": "Explore E+ 2", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2020},
        {"model": "FastRoad E+ EX", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2021},
        {"model": "Trance X E+ Elite", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2022},
        {"model": "Talon E+", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2021},
        {"model": "Liv Amiti E+", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2020},
    ],
    "Kaabo": [
        {"model": "Wolf King GT", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2021},
        {"model": "Mantis 10 Pro", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "Mantis 8", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2019},
        {"model": "Skywalker 8S", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2019},
        {"model": "Wolf Warrior X", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2022},
    ],
    "Segway (Ninebot)": [
        {"model": "Ninebot KickScooter MAX G30", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2019},
        {"model": "Ninebot KickScooter F40", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2021},
        {"model": "Ninebot KickScooter D38", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "GT2", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2022},
        {"model": "PNT", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2023},
    ],
    "Specialized": [
        {"model": "Turbo Vado 3.0", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2020},
        {"model": "Turbo Creo 2", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2022},
        {"model": "Turbo Levo", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2021},
        {"model": "Turbo Como 4.0", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2020},
        {"model": "Turbo Tero X", "kasa_tipleri": ["e-Bisiklet"], "uretim_baslangic": 2023},
    ],
    "Xiaomi": [
        {"model": "Mi Electric Scooter 1S", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "Mi Electric Scooter 3", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2021},
        {"model": "Mi Electric Scooter Pro 2", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2020},
        {"model": "Mi Electric Scooter 4 Pro", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2022},
        {"model": "Mi Electric Scooter 4 Lite", "kasa_tipleri": ["Scooter"], "uretim_baslangic": 2022},
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
