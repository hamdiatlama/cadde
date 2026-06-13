# Otobüs - Manuel Model Verileri
# Bu dosyayı çalıştırmak için: python manual_fill.py

import json, os

DATA = {
    "BMC": [
        {"model": "Megastar", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2018},
        {"model": "Tugra", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2016},
        {"model": "Profesyonel", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013, "uretim_bitis": 2020},
        {"model": "Levend", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2020},
        {"model": "415", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2015},
        {"model": "BMC Otobüs 220", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "BMC Otobüs 280", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "BMC Midibus 180", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
    ],
    "DAF": [
        {"model": "LF Serisi", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2012},
        {"model": "CF Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2012},
        {"model": "XF Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2012},
        {"model": "XG Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2021},
        {"model": "XG+ Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2021},
        {"model": "XD Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2022},
        {"model": "LF Electric", "kasa_tipleri": ["Elektrikli Orta Kamyon"], "uretim_baslangic": 2021},
    ],
    "Ford Trucks": [
        {"model": "F-MAX", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2018},
        {"model": "F-LINE", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2023},
        {"model": "Cargo 1832", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2018},
        {"model": "Cargo 1843", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2020},
        {"model": "Transit Custom", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2012},
        {"model": "Transit Courier", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2014},
        {"model": "Transit", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2014},
        {"model": "Tourneo Custom", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2012},
    ],
    "Isuzu": [
        {"model": "D-Max", "kasa_tipleri": ["Pick-up"], "uretim_baslangic": 2019},
        {"model": "N-Serisi (NPR/NQR/NRR)", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2015},
        {"model": "F-Serisi (FRR/FSR/FRD)", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2016},
        {"model": "Turkuaz", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2018},
        {"model": "Saiph", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2021},
        {"model": "Novo", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2021},
        {"model": "MU-X", "kasa_tipleri": ["SUV"], "uretim_baslangic": 2021},
    ],
    "Iveco": [
        {"model": "Daily", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2014},
        {"model": "Daily Hi-Matic", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2016},
        {"model": "Eurocargo", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2015},
        {"model": "Stralis", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2012, "uretim_bitis": 2021},
        {"model": "S-Way", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2019},
        {"model": "X-Way", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2019},
        {"model": "T-Way", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2021},
        {"model": "Astra HD9", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2015},
    ],
    "KamAZ": [
        {"model": "54901", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2019},
        {"model": "6520", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2010},
        {"model": "65115", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2010},
        {"model": "43118", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2005},
        {"model": "5350", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2005},
        {"model": "6282", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2019},
    ],
    "Karsan": [
        {"model": "Jest", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "Atak", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "Menarinibus", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
        {"model": "e-Jest", "kasa_tipleri": ["Elektrikli Otobüs"], "uretim_baslangic": 2019},
        {"model": "e-Atak", "kasa_tipleri": ["Elektrikli Otobüs"], "uretim_baslangic": 2022},
    ],
    "MAN": [
        {"model": "TGL", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2013},
        {"model": "TGM", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2013},
        {"model": "TGS", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "TGX", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "TGE", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2016},
        {"model": "eTGE", "kasa_tipleri": ["Elektrikli Hafif Ticari"], "uretim_baslangic": 2020},
        {"model": "Lions City", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
        {"model": "Lions Intercity", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "Lions Coach", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "Lions TopCoach", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
    ],
    "Mercedes-Benz Trucks": [
        {"model": "Atego", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2013},
        {"model": "Actros", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2011},
        {"model": "Arocs", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "Antos", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2012, "uretim_bitis": 2020},
        {"model": "Econic", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2014},
        {"model": "Unimog", "kasa_tipleri": ["Özel Amaçlı"], "uretim_baslangic": 2013},
        {"model": "Zetros", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2015},
        {"model": "eActros", "kasa_tipleri": ["Elektrikli Ağır Kamyon"], "uretim_baslangic": 2021},
        {"model": "eEconic", "kasa_tipleri": ["Elektrikli Orta Kamyon"], "uretim_baslangic": 2021},
        {"model": "Sprinter", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2018},
        {"model": "Vito", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2014},
        {"model": "Citan", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2019},
    ],
    "Otokar": [
        {"model": "Doruk", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
        {"model": "Naviga", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
        {"model": "Kentin", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2020},
        {"model": "Territo", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2019},
        {"model": "Centro", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "Sultan", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "M-3000", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2012},
        {"model": "Ares", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2022},
    ],
    "Renault Trucks": [
        {"model": "Master", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2010},
        {"model": "Trafic", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2014},
        {"model": "Kangoo", "kasa_tipleri": ["Hafif Ticari"], "uretim_baslangic": 2021},
        {"model": "D", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2017},
        {"model": "C", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2017},
        {"model": "K", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2017},
        {"model": "T", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "E-Tech D", "kasa_tipleri": ["Elektrikli Orta Kamyon"], "uretim_baslangic": 2021},
        {"model": "E-Tech T", "kasa_tipleri": ["Elektrikli Ağır Kamyon"], "uretim_baslangic": 2023},
    ],
    "Scania": [
        {"model": "P Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2016},
        {"model": "G Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2016},
        {"model": "R Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2016},
        {"model": "S Serisi", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2016},
        {"model": "PXT", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2022},
        {"model": "Super", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2022},
        {"model": "Scania Citywide", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2014},
        {"model": "Scania Interlink", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
    ],
    "TEMSA": [
        {"model": "MD7", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
        {"model": "MD9", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "HD12", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
        {"model": "HD13", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
        {"model": "HD14", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2020},
        {"model": "Safari", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2017},
        {"model": "Opalin", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2019},
        {"model": "Prestij", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2020},
        {"model": "Tourmalin", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2020},
        {"model": "LD SB", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2018},
        {"model": "LD MB", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2019},
    ],
    "Volvo Buses": [
        {"model": "7900", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2014},
        {"model": "8900", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2014},
        {"model": "8900 LE", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "9700", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2015},
        {"model": "9900", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2016},
        {"model": "7400", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2014},
        {"model": "7700", "kasa_tipleri": ["Otobüs"], "uretim_baslangic": 2014},
        {"model": "7900 Electric", "kasa_tipleri": ["Elektrikli Otobüs"], "uretim_baslangic": 2018},
        {"model": "8900 Electric", "kasa_tipleri": ["Elektrikli Otobüs"], "uretim_baslangic": 2021},
    ],
    "Volvo Trucks": [
        {"model": "FH", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "FH16", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "FM", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "FMX", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2013},
        {"model": "FE", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2014},
        {"model": "FL", "kasa_tipleri": ["Orta Kamyon"], "uretim_baslangic": 2014},
        {"model": "VNR", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2017},
        {"model": "VHD", "kasa_tipleri": ["Ağır Kamyon"], "uretim_baslangic": 2014},
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
