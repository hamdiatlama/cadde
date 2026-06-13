# Veritabanı Şema Yapısı — E-Ticaret + Kurye/Taksi Navigasyon + Mobil

**Hedef:** 50.000.000 kullanıcı, 100% açık kaynak (FCM hariç)
**Teknoloji:** PostgreSQL 16+ (self-hosted) + PostGIS + Redis + MinIO

## Domain Modülleri

| # | Domain | Migration | Açıklama |
|---|--------|-----------|----------|
| 0 | Extensions | `000000` | postgis, uuid-ossp, ltree |
| 1 | Kullanıcılar & Konum | `000001` | users, provinces, districts, neighborhoods, PostGIS |
| 2 | Meslekler | `000002` | profession_categories, professions, hierarchy |
| 3 | Araç Kataloğu | `000003` | brands, models, features, segments, body types |
| 4 | Oto Ekspertiz | `000004` | reports, inspections, measurements, TRAMER |
| 5 | Ürün & Sipariş | `000005` | products, carts, orders, payments, stock |
| 6 | Kurye/Taksi | `000006` | drivers, rides, routes, delivery zones |
| 7 | Kampanya & Bildirim | `000007` | campaigns, reviews, notifications |

## Mimari Kararlar

- **Partitioning:** Siparişler, bildirimler, konum geçmişi, raporlar
  — tarih bazlı partition (aylık). 50M kullanıcıda sorgu performansı için kritik.
- **PostGIS:** Tüm konum verileri `GEOGRAPHY(POINT, 4326)` tipinde.
  Teslimat bölgeleri `GEOGRAPHY(POLYGON, 4326)`. GIST indeksleri.
- **Race Condition Önlemi:** Stok tablosunda `version` sütunu ile
  optimistic locking. Sipariş oluşturma akışında `SELECT ... FOR UPDATE`.
- **Redis/PostgreSQL Ayrımı:** Canlı sürücü konumu Redis GEO'da,
  geçmiş özet PostgreSQL'de. Sepet Redis'te (geçici), sipariş PostgreSQL'de (kalıcı).
- **Mobil Uyum:** `device_token`, `last_login_at` alanları.
  Bildirimler partition'lı ve adapter pattern'e hazır.

## Tablo Sayıları

- Toplam tablo: ~60
- Partition tablolar: ~30
- Lookup/yardımcı tablolar: ~10
- İndeks: ~80

## Seed Sırası

1. `000001_seed_locations.sql` — Bölgeler, iller
2. `000002_seed_professions.sql` — Meslek kategorileri ve meslekler
3. `000003_seed_vehicle_catalog.sql` — Araç kategorileri, markalar, modeller

## Migration Sırası (golang-migrate)

```bash
migrate -path migrations -database "postgres://..." up
```

Migration'lar yukarıdaki domain numarası sırasıyla uygulanmalıdır
(çünkü sonraki migration'lar önceki tablolara FK ile bağlanır).
