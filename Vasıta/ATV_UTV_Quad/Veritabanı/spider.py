import requests
import json
import os
import re
import time
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DATA_DIR = os.path.join(os.path.dirname(__file__), "modeller")

SEGMENT_MAP = {
    "mini": "A", "city car": "A", "microcar": "A",
    "supermini": "B", "subcompact": "B", "small": "B",
    "compact": "C", "small family": "C", "lower medium": "C",
    "mid-size": "D", "large family": "D", "upper medium": "D",
    "executive": "E", "mid-size luxury": "E", "full-size": "E",
    "luxury": "F", "full-size luxury": "F", "ultra-luxury": "F",
    "suv": "J", "off-road": "J", "crossover": "J", "4x4": "J",
    "sports": "S", "supercar": "S", "roadster": "S", "convertible": "S",
    "mpv": "M", "minivan": "M", "multi-purpose": "M", "people carrier": "M",
    "pickup": "P", "pick-up": "P", "van": "V",
}

BRAND_WIKI = {
    "Audi": "/wiki/List_of_Audi_vehicles",
    "BMW": "/wiki/List_of_BMW_vehicles",
    "Mercedes-Benz": "/wiki/List_of_Mercedes-Benz_vehicles",
    "Volkswagen": "/wiki/List_of_Volkswagen_vehicles",
    "Porsche": "/wiki/List_of_Porsche_vehicles",
    "Opel": "/wiki/List_of_Opel_vehicles",
    "Ford": "/wiki/List_of_Ford_vehicles",
    "Toyota": "/wiki/List_of_Toyota_vehicles",
    "Honda": "/wiki/List_of_Honda_automobiles",
    "Nissan": "/wiki/List_of_Nissan_vehicles",
    "Mazda": "/wiki/List_of_Mazda_vehicles",
    "Mitsubishi": "/wiki/List_of_Mitsubishi_vehicles",
    "Subaru": "/wiki/List_of_Subaru_vehicles",
    "Suzuki": "/wiki/List_of_Suzuki_vehicles",
    "Hyundai": "/wiki/List_of_Hyundai_vehicles",
    "Kia": "/wiki/List_of_Kia_vehicles",
    "Renault": "/wiki/List_of_Renault_vehicles",
    "Peugeot": "/wiki/List_of_Peugeot_vehicles",
    "Citro\u00ebn": "/wiki/List_of_Citro%C3%ABn_vehicles",
    "Fiat": "/wiki/List_of_Fiat_vehicles",
    "Alfa Romeo": "/wiki/List_of_Alfa_Romeo_vehicles",
    "Lancia": "/wiki/List_of_Lancia_vehicles",
    "Maserati": "/wiki/List_of_Maserati_vehicles",
    "Ferrari": "/wiki/List_of_Ferrari_road_vehicles",
    "Lamborghini": "/wiki/List_of_Lamborghini_vehicles",
    "Jaguar": "/wiki/List_of_Jaguar_vehicles",
    "Land Rover": "/wiki/List_of_Land_Rover_vehicles",
    "Volvo": "/wiki/List_of_Volvo_vehicles",
    "Saab": "/wiki/Saab_Automobile",
    "SEAT": "/wiki/List_of_SEAT_vehicles",
    "\u0160koda": "/wiki/List_of_\u0160koda_vehicles",
    "Dacia": "/wiki/List_of_Dacia_vehicles",
    "Chevrolet": "/wiki/List_of_Chevrolet_vehicles",
    "Cadillac": "/wiki/List_of_Cadillac_vehicles",
    "Buick": "/wiki/List_of_Buick_vehicles",
    "GMC": "/wiki/List_of_GMC_vehicles",
    "Jeep": "/wiki/List_of_Jeep_vehicles",
    "Dodge": "/wiki/List_of_Dodge_vehicles",
    "Chrysler": "/wiki/List_of_Chrysler_vehicles",
    "Ram": "/wiki/Ram_(brand)",
    "Tesla": "/wiki/List_of_Tesla_vehicles",
    "Bentley": "/wiki/List_of_Bentley_vehicles",
    "Rolls-Royce": "/wiki/Rolls-Royce_Motor_Cars",
    "Aston Martin": "/wiki/Aston_Martin",
    "McLaren": "/wiki/McLaren_Automotive",
    "Bugatti": "/wiki/Bugatti_Automobiles",
    "Lexus": "/wiki/List_of_Lexus_vehicles",
    "Infiniti": "/wiki/List_of_Infiniti_vehicles",
    "Acura": "/wiki/List_of_Acura_vehicles",
    "Mini": "/wiki/Mini_(marque)",
    "Smart": "/wiki/Smart_(marque)",
    "Praga": "/wiki/Praga_(company)",
    "Rimac": "/wiki/Rimac_Automobili",
    "Polestar": "/wiki/Polestar",
    "Cupra": "/wiki/CUPRA",
    "BYD": "/wiki/BYD_Auto",
    "MG": "/wiki/List_of_MG_vehicles",
    "Great Wall": "/wiki/Great_Wall_Motors",
    "Haval": "/wiki/Haval_(marque)",
    "Tata": "/wiki/Tata_Motors",
    "Mahindra": "/wiki/Mahindra_%26_Mahindra",
    "Proton": "/wiki/List_of_Proton_vehicles",
    "Perodua": "/wiki/Perodua",
    "Lotus": "/wiki/Lotus_Cars",
    "Togg": "/wiki/Togg",
}

