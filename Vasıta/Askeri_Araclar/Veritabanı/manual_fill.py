# Askeri Araçlar - Manuel Model Verileri
import json, os

DATA = {
    "BMC (Askeri)": [
        {"model": "Amazon (4x4)", "kasa_tipleri": ["Askeri Cip"], "uretim_baslangic": 2015},
        {"model": "Kirpi", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2014},
        {"model": "Afyon", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2016},
        {"model": "Kıraç", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2019},
        {"model": "Altuğ 8x8", "kasa_tipleri": ["Askeri Kamyon"], "uretim_baslangic": 2020},
        {"model": "380-26", "kasa_tipleri": ["Askeri Kamyon"], "uretim_baslangic": 2018},
    ],
    "FNSS": [
        {"model": "ACV-15", "kasa_tipleri": ["ZMA (Zırhlı Muharebe)"], "uretim_baslangic": 2014},
        {"model": "Kaplan-10", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2019},
        {"model": "Kaplan-20", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2021},
        {"model": "Pars 8x8", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2018},
        {"model": "Kunduz", "kasa_tipleri": ["ZMA"], "uretim_baslangic": 2016},
    ],
    "Nurol Makina": [
        {"model": "Ejder Yalçın", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2017},
        {"model": "Ejder TOMA", "kasa_tipleri": ["Zırhlı (Toplumsal Olay)"], "uretim_baslangic": 2018},
        {"model": "Ejder Kama", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2020},
    ],
    "Oshkosh Defense": [
        {"model": "JLTV", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2016},
        {"model": "L-ATV", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2017},
        {"model": "M-ATV", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2012, "uretim_bitis": 2020},
        {"model": "MTVR MK23", "kasa_tipleri": ["Askeri Kamyon"], "uretim_baslangic": 2014},
        {"model": "HEMTT M977", "kasa_tipleri": ["Askeri Kamyon"], "uretim_baslangic": 2013},
    ],
    "Otokar (Askeri)": [
        {"model": "Cobra", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2014},
        {"model": "Cobra II", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2017},
        {"model": "Arma 8x8", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2019},
        {"model": "Akrep II", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2018},
        {"model": "Ural", "kasa_tipleri": ["Askeri Kamyon"], "uretim_baslangic": 2015},
    ],
    "Rheinmetall": [
        {"model": "Yak", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2015},
        {"model": "Boxer", "kasa_tipleri": ["ZMA"], "uretim_baslangic": 2016},
        {"model": "Lynx KF41", "kasa_tipleri": ["ZMA"], "uretim_baslangic": 2019},
        {"model": "Wiesel 2", "kasa_tipleri": ["Zırhlı"], "uretim_baslangic": 2014},
        {"model": "GTK Boxer", "kasa_tipleri": ["ZMA"], "uretim_baslangic": 2017},
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
