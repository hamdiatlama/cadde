# ATV / UTV / Quad - Manuel Model Verileri
import json, os

DATA = {
    "CFMoto": [
        {"model": "CForce 400", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "CForce 500", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "CForce 600", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2019},
        {"model": "CForce 800", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2020},
        {"model": "ZForce 800", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2018},
        {"model": "ZForce 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2019},
        {"model": "UForce 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2020},
    ],
    "Can-Am (BRP)": [
        {"model": "Outlander 450", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "Outlander 850", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "Outlander XT 1000", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "Renegade 850", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "Maverick X3", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2017},
        {"model": "Maverick Trail 800", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2019},
        {"model": "Defender Max XT", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2018},
        {"model": "Commander XT", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2017},
    ],
    "Honda": [
        {"model": "TRX450R", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "TRX420FM FourTrax", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "TRX520 FourTrax", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "Rancher 420", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "Foreman 520", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "Talon 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2019},
        {"model": "Pioneer 700", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2017},
    ],
    "Polaris": [
        {"model": "Sportsman 570", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "Sportsman 850", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "Sportsman XP 1000", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "Outlaw 110", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2019},
        {"model": "Ranger 570", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2016},
        {"model": "Ranger XP 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2017},
        {"model": "General XP 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2018},
        {"model": "RZR XP 1000", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2017},
        {"model": "RZR Pro R", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2021},
    ],
    "Yamaha": [
        {"model": "Raptor 700", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "YFZ450R", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "Kodiak 700", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2016},
        {"model": "Grizzly 700", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2017},
        {"model": "Grizzly 90", "kasa_tipleri": ["ATV"], "uretim_baslangic": 2018},
        {"model": "Viking 700", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2016},
        {"model": "Wolverine X4", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2019},
        {"model": "YXZ1000R", "kasa_tipleri": ["UTV"], "uretim_baslangic": 2016},
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
