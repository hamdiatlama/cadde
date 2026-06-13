# 📋 SİSTEM EKSİK ANALİZİ — GAP ANALYSIS

> **Tarih:** Haziran 2026
> **Kapsam:** Tüm platform modülleri (çiçek, yemek, taksi, kurye)
> **Durum:** 11/31 alan tamam, 4/31 kısmi, 16/31 hiç başlanmamış

---

## 🧭 GENEL DURUM

```
                    ┌──────────────────────┐
                    │  TOPLAM 31 ALAN       │
                    │                       │
                    │  ✅ 11 Tamam          │
                    │  🟡  4 Kısmi          │
                    │  ❌ 16 Eksik          │
                    └──────────────────────┘

    ──── KATEGORİ BAZINDA ────

    📐 Tasarım/Doküman       │███████████████████████░░│ 9/9   ✅
    🔧 Backend/Altyapı      │░░░░░░░░░░░░░░░░░░░░░░░░│ 0/10  ❌
    🎨 Frontend/UI           │██████████████░░░░░░░░░░│ 5/8   🟡
    👤 Kullanıcı Yönetimi   │░░░░░░░░░░░░░░░░░░░░░░░░│ 1/5   ❌
    🛡️ Hukuk/Uyumluluk     │░░░░░░░░░░░░░░░░░░░░░░░░│ 0/4   ❌
    📊 İş/Pazarlama          │░░░░░░░░░░░░░░░░░░░░░░░░│ 1/4   ❌
    🔐 Güvenlik              │░░░░░░░░░░░░░░░░░░░░░░░░│ 0/5   ❌
    🧪 Test/QA               │░░░░░░░░░░░░░░░░░░░░░░░░│ 0/4   ❌
```

---

## 1. 📐 TASARIM / DOKÜMANTASYON (9/9 ✅)

### 1.1 Tamamlananlar

| # | Dosya | Açıklama | Durum |
|---|-------|----------|-------|
| 1 | `MASTER-PLAN.md` | Platform ana planı, hesap türleri, iş modeli, komisyon yapısı | ✅ |
| 2 | `CICEK-SISTEMI-DESIGN.md` | Çiçek sistemi — 21 bölüm, tedarik zinciri, özel sipariş, tazelik, puanlama, akış diyagramları, API, DB | ✅ |
| 3 | `YEMEK-SISTEMI-DESIGN.md` | Yemek sistemi — 20 bölüm, evrak puanlama, canlı kamera, kurye, akış | ✅ |
| 4 | `TAXI-SYSTEM-DESIGN.md` | Taksi sistemi — 38 bölüm, 8700+ satır, plaka, vardiya, puanlama | ✅ |
| 5 | `KURY-SISTEMI-DESIGN.md` | Bağımsız kurye havuzu — tüm servisler için ortak | ✅ |
| 6 | `RAKIP-ANALIZI.md` | 11 Türk + 10 global platform analizi | ✅ |
| 7 | `YURT-DISI-GENISLEME.md` | Uluslararası genişleme stratejisi | ✅ |

### 1.2 Kısmi Olanlar

| # | Dosya | Eksik | Durum |
|---|-------|-------|-------|
| 8 | `DATABASE.md` | Şema var ama tüm servisleri (çiçek+yemek+taksi+kurye) tek birleşik ERD'de göstermiyor. İlişkiler dağınık. | 🟡 |
| 9 | `FLOW-DIAGRAMS.md` | Diyagramlar ayrı ayrı dosyalarda. Tek bir "platform ana akışı" yok. | 🟡 |

---

## 2. 🔧 BACKEND / ALTYAPI (0/10 ❌)

> **En kritik eksik.** Tasarım var ama HİÇBİR backend kodu yazılmadı.

### 2.1 API Sunucusu

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 1 | **HTTP Server + Router** | Express/Fastify/FastAPI benzeri bir framework kurulumu yok. Route, middleware, error handler yok. | 🔴 |
| 2 | **API Endpoint'leri** | Tüm modüllerde API tabloları çizildi ama hiçbiri kodlanmadı. | 🔴 |
| 3 | **Middleware** | Auth, CORS, logging, rate-limit, validation middleware'leri yok. | 🔴 |

### 2.2 Veritabanı

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 4 | **Migration Sistemi** | DB şeması var ama migration dosyası (SQL dosyası veya ORM migration) yok. | 🔴 |
| 5 | **Bağlantı + ORM/Query Builder** | Prisma/TypeORM/Sequelize kurulumu yok. raw SQL için connection pool yok. | 🔴 |
| 6 | **Seed Data** | Örnek veri (çiçekler, kuryeler, dükkanlar) için seed script'i yok. | 🟡 |