def segment_bul(text):
    if not text:
        return "B"
    text = text.lower()
    if "segment" in text:
        for key, val in SEGMENT_MAP.items():
            if key in text:
                return val
    for key, val in SEGMENT_MAP.items():
        if key in text:
            return val
    if any(w in text for w in ["sport", "supercar", "performance"]):
        return "S"
    if any(w in text for w in ["suv", "crossover", "off-road", "4x4"]):
        return "J"
    if any(w in text for w in ["compact", "small family"]):
        return "C"
    if any(w in text for w in ["executive", "mid-size luxury"]):
        return "E"
    if any(w in text for w in ["luxury", "full-size"]):
        return "F"
    if any(w in text for w in ["mpv", "minivan", "multi"]):
        return "M"
    if any(w in text for w in ["pickup", "pick-up"]):
        return "P"
    if any(w in text for w in ["supermini", "subcompact"]):
        return "B"
    if any(w in text for w in ["mini", "city"]):
        return "A"
    return "B"

def kasa_tipini_bul(text):
    if not text:
        return []
    text = text.lower()
    tipler = []
    if any(w in text for w in ["sedan", "saloon", "berline"]):
        tipler.append("Sedan")
    if any(w in text for w in ["hatchback", "hatch"]):
        tipler.append("Hatchback")
    if any(w in text for w in ["estate", "wagon", "station", "tourer", "avant", "touring"]):
        tipler.append("Station Wagon")
    if any(w in text for w in ["coupe", "coup\u00e9"]):
        tipler.append("Coupe")
    if any(w in text for w in ["cabrio", "convertible", "roadster", "spider", "spyder", "open"]):
        tipler.append("Cabrio")
    if any(w in text for w in ["suv", "crossover", "off-road"]):
        tipler.append("SUV")
    if any(w in text for w in ["mpv", "minivan", "people carrier"]):
        tipler.append("MPV")
    if any(w in text for w in ["pickup", "pick-up"]):
        tipler.append("Pick-up")
    if any(w in text for w in ["van"]):
        tipler.append("Van")
    if any(w in text for w in ["fastback", "liftback"]):
        tipler.append("Fastback")
    if not tipler:
        if any(w in text for w in ["sport", "supercar"]):
            tipler.append("Coupe")
    return tipler

def model_adi_temizle(ad):
    if not ad:
        return ""
    ad = ad.strip()
    skip_list = ["introduction", "update/facelift", "photo", "image", "model", "name"]
    if ad.lower() in skip_list:
        return ""
    return ad

def tablo_parse(soup, brand):
    modeller = []
    tables = soup.find_all("table", class_="wikitable")
    if not tables:
        tables = soup.find_all("table", {"class": "wikitable"})

    for table in tables:
        baslik = table.find_previous(["h2", "h3", "h4"])
        baslik_text = baslik.get_text(strip=True).lower() if baslik else ""

        if any(skip in baslik_text for skip in ["concept", "racing", "prototype", "discontinued", "commercial", "truck", "bus", "tractor", "engine", "transmission", "motor"]):
            continue

        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        basliklar = [th.get_text(strip=True).lower() for th in rows[0].find_all("th")]
        has_model_header = any(k in b for k in ["model", "name", "make", "vehicle"] for b in basliklar) if basliklar else False

        if not basliklar or ("name" not in basliklar[0].lower() and "model" not in basliklar[0].lower() and not has_model_header):
            if len(rows) > 3:
                hucreler = rows[1].find_all(["td", "th"])
                ilk_hucre = hucreler[0].get_text(strip=True).lower() if hucreler else ""
                if ilk_hucre in ["introduction", "update/facelift", ""]:
                    has_model_header = True

        for row in rows[1:]:
            hucreler = row.find_all(["td", "th"])
            if len(hucreler) < 1:
                continue

            ilk_text = hucreler[0].get_text(strip=True)
            if not ilk_text or len(ilk_text) < 1:
                continue

            if ilk_text.lower() in ["introduction", "update/facelift", "photo", "image"]:
                continue

            ilk_rowspan = hucreler[0].get("rowspan")
            if ilk_rowspan:
                if len(hucreler) < 2:
                    continue
                model_adi = model_adi_temizle(hucreler[1].get_text(strip=True))
                aciklama_kolon = 2 if len(hucreler) > 2 else None
            else:
                model_adi = model_adi_temizle(ilk_text)
                aciklama_kolon = 1 if len(hucreler) > 1 else None

            if not model_adi or len(model_adi) < 2:
                continue

            yil_bas = None
            yil_bit = None
            kasa_str = baslik_text

            for i, col in enumerate(hucreler):
                text = col.get_text(strip=True)
                year_match = re.findall(r"\b(19|20)\d{2}\b", text)
                if year_match:
                    if not yil_bas:
                        yil_bas = int(year_match[0])
                    if len(year_match) > 1:
                        yil_bit = int(year_match[-1])
                    elif yil_bas and int(year_match[0]) > yil_bas:
                        yil_bit = int(year_match[-1])

                if not kasa_str or kasa_str == baslik_text:
                    if any(k in text.lower() for k in ["hatchback", "sedan", "suv", "coupe", "cabrio", "estate", "wagon", "liftback", "executive", "compact", "mid-size", "subcompact", "sports", "luxury", "convertible", "roadster"]):
                        kasa_str = text

            if not yil_bas:
                for i, col in enumerate(hucreler):
                    text = col.get_text(strip=True)
                    year_match = re.findall(r"\b(19|20)\d{2}\b", text)
                    if year_match:
                        yil_bas = int(year_match[0])
                        if len(year_match) > 1:
                            yil_bit = int(year_match[-1])
                        break

            segment = segment_bul(kasa_str)
            kasa_tipleri = kasa_tipini_bul(kasa_str)

            var_mi = any(m["model"] == model_adi for m in modeller)
            if not var_mi:
                modeller.append({
                    "model": model_adi,
                    "segment": segment,
                    "kasa_tipleri": kasa_tipleri if kasa_tipleri else [],
                    "uretim_baslangic": yil_bas,
                    "uretim_bitis": yil_bit,
                })

    return modeller

