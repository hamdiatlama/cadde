# PROJE BAŞLANGIÇ TALİMATI (E-TİCARET + KURYE/TAKSİ NAVİGASYON + MOBİL / 50M KULLANICI ÖLÇEĞİ)

Bu projeye başlamadan önce aşağıdaki teknik kararları ve standartları temel al. Kod yazarken, veritabanı tasarlarken ve mimari önerilerde bulunurken bunlara sadık kal.

## Hedef ve Ölçek
- Bu proje, en az **50.000.000 kullanıcıya** ulaşması hedeflenen, çok kullanıcılı, interaktif bir **e-ticaret web ve mobil portalıdır**.
- Sistem içinde ürün katalog, sepet, sipariş, ödeme, stok yönetimi, kullanıcı hesapları, kampanya/indirim ve değerlendirme/yorum modülleri olacak.
- Ayrıca sistemde **kurye/teslimat takibi** ve **taksi/araç çağırma uygulaması** modülleri bulunacak: canlı konum takibi, yol/rota hesaplama, yakındaki sürücü/kurye eşleştirme.
- Sistem **web ve mobil (iOS + Android) olarak** kullanılacak. Backend tek, istemciler (web + mobil) aynı API'leri kullanacak.
- **KRİTİK KISIT: Tüm teknoloji yığını %100 ücretsiz / açık kaynak olmalı.** Lisans ücreti gerektiren, "free tier" sınırlamalı veya kullanım arttıkça ücretlendirilen (cloud managed servisler, Google Maps API gibi) hiçbir bileşen kullanılmayacak. Self-hosted açık kaynak çözümler tercih edilecek. (Push bildirim servisi (FCM) bu kuralın istisnasıdır — aşağıda açıklanmıştır.)
- Tasarım kararları "küçük başla ama büyümeye hazır ol" prensibiyle alınmalı. Erken aşırı mühendislik yok, ama ileride sancısız ölçeklenecek temel atılmalı.

## Teknoloji Yığını (Tech Stack) — Tamamı Açık Kaynak / Ücretsiz

### Temel
- **Backend dili:** Go (Golang)
  - Yüksek eşzamanlılık, düşük kaynak tüketimi. Lisans maliyeti yok.
  - goroutine/channel kullanımını idiomatic Go standartlarına göre yap.
  - Canlı konum takibi gibi yüksek frekanslı veri akışları için Go'nun concurrency modeli kritik avantaj.
- **Ana Veritabanı:** PostgreSQL (self-hosted)
  - Sipariş, ödeme kaydı, kullanıcı, kampanya gibi **güçlü tutarlılık (ACID)** gerektiren tüm veriler burada.
  - Transaction bütünlüğüne özel önem ver — özellikle sipariş/ödeme/stok güncelleme akışlarında.
- **API tasarımı:** Tek backend, REST (veya gerekirse gRPC) API. Web ve mobil istemciler aynı API'leri tüketir — istemciye özel ayrı backend yazılmaz.
- **Web Frontend:** React / Next.js
  - SEO kritik (ürün sayfaları) olduğu için Next.js'in SSR/ISR özellikleri önemli.
- **Mobil Uygulama:** React Native (veya Flutter)
  - Tek kod tabanından iOS + Android. React Native, web'de React kullanıldığı için ekip/kod tutarlılığı sağlar (tercih); Flutter performans öncelikliyse alternatif.
- **Konteynerleştirme:** Docker + Docker Compose (başlangıç), ileride Kubernetes (k3s gibi hafif açık kaynak dağıtım) ölçek büyüdükçe.

### Cache, Arama, Mesajlaşma, Depolama
- **Cache / Session / Sepet:** Redis (self-hosted)
  - Sepet verisi, oturum, sık okunan ürün/kategori verisi için.
  - Rate limiting ve geçici kilitler (örn. stok rezervasyonu) için de kullanılabilir.
- **Arama Motoru:** Meilisearch veya Elasticsearch (açık kaynak sürüm, self-hosted)
  - Ürün arama, filtreleme, otomatik tamamlama için. Meilisearch daha hafif ve kurulumu kolay, başlangıç için önerilir.