### 2.3 Kimlik Doğrulama

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 7 | **Auth Sistemi** | JWT/OAuth, register, login, refresh token, email doğrulama, şifre sıfırlama yok. | 🔴 |
| 8 | **Yetkilendirme (RBAC)** | Rol bazlı erişim (admin, çiçekçi, kurye, müşteri) yok. | 🔴 |

### 2.4 Ödeme

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 9 | **Ödeme Gateway** | İyzico/PayTR/PayPal/Stripe entegrasyonu yok. Kart, kapıda nakit, cüzdan, taksit yok. | 🔴 |
| 10 | **İade / İptal Akışı** | Ödeme iadesi, kısmi iade, chargeback yok. | 🔴 |

### 2.5 Bildirim

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 11 | **Push Bildirim** | Firebase Cloud Messaging (FCM) kurulumu yok. | 🔴 |
| 12 | **SMS** | Twilio/Netgsm entegrasyonu yok. | 🟡 |
| 13 | **E-posta** | SMTP ayarı, e-posta şablonları (sipariş onay, hatırlatma) yok. | 🟡 |
| 14 | **Bildirim Kuyruğu** | RabbitMQ/Bull/Redis Queue yok. Bildirimler senkron kalır, ölçeklenemez. | 🟡 |

### 2.6 Dosya Yönetimi

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 15 | **Dosya Yükleme** | Fotoğraf/sertifika yükleme API'si yok. Multer/S3/Cloudinary yok. | 🔴 |
| 16 | **CDN + Resize** | Görsel optimize etme, thumbnail, CDN dağıtımı yok. | 🟡 |

### 2.7 Gerçek Zamanlı / Harita

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 17 | **WebSocket / Socket.io** | Canlı kurye takibi, anlık bildirim, stok güncellemesi için WS sunucusu yok. | 🔴 |
| 18 | **Harita Entegrasyonu** | Mapbox/Google Maps API, geocoding, distance matrix, rotalama yok. | 🔴 |

### 2.8 Arama / Önbellek / DevOps

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 19 | **Arama Motoru** | Elasticsearch/Meilisearch/Typesense yok. Ürün/dükkan arama yok. | 🟡 |
| 20 | **Redis** | Cache, session store, rate-limit, pub/sub yok. | 🟡 |
| 21 | **Docker + CI/CD** | Dockerfile, docker-compose, GitHub Actions yok. | 🟡 |
| 22 | **Loglama + Monitoring** | Winston/Sentry/Datadog yok. Hata takibi, metrik toplama yok. | 🟡 |

---

## 3. 🎨 FRONTEND / UI (5/8)

### 3.1 Tamamlananlar

| # | Dosya | Açıklama | Durum |
|---|-------|----------|-------|
| 1 | `cicek-dukkan.html` | Çiçek ana demo — tüm özellikler (sipariş, fotoğraf onay, yorum, puan, abonelik, kurumsal, hediy kartı) | ✅ |
| 2 | `yemek-ana-sayfa.html` | Yemek ana sayfa demo — restoran listeleme, filtreleme | ✅ |
| 3 | `yemek-ui-demo.html` | Yemek UI demo — 2023 satırlık kapsamlı UI | ✅ |
| 4 | `cicek-teslimat-demo.html` | Teslimat süresi + zaman çizelgesi + ortak kurye havuzu | ✅ |
| 5 | `cicek-arti-eksi-karsilastirma.html` | Artı/eksi karşılaştırma sayfası | ✅ |

### 3.2 Eksik Olanlar

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 6 | **React/Vue/Angular Uygulaması** | Tüm HTML demolar statik. Modern SPA framework ile yeniden yazılmalı. Component yapısı, state management, routing yok. | 🔴 |
| 7 | **Mobil Uygulama** | iOS + Android için native veya React Native uygulama yok. Kurye uygulaması, müşteri uygulaması yok. | 🔴 |
| 8 | **Admin Paneli** | Platform yönetimi için admin dashboard (kullanıcı yönetimi, komisyon, raporlama) yok. | 🟡 |

### 3.3 Kısmi Olanlar

| # | Dosya | Eksik | Durum |
|---|-------|-------|-------|
| 9 | CSS/Design System | CSS değişkenleri var ama Figma tasarım sistemi, component kütüphanesi yok. | 🟡 |

---

## 4. 👤 KULLANICI YÖNETİMİ (1/5)

### 4.1 Tamamlananlar

| # | Açıklama | Durum |
|---|----------|-------|
| 1 | Kurye ekran tasarımları (KURY-SISTEMI-DESIGN.md içinde) | ✅ |

