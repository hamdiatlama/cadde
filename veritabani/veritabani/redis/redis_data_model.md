# Redis Veri Modeli — Canlı & Geçici Veri Katmanı

50M kullanıcı ölçeğinde, PostgreSQL'de tutulması performans sorunu yaratacak
yüksek frekanslı / geçici veriler Redis'te tutulur.

## Kullanım Alanları

| Veri Türü | Redis Veri Yapısı | TTL | Açıklama |
|-----------|-------------------|-----|----------|
| Oturum (Session) | `STRING` | 7 gün | JWT refresh token blacklist |
| Sepet (Cart) | `HASH` | 7 gün | `cart:{id}` — sepet öğeleri, kullanıcı ID |
| Ürün görüntüleme sayacı | `SORTED SET` | 24 saat | `product:views:{product_id}` |
| Rate limiting | `STRING` | 1-60 sn | `ratelimit:{ip}:{endpoint}` |
| Stok rezervasyonu (geçici) | `STRING` | 15 dk | `stock:reserve:{product_id}:{cart_id}` |
| Kampanya kullanım sayacı | `STRING` | kampanya süresi | `campaign:usage:{campaign_id}` |
| Sürücü/Kurye canlı konumu | `GEO` | sürekli | `drivers:live` — GEOADD, GEORADIUS |
| Sürücü durumu | `STRING` | sürekli | `driver:status:{driver_id}` |
| En yakın sürücü önbelleği | `STRING` | 5 saniye | `nearest:drivers:{lat}:{lng}` |
| WebSocket bağlantıları | `SET` | heartbeat | `ws:connections:{driver_id}` |
| Sipariş durumu önbelleği | `STRING` | 5 dk | `order:status:{order_id}` |

## Anahtar İsimlendirme Standardı

```
{domain}:{entity}:{id}:{field}
```

Örnekler:
- `cart:a1b2c3d4` — Sepet hash'i
- `session:blacklist:eyJhbG...` — Geçersiz token
- `driver:loc:d5e6f7g8` — Sürücü konumu (GEO)
- `product:views:12345` — Ürün görüntüleme sayacı
- `rate:limit:192.168.1.1:api/orders` — Rate limit

## Önemli Notlar

1. **Sürücü/Kurye Konumu (GEO):** Redis GEO yapısı kullanılır.
   `GEOADD drivers:live {lng} {lat} {driver_id}` ile eklenir,
   `GEORADIUS drivers:live {lng} {lat} {radius} km` ile sorgulanır.
   Her N saniyede bir güncellenir. Sürücü çevrimdışı olduğunda
   `ZREM` ile silinir. Konum geçmişi için periyodik olarak PostgreSQL'e
   `driver_location_history` tablosuna yazılır.

2. **Stok Rezervasyonu:** Sepete ekleme anında stok geçici olarak
   rezerve edilir. Ödeme tamamlanmazsa TTL sona erdiğinde otomatik
   serbest bırakılır. Bu, race condition'ı önlemek için
   atomik `SETNX` ile yapılır.

3. **Session Yönetimi:** JWT refresh token'lar geçersiz kılındığında
   Redis'e blacklist olarak eklenir. Access token süresi kısa tutulur
   (15 dk), refresh token uzun (7 gün).

4. **Rate Limiting:** Her IP/endpoint çifti için saniyelik/ dakikalık
   limitler Redis'te tutulur. Aşım durumunda 429 dönülür.

5. **Önbellek Geçersiz Kılma:** Ürün fiyatı/stoku değiştiğinde
   ilgili Redis anahtarları silinir (cache invalidation pattern).