- **Mesaj Kuyruğu / Event Bus:** NATS veya RabbitMQ (açık kaynak)
  - Sipariş oluşturma, stok güncelleme, bildirim gönderme, kurye/sürücü durum değişiklikleri (kabul etti / yolda / vardı) gibi asenkron işler için.
  - E-ticarette "sipariş alındı ama stok düşmedi" gibi tutarsızlıkları önlemek için event-driven yaklaşım önemli.
- **Dosya / Görsel Depolama:** MinIO (S3 uyumlu, açık kaynak, self-hosted)
  - Ürün görselleri, fatura PDF'leri, sürücü/kurye belgeleri vs. için.

### Navigasyon, Konum ve Rota Sistemi (Kurye/Taksi Modülü)
- **PostGIS (PostgreSQL eklentisi, açık kaynak)**
  - Coğrafi veri sorguları için (mesafe, alan, en yakın nokta vb.). PostgreSQL'in doğal uzantısı, ek lisans gerektirmez.
  - Kalıcı konum geçmişi, adres/bölge verisi, teslimat bölgeleri gibi veriler burada tutulur.
- **Redis Geo (GEOADD, GEORADIUS, GEOSEARCH)**
  - Anlık "yakındaki sürücü/kurye" sorguları için. Sık güncellenen canlı konum verisi burada, PostGIS'e göre çok daha hızlı.
- **OSRM (Open Source Routing Machine, self-hosted)**
  - Rota, mesafe ve süre hesaplama için. Google Maps Directions API'nin ücretsiz açık kaynak alternatifi.
  - OpenStreetMap verisiyle çalışır, kendi sunucunda host edilir.
- **OpenStreetMap (OSM) verisi**
  - Harita ve yol ağı verisi kaynağı, tamamen ücretsiz. Mobil tarafta harita gösterimi için (örn. MapLibre GL — açık kaynak Mapbox alternatifi) ile birlikte kullanılır.
- **WebSocket katmanı (Go - gorilla/websocket veya benzeri)**
  - Canlı konum takibi, sipariş/sürücü durum güncellemeleri için gerçek zamanlı iletişim. Normal HTTP polling yerine.
  - Mobil istemcilerde bağlantı sık kesilebileceğinden (ağ değişimi, arka plana alma) **reconnect ve heartbeat mekanizması** baştan tasarıma dahil edilmeli.

### Mobil'e Özel Bileşenler
- **Push Bildirimleri: Firebase Cloud Messaging (FCM)**
  - "Siparişiniz onaylandı", "Kuryeniz yolda" gibi anlık bildirimler için iOS/Android sektör standardı.
  - Bu, "tamamen açık kaynak" kuralının tek istisnasıdır — bildirim gönderimi pratikte ücretsizdir ve gerçekçi bir self-hosted alternatifi yoktur. Mimari, bildirim gönderme mantığını adapter pattern ile soyutlamalı (ileride başka sağlayıcıya geçiş kolay olsun).
- **Konum gönderim sıklığı (adaptif):** Mobil cihazda pil tüketimini azaltmak için, kullanıcı hareketsizken konum güncelleme sıklığı azaltılmalı, hareket halindeyken artırılmalı. Backend bu farklı sıklıklara göre veri akışını yönetebilmeli.

### Ödeme
- **Ödeme Altyapısı Notu:** Ödeme sağlayıcı (banka/PSP entegrasyonu) konusunda "ücretsiz" mümkün değildir — bu, iş modelinin bir parçası ve ayrı bir konudur. Yazılım mimarisi, hangi ödeme sağlayıcısı seçilirse seçilsin değiştirilebilir (adapter pattern) şekilde tasarlanmalı.