### 4.2 Eksik Olanlar

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 2 | **Kayıt / Giriş Sayfaları** | Register, login, şifre sıfırlama, email doğrulama UI'ı yok. | 🔴 |
| 3 | **Profil Sayfası** | Kullanıcı bilgileri, adres defteri, sipariş geçmişi, puan bakiyesi görüntüleme yok. | 🔴 |
| 4 | **Kurumsal Hesap** | Şirket profili, çalışan ekleme, rol yönetimi UI'ı yok. | 🟡 |
| 5 | **Kamusal Hesap** | Resmi kurum kaydı, duyuru yönetimi UI'ı yok. | 🟢 |

---

## 5. 🛡️ HUKUK / UYUMLULUK (0/4 ❌)

> **Yayına almadan önce MUTLAKA tamamlanmalı.** Eksik hukuk metni = yasal risk.

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 1 | **KVKK / GDPR Aydınlatma Metni** | Hangi veri toplanır, neden toplanır, kimlerle paylaşılır, nasıl silinir? | 🔴 |
| 2 | **Kullanım Koşulları (ToS)** | Platform kuralları, üyelik şartları, hesap kapatma, yasaklı işlemler. | 🔴 |
| 3 | **Mesafeli Satış Sözleşmesi** | Cayma hakkı, iade koşulları, teslimat süresi, ödeme taahhüdü. | 🔴 |
| 4 | **Çerez Politikası** | Hangi çerezler kullanılır, çerez izni banner'ı, Google Analytics/Tag Manager. | 🟡 |

---

## 6. 📊 İŞ / PAZARLAMA (1/4)

### 6.1 Kısmi Olanlar

| # | Açıklama | Eksik | Durum |
|---|----------|-------|-------|
| 1 | Sadakat puanı | HTML demo'da gösterim var ama backend hesaplama, harcama, süre yönetimi yok. | 🟡 |

### 6.2 Eksik Olanlar

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 2 | **SEO Altyapısı** | Robots.txt, sitemap.xml, canonical URL, schema.org, meta etiketler, Open Graph yok. | 🟡 |
| 3 | **Referans / Davet Sistemi** | "Arkadaşını davet et, 20₺ kazan" mekanizması yok. | 🟢 |
| 4 | **Çoklu Dil (i18n)** | Türkçe dışında dil yok. İngilizce, Arapça, Rusça çevirisi yok. | 🟢 |

---

## 7. 🔐 GÜVENLİK (0/5 ❌)

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 1 | **SSL / HTTPS** | Sertifika yok, tüm bağlantı şifresiz. | 🔴 |
| 2 | **Rate Limiting** | API brute-force, DDoS koruması yok. | 🔴 |
| 3 | **Input Validation** | SQL Injection, XSS, CSRF koruması kodlanmadı. | 🔴 |
| 4 | **Veri Yedekleme** | Otomatik DB yedekleme, disaster recovery planı yok. RPO/RTO tanımlı değil. | 🔴 |
| 5 | **Penetrasyon Testi** | Hiç yapılmadı. Güvenlik açıkları tespit edilmedi. | 🟡 |

---

## 8. 🧪 TEST / QA (0/4 ❌)

| # | Eksik | Detay | Öncelik |
|---|-------|-------|---------|
| 1 | **Unit Test** | Hiçbir test dosyası yok. Backend için Jest/PyTest, frontend için Vitest yok. | 🔴 |
| 2 | **Integration Test** | API test, DB test (SuperTest + TestContainers) yok. | 🔴 |
| 3 | **E2E Test** | Cypress/Playwright ile UI testi yok. | 🟡 |
| 4 | **Yük Testi** | k6/Artillery ile performans testi yok. Sistemin kaç kullanıcı kaldıracağı bilinmiyor. | 🟡 |

---

## 9. 🚀 ÖNCELİKLİ YOL HARİTASI

### Aşama 1 — MVP (1-2 ay)
```
🔴 Acil — Sistem çalışmazsa olmaz
├── API Sunucusu kurulumu (Node.js/Python/FastAPI)
├── PostgreSQL + Migration + Seed
├── Auth sistemi (register, login, JWT)
├── Ödeme entegrasyonu (iyzico/PayTR)
├── Çiçekçi CRUD (dükkan açma, ürün ekleme)
├── Sipariş akışı (oluşturma → hazırlık → fotoğraf → onay → kurye → teslimat)
├── Kurye atama (ortak havuz temel seviye)
└── Dosya yükleme (fotoğraf onay sistemi)
```

