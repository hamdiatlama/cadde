# Traktör & Tarım - Manuel Model Verileri
# Bu dosyayı çalıştırmak için: python manual_fill.py

import json, os

DATA = {
    "Case IH": [
        {"model": "Farmall U", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2020},
        {"model": "Farmall C", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2018},
        {"model": "Puma", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2019},
        {"model": "Optum", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "Magnum", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "Steiger", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "Quadtrac", "kasa_tipleri": ["Paletli Traktör"], "uretim_baslangic": 2015},
        {"model": "Vestrum", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2021},
    ],
    "Claas": [
        {"model": "Arion 400", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "Arion 500", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "Arion 600", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2019},
        {"model": "Axion 800", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "Axion 900", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "Xerion 5000", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2019},
        {"model": "Elios", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "Nexos", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2014, "uretim_bitis": 2020},
    ],
    "Deutz-Fahr": [
        {"model": "5D Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "6C Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2021},
        {"model": "7C Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2022},
        {"model": "8C Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2022},
        {"model": "9C Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2023},
        {"model": "6B Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "5G Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2018},
        {"model": "Agroplus", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2014},
    ],
    "Fendt": [
        {"model": "200 Vario", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2017},
        {"model": "300 Vario", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "500 Vario", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2019},
        {"model": "700 Vario", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "900 Vario", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "1000 Vario", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2015},
        {"model": "1100 Vario", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2020},
    ],
    "Hattat Traktör": [
        {"model": "60 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "70 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "80 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "90 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "100 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "110 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2019},
    ],
    "John Deere": [
        {"model": "5E Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "5M Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "6M Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "6R Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2020},
        {"model": "7R Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "8R Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "8RX Serisi", "kasa_tipleri": ["Paletli Traktör"], "uretim_baslangic": 2021},
        {"model": "9R Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2019},
        {"model": "9RX Serisi", "kasa_tipleri": ["Paletli Traktör"], "uretim_baslangic": 2019},
        {"model": "XUV Serisi", "kasa_tipleri": ["Yanlısız Traktör"], "uretim_baslangic": 2010},
        {"model": "T Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2010, "uretim_bitis": 2020},
    ],
    "Kubota": [
        {"model": "M8 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2021},
        {"model": "M7 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2018},
        {"model": "M6 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "M5 Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "L Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "B Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2018},
        {"model": "BX Serisi", "kasa_tipleri": ["Bahçe Traktörü"], "uretim_baslangic": 2015},
        {"model": "ZD Serisi", "kasa_tipleri": ["Çim Biçme"], "uretim_baslangic": 2017},
    ],
    "Landini": [
        {"model": "Rex 4", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "Rex 3", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "Rex F", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2020},
        {"model": "Rex 4 GT", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2018},
        {"model": "Powerfarm", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2019},
        {"model": "Legend", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2021},
    ],
    "Massey Ferguson": [
        {"model": "MF 4700 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "MF 5700 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "MF 6700 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "MF 7700 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "MF 8700 Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2019},
        {"model": "MF 8S Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2020},
        {"model": "MF 1700M Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2018},
        {"model": "MF GC1700 Serisi", "kasa_tipleri": ["Bahçe Traktörü"], "uretim_baslangic": 2015},
    ],
    "New Holland": [
        {"model": "T4 Serisi", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2015},
        {"model": "T5 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "T6 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "T7 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2016},
        {"model": "T8 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "T9 Serisi", "kasa_tipleri": ["Çok Büyük Traktör"], "uretim_baslangic": 2021},
        {"model": "Workmaster", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "Boomer 50", "kasa_tipleri": ["Kompakt Traktör"], "uretim_baslangic": 2018},
        {"model": "TT4 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2018},
    ],
    "Tümosan": [
        {"model": "70 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "80 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "90 Serisi", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2015},
        {"model": "100 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2017},
        {"model": "110 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "120 Serisi", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2019},
    ],
    "TürkTraktör": [
        {"model": "New Holland TT4.55", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2020},
        {"model": "New Holland T4.85", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2019},
        {"model": "New Holland T5.95", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2021},
        {"model": "New Holland T6.150", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2020},
        {"model": "Case IH Farmall 75C", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2019},
        {"model": "Case IH Farmall 90U", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2021},
        {"model": "Case IH Farmall 110U", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2021},
        {"model": "Case IH Puma 165", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2020},
    ],
    "Zetor": [
        {"model": "Major 80", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "Major 100", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2018},
        {"model": "Proxima 80", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "Proxima 100", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2016},
        {"model": "Proxima 120", "kasa_tipleri": ["Orta Traktör"], "uretim_baslangic": 2017},
        {"model": "Forterra 130", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2018},
        {"model": "Forterra 150", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2019},
        {"model": "Crystal 160", "kasa_tipleri": ["Büyük Traktör"], "uretim_baslangic": 2021},
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