def marka_cek(brand_name, wiki_path):
    url = BASE_URL + wiki_path
    print(f"[{brand_name}] \u00c7ekiliyor: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  HATA: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    modeller = tablo_parse(soup, brand_name)

    if modeller:
        modeller.sort(key=lambda x: x.get("uretim_baslangic") or 9999)
        dosya_adi = brand_name.lower().replace(" ", "_").replace("\u00fc", "u").replace("\u00f6", "o").replace("\u0131", "i").replace("\u015f", "s").replace("\u00e7", "c").replace("\u011f", "g").replace("\u00e9", "e")
        dosya_yolu = os.path.join(DATA_DIR, f"{dosya_adi}.json")
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump({"marka": brand_name, "modeller": modeller, "kaynak": url}, f, ensure_ascii=False, indent=2)
        print(f"  -> {len(modeller)} model kaydedildi: {dosya_adi}.json")
    else:
        print(f"  UYARI: Hi\u00e7 model bulunamad\u0131!")

    return modeller

def hepsini_cek():
    os.makedirs(DATA_DIR, exist_ok=True)
    toplam = 0
    basarili = 0

    print("=" * 60)
    print("ARABA MARKA / MODEL \u00d6R\u00dcMC\u00dcK S\u0130STEM\u0130")
    print("Kaynak: Wikipedia")
    print("=" * 60)
    print()

    for brand, path in BRAND_WIKI.items():
        modeller = marka_cek(brand, path)
        if modeller:
            basarili += 1
            toplam += len(modeller)
        time.sleep(0.4)

    print()
    print("=" * 60)
    print(f"\u00d6ZET: {len(BRAND_WIKI)} marka i\u00e7inden {basarili} ba\u015far\u0131l\u0131")
    print(f"      Toplam {toplam} model \u00e7ekildi")
    print("=" * 60)

def toplu_birlesim():
    butun = []
    for dosya in sorted(os.listdir(DATA_DIR)):
        if dosya.endswith(".json"):
            with open(os.path.join(DATA_DIR, dosya), "r", encoding="utf-8") as f:
                butun.append(json.load(f))
    dosya_yolu = os.path.join(os.path.dirname(__file__), "tum_modeller.json")
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(butun, f, ensure_ascii=False, indent=2)
    print(f"T\u00fcm modeller tek dosyaya birle\u015ftirildi: tum_modeller.json ({len(butun)} marka)")

def segment_ozeti():
    sayac = {}
    for dosya in sorted(os.listdir(DATA_DIR)):
        if dosya.endswith(".json"):
            with open(os.path.join(DATA_DIR, dosya), "r", encoding="utf-8") as f:
                data = json.load(f)
            for m in data.get("modeller", []):
                seg = m.get("segment", "?")
                sayac[seg] = sayac.get(seg, 0) + 1
    print("\nSegment Da\u011f\u0131l\u0131m\u0131:")
    for seg, count in sorted(sayac.items()):
        seg_acik = {"A": "Mini", "B": "K\u00fc\u00e7\u00fck", "C": "Kompakt", "D": "Orta",
                    "E": "\u00dcst Orta", "F": "L\u00fcks", "J": "SUV", "S": "Spor",
                    "M": "MPV", "P": "Pick-up", "V": "Van"}.get(seg, seg)
        print(f"  {seg} ({seg_acik}): {count} model")

if __name__ == "__main__":
    hepsini_cek()
    print()
    toplu_birlesim()
    print()
    segment_ozeti()