### Aşama 2 — Genişletme (2-4 ay)
```
🟡 Orta — Kullanıcı deneyimi için gerekli
├── WebSocket ile canlı takip
├── Harita entegrasyonu
├── Bildirim sistemi (push + SMS + email)
├── Admin paneli
├── Zaman çizelgesi backend
├── Puanlama + yorum sistemi
├── Hukuk metinleri (KVKK, ToS)
├── Redis cache
└── Docker + CI/CD
```

### Aşama 3 — Optimizasyon (4-6 ay)
```
🟢 Düşük — İşi büyütmek için
├── React/Vue ile SPA yeniden yazım
├── Mobil uygulama (React Native)
├── AI tazelik kontrolü
├── Arama motoru (Meilisearch)
├── Unit + Integration + E2E testleri
├── SEO altyapısı
├── Çoklu dil desteği
├── Canlı kamera entegrasyonu
├── Penetrasyon testi
└── Yük testi + performans optimizasyonu
```

---

## 10. ÇİÇEK SİSTEMİ ÖZEL EKSİKLER

Çiçek sisteminde **tasarımı var, kodu olmayan** özellikler:

| # | Özellik | Tasarım (Nerede?) | Kod Durumu | Öncelik |
|---|---------|-------------------|------------|---------|
| 1 | Dükkan kaydı + belge yükleme | CICEK-SISTEMI-DESIGN.md §2 | ❌ | 🔴 |
| 2 | Hazır ürün + özel sipariş sistemi | CICEK-SISTEMI-DESIGN.md §4 | ❌ | 🔴 |
| 3 | Sipariş akışı (6 aşama) | CICEK-SISTEMI-DESIGN.md §8 | ❌ (HTML demo'da simüle) | 🔴 |
| 4 | Zaman çizelgesi / ön sipariş | CICEK-SISTEMI-DESIGN.md §2.3 | ❌ (HTML demo'da simüle) | 🔴 |
| 5 | Mesaj kartı zorunluluğu | CICEK-SISTEMI-DESIGN.md §4.2-a | ❌ | 🔴 |
| 6 | Fotoğraflı onay sistemi | CICEK-SISTEMI-DESIGN.md §4.4 | ❌ (HTML demo'da simüle) | 🔴 |
| 7 | Tazelik garantisi + AI kontrol | CICEK-SISTEMI-DESIGN.md §15 | ❌ | 🟡 |
| 8 | 3 yönlü puanlama | CICEK-SISTEMI-DESIGN.md §16 | ❌ | 🟡 |
| 9 | Zorunlu görsel sistemi (5 kat.) | CICEK-SISTEMI-DESIGN.md §12 | ❌ | 🟡 |
| 10 | Canlı kamera | CICEK-SISTEMI-DESIGN.md §13 | ❌ | 🟢 |
| 11 | Evrak bazlı puanlama | CICEK-SISTEMI-DESIGN.md §14 | ❌ | 🟡 |
| 12 | Abonelik sistemi | HTML demo'da var | ❌ | 🟡 |
| 13 | Kurumsal sipariş modülü | HTML demo'da var | ❌ | 🟡 |
| 14 | Hediye kartı sistemi | HTML demo'da var | ❌ | 🟡 |
| 15 | Sadakat puanı (back-end) | HTML demo'da var | ❌ | 🟡 |
| 16 | Özel gün takvimi + hatırlatma | CICEK-SISTEMI-DESIGN.md §10 | ❌ | 🟡 |
| 17 | Dinamik teslimat süresi (API) | CICEK-SISTEMI-DESIGN.md §17 | ❌ (HTML demo'da simüle) | 🔴 |
| 18 | Dükkan durum yönetimi (3 seviye) | CICEK-SISTEMI-DESIGN.md §2.3 | ❌ (HTML demo'da simüle) | 🔴 |

---

## 11. ÖZET

```
✅ DOKÜMANTASYON TAMAM    → Kodlamaya hazır
❌ BACKEND YOK            → API sunucusu kurulumu Aşama 1
❌ FRONTEND STATİK HTML   → React/Vue geçişi Aşama 3
❌ MOBİL UYGULAMA YOK     → React Native Aşama 3
❌ ÖDEME YOK              → Aşama 1'in kritik parçası
❌ TEST YOK               → Aşama 3
❌ GÜVENLİK YOK           → Aşama 1'de temel, Aşama 3'te ileri
❌ HUKUK METİNLERİ YOK    → Aşama 2 (yayından önce)
```

> **Öncelik:** Backend API + PostgreSQL + Auth + Ödeme + Sipariş Akışı. Bunlar olmadan sistem ÇALIŞMAZ. Gerisi sonra gelir.
