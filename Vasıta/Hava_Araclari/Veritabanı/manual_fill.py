# Hava Araçları - Manuel Model Verileri
import json, os

DATA = {
    "Cessna (Textron)": [
        {"model": "172 Skyhawk", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2014},
        {"model": "182 Skylane", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2015},
        {"model": "206 Stationair", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2016},
        {"model": "T182T Turbo Skylane", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2017},
        {"model": "Citation CJ4", "kasa_tipleri": ["Uçak (Jet)"], "uretim_baslangic": 2016},
        {"model": "Citation M2", "kasa_tipleri": ["Uçak (Jet)"], "uretim_baslangic": 2015},
        {"model": "Citation Latitude", "kasa_tipleri": ["Uçak (Jet)"], "uretim_baslangic": 2017},
        {"model": "Citation Longitude", "kasa_tipleri": ["Uçak (Jet)"], "uretim_baslangic": 2019},
    ],
    "Cirrus Aircraft": [
        {"model": "SR20", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2015},
        {"model": "SR22", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2014},
        {"model": "SR22T", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2016},
        {"model": "SF50 Vision Jet", "kasa_tipleri": ["Uçak (Jet)"], "uretim_baslangic": 2018},
    ],
    "DJI": [
        {"model": "Mavic 3 Pro", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2023},
        {"model": "Mavic 3 Classic", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2022},
        {"model": "Air 3", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2023},
        {"model": "Mini 4 Pro", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2023},
        {"model": "Mini 3 Pro", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2022},
        {"model": "Avata 2", "kasa_tipleri": ["Drone (FPV)"], "uretim_baslangic": 2024},
        {"model": "Inspire 3", "kasa_tipleri": ["Drone"], "uretim_baslangic": 2023},
        {"model": "Matrice 350 RTK", "kasa_tipleri": ["Drone (Endüstriyel)"], "uretim_baslangic": 2023},
    ],
    "Pipistrel": [
        {"model": "Virus SW 121", "kasa_tipleri": ["Ultralight"], "uretim_baslangic": 2016},
        {"model": "Alpha A2", "kasa_tipleri": ["Ultralight"], "uretim_baslangic": 2017},
        {"model": "Panthera", "kasa_tipleri": ["Uçak"], "uretim_baslangic": 2020},
        {"model": "Velis Electro", "kasa_tipleri": ["Ultralight (Elektrikli)"], "uretim_baslangic": 2021},
    ],
    "Robinson Helicopter": [
        {"model": "R22 Beta II", "kasa_tipleri": ["Helikopter"], "uretim_baslangic": 2015},
        {"model": "R44 Raven II", "kasa_tipleri": ["Helikopter"], "uretim_baslangic": 2014},
        {"model": "R44 Clipper II", "kasa_tipleri": ["Helikopter"], "uretim_baslangic": 2016},
        {"model": "R66 Turbine", "kasa_tipleri": ["Helikopter"], "uretim_baslangic": 2015},
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
