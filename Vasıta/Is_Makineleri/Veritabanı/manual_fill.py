# İş Makineleri - Manuel Model Verileri
# Bu dosyayı çalıştırmak için: python manual_fill.py

import json, os

DATA = {
    "Caterpillar": [
        {"model": "320", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "320 GC", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2020},
        {"model": "323", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "330", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "336", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "395", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2022},
        {"model": "D6", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2015},
        {"model": "D8", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2017},
        {"model": "D11", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2013},
        {"model": "950 GC", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2019},
        {"model": "966", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "980", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "MH3022", "kasa_tipleri": ["Malzeme Elleçleme"], "uretim_baslangic": 2019},
        {"model": "CS78B", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2018},
        {"model": "CB10", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2016},
        {"model": "725", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2016},
        {"model": "770G", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2015},
        {"model": "793", "kasa_tipleri": ["Maden Kamyonu"], "uretim_baslangic": 2014},
        {"model": "M315D2", "kasa_tipleri": ["Mini Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "303.5E", "kasa_tipleri": ["Mini Ekskavatör"], "uretim_baslangic": 2016},
    ],
    "Doosan": [
        {"model": "DX225", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "DX300", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "DX380", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "DX530", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2015},
        {"model": "DL420", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "DL550", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2018},
        {"model": "Bobcat E50", "kasa_tipleri": ["Mini Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "Bobcat S70", "kasa_tipleri": ["Mini Yükleyici"], "uretim_baslangic": 2015},
        {"model": "Bobcat T770", "kasa_tipleri": ["Mini Yükleyici"], "uretim_baslangic": 2017},
    ],
    "Hidromek": [
        {"model": "H88", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "H102", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "H135", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2019},
        {"model": "H220", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2020},
        {"model": "H350", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2021},
        {"model": "HMK 140", "kasa_tipleri": ["Kazıcı Yükleyici"], "uretim_baslangic": 2016},
        {"model": "HMK 200", "kasa_tipleri": ["Kazıcı Yükleyici"], "uretim_baslangic": 2018},
        {"model": "S185", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2017},
    ],
    "Hitachi CE": [
        {"model": "ZX130", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "ZX210", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "ZX330", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "ZX490", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "ZW180", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "ZW220", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "EH3500", "kasa_tipleri": ["Maden Kamyonu"], "uretim_baslangic": 2015},
    ],
    "Hyundai CE": [
        {"model": "HX220L", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "HX300L", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "HX520L", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2019},
        {"model": "HL940", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "HL955", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2018},
        {"model": "HW169", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2016},
    ],
    "JCB": [
        {"model": "3CX", "kasa_tipleri": ["Kazıcı Yükleyici"], "uretim_baslangic": 2015},
        {"model": "4CX", "kasa_tipleri": ["Kazıcı Yükleyici"], "uretim_baslangic": 2016},
        {"model": "220X", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "JS220", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "Hydradig", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "TM320", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2015},
        {"model": "457", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "Teleskobik 535-125", "kasa_tipleri": ["Teleskobik"], "uretim_baslangic": 2016},
    ],
    "Komatsu": [
        {"model": "PC210", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "PC300", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "PC400", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "PC490", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2019},
        {"model": "PC800", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2014},
        {"model": "D155", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2016},
        {"model": "D375", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2014},
        {"model": "WA380", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "WA500", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "HD325", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2015},
        {"model": "HM300", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2017},
        {"model": "GD655", "kasa_tipleri": ["Greyder"], "uretim_baslangic": 2017},
    ],
    "Liebherr": [
        {"model": "R914", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "R920", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "R925", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "R950", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2016},
        {"model": "R960", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2020},
        {"model": "R980 SME", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "L524", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "L550", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "L580", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2018},
        {"model": "PR736", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2017},
    ],
    "Sany": [
        {"model": "SY215", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "SY335", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2019},
        {"model": "SY485", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2020},
        {"model": "SY550H", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2021},
        {"model": "SMT98A", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2018},
        {"model": "SR150", "kasa_tipleri": ["Dozer"], "uretim_baslangic": 2019},
        {"model": "STG170", "kasa_tipleri": ["Greyder"], "uretim_baslangic": 2020},
    ],
    "Volvo CE": [
        {"model": "EC220E", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "EC350E", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "L120H", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "L150H", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2016},
        {"model": "L260H", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "A40G", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2015},
        {"model": "A60H", "kasa_tipleri": ["Damperli Kamyon"], "uretim_baslangic": 2018},
        {"model": "G940", "kasa_tipleri": ["Greyder"], "uretim_baslangic": 2015},
        {"model": "SD115", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2016},
        {"model": "ECR145EL", "kasa_tipleri": ["Mini Ekskavatör"], "uretim_baslangic": 2018},
    ],
    "XCMG": [
        {"model": "XE215C", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2017},
        {"model": "XE335C", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2018},
        {"model": "XE470C", "kasa_tipleri": ["Ekskavatör"], "uretim_baslangic": 2019},
        {"model": "ZL50GN", "kasa_tipleri": ["Yükleyici"], "uretim_baslangic": 2017},
        {"model": "GR1803", "kasa_tipleri": ["Greyder"], "uretim_baslangic": 2016},
        {"model": "XS182J", "kasa_tipleri": ["Silindir"], "uretim_baslangic": 2017},
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
