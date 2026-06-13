# Otomobil Veritabanı Veri Modeli

## Klasör Yapısı

```
Otomobil/Veritabanı/
├── spider.py                 # Ana örümcek scripti
├── tum_modeller.json          # Tüm markalar tek dosyada
├── veri_modeli.md             # Bu dosya
├── modeller/                  # Her marka için ayrı JSON
│   ├── audi.json
│   ├── bmw.json
│   └── ...
```

## JSON Veri Modeli (Her Marka İçin)

```json
{
  "marka": "Audi",
  "kaynak": "https://en.wikipedia.org/wiki/List_of_Audi_vehicles",
  "modeller": [
    {
      "model": "A3",
      "segment": "C",
      "kasa_tipleri": ["Sedan", "Hatchback", "Cabrio"],
      "uretim_baslangic": 1996,
      "uretim_bitis": null
    }
  ]
}
```

## Segment Sınıflandırması

| Kod | Sınıf     | Örnek Modeller               |
|-----|-----------|-------------------------------|
| A   | Mini      | Fiat 500, Smart Fortwo        |
| B   | Küçük     | Renault Clio, Ford Fiesta     |
| C   | Kompakt   | VW Golf, Honda Civic          |
| D   | Orta      | VW Passat, BMW 3 Serisi      |
| E   | Üst Orta  | Mercedes E-Class, BMW 5       |
| F   | Lüks      | Mercedes S-Class, BMW 7       |
| J   | SUV       | Toyota RAV4, BMW X5          |
| S   | Spor      | Porsche 911, Ferrari          |
| M   | MPV       | Renault Scenic, VW Touran     |
| P   | Pick-up   | Ford Ranger, Toyota Hilux     |
| V   | Van       | Mercedes Vito, VW Transporter |

## Kasa Tipleri

- Sedan
- Hatchback
- Station Wagon
- Coupe
- Cabrio
- SUV
- MPV
- Pick-up
- Van
- Fastback

## Kullanım

```python
# Tek marka oku
import json
with open("modeller/audi.json") as f:
    data = json.load(f)
    print(data["marka"])
    for m in data["modeller"]:
        print(f"  {m['model']} ({m['segment']})")

# Tüm modelleri oku
with open("tum_modeller.json") as f:
    markalar = json.load(f)
    for marka in markalar:
        print(marka["marka"], len(marka["modeller"]), "model")
```