## Mimari Prensipler
1. **Clean / Hexagonal Architecture** — iş mantığı framework ve veritabanından bağımsız.
2. **Domain-Driven Tasarım yaklaşımı:** Kullanıcı, Katalog, Sepet, Sipariş, Ödeme, Stok, Bildirim, Kurye/Sürücü, Konum/Navigasyon gibi alanları ayrı modüller/servisler olarak düşün (monolith içinde modüler olabilir, ileride mikroservise bölünebilir — "modüler monolith" ile başla).
3. **Tek backend, çoklu istemci:** Web ve mobil için ayrı backend yazılmaz; aynı API katmanı her ikisine de hizmet eder. İstemciye özel mantık (örn. push bildirim tetikleme) API içinde ayrı, izole bir katmanda tutulur.
4. **Veri tutarlılığı kritik noktalarda öncelik:** Sipariş oluşturma, ödeme onayı, stok düşürme, sürücü-yolcu eşleştirme gibi işlemler veritabanı transaction'ları veya event-driven saga pattern ile garanti altına alınmalı.
5. **Canlı veri ile kalıcı veri ayrımı:** Sürücü/kurye konumu gibi yüksek frekanslı veriler Redis'te tutulur, sadece gerekli özet/geçmiş bilgi PostgreSQL'e yazılır (her konum güncellemesini doğrudan PostgreSQL'e yazmak performans sorununa yol açar).
6. Repository pattern — DB erişimi soyutlanmalı, ileride sharding/read-replica eklemek kolay olsun.
7. Konfigürasyon (DB, Redis, mesaj kuyruğu, OSRM, MinIO, FCM bağlantıları, secret'lar) environment variable üzerinden yönetilmeli.
8. Structured logging ve merkezi hata yönetimi.
9. Güvenlik: SQL injection, XSS, CSRF, ayrıca e-ticarete özel olarak **fiyat manipülasyonu, stok yarışı (race condition), ödeme tekrar saldırıları (replay attack)**; navigasyon/taksi modülüne özel olarak **sahte konum (GPS spoofing) ve sürücü-yolcu eşleştirme manipülasyonu**; mobil'e özel olarak **API token/oturum güvenliği ve cihaz bazlı kimlik doğrulama** gibi riskler en baştan düşünülmeli.

## Veritabanı Kurulumu İçin Beklenti
- Sana dosya/şema/gereksinim verdiğimde, önce mevcut yapıyı analiz et.
- Tablo tasarımında: birincil anahtarlar, ilişkiler, indeksler, partition stratejisi (özellikle sipariş/log/konum geçmişi tabloları büyüyeceği için tarih bazlı partition düşün).
- Stok ve sipariş gibi kritik tablolarda **race condition** önlemleri (örn. `SELECT ... FOR UPDATE`, optimistic locking) baştan tasarıma dahil edilmeli.
- Konum/coğrafi veri içeren tablolarda PostGIS veri tipleri (`geography`/`geometry`) ve uygun mekansal indeksler (`GIST`) kullanılmalı.
- Migration dosyaları (golang-migrate veya benzeri) düzenli ve sıralı oluşturulmalı.
- Şema değişikliklerini açıklamalarla sun, onaylamadan kalıcı değişiklik yapma.

## Kod Yazım Standartları
- `gofmt` / `golangci-lint` standartlarına uy.
- Fonksiyonlar küçük, okunabilir, test edilebilir.
- Önemli modüller için açıklama yorumları ekle.
- Performans kritik noktalarda (N+1 query, gereksiz lock, büyük transaction, sık WebSocket yayını, mobil için gereksiz veri trafiği) proaktif uyarıda bulun.

## Davranış Beklentisi
- Önerilerini her zaman "50 milyon kullanıcı + e-ticaret + canlı navigasyon/kurye/taksi + web ve mobil + sıfır lisans maliyeti (FCM hariç)" perspektifinden değerlendir.
- Ücretli/managed bir cloud servisi veya API (örn. Google Maps) önermeden önce, açık kaynak self-hosted alternatifini öner.
- Basit ama yanlış çözüm yerine, biraz daha emek isteyen ama doğru/ölçeklenebilir/tutarlı çözümü öner.
- Bir karar ileride teknik borç oluşturacaksa açıkça belirt, alternatif sun.
- Karmaşık kararlarda seçenekleri kısaca açıkla, sonra net önerini belirt.

---

**Bu talimatları okudum ve anladım. Şimdi sana proje dosyalarını/gereksinimlerini vereceğim, bunlara göre veritabanı şemasını ve kod yapısını oluşturmaya başla.**
