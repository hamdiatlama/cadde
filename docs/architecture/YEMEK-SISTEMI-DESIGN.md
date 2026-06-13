# 🍽️ YEMEK SİSTEMİ - KAPSAMLI TASARIM DOKÜMANI

---

## 📋 İÇİNDEKİLER

1. [Restoran Kaydı ve Zorunlu Belgeler](#1-restoran-kaydı-ve-zorunlu-belgeler)
   1.5 [Küçük Üretici / Ev Üreticisi Kaydı](#15-küçük-üretici--ev-üreticisi-kaydı)
2. [Restoran Görsel Sistemi (6+ Zorunlu)](#2-restoran-görsel-sistemi-6-zorunlu)
3. [Canlı Kamera Entegrasyonu](#3-canlı-kamera-entegrasyonu)
4. [Evrak Bazlı Puanlama](#4-evrak-bazlı-puanlama)
5. [Ürün Tazeliği Garantisi ve Zaman Damgası](#5-ürün-tazeliği-garantisi-ve-zaman-damgası)
6. [Çift Yönlü Puanlama Sistemi](#6-çift-yönlü-puanlama-sistemi)
7. [%2 Komisyon Modeli](#7-2-komisyon-modeli)
8. [Dinamik Teslimat Süresi Hesaplama](#8-dinamik-teslimat-süresi-hesaplama)
9. [Platform Kurye Havuzu ve Atama Modelleri](#9-platform-kurye-havuzu-ve-atama-modelleri) → Detay: [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md)
10. [Kurye Yönetimi ve Mobing Önleme](#10-kurye-yönetimi-ve-mobing-önleme) → Detay: [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md)
11. [QR Kod Teslimat Onay Sistemi](#11-qr-kod-teslimat-onay-sistemi)
12. [Akıllı Kapıda Ödeme Sistemi](#12-akıllı-kapıda-ödeme-sistemi)
13. [Yerinde Yemek Ödeme Sistemi (Dine-In)](#13-yerinde-yemek-ödeme-sistemi-dine-in)
14. [Zorunlu Aktif Müşteri Hizmetleri](#14-zorunlu-aktif-müşteri-hizmetleri)
15. [Restoran Sahibi Kurumsal Paneli](#15-restoran-sahibi-kurumsal-paneli)
16. [Sipariş Yönetimi ve Canlı Takip](#16-sipariş-yönetimi-ve-canlı-takip)
17. [Cüzdan ve Ödeme Sistemi (Taksi ile Ortak)](#17-cüzdan-ve-ödeme-sistemi-taksi-ile-ortak)
18. [Veritabanı Şeması](#18-veritabanı-şeması)
19. [API Endpoint'leri](#19-api-endpointleri)
20. [Akış Diyagramları](#20-akış-diyagramları)

---

## 1. RESTORAN KAYDI VE ZORUNLU BELGELER

### 1.1 Ön Koşul
Her restoran öncelikle **Kurumsal Hesap** açmak zorundadır. Bireysel hesap üzerinden restoran kaydı yapılamaz. Restoran sahibi veya yetkilisi, şirket adına kurumsal hesap açar ve restoranı bu hesaba bağlar.

### 1.2 Zorunlu Belgeler

| Belge | Açıklama | Geçerlilik Süresi |
|-------|----------|-------------------|
| **Vergi Levhası** | Restoranın bağlı olduğu vergi dairesi | 1 yıl |
| **İşletme Ruhsatı** | Belediye/ilçe kaymakamlığı onaylı | 5 yıl |
| **Hijyen Sertifikası** | Tarım ve Orman Bakanlığı onaylı | 2 yıl |
| **SGK İşyeri Tescil** | Aktif SGK sicil numarası | Süresiz |
| **İmza Sirküleri** | Yetkili imza sahiplerini gösterir | Süresiz |
| **Kepçe/Gıda Sicil** | Gıda üretim izni | 5 yıl |
| **Yangın Güvenlik Raporu** | İtfaiye onaylı | 2 yıl |
| **Adli Sicil (İşletme Sahibi)** | Sabıka kaydı | 3 ay |
| **Otopark Kapasite Belgesi** | Varsa otopark bilgisi | Süresiz |

### 1.3 Restoran Profil Bilgileri

```
RESTORAN PROFİLİ:
├── 🏢 İşletme Adı (Ticari unvan)
├── 📛 Marka Adı (görünen isim)
├── 📍 Adres (açık + harita konumu)
├── 📞 Telefon (zorunlu, görünür)
├── 📧 E-posta (zorunlu)
├── 🌐 Web Sitesi (opsiyonel)
├── 🕐 Çalışma Saatleri (gün bazlı)
├── 🗺️ Servis Bölgesi (çap olarak km)
├── 🍽️ Mutfak Türü (Türk, İtalyan, vs.)
├── 🏷️ Fiyat Aralığı (₺, ₺₺, ₺₺₺)
├── 🪑 Masa Sayısı (Dine-In için zorunlu, 0 = sadece paket)
└── 📋 Menü Tipi (paket servis, restoran içi, ikisi de)
```

### 1.4 Çalışma Saatleri Zorunluluğu

Restoran çalışma saatlerini **gün bazlı** girmek zorundadır. Sistem şu kuralları uygular:

- Saat girilmeyen gün **kapalı** kabul edilir
- Sipariş sadece **açık** gün ve saatlerde alınır
- Tatil günleri önceden bildirilmelidir (en az 24 saat)
- Ani kapanışlarda aktif siparişler iptal edilir, restorana ceza puanı yazılır

---

### 1.5 Küçük Üretici / Ev Üreticisi Kaydı

#### 1.5.1 Tanım

Küçük üretici modülü, fişek bir restoran açamayan ancak ev usulü yemek üreten kişiler için tasarlanmıştır. Bu kişiler:
- Fiziksel restoranı olmayan ev üreticileri
- Köy/kasaba üreticileri (reçel, turşu, börek, mantı)
- Haftalık/aylık periyodik üretim yapanlar
- Sınırlı kapasiteli butik üreticiler

#### 1.5.2 Küçük Üretici Kayıt Şartları

Küçük üreticiler için belge yükü **azaltılmıştır** ancak güvenlik düşürülmemiştir:

| Belge | Zorunlu | Açıklama |
|-------|---------|----------|
| Kimlik (TC/YK) | Evet | Nüfus cüzdanı veya pasaport |
| Adli sicil | Evet | Temiz sabıka kaydı |
| İkametgah | Evet | Adres teyidi |
| Hijyen Sertifikası | Evet | Halk Eğitim veya Tarım Bakanlığı onaylı temel hijyen |
| Vergi Mükellefiyeti | Evet | Şahıs şirketi veya esnaf muafiyeti |
| SGK Kaydı | Evet | İsteğe bağlı veya aktif sigorta |
| Üretim Alanı Fotoğrafı | Evet | Mutfak/üretim alanı net görünür |
| Su/Atık Belgesi | Evet | Altyapı uygunluk (belediye) |

#### 1.5.3 Küçük Üretici vs Tam Restoran Farkları

| Özellik | Küçük Üretici | Tam Restoran |
|---------|---------------|--------------|
| Fiziksel restoran | Gerekmez (ev mutfağı) | Zorunlu |
| İşletme ruhsatı | Gerekmez (ev) | Zorunlu |
| Görsel zorunluluğu | 3 fotoğraf | 6+ fotoğraf |
| Canlı kamera | Opsiyonel | Opsiyonel (+100 puan) |
| Kurye | Sadece platform kuryesi | Kendi + platform kuryesi |
| Komisyon | %1.5 (teşvik) | %2 |
| Günlük sipariş limiti | 50 sipariş/gün | Limitsiz |
| Haftalık üretim | Planlı (önceden bildirim) | Her gün |
| Müşteri hizmetleri | Platform üzerinden | Kendi + platform |

#### 1.5.4 Küçük Üretici Sipariş Limiti ve Kapasite

Küçük üreticinin kapasitesini aşmaması için:

```
KAPASİTE YÖNETİMİ:
├── Maksimum günlük sipariş: Sistem onaylı (varsayılan 50)
├── Üretici kapasite artışı talep edebilir (belge + değerlendirme)
├── Her ürün için maksimum günlük adet limiti
├── Hazırlık süresi otomatik hesaplanır (tecrübeye göre)
├── Aşırı sipariş durumunda otomatik kapanma
└── Kapasite aşımı: 1 saat mola + uyarı
```

#### 1.5.5 Küçük Üretici Kurye Modeli

Küçük üreticiler **sadece platform kurye havuzu** kullanır. Kendi kuryeleri yoktur.

```
KÜÇÜK ÜRETİCİ TESLİMAT:
├── Sipariş alınır → Hazırlık başlar
├── Hazırlık bitince → Platform kuryesi atanır
├── Kurye ücreti: Müşteri öder (standart tarife)
├── Kurye bekleme süresi: Maksimum 3 dk
└── Ek süre: Üreticiye ek ücret (gecikme)
```

---

### 1.1 Zorunlu Görsel Kategorileri

Her restoranın aşağıdaki **6 kategoride** en az 1'er fotoğraf yüklemesi zorunludur:

```
📸 ZORUNLU GÖRSELLER:
├── 1️⃣ DIŞ CEPHE
│   ├── Restoranın sokak görünümü
│   ├── Tabela net okunur olmalı
│   └── Çevre düzeni görünmeli
│
├── 2️⃣ SERVİS/SALON ALANI
│   ├── İç mekan genel görünümü
│   ├── Masa düzeni ve oturma alanı
│   └── Aydınlatma ve dekorasyon
│
├── 3️⃣ MUTFAK
│   ├── Tezgah ve ekipmanlar
│   ├── Temizlik durumu net görünür
│   └── Personel çalışma alanı
│
├── 4️⃣ ÇEVRE VE KONUM
│   ├── Sokak görünümü (çevredeki işletmeler)
│   ├── Ulaşım noktaları (varsa metro/otobüs)
│   └── Yaya yolu ve erişim
│
├── 5️⃣ TUVALET / HİJYEN ALANI
│   ├── Tuvalet temizliği net görünür
│   ├── Lavabo ve hijyen malzemeleri
│   └── Varsa bebek bakım ünitesi
│
└── 6️⃣ OTOPARK
    ├── Otopark alanı (varsa)
    ├── Kapasite bilgisi
    └── Engelli park yeri (varsa)
```

### 1.2 Görsel Kalite Standartları

| Kriter | Şart | Puan |
|--------|------|------|
| Minimum çözünürlük | 1920x1080 | - |
| Netlik | Bulanık olmayacak | +5/her net foto |
| Aydınlatma | Doğal/yapay yeterli ışık | +5 |
| Filtresiz | Orijinal renkler | +5 |
| Tarih damgası | Son 30 gün içinde çekilmiş | +10 |
| Geotag | Çekim koordinatı eşleşiyor | +10 |

### 1.3 Görsel Eksiklik Cezaları

| Durum | Yaptırım |
|-------|----------|
| 0-2 fotoğraf | Profil pasif, sipariş alınamaz |
| 3-4 fotoğraf | Sadece %50 kapasite sipariş |
| 5 fotoğraf | Tam kapasite, eksik kategoriler belirtilir |
| 6+ fotoğraf | Tam kapasite + öne çıkarma |

### 1.4 Periyodik Görsel Yenileme

Restoranların görsellerini **her 90 günde bir** yenilemesi zorunludur:

- Yenilenmeyen görseller eski olarak işaretlenir (-5 puan)
- 120 günü geçen görsel otomatik silinir
- Yenileme hatırlatması: 75., 80., 85. günlerde SMS/E-posta

---

## 3. CANLI KAMERA ENTEGRASYONU

### 3.1 Sistem Tanımı

Restoranlar, mutfak ve/veya servis alanında **canlı kamera** yayını açabilir. Bu tamamen opsiyoneldir ancak **+100 puan** bonusu sağlar.

### 3.2 Kamera Şartları

| Kriter | Zorunluluk |
|--------|-----------|
| Minimum çözünürlük | 720p (1280x720) |
| Minimum FPS | 15 |
| Ses | Sadece ortam sesi (mikrofon kapalı opsiyonel) |
| Kayıt saklama | Son 7 gün (sadece şikayet durumunda erişim) |
| Yayın gecikmesi | Maksimum 5 saniye |
| Çalışma saati | Restoran açıkken yayın zorunlu |
| Kamera açısı | Tezgah ve pişirme alanı net görünmeli |

### 3.3 Puan Katkısı

```
CANLI KAMERA PUAN HESABI:
├── Kamera var, aktif ve şartlara uygun:    +100 puan
├── Kamera var ama günde 1+ saat kapalı:    +50 puan
├── Kamera var ama günde 3+ saat kapalı:    +0 puan (ceza yok)
├── Kamera yok:                              +0 puan (ceza yok)
└── Kamera yayını kesintili/gecikmeli:       +25 puan
```

### 3.4 Müşteri Deneyimi

- Müşteri, sipariş öncesi canlı mutfak izleyebilir
- Sipariş sonrası "Mutfak Canlı" butonu ile yayına bağlanabilir
- Yayın sırasında ekran görüntüsü alınamaz (DRM koruması)
- Müşteri, yayında şikayet edecek bir durum görürse anlık bildirim gönderebilir

### 3.5 Teknik Altyapı

```
TEKNOLOJİ YIĞINI:
├── WebRTC (düşük gecikmeli yayın)
├── HLS (fallback yayın)
├── RTMP (kamera gönderimi)
├── AWS Kinesis Video Streams (depolama)
├── 7 gün sonra otomatik silme (GDPR uyumlu)
└── Şikayet durumunda dondurma ve inceleme
```

---

## 4. EVRAK BAZLI PUANLAMA

> ⚠️ **Görsel Zorunluluğu:** Sertifika ve izin evraklarının **fotoğrafı/tarayıcı görüntüsü** yüklenmelidir. Sadece evrak adı girmek puan kazandırmaz. Görsel olmayan evraklar işleme alınmaz.

### 4.1 Puanlandırılabilir Evraklar

Restoranın sisteme yüklediği her ek belge görseli (fotoğraf/tarama), puanına katkı sağlar:

| Evrak | Puan | Açıklama |
|-------|------|----------|
| Hijyen Sertifikası (temel) | +25 | Zorunlu, gelirse puan |
| Hijyen Sertifikası (ileri düzey) | +15 | ISO 22000 benzeri |
| TSE Belgesi | +20 | Türk Standartları Enstitüsü |
| Helal Sertifikası | +15 | Helal gıda onayı |
| Organik Gıda Sertifikası | +20 | Organik üretim onayı |
| Vegan/Vejetaryen Sertifikası | +10 | Bitkisel gıda onayı |
| Glutensiz Mutfak Sertifikası | +15 | Çölyak dostu |
| Sürdürülebilirlik Raporu | +10 | Çevre dostu uygulamalar |
| İşletme Sigorta Poliçesi | +20 | İş yeri sigortası |
| Ürün Sorumluluk Sigortası | +25 | Müşteriye karşı sorumluluk |
| Deprem Güvenlik Raporu | +10 | Yapı güvenliği |
| Engelli Erişim Raporu | +10 | Tekerlekli sandalye erişimi |
| İSG (İş Sağlığı Güvenlik) | +15 | İş güvenliği uzmanı raporu |
| Gıda Güvenlik Yönetim Sistemi | +30 | ISO 22000 |
| Çevre Yönetim Sistemi | +10 | ISO 14001 |
| Müşteri Memnuniyet Sertifikası | +10 | Bağımsız kuruluş onayı |

### 4.2 Toplam Evrak Puanı

```
TOPLAM PUAN: 0 - 270 arası
├── 0-50:     Başlangıç seviyesi 🟢
├── 51-100:   Standart restoran 🟡
├── 101-150:  Güvenilir restoran 🟠
├── 151-200:  Premium restoran 🔵
└── 201+:     Elit restoran 🟣
```

### 4.3 Evrak Doğrulama Süreci

Her evrak 3 aşamalı doğrulamadan geçer:

```
AŞAMA 1: OTOMATİK KONTROL (AI)
├── OCR ile evrak okuma
├── Tarih kontrolü (geçerlilik)
├── QR/barkod doğrulama (varsa)
├── Dosya formatı kontrolü (PDF/JPG)
└── Çözünürlük ve okunurluk
    └── Geçti: AŞAMA 2'ye geç
    └── Kaldı: 24 saat içinde yeniden yükleme hakkı

AŞAMA 2: YAPAY ZEKA KARŞILAŞTIRMA
├── Devlet veritabanları ile eşleştirme
├── MERSİS doğrulama
├── SGK doğrulama
├── Belediye ruhsat sorgulama
└── Geçti: AŞAMA 3'e geç
    └── Kaldı: manuel incelemeye yönlendir

AŞAMA 3: MANUEL İNCELEME (İNSAN)
├── Uzman ekip tarafından kontrol
├── Sahte belge tespiti
├── Referans kontrolü
└── Onay: Puan aktif +24 saat içinde
    └── Red: Neden belirtilir, 7 gün sonra tekrar başvuru
```

### 4.4 Evrak Süre Takip

Sistem, her evrağın son kullanma tarihini takip eder:

- **30 gün kala**: SMS/E-posta hatırlatma
- **15 gün kala**: SMS/E-posta + uyarı (puan düşecek)
- **7 gün kala**: Yoğun hatırlatma (günlük)
- **Süre doldu**: Puan düşer, "evrak yenile" statüsü
- **30 gün gecikme**: Restoran profili pasif olur

### 4.5 Kurumsal İçerik Puanı

Restoranın **kurumsal kimlik** içeriklerini doldurması da ek puan kazandırır. Bu içerikler müşteri güvenini artırır ve restoranın ciddiyetini gösterir.

> **Kural: Ne kadar çok puan, o kadar üst sıra.** Puanlar doğrudan sıralamayı belirler. Reklamla sıralama satın alınamaz.

```
KURUMSAL İÇERİKLER:
├── 📖 Hakkımızda (en az 150 kelime)           → +10 puan
│   └── Restoranın hikayesi, ne zaman kurulduğu, hangi değerlerle
│       çalıştığına dair samimi bir yazı
│
├── 📅 Tarihçe (en az 50 kelime + görsel)      → +10 puan
│   └── Kuruluş yılı, dönüm noktaları, büyüme hikayesi
│
├── 🎯 Vizyon (en az 30 kelime)                → +5 puan
│   └── Restoranın gelecek hedefleri, hayali
│
├── 🛡️ Misyon (en az 30 kelime)                → +5 puan
│   └── Restoranın varoluş amacı, müşteriye verdiği söz
│
├── 🏆 Sertifika Galerisi (en az 3 görsel)     → +15 puan
│   └── Hijyen, TSE, Helal vb. sertifika görsellerinin galerisi
│       (4.1'deki evraklardan bağımsız, ayrıca sergilenir)
│
├── 👨‍🍳 Ekip Tanıtımı (şef/aşçı fotoğrafları)   → +10 puan
│   └── Şefin eğitimi, deneyimi, uzmanlık alanı
│
└── 📸 Mutfak Fotoğrafları (en az 5 görsel)    → +10 puan
    └── Üretim alanı, mutfak hijyeni, ekipman
```

TOPLAM KURUMSAL İÇERİK PUANI: 0 - 65 arası

> Kurumsal içerik puanı, evrak puanından (4.1-4.3) **bağımsızdır** ve toplam restoran puanına ayrıca eklenir. Ne kadar çok puan = o kadar üst sıra.

---

## 5. ÜRÜN TAZELİĞİ GARANTİSİ VE ZAMAN DAMGASI

### 5.1 Zaman Damgası Sistemi

Her ürünün üretim ve paketlenme zamanı **saniye hassasiyetiyle** kaydedilir:

```
ÜRÜN ZAMAN ÇİZGİSİ:
├── 🕐 Hazırlanma başlangıcı: 14:32:17
├── 🕐 Pişirme/Uretim tamam: 14:47:03
├── 🕐 Paketleme: 14:49:11
├── 🕐 Kuryeye teslim: 14:50:45
├── 🕐 Müşteriye teslim: 15:02:23
└── ⏱️ TOPLAM SÜRE: 30 dk 6 sn
```

### 5.2 Tazelik Sınıflandırması

```
TAZELİK DERECELERİ:
├── 🥇 PREMIUM (0-15 dk) — Taze üretim, sıcak
├── 🥈 STANDART (15-30 dk) — Normal tazelik
├── 🥉 GEÇ (30-45 dk) — Soğumuş olabilir
└── ❌ GECİKMİŞ (45+ dk) — Tazelik garantisi kapsamı dışı
```

### 5.3 Tazelik Garantisi Şartları

Restoranlar tazelik garantisi için aşağıdaki şartları kabul eder:

- Müşteriye teslim süresi **45 dakikayı geçerse** ücretsiz
- 30-45 dk arası: %50 indirim kuponu (bir sonraki siparişte)
- Şikayet durumunda zaman damgası delil olarak kullanılır
- Sahte zaman damgası: restoran kalıcı olarak banlanır

### 5.4 Üretim Takvimi ve Stok Yönetimi

Her ürün için ayrı ayrı üretim zamanı girilir:

```
MENÜ ÜRÜN TAZELİK:
├── Lahmacun: 8 dk üretim, 5 dk tazelik ömrü
├── Pizza: 15 dk üretim, 10 dk tazelik ömrü
├── Çorba: 20 dk üretim, 30 dk tazelik ömrü (termos)
├── Salata: 5 dk hazırlık, 10 dk tazelik ömrü
└── İçecek: 1 dk hazırlık, 60 dk tazelik (soğuk)
```

Sistem, her ürün için **stoktan düşme takibi** yapar. Ürün tazelik ömrünü doldurduysa otomatik olarak **menüden gizlenir** ve restorana uyarı gönderilir.

### 5.5 Isı Takibi (Opsiyonel)

Akıllı termal çanta kullanan kuryeler için:

```
ISIL TAKİP:
├── Sıcak ürün: >60°C (ideal)
├── Sıcak koruma: >50°C (kabul edilebilir)
├── Soğuk ürün: <8°C (ideal)
├── Soğuk koruma: <12°C (kabul edilebilir)
└── Limit aşımı: Müşteriye anlık bildirim
```

---

### 5.6 Ürün Görsel ve Açıklama Standartları

#### 5.6.1 Gerçek Ürün Fotoğrafı Zorunluluğu

Sistemdeki her ürünün fotoğrafı **restoran tarafından çekilmiş gerçek fotoğraf** olmak zorundadır. Stok fotoğraf, internetten alıntı veya başka restorandan kopya **kesinlikle yasaktır**.

```
FOTOĞRAF KURALLARI:
├── 📸 GERÇEK ÜRÜN FOTOĞRAFI ZORUNLU
│   ├── Restoran kendi ürününü fotoğraflamalı
│   ├── Stok fotoğraf / internet görseli yasak
│   ├── Başka restoranın fotoğrafını kullanmak yasak
│   └── Filter / aşırı düzenleme yasak (sadece ışık ayarı serbest)
│
├── 📏 ÇÖZÜNÜRLÜK VE BOYUT
│   ├── Minimum: 1080×1080 px (kare)
│   ├── Maksimum: 12 MP (sistem kasmamalı)
│   ├── Format: JPEG veya WebP (PNG gereksiz büyük)
│   ├── Dosya boyutu: Maksimum 2 MB (sıkıştırma yapılır)
│   └── Otomatik sıkıştırma: Sistem yüklerken WebP'ye çevirir
│
├── 🎯 AÇI VE SUNUM
│   ├── Ürün net görünmeli, tabağın en az %70'i kadrolı
│   ├── Yan ürünler (yanında ne var?) varsa belirtilmeli
│   ├── Masa/zemin temiz olmalı
│   └── İçeceklerde: Bardak etiketi / şişe görünmeli
│
├── 🚫 YASAK OLANLAR
│   ├── Stok fotoğraf (Google/img görseli)
│   ├── Rakip restoran fotoğrafı
│   ├── Aşırı filter / photoshop / renk oynama
│   ├── Başka ürünün fotoğrafını koymak
│   └── Ürünü olduğundan büyük göstermek (açı ile oynama)
│
└── ✅ İZİN VERİLEN DÜZENLEMELER
    ├── Işık ayarı (karanlık fotoğraflar için)
    ├── Kırpma (sadece ürünü ortalamak için)
    ├── Renk sıcaklığı (çok sarıysa düzeltme)
    └── Arka plan (düz arka plana alınabilir, ürün aynı kalmalı)
```

#### 5.6.2 Yanıltıcı Fotoğraf Cezaları

| İhlal | Tespit | Ceza |
|-------|--------|------|
| Stok fotoğraf kullanımı | AI tespit + manuel kontrol | Ürün pasif + -2.0 puan |
| Başka restorandan kopya | AI karşılaştırma | Hesap pasif + -5.0 puan |
| Aşırı filter/düzenleme | AI analiz | Uyarı + fotoğraf silinir |
| Ürünle alakasız fotoğraf | Müşteri şikayeti | Ürün pasif + -1.5 puan |
| Gerçek dışı porsiyon | Müşteri şikayeti + kanıt | -2.0 puan + fotoğraf yenileme |
| 3+ ihlal | Tekrarlayan | Restoran geçici ban (7 gün) |

#### 5.6.3 Ürün Açıklama Standartları

Açıklama ne çok kısa ne çok uzun olmalı. Sistem performansı ve kullanıcı deneyimi dengelenir:

```
AÇIKLAMA KURALLARI:
├── 📝 UZUNLUK
│   ├── Minimum: 30 karakter (tek satır)
│   ├── Maksimum: 300 karakter (sistemi kasmamalı)
│   ├── İdeal: 80-150 karakter
│   └── Türkçe karakter desteği zorunlu
│
├── 📋 İÇERİK
│   ├── Ana malzemeler (en önemli 3-5 malzeme)
│   ├── Porsiyon büyüklüğü (kaç kişilik?)
│   ├── Varsa alerjen uyarısı (gluten, süt, yumurta, fıstık...)
│   └── Hazırlama süresi (opsiyonel, menüde varsa)
│
├── 🚫 YASAK İFADELER
│   ├── "En iyi", "bir numara", "harika" gibi abartılı ifadeler
│   ├── Rakip restoran adı geçemez
│   ├── İletişim bilgisi (tel, adres) yazılamaz
│   └── Reklam amaçlı yönlendirme yapılamaz
│
└── ✅ İYİ AÇIKLAMA ÖRNEKLERİ
    ├── ✅ "Fırında kaşarlı pide, kıymalı ve kuşbaşılı, 2 kişilik"
    ├── ✅ "Mevsim yeşillikleri, nar ekşisi, ceviz, 300gr"
    ├── ✅ "Soğuk içecek, 330ml cam şişe, kafeinsiz"
    └── ❌ "Süper lezzetli harika pide, herkes çok seviyor, kesin dene"
```

#### 5.6.4 Müşteri Ne Görüyorsa Onu Yer (Garanti)

```
GÖRÜNEN = GERÇEK GARANTİSİ:
├── Photoğraftaki ürün ile gelen ürün aynı olmalı
├── Porsiyon fotoğraftaki ile tutarlı olmalı
├── Malzemeler fotoğrafta görünenle aynı olmalı
│   └── Örn: Fotoğrafta kaşar peyniri varsa, kaşar peyniri gelmeli
│       (işlenmiş peynir değil)
├── Şikayet durumunda:
│   ├── Müşteri fotoğraf çeker (gelen ürün)
│   ├── Sistem fotoğrafı karşılaştırır (AI)
│   ├── Uyuşmazlık tespit edilirse:
│   │   ├── 1. ihlal: İade + %50 kupon
│   │   ├── 2. ihlal: İade + ücretsiz yemek
│   │   └── 3. ihlal: Restoran pasif + inceleme
│   └── Haksız şikayet (müşteri yalan söylüyorsa):
│       └── Müşteri ceza puanı + uyarı
|
└── Restoran fotoğrafı her 90 günde bir yenilemek zorunda
    (ürün değişmediyse aynı fotoğraf kalabilir, sistem onayı ile)
```

#### 5.6.5 Üreticiyi Kendi Fotoğrafını Çekmeye Teşvik Sistemi

Yasaklamak yetmez, üreticiyi **özendirmek** ve **kolaylaştırmak** gerekir.

```
TEŞVİK MEKANİZMALARI:

A) UYGULAMA İÇİ FOTOĞRAF ÇEKİM ASİSTANI
├── Kullanıcı "Fotoğraf Çek" butonuna basar
├── Uygulama kamerayı açar, üst üste çerçeve gösterir
│   ├── "Tabağı şu çerçeveye yerleştirin" (kılavuz)
│   ├── "Işık yeterli mi?" (otomatik parlaklık kontrolü)
│   ├── "Net mi?" (otomatik odak kontrolü)
│   └── "Çekimi yapın" (tek dokunuş)
├── Çekilen fotoğraf otomatik sıkıştırılır (WebP, max 2MB)
└── "Başarıyla yüklendi ✓" onayı

B) PUAN VE SIRALAMA AVANTAJI
├── Gerçek fotoğraf (AI doğrulamalı): +5 puan
├── Yüksek kalite fotoğraf (net, aydınlık): +3 puan
├── Fotoğrafta ürün + yan ürünler görünüyor: +2 puan
├── Her ürün için ayrı fotoğraf: +1 puan/ürün
└── Sıralamada gerçek fotoğraflı ürünler önce gösterilir

C) ÖRNEK FOTOĞRAFLAR VE REHBER
├── "Nasıl çekilmeli?" sayfası (örnek iyi/kötü fotoğraflar)
├── İyi örnek: "Net, aydınlık, tabak ortalanmış, masa temiz"
├── Kötü örnek: "Bulanık, karanlık, tabak kaymış, masa dağınık"
├── Video: "Cep telefonunuzla 30 saniyede profesyonel yemek fotoğrafı"
└── Haftalık ipucu: "Işık nereden gelmeli?", "Arka plan nasıl olmalı?"

D) ÖDÜL SİSTEMİ
├── Ayın en iyi fotoğrafları: Ana sayfada sergileme (+10 puan)
├── 30 gün boyunca her ürün güncel fotoğraflı: "Güvenilir" rozeti
├── 90 gün boyunca hiç stok fotoğraf kullanmamış: "Gerçek" rozeti
├── En çok fotoğraf yükleyen üretici: Premium destek (öncelikli müşteri hizmeti)
└── Yıllık "En İyi Görsel" yarışması: Platformda öne çıkarma

E) MİMARİ ENTEGRASYON
├── Fotoğraf çekim asistanı doğrudan menü yönetimi sayfasında
├── Ürün eklerken "Fotoğraf Çek" butonu (galeri değil, direkt kamera)
├── Galeriden yükleme de mümkün ama "kamera ile çek" öncelikli
├── Çekilen fotoğraf otomatik olarak doğru boyuta kırpılır
└── Saniyeler içinde yayına alınır (onay beklemez)
```

**Neden teşvik?** Stok fotoğraf yasaklayıp denetlemek yerine, üreticiye "kendi fotoğrafını çekmesi için" araç + puan + ödül verirsek:
- Denetim maliyeti düşer
- Üretici memnun olur (kontrol onda)
- Müşteri güveni artar
- Platformda her ürün gerçek görünür

#### 5.6.6 Mükemmel Üretici Rozet Sistemi

Tüm şartları **eksiksiz** yerine getiren üreticilere özel rozetler verilir. Rozetler hem puan kazandırır hem de müşteri gözünde güven işaretidir.

```
ROZET SİSTEMİ:

┌─────────────────────────────────────────────────────────────┐
│                     🏆 ROZETLER                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🟢 GERÇEK FOTOĞRAF ROZETİ                                 │
│  Koşul: Tüm ürünler gerçek fotoğraflı, stok fotoğraf yok   │
│  ├── Tüm ürünler için ayrı ayrı çekilmiş gerçek fotoğraf  │
│  ├── AI doğrulamasından geçmiş                             │
│  ├── Hiç stok/kopya fotoğraf tespit edilmemiş             │
│  └── +10 puan                                              │
│                                                             │
│  🔵 YÜKSEK KALİTE ROZETİ                                   │
│  Koşul: Tüm fotoğraflar net, aydınlık, düzgün kadrajlı    │
│  ├── AI kalite puanı >80/100                              │
│  ├── Bulanık/karanlık/kaymış fotoğraf yok                │
│  └── +5 puan                                              │
│                                                             │
│  🟣 GÖRSEL TAMAMLIK ROZETİ                                 │
│  Koşul: 6+ zorunlu görsel + her ürün fotoğraflı           │
│  ├── Restoran görselleri (6 kategori) tam                 │
│  ├── Menüdeki her ürünün fotoğrafı var                   │
│  ├── Eksik görsel sayısı: 0                               │
│  └── +15 puan                                             │
│                                                             │
│  🟡 AÇIKLAMA ROZETİ                                        │
│  Koşul: Tüm ürün açıklamaları eksiksiz ve kurallara uygun │
│  ├── Her ürün için 30-300 karakter açıklama              │
│  ├── Malzemeler, porsiyon, alerjen bilgisi tam           │
│  ├── Yasak ifade (abartı/reklam) yok                     │
│  └── +5 puan                                              │
│                                                             │
│  🔴 GÜNCEL ROZET                                           │
│  Koşul: Tüm görseller son 90 gün içinde yenilenmiş        │
│  ├── Hiç eski görsel yok                                  │
│  ├── Menü güncel (fiyat/ürün değişikliği yansıtılmış)    │
│  └── +5 puan                                              │
│                                                             │
│  ⭐ MÜKEMMEL ÜRETİCİ ROZETİ (TÜMÜNÜ ALANA)                │
│  Koşul: Yukarıdaki 5 rozetin hepsine sahip olmak          │
│  ├── Gerçek Fotoğraf ✓                                    │
│  ├── Yüksek Kalite ✓                                      │
│  ├── Görsel Tamamlık ✓                                    │
│  ├── Açıklama ✓                                          │
│  └── Güncel ✓                                            │
│                                                             │
│  MÜKEMMEL ÜRETİCİ AVANTAJLARI:                              │
│  ├── Toplam +40 puan (10+5+15+5+5)                        │
│  ├── Ana sayfada "⭐ Mükemmel" etiketi                     │
│  ├── Aramalarda üst sıra (puan bazlı sıralamada öncelik)  │
│  ├── "Mükemmel Üretici" filtresinde görünür              │
│  ├── Müşteriye özel "Bu restoran mükemmel" bildirimi      │
│  └── Premium destek hattına erişim                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Rozetler ne işe yarar?**
- Müşteri: "Bu restoranda her şey eksiksiz" diye bilir, güvenle sipariş verir
- Üretici: Rozet aldıkça puanı artar, üst sıralarda görünür, daha çok sipariş alır
- Platform: Her ürün gerçek fotoğraflı ve düzgün açıklamalı olduğu için güven artar

**Rozet kaybetme:**
- Kural ihlali tespit edilince rozet otomatik düşer
- 7 gün içinde düzeltme hakkı
- 3. ihlalde rozet kalıcı gider, 30 gün boyunca tekrar alınamaz

---

## 6. ÇİFT YÖNLÜ PUANLAMA SİSTEMİ

### 🧱 TEMEL KURAL: Her İşlem = 1 Yorum Hakkı

Bu sistemin **kemik kuralıdır**, değişmez:

```
📜 KURAL 1: İŞLEM = YORUM HAKKI

> ⚠️ **TÜM PLATFORM İÇİN ORTAK KURAL:** Bu bölümdeki kurallar (1 işlem = 1 yorum hakkı, 3 seçenekli oylama, yorum silinemez, anti-troll) **taksi, yemek ve diğer tüm platform servisleri için geçerlidir.** Ayrıca **adres ve konum bilgisi** her kullanıcı için zorunludur; adressiz/konumsuz hesap ile işlem yapılamaz. Taksi sistemindeki karşılığı için [TAXI-SYSTEM-DESIGN.md → Bölüm 7.0](../architecture/TAXI-SYSTEM-DESIGN.md#7-çift-yönlü-puanlama-sistemi) bölümüne bakın.

Her işlem (sipariş, teslimat, yerinde ödeme) için sadece 1 (bir) yorum + puan hakkı vardır.

├── ✅ Müşteri platformdan ödeme yaptıysa → 1 yorum + 1 puan hakkı DOĞAR
├── ❌ Müşteri platform dışı ödediyse (nakit/kendi POS) → Yorum + puan hakkı DOĞMAZ
├── ✅ Yorum yazıldıktan sonra KALICI olarak durur
├── ❌ Aynı işlem için yorum/puan DEĞİŞTİRİLEMEZ
├── ✅ Bir sonraki ödemeye kadar yeni yorum hakkı AÇILMAZ
└── ✅ İptal edilen işlemde yorum hakkı İPTAL olur

📜 KURAL 2: YORUM SİLİNEMEZ

├── 🏪 Restoran, olumlu veya olumsuz hiçbir yorumu SİLEMEZ
├── Müşteri de yorumu SİLEMEZ (kalıcı kayıt)
├── ⚠️ İstisna: Platform kurallarını ihlal eden yorumlar (küfür, hakaret, ticari reklam)
│   └── Sadece PLATFORM yetkilisi silebilir
└── Restoran yoruma CEVAP YAZABİLİR (1 kere, silinemez)

📜 KURAL 3: YORUM + PUAN BİRLİKTE

├── Yorum varsa puan da olmak zorunda DEĞİL (sadece yorum yazılabilir)
├── Puan varsa yorum zorunlu DEĞİL (sadece puan verilebilir)
├── İkisi de aynı işleme bağlı, ayrı ayrı kullanılamaz
│   └── Yani 1 işlem = ya yorum ya puan ya ikisi = 1 hakkın içinde
└── 2. işlem yapılmadan 2. yorum/puan hakkı doğmaz
```

**Neden bu kural?**
- Müşteri yorum yapmak/puan vermek istiyorsa → platformdan ödemek zorunda
- Restoran yorum/puan almak istiyorsa → müşteriyi platformdan ödemeye teşvik eder
- Sahte/çoklu/çakma yorumlar tamamen önlenir
- Restoran kötü yorumu silemez → müşteri güveni tam
- Her yorum gerçek bir ödemeye dayanır → güvenilirlik
- Yorum silinemez olduğu için müşteri de düşünerek yazar

### 📜 KURAL 4: Olumsuz Oy Takip Sistemi (Anti-Troll)

```
SİSTEM HER KULLANICININ OY GEÇMİŞİNİ TUTAR:

3 OY SEÇENEĞİ:
├── 🟢 BEĞENDİM (olumlu) → sıralamada +1 YUKARI
├── ⚪ BEĞENMEDİM (pas geç) → sıralamaya etki YOK
└── 🔴 KÖTÜ BEĞENİ (olumsuz) → sıralamada -1 AŞAĞI

Her işlemde 1 oy hakkı: Yukarı kullan, aşağı kullan, veya pas geç.

TROLL TESPİT ALGORİTMASI:
├── Bir kullanıcının oylarının %90+ KÖTÜ BEĞENİ ise → TROLL
│   ├── Normal kullanıcı: %40-50 olumlu, %30-40 pas, %10-20 olumsuz
│   ├── Troll: %90+ olumsuz (sürekli aşağı oylar, hiç yukarı oy yok)
│   └── Rakip/art niyetli: Sadece rakipleri aşağı oylar
│
├── Tespit edilince:
│   ├── Kullanıcının TÜM oyları GEÇERSİZ sayılır
│   ├── Geçersiz oylar geri alınır (puan/sıra düzeltilir)
│   ├── Kullanıcı uyarılır (1. ihlal)
│   ├── Tekrar ederse → oy hakkı askıya alınır (2. ihlal)
│   └── Kalıcı troll → hesap kısıtlanır (sadece yemek yiyebilir, oy kullanamaz)
│
└── İTİRAZ HAKKI:
    ├── Kullanıcı "ben gerçekten beğenmedim" derse
    ├── Sistem son 10 oyunu inceler
    ├── Gerçekten hep kötü mü yoksa sadece bir restorana mı?
    │   └── Tek restorana sürekli olumsuz → rakip trollü
    │   └── Herkese olumsuz → kişisel zevk (yine de anormal)
    └── İtiraz kabul edilmezse oylar kalıcı geçersiz

ÖRNEK:
├── Normal müşteri: 20 işlem
│   ├── 10 beğendim (%50)
│   ├── 6 pas geçtim (%30)
│   └── 4 kötü beğeni (%20)
│   → ✅ NORMAL
│
├── Troll: 20 işlem
│   ├── 0 beğendim (%0)
│   ├── 1 pas geçtim (%5)
│   └── 19 kötü beğeni (%95)
│   → ❌ TESPİT EDİLDİ → 19 oy geçersiz
│
└── Rakip restoran: 30 işlem, hep A rakibine kötü beğeni
    → ❌ TESPİT EDİLDİ → 30 oy geçersiz, rakip ceza aldı
```

**Kural özeti:** Herkes oyunu istediği gibi kullanır ama sistematik olarak sadece olumsuz oy veren tespit edilir ve tüm oyları iptal edilir. Adil sıralama korunur.

### 6.1 Puanlama Üçgeni

Her sipariş sonrası **3 taraf** birbirini puanlar:

```
     MÜŞTERİ
     ╱       ╲
    ╱         ╲
RESTORAN ──── KURYE
```

| Gönderen | Alan | Puan Kriterleri |
|----------|------|----------------|
| Müşteri | Restoran | Lezzet, porsiyon, sunum, hijyen, süre |
| Müşteri | Kurye | Hız, nezaket, paket durumu, iletişim |
| Restoran | Müşteri | İletişim, adres doğruluğu, teslim alma hızı |
| Restoran | Kurye | Bekleme süresi, paket taşıma kalitesi |
| Kurye | Restoran | Hazırlık süresi, paketleme kalitesi |
| Kurye | Müşteri | Adres bulma kolaylığı, bekleme süresi |

### 6.2 Puanlama Aralığı ve Ağırlıklar

```
PUAN ARALIĞI: 1.0 - 5.0 (0.1 hassasiyet)

AĞIRLIKLI ORTALAMA HESABI:
├── Müşteri → Restoran: %50
├── Kurye → Restoran: %20
├── Evrak bazlı puan: %20
├── Canlı kamera: %10
└── TOPLAM: %100
```

### 6.3 Puan Kuralları

- **Müşteri** puansız bırakırsa: 24 saat sonra varsayılan 4.0
- **Restoran** puansız bırakırsa: 48 saat sonra varsayılan 4.0
- **Kurye** puansız bırakırsa: 12 saat sonra varsayılan 4.0
- **Varsayılan puanlama devre dışı** bırakılabilir (ayarlar)
- Oy kullanmayan tarafın bir sonraki puanı %10 daha ağırlıklı

### 6.4 Sıralama (Reklam Satın Alınamaz)

```
SIRALAMA FORMÜLÜ:
├── Puan tabanlı (4.5+ → üst sıra)
├── Teslimat süresi (hızlı → üst sıra)
├── Görsel kalitesi (yüksek çöz. → öne çıkarma)
├── Canlı kamera (+100 puan avantaj)
├── Aktif sipariş sayısı (popülerlik)
└── REKLAMLA SIRALAMA SATILMAZ
```

Sıralamada reklam satın alınamaz. Restoranlar sadece hizmet kalitesiyle öne çıkar.

### 6.5 Puan Kırıcılar ve Cezalar

| İhlal | Puan Etkisi | Süre |
|-------|-----------|------|
| Eksik ürün gönderme | -1.0 | 30 sipariş |
| Geç teslimat (%50 üzeri) | -0.5 | 20 sipariş |
| Kötü paketleme (dökülme) | -0.7 | 25 sipariş |
| Müşteriye kötü davranış | -2.0 | 50 sipariş |
| Sahte zaman damgası | -5.0 (kalıcı ban) | Süresiz |
| Hijyen şikayeti (kanıtlı) | -3.0 | 100 sipariş |
| Kurye mobing | -1.5 | 40 sipariş |
| Menüde olmayan ürün gönderme | -0.8 | 20 sipariş |

---

## 7. %2 KOMİSYON MODELİ

### 7.1 Komisyon Oranları

| Kalem | Oran | Açıklama |
|-------|------|----------|
| Restoran komisyonu | **%2** | Sipariş başına (rakip %25-30) |
| Kurye hizmet bedeli | %5 | Kuryeye ödenen ücretten kesinti |
| Müşteri hizmet bedeli | 0 ₺ | Ücretsiz |
| Premium liste üyeliği | 0 ₺ | Puana göre otomatik |
| Reklam | Satılmaz | Sadece puan bazlı sıralama |

### 7.2 %2 Komisyonun Sürdürülebilirliği

```
GELİR MODELİ:
├── %2 restoran komisyonu (ana gelir)
├── %5 kurye hizmet bedeli (ikincil gelir)
├── Restoran görsel hizmeti (fotoğrafçı gönderme)
├── Termal çanta kiralama (opsiyonel)
├── POS cihazı kiralama (opsiyonel)
├── Canlı kamera sistemi kurulum (opsiyonel)
└── Premium araç gereç satışı (iştirak geliri)
```

### 7.3 Komisyon Hesaplama Detayı

```
ÖRNEK HESAP:
Sipariş: 150 ₺
├── Restoran komisyonu: 150 × %2 = 3 ₺
├── Kurye ücreti: 25 ₺ (müşteriden)
├── Kurye hizmet bedeli: 25 × %5 = 1.25 ₺
├── Platform geliri: 3 + 1.25 = 4.25 ₺
└── Müşteri öder: 150 + 25 (kurye) = 175 ₺
```

### 7.4 Restoran Gelir Avantajı

```
RAKİP KARŞILAŞTIRMASI:
├── Yemeksepeti: %28 komisyon
│   └── 150 ₺ siparişte restorana kalan: 108 ₺
│
├── Trendyol Yemek: %25 komisyon
│   └── 150 ₺ siparişte restorana kalan: 112.50 ₺
│
├── Getir Yemek: %30 komisyon
│   └── 150 ₺ siparişte restorana kalan: 105 ₺
│
└── BİZİM SİSTEM: %2 komisyon
    └── 150 ₺ siparişte restorana kalan: 147 ₺
    └── **Restoran 35-42 ₺ daha fazla kazanır**
```

---

## 8. DİNAMİK TESLİMAT SÜRESİ HESAPLAMA

### 8.1 Süre Bileşenleri

```
TOPLAM TESLİMAT SÜRESİ = Hazırlık + Trafik + Meteoroloji + Mesafe

├── HAZIRLIK SÜRESİ
│   ├── Restoranın geçmiş ortalama hazırlık süresi
│   ├── Ürün bazında baz süre (menüde tanımlı)
│   ├── Anlık yoğunluk faktörü (bekleyen sipariş sayısı)
│   └── Dinamik: Her siparişte güncellenir
│
├── TRAFİK SÜRESİ
│   ├── Google Traffic API (canlı trafik verisi)
│   ├── Tarihsel trafik verisi (saat/gün bazlı)
│   ├── Tatil/hafta sonu modelleri
│   └── Anlık kaza/etkinlik verisi
│
├── METEOROLOJİ SÜRESİ
│   ├── Meteoroloji API (yağmur/kar/fırtına)
│   ├── Yağış şiddeti katsayısı (mm/saat)
│   ├── Görüş mesafesi (sis/pus)
│   ├── Rüzgar hızı (fırtına durumları)
│   ├── Sıcaklık (buzlanma riski)
│   └── Toplam meteoroloji +%0-40 arası ekleme
│
└── MESAFE SÜRESİ
    ├── Restoran - Müşteri kuş uçuşu mesafe
    ├── Motor için optimize edilmiş rota
    ├── Yokuş/merdiven gibi zorlayıcı faktörler
    └── Bina içi süre (asansör beklenmesi, kat bilgisi)
```

### 8.2 Meteoroloji Katsayıları

| Hava Durumu | Katsayı | Süre Etkisi |
|------------|---------|-------------|
| Açık güneşli | 1.0x | Baz süre |
| Hafif bulutlu | 1.05x | +%5 |
| Kapalı bulutlu | 1.10x | +%10 |
| Hafif yağmur | 1.15x | +%15 |
| Orta şiddetli yağmur | 1.25x | +%25 |
| Şiddetli yağmur/sağanak | 1.40x | +%40 |
| Kar yağışı (hafif) | 1.20x | +%20 |
| Kar yağışı (yoğun) | 1.50x | +%50 |
| Sis (hafif) | 1.15x | +%15 |
| Sis (yoğun) | 1.30x | +%30 |
| Fırtına (rüzgar) | 1.25x | +%25 |
| Dolu | 1.40x | +%40 |
| Rüzgarsız/normal | 1.0x | Baz süre |

### 8.3 Trafik Katsayıları

| Trafik Durumu | Katsayı | Süre Etkisi |
|--------------|---------|-------------|
| Trafiksiz (gece/çok erken) | 0.85x | -%15 |
| Normal akıcı | 1.0x | Baz süre |
| Hafif yoğun | 1.15x | +%15 |
| Orta yoğun | 1.30x | +%30 |
| Yoğun | 1.50x | +%50 |
| Çok yoğun | 1.75x | +%75 |
| Kilitlenme (kaza/etkinlik) | 2.0x | +%100 |

### 8.4 Gerçekçi Süre Zorunluluğu (Mobing Önleme)

Sistem gerçekçi süre hesaplamak zorundadır. Kurye mobingini önlemek için:

```
MOBİNG ÖNLEME KURALLARI:
├── Hesaplanan süre MINIMUM olarak kabul edilir
├── Kurye hesaplanan süreden DAHA KISA sürede teslim edebilir
├── Ancak hesaplanan süreden FAZLA sürerse mazeret gerekir
├── Gerçekçi olmayan süre (çok kısa) → müşteri şikayet eder
├── Gerçekçi olmayan süre (çok uzun) → müşteri vazgeçer
└── Sistem her teslimat sonrası kendi süresini gerçek süreyle karşılaştırır
    └── Hata >%20 ise algoritma güncellenir
```

### 8.5 Süre Tahmin Gösterimi

Müşteriye gösterilen süre, detaylı döküm ile sunulur:

```
🕐 TAHMİNİ TESLİMAT: 28 DAKİKA
├── Hazırlık:      12 dk
├── Trafik:         8 dk (normal akıcı)
├── Mesafe:         5 dk (1.2 km)
├── Hava:           3 dk (hafif yağmur +%15)
└── TOPLAM:        28 dk
```

---

## 9. PLATFORM KURYE HAVUZU VE ATAMA MODELLERİ

> ⚠️ **GÜNCELLEME:** Bu bölüm, platformun bağımsız kurye sistemi ile değiştirilmiştir. Kuryeler artık tüm servislerden (yemek, çiçek, market) tek bir havuzda teslimat alır.
>
> 📖 **Detaylı kurye sistemi:** [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md) — bağımsız, tüm servislere hizmet veren ortak kurye havuzu.

Aşağıdaki içerik, yemek sistemine özel kurye kurallarını tanımlar. Kurye atama, durum yönetimi, mola ve ücretlendirme için [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md)'e bakınız.

### 9.1 Sipariş Anında Kurye Sorgulama ve Süre Bildirimi

Müşteri siparişi **vermeden önce** sistem kurye durumunu sorgular ve gerçekçi teslimat süresini gösterir:

```
SİPARİŞ ÖNCESİ SÜRE HESAPLAMA (CHECKOUT ANI):

MÜŞTERİ: Sepet onayla butonuna tıklar
         │
         ▼
SİSTEM: ANLIK KURYE TARAMASI BAŞLATIR
         │
         ├── Bölgedeki tüm kuryeler taranır
         │   ├── Müsait kuryeler (şu an boşta)
         │   ├── Siparişteki kuryeler (ne zaman boşalır?)
         │   ├── Dönüşteki kuryeler (restorana yaklaşıyor mu?)
         │   └── Çevrimdışı kuryeler (sayılmaz)
         │
         ├── Her kuryenin anlık konumu alınır
         │   ├── Kurye A: Restorana 1.2 km, 3 dk
         │   ├── Kurye B: Restorana 3.5 km, 8 dk (dönüşte)
         │   ├── Kurye C: Restorana 0.8 km, 2 dk (müsait)
         │   └── Kurye D: Başka teslimatta, 12 dk sonra boşalır
         │
         ├── En uygun kurye seçilir
         │   ├── Kurye C: 2 dk içinde restoranda
         │   ├── Restoran hazırlık: 15 dk
         │   ├── Teslimat süresi: 8 dk (trafik + hava)
         │   └── TOPLAM: 2 + 15 + 8 = 25 dk
         │
         └── Müşteriye gösterilir:
             ├── "🕐 Tahmini teslimat: 25 dakika"
             ├── "📍 Kurye hazır, en yakın kurye 2 dk uzakta"
             └── "✅ Sipariş ver" butonu aktif
```

#### 9.1.1 Kurye Bulunamazsa (Edge Case)

```
KURYE BULUNAMADI:
├── Bölgede hiç müsait kurye yok
├── Siparişteki kuryeler de uzak (>15 dk)
├── Sistem müşteriye bildirir:
│   ├── "⚠️ Şu an bölgenizde müsait kurye bulunamadı"
│   ├── "🕐 Tahmini bekleme: 30+ dakika"
│   └── Seçenekler:
│       ├── "Yine de sipariş ver" (sipariş alınır, bekleme listesine eklenir)
│       ├── "Planlı sipariş" (istediğin saatte gelsin)
│       └── "Vazgeç" (sipariş oluşturulmaz)
└── Sistem alternatif restoran önerebilir:
    └── "Yakındaki X restoranından sipariş verebilirsiniz (15 dk)"
```

#### 9.1.2 Sürekli Konum Takip Zorunluluğu

Kuryeler çevrimiçi olduğu sürece **sürekli konum paylaşmak** zorundadır:

```
KONUM PAYLAŞIM KURALLARI:
├── Kurye çevrimiçi → konum her 10 saniyede bir güncellenir
├── Kurye siparişte → konum her 5 saniyede bir güncellenir
├── Kurye molada → konum her 30 saniyede bir güncellenir
├── Konum paylaşımı kapalıysa → kurye "çevrimdışı" sayılır
├── Konum sapması >100m → sistem uyarı verir
├── GPS kapalı/bozuk → kurye sipariş alamaz
└── Kurye evde/kafede/beklerken → konumu hala sistemde görünür
```

#### 9.1.3 Zaman Uyumsuzluğu Yönetimi (Kurye Meşgul)

Sistemin en kritik karar anı: **yemek hazır, kurye yolda ama zamanlar uyuşmuyor.**

```
SENARYO: MÜŞTERİ SİPARİŞ VERDİ
├── Restoran hazırlık: 5 dk
├── En yakın kurye: Başka teslimatta, 10 dk sonra müsait
├── Kurye restorana varış: Müsait olduktan sonra +5 dk = 15 dk
└── UYUMSUZLUK: Yemek 5 dk'da hazır, kurye 15 dk'da gelir → 10 dk bekleme

SİSTEM KARARI:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ADIM 1: TÜM SEÇENEKLERİ TARA                                  │
│                                                                  │
│  A) BU KURYE BEKLENSİN?                                         │
│     ├── Kurye 15 dk'da gelir                                    │
│     ├── Yemek 10 dk bekler (+soğuma riski)                      │
│     └── TOPLAM TESLİMAT: 5 (hazırlık) + 10 (bekleme) + 5 (yol) │
│         = 20 dk                                                 │
│                                                                  │
│  B) BAŞKA KURYE VAR MI?                                         │
│     ├── Kurye X: 8 dk uzakta, müsait                            │
│     │   → 5 dk hazırlık + 8 dk yol = 13 dk (bekleme yok)       │
│     │   → TOPLAM: 5 + 8 = 13 dk ← DAHA İYİ                      │
│     ├── Kurye Y: 12 dk uzakta, başka teslimattan dönüyor        │
│     │   → 5 dk hazırlık + 12 dk yol = 17 dk                    │
│     └── Kurye Z: 3 dk uzakta ama molada (10 dk kaldı)           │
│         → 5 + (10+3) = 18 dk                                    │
│                                                                  │
│  C) HAZIRLIK GECİKTİRİLEBİLİR Mİ?                                │
│     ├── Restorana bildirim: "Kurye 15 dk'da gelir,              │
│     │   hazırlığı 12. dakikada bitirin"                         │
│     ├── Yemek taze kalır (+beklemez, +soğumaz)                  │
│     └── TOPLAM: 15 (kurye bekleme) + 0 (yemek beklemez) = 15 dk │
│                                                                  │
│  ADIM 2: EN İYİ SEÇENEĞİ BELİRLE                                │
│                                                                  │
│  Seçenek B (Kurye X): 13 dk ← EN HIZLI                          │
│  Seçenek C (Gecikmeli hazırlık): 15 dk                          │
│  Seçenek A (Bekle): 20 dk ← EN YAVAŞ                            │
│                                                                  │
│  ➡ SİSTEM: Kurye X'i atar, müşteriye "13 dk" gösterir          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Kural**: Sistem her zaman **en kısa teslimat süresini** hedefleyen kuryeyi seçer. Bekleme süresi minimize edilir.

| Durum | Karar | Müşteriye Gösterilen Süre |
|-------|-------|--------------------------|
| Kurye müsait ve yakın | Doğrudan ata | Hazırlık + yol süresi |
| Kurye meşgul, başkası var | Alternatif kurye ata | Alternatif kurye süresi |
| Kurye meşgul, başkası yok, geciktirilebilir | Hazırlığı geciktir | Kurye varış süresi |
| Kurye meşgul, alternatif yok, geciktirilemez | Yemek bekle + kuryeyi bekle | Toplam süre (en kötü) |
| Hiç kurye yok | Sipariş alınmaz, müşteri bilgilendirilir | - |

#### 9.1.4 Çok Kuryeli Restoranda Bireysel Kurye Takibi

Restoranın 15 kuryesi var ama hepsi aynı anda müsait değil. Sistem her kuryeyi **bireysel** takip eder:

```
SENARYO: 15 KURYESİ OLAN BÜYÜK RESTORAN

ANLIK KURYE DURUMU:
┌──────────┬────────────────┬────────────────┬──────────────┐
│ Kurye #  │ Durum          │ Konum          │ Müsait       │
├──────────┼────────────────┼────────────────┼──────────────┤
│ K1       │ Restoranda     │ Restoran       │ ✅ HEMEN     │
│ K2       │ Teslimat-1'de  │ Müşteri A (2km)│ 8 dk sonra   │
│ K3       │ Teslimat-2'de  │ Müşteri B (3km)│ 12 dk sonra  │
│ K4       │ Dönüşte        │ 1km uzakta     │ 3 dk sonra   │
│ K5       │ Molada (yemek) │ Kafe (500m)    │ 20 dk sonra  │
│ K6       │ Teslimat-3'de  │ Müşteri C (4km)│ 15 dk sonra  │
│ K7       │ Restoranda     │ Restoran       │ ✅ HEMEN     │
│ K8       │ Evden çıkıyor  │ Ev (2km)       │ 10 dk sonra  │
│ K9       │ Teslimat-4'de  │ Müşteri D (1km)│ 5 dk sonra   │
│ K10      │ Dönüşte        │ 500m uzakta    │ 2 dk sonra   │
│ K11-K15  │ Çevrimdışı     │ -              │ Bugün yok    │
└──────────┴────────────────┴────────────────┴──────────────┘

SİPARİŞ GELDİ: Yeni sipariş → Restoran hazırlık: 10 dk

SİSTEM KARARI:
├── HEMEN MÜSAİT OLANLAR: K1, K7 (restoranda)
│   → 0 dk bekleme, hemen çıkabilir
│   → Ama yemek 10 dk'da hazır olacak
│   → Kurye restoranda beklerse: 10 dk bekleme (kurye için kötü)
│
├── YAKINDA MÜSAİT OLACAKLAR:
│   → K10 (2 dk) + restorana varış: 3 dk = 5 dk
│   → K4 (3 dk) + restorana varış: 2 dk = 5 dk
│   → K9 (5 dk) + restorana varış: 4 dk = 9 dk
│
├── EN İYİ SEÇİM: K10
│   ├── 2 dk sonra müsait (dönüşte, 500m)
│   ├── Restorana varış: +1 dk = 3 dk içinde restoranda
│   ├── Yemek hazır olana kadar bekler: 10 - 3 = 7 dk (çok değil)
│   └── VEYA hazırlık 3 dk geciktirilir → kurye hiç beklemez
│
├── MÜŞTERİYE GÖSTERİLEN:
│   ├── "🕐 Teslimat: 22 dakika"
│   ├── "👤 Kurye: K10 (Mehmet) - 4.8⭐"
│   └── "📍 Kurye şu an dönüşte, 3 dk içinde restoranda"
│
└── SİSTEM HER KURYE İÇİN AYRI HESAP YAPTI:
    ├── K1: 10 dk hazırlık + 0 dk bekleme + 8 dk yol = 18 dk (ama kurye bekler)
    ├── K7: 10 dk hazırlık + 0 dk bekleme + 6 dk yol = 16 dk (ama kurye bekler)
    ├── K10: 10 dk hazırlık + (3 dk gecikme) + 7 dk yol = 20 dk (bekleme yok) ←
    ├── K4: 10 dk hazırlık + 5 dk bekleme + 5 dk yol = 20 dk
    └── K9: 10 dk hazırlık + 9 dk bekleme + 3 dk yol = 22 dk
```

**Kural**: Restoranın kendi kuryeleri de olsa, her biri **bireysel** takip edilir. Sistem, hangi kuryenin hangi siparişe gideceğini **o sipariş anında** belirler. Önceden atanmış sabit kurye yoktur.

### 9.2 Kurye Durum Makinesi ve Mola Yönetimi

Her kurye anlık olarak aşağıdaki durumlardan birindedir ve sistem bu durumu sürekli izler:

```
KURYE DURUM MAKİNESİ:
┌──────────────────────────────────────────────────────────────┐
│                       ÇEVRİMDIŞI                           │
│                          │                                  │
│                          ▼                                  │
│                       ÇEVRİMİÇİ                             │
│                          │                                  │
│            ┌─────────────┼─────────────┐                    │
│            ▼              ▼             ▼                    │
│         MÜSAİT        SİPARİŞTE      PLANLI                │
│         (bekliyor)     (teslimde)    (rezerve)             │
│            │              │             │                    │
│            │              ▼             │                    │
│            │           DÖNÜŞTE         │                    │
│            │        (restorana dön)    │                    │
│            │              │             │                    │
│            └──────────────┴─────────────┘                    │
│                          │                                  │
│                          ▼                                  │
│                       MOLA                                 │
│              "X dk sonra dönerim"                          │
│                          │                                  │
│                          ▼                                  │
│                       ÇEVRİMDIŞI                           │
└──────────────────────────────────────────────────────────────┘
```

| Durum | Açıklama | Sistem Aksiyonu |
|-------|----------|-----------------|
| **Çevrimdışı** | Online değil, sipariş alamaz | Yok sayılır |
| **Çevrimiçi** | Sisteme bağlı, durum seçmemiş | Havuza ekle |
| **Müsait** | Beklemede, hemen çıkabilir | Öncelikli ata |
| **Planlı/Rezerve** | X dk sonra müsait olacak | Gelecek siparişe ata |
| **Siparişte** | Teslimat yapıyor | Takip et, ETA hesapla |
| **Dönüşte** | Restorana dönüyor | Dönüş bitince müsait yap |
| **Mola** | "X dk sonra dönerim" | Süre bitince müsait yap |

#### 9.2.1 Mola Bildirimi (Tek Adım)

Kurye mola vermek istediğinde sadece **2 şey** söyler:

```
MOLA BİLDİRİMİ:
├── 1️⃣ "MOLADAYIM" butonuna basar
├── 2️⃣ "KAÇ DAKİKA?" — kurye yazar (ör: 15 dk)
└── 3️⃣ Sistem otomatik konum alır (GPS)

KURYENİN EKRANI:
╔═══════════════════════════╗
║   ☕ MOLA                 ║
║                           ║
║   Ne kadar süre?          ║
║                           ║
║   ┌─────────────────┐     ║
║   │ 15 dakika      │     ║
║   └─────────────────┘     ║
║                           ║
║   📍 Şu an: Kafe X       ║
║                           ║
║   [ ✅ MOLA BAŞLA ]      ║
║   [ 🔄 Hazırım / İptal ] ║
╚═══════════════════════════╝
```

Neden tür seçimi yok?

```
NEDEN BASİT MOLA?
├── Kurye "yemek" derse 30 dk → ama 15 dk'da bitti → kısıtlama saçma
├── Kurye "çay" derse 15 dk → ama 20 dk sürdü → ceza mı yiyecek?
├── Kurye "lavabo" derse 10 dk → ama camide 15 dk durdu → sorun değil
└── Kurye en iyi kendini bilir: "Kaç dk?" dersen doğru söyler
```

#### 9.2.2 Mola Kuralları

```
MOLA KURALLARI:
├── Kurye süreyi KENDİSİ belirler
│   ├── Minimum: 1 dk
│   ├── Maksimum: 45 dk (üzeri çevrimdışı sayılır)
│   └── Varsayılan: 15 dk (hiçbir şey yazmazsa)
│
├── Süre dolunca sistem otomatik hatırlatır
│   ├── ⏰ Süre doldu → bildirim: "Mola bitti, müsait misin?"
│   ├── Kurye: "Hazırım" → müsait olur
│   ├── Kurye: "5 dk daha" → uzatır (1 kere)
│   └── Kurye: hiçbir şey yapmazsa → 5 dk sonra çevrimdışı
│
├── Mola sırasında konum paylaşımı devam eder
│   ├── GPS her 30 saniyede bir güncellenir
│   ├── Sistem nerede olduğunu bilir (kafe/cami/park)
│   └── Konum sapması >200m: "Mola yeriniz değişti, yeni konum kaydedildi"
│
├── Mola sırasında sipariş GELMEZ
│   ├── Sistem moladaki kuryeyi havuzdan çıkarır
│   └── Acil durumda: "Acil sipariş var, çıkar mısın? (+%50 prim)"
│
└── Kurye molayı erken bitirebilir
    ├── "Hazırım" butonu
    └── Anında müsait → sipariş alabilir
```

### 9.3 3 Aşamalı Kurye Zamanlama Sistemi

Küçük üreticiler ve büyük restoranlar için ortak çözüm:

```
AŞAMA 1 — ÖN BİLDİRİM (sipariş anında)
├── Sipariş oluşur oluşmaz sistem devreye girer
├── Restoranın geçmiş hazırlık süresi hesaplanır
│   ├── Büyük restoran: Son 50 siparişin ortalaması (15 dk ±2)
│   ├── Küçük üretici: Son 20 siparişin ortalaması (18 dk ±7)
│   └── Yeni üretici: Menüdeki baz süre × 1.5 (güvenli)
├── Bölgedeki kuryeler taranır
│   ├── Müsait kuryeler: "Tahmini X dk sonra sipariş hazır"
│   ├── Dönüşteki kuryeler: "Y rotasını bitirince yeni sipariş"
│   └── Planlı kuryeler: "Z saatinde müsait olacak"
└── Henüz atama yapılmaz, sadece kuryeler bilgilendirilir

AŞAMA 2 — ÖN REZERVASYON (tahmini bitiş - 5 dk)
├── Sistem hazırlık takibine başlar
├── Hazırlık %70 tamamlandığında veya bitişe 5 dk kala:
│   ├── En uygun kurye seçilir
│   │   ├── Kriter 1: Mesafe (üreticiye en yakın)
│   │   ├── Kriter 2: ETA (tahmini varış süresi)
│   │   ├── Kriter 3: Kurye puanı (4.5+ öncelik)
│   │   └── Kriter 4: Yön (dönüşteyse rotaya uygun mu?)
│   └── Kurye rezerve edilir, üreticiye yönlendirilir
│
├── REZERVASYON TÜRLERİ:
│   ├── MÜSAİT KURYE: "Git, vardığında hazır olacak"
│   ├── SİPARİŞTE KURYE: "Teslimatı bitir, oradan yeni siparişe git"
│   │   └── ÇİFTE ZİNCİR: Kurye A'yı müşteri X'e gönder,
│   │       aynı anda kurye B'yi üreticiye hazırla
│   └── PLANLI KURYE: "15 dk sonra müsait ol, seni bekleyen sipariş var"

AŞAMA 3 — KESİN ATAMA (hazır olunca)
├── Yemek hazır, paketlendi, zaman damgası eklendi
├── Kuryeye kesin bildirim: "Almaya gel"
├── Kurye zaten yoldaysa → direkt varış
├── Kurye henüz yeni atandıysa → yola çık
├── Bekleme durumu:
│   ├── Kurye geldi, yemek yok: Kurye bekler (dakika ücreti)
│   ├── Yemek hazır, kurye yok: Acil durum (yedek kurye)
│   └── Optimal: Kurye gelir, 1-2 dk içinde yemek hazır
└── Teslimat başlar
```

### 9.4 Kurye Sürekli Online Olma Zorunluluğu

Platform kurye havuzunun çalışması için kuryelerin belirli saatlerde online olması **teşvik edilir**, zorunlu değildir. Ancak sistem şu mekanizmalarla sürekli kullanılabilirliği sağlar:

```
KULLANILABİLİRLİK MEKANİZMALARI:
├── 📊 YOĞUNLUK TAHMİNİ (AI)
│   ├── Geçmiş verilere göre yoğun saatler hesaplanır
│   ├── 12:00-13:30: Öğle yoğunluğu (tahmini +%300 sipariş)
│   ├── 18:00-20:30: Akşam yoğunluğu (tahmini +%500 sipariş)
│   ├── Yağmurlu günler: +%200 sipariş artışı
│   └── Sistem 24 saat önceden "tahmini ihtiyaç" yayınlar
│
├── 💰 DİNAMİK KURYE ÜCRETİ
│   ├── Düşük talep: Baz ücret (20 ₺/teslimat)
│   ├── Normal talep: Standart (25 ₺/teslimat)
│   ├── Yüksek talep: +%50 prim (37.5 ₺/teslimat)
│   ├── Kritik talep: +%100 prim (50 ₺/teslimat)
│   └── Kuryeler yoğun saatte daha çok kazanır → online kalır
│
├── 🎯 GARANTİLİ GELİR
│   ├── Haftalık minimum gelir garantisi (belirli saat online olana)
│   ├── Örnek: Haftada 30 saat online → 3000 ₺ garanti
│   └── Farkı platform tamamlar
│
├── 🔄 YEDEK HAVUZ
│   ├── Her bölge için minimum kurye sayısı belirlenir
│   ├── Eşik altına düşülürse: Komşu bölgeden kurye çağrılır
│   ├── Acil durumda: Taksi kuryeleri devreye girer (ortak havuz)
│   └── Hiç kurye yoksa: Sipariş alınmaz (müşteriye bildirim)
│
└── 🚀 AVANTAJ
    ├── Kurye online kaldıkça daha çok sipariş → daha çok kazanç
    ├── Elit kurye statüsü (4.5+) daha çok sipariş önceliği
    └── Platform sadakat puanı (ek indirimler, avantajlar)
```

### 9.5 Dinamik Sevk Algoritması

Sistem, her saniye aşağıdaki hesaplamayı yaparak en uygun kuryeyi belirler:

```
SEVK KARAR MATEMATİĞİ:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Kurye Skoru = (1/msf) × 0.40 + puan × 0.25 + (1/bks) × 0.20  │
│                     + yon × 0.10 + yuk × 0.05                    │
│                                                                  │
│  msf = Mesafe Faktörü (kurye → restoran, km)                    │
│  puan = Kurye puanı (1.0 - 5.0)                                 │
│  bks = Bekleme Süresi (kuryenin bekleme ihtimali, dk)           │
│  yon = Yön Uyumu (dönüş rotasına uygun mu? 0 veya 1)           │
│  yuk = Yük Faktörü (o bölgedeki kurye yoğunluğu)               │
│                                                                  │
│  En yüksek skorlu kurye atanır.                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.4.1 Sevk Senaryoları

```
SENARYO 1: KURYE MÜSAİT
├── Durum: Sipariş hazırlanıyor, bölgede müsait kurye var
├── Aksiyon: Kuryeye 5 dk kala rezervasyon, hazır olunca atama
├── Kurye restorana varış: Yemekle eş zamanlı (±2 dk)
└── Bekleme: Yok veya minimal

SENARYO 2: KURYE SİPARİŞTE (ZİNCİRLEME)
├── Durum: Kurye A, müşteri X'e teslimat yapıyor
├── Müşteri X, üretici Y'ye yakın (500m)
├── Aksiyon: Kurye A, müşteri X'e teslim yapar yapmaz
│           üretici Y'ye yönlendirilir
├── Avantaj: Kurye boş dönmez, sürekli çalışır
├── Risk: Üretici Y'de hazırlık gecikirse kurye bekler
└── Çözüm: Bekleme ücreti + plandan sapma uyarısı

SENARYO 3: KURYE YOK (BÖLGE BOŞ)
├── Durum: Bölgede hiç müsait kurye yok, tümü meşgul
├── Aksiyon 1: Komşu bölgeden en yakın kurye çağrılır
│   └── Ek süre müşteriye bildirilir (+5-10 dk)
├── Aksiyon 2: Taksi kurye havuzu devreye sokulur
│   └── Taksi kuryeleri "çoklu görev" yapabilir mi?
├── Aksiyon 3: Müşteriye alternatif sunulur
│   ├── "30 dk sonra teslimat" (kurye gelince)
│   └── "Şimdi sipariş ver, X saatinde gelir" (planlı)
└── Son çare: Sipariş alınmaz, restorana bildirim

SENARYO 4: RESTORANIN KENDİ KURYESİ MEŞGUL
├── Durum: Restoranın özel kuryesi başka teslimatta
├── Aksiyon: Platform havuzundan kurye atanır (yedek)
├── Restorana maliyet: Platform kuryesi ücreti (%5 ek)
├── Kurye dönünce: Platform kuryesi iptal edilmez, devam eder
└── Optimal: İki kurye paralel çalışır (özel + platform)

SENARYO 5: YOĞUN SAAT KRİZİ
├── Durum: Öğle yoğunluğu, 20 sipariş, 5 kurye
├── Aksiyon: Sistem önceliklendirme yapar
│   ├── Öncelik 1: Bekleyen siparişler (10+ dk beklemiş)
│   ├── Öncelik 2: Kısa mesafe (hızlı teslimat)
│   ├── Öncelik 3: Yüksek puanlı müşteri (sadakat)
│   └── Öncelik 4: Rotaya uygun zincirleme
├── Kuryeler arası: Canlı rota optimizasyonu
│   ├── Kurye A'yı rota 1'e, Kurye B'yi rota 2'ye ata
│   └── Toplam teslimat süresini minimize et
└── Yeni sipariş: Gecikme uyarısı ile alınır
```

### 9.6 Gerçek Zamanlı Yön Düzeltme (Pilot Sistem)

Hazırlık süresindeki sapmalara karşı anlık müdahale:

```
PİLOT SİSTEM AKIŞI:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  SİPARİŞ OLUŞTU: Hazırlık süresi tahmini: 18 dk                │
│  → Kurye rezerve: 13. dakikada atanacak                         │
│                                                                  │
│  10. DAKİKA: Üretici geride (%50 tamam, beklenen %70)           │
│  → Sistem tespit: Gecikme sinyali                               │
│  → Aksiyon: Kurye rezervasyonunu 3 dk ötele                     │
│  → Kuryeye bildirim: "Hazırlık gecikiyor, 3 dk geç gel"         │
│                                                                  │
│  15. DAKİKA: Üretici hızlandı (%90 tamam)                        │
│  → Sistem tespit: Toparlıyor                                    │
│  → Aksiyon: Kuryeyi şimdi ata                                   │
│  → Kurye 3 dk içinde varır, yemek 2 dk içinde hazır             │
│  → Eş zamanlı: ±1 dk hata payı                                  │
│                                                                  │
│  20. DAKİKA: Kurye vardı, yemek hazır, teslim alma              │
│  → SONUÇ: Kurye beklemedi, yemek soğumadı                       │
│  → Sapma: Tahmin 18 dk, gerçek 20 dk → +2 dk                    │
│  → Algoritma güncellemesi: Bu üretici için +%10 güvenlik payı   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.5.1 Pilot Sistem Kuralları

| Sapma | Tespit | Aksiyon |
|-------|--------|---------|
| Hazırlık %20 geri | 2 dk gecikme sinyali | Rezervasyonu 1 dk ötele |
| Hazırlık %40 geri | 4 dk gecikme sinyali | Rezervasyonu 3 dk ötele |
| Hazırlık %60 geri | Kritik gecikme | Rezervasyon iptal, yeni kurye |
| Hazırlık %20 önde | Erken bitiyor | Kuryeyi hemen ata |
| Hazırlık %40 önde | Çok erken | En yakın müsait kuryeyi bul |
| Bekleme >5 dk | Kurye bekliyor | Dakika başına bekleme ücreti |

### 9.7 Kurye Bekleme Süresi Yönetimi

Bekleme süresi, sistemin en kritik metriğidir. Kuryeler beklemek istemez.

```
BEKLEME ÜCRETİ TARİFESİ:
├── 0-2 dk: Ücretsiz (normal tolerans)
├── 2-5 dk: 2 ₺/dk (üreticiden kesilir)
├── 5-10 dk: 4 ₺/dk (üreticiden kesilir)
├── 10+ dk: Kurye siparişi bırakabilir (cezasız)
└── Maksimum bekleme: 15 dk (sistem zorla iptal eder)

BEKLEME ÖNLEME:
├── Üretici "gecikeceğim" bildirimi yapabilir (+3 dk tolerans)
├── Haftada 3+ bekleme: Üreticiye kapasite düşürme uyarısı
├── Haftada 5+ bekleme: Otomatik kapasite %50 azaltma
└── Kurye onayı olmadan bekleme süresi uzatılamaz
```

### 9.8 Restoran Özel Kurye + Platform Havuzu Karma Modeli

Büyük restoranların kendi kuryeleri vardır ancak platform havuzunu da yedek olarak kullanabilir:

```
KARMA MODEL ÇALIŞMA PRENSİBİ:
├── RESTORANIN KENDİ KURYESİ:
│   ├── Öncelikli olarak restoranın siparişlerine atanır
│   ├── Restoran kuryenin çalışma saatlerini belirler
│   ├── Kurye müsait değilse → platform havuzuna düşer
│   └── Restoran, kurye başına aylık sabit ücret öder (opsiyonel)
│
├── PLATFORM HAVUZU (YEDEK):
│   ├── Restoranın kuryesi meşgulse devreye girer
│   ├── Restoran, platform kuryesi başına %5 ek komisyon öder
│   └── Müşteriye "Restoran Kuryesi" veya "Platform Kuryesi" bilgisi
│
├── ÇİFTE ATAMA ÖNLEME:
│   ├── Restoran kuryesi bir siparişe atandıysa
│   ├── Sistem o kuryeyi ikinci siparişe atamaz
│   └── İkinci sipariş otomatik platform havuzuna düşer
│
└── ÖNCELİK SIRASI:
    1. Restoranın kendi kuryesi (müsaitse)
    2. Restorana en yakın platform kuryesi
    3. Komşu bölgeden platform kuryesi
```

### 9.9 Edge Case Yönetimi

| Senaryo | Sistem Tepkisi |
|---------|---------------|
| **Kurye yok, yoğun saat** | Sipariş alınır, "Kurye bulunamadı, 10 dk içinde teyit" bildirimi |
| **Kurye siparişi bıraktı** | Acil durum, yedek kurye atanır, yoksa restoran iptal |
| **Restoran kapandı (ani)** | Aktif siparişler iptal, kurye ücreti restorandan kesilir |
| **Müşteri adreste yok** | 5 dk bekleme, sonra sipariş iptal, kurye ücreti müşteriden |
| **Çift sipariş aynı kuryeye** | Sistem optimize eder: Aynı restoransa tek kurye, farklıysa iki kurye |
| **Kurye kaza yaptı** | Acil durum butonu, yedek kurye atanır, sağlık ekipleri |
| **Motor bozuldu** | En yakın tamir noktası + yedek kurye ataması |
| **Ekstrem hava** | Kurye ücreti +%50-100, gönüllü kurye aranır |

---

## 10. KURYE YÖNETİMİ VE MOBİNG ÖNLEME

> 📖 Kurye yönetimi, durum makinesi, mola sistemi, puanlama ve mobing önleme kuralları artık [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md)'de tanımlanmıştır.

### 10.1 Kurye Kayıt Şartları

Kuryelik ayrı bir hesap türü değil, **mevcut bireysel hesabın bir rolüdür**.

```
KULLANICI → HESAP AÇAR → MESLEK SEÇER → KURYE ROLÜ AKTİF OLUR
                │
                ├── Öğrenci
                ├── Memur
                ├── Esnaf
                ├── Emekli
                ├── Kurye (tam zamanlı)
                └── Kurye (yarı zamanlı)
```

Kurye mesleğini seçince ek belgeler istenir:

| Belge/Kriter | Açıklama |
|-------------|----------|
| Ehliyet (A2 veya B) | Motor veya araç için |
| Adli sicil | Temiz kayıt |
| Sigorta | İş kazası sigortası |
| Sağlık raporu | Sürüşe engel durum yok |
| Deneme sürüşü | 5 sipariş mentor eşliğinde |
| Termal çanta | Ölçülere uygun (opsiyonel kiralık) |
| Akıllı telefon | GPS + kamera çalışır durumda |

#### 10.1.1 Hesap Menüsünde Kurye Bölümü

Kurye olan kullanıcının hesabında ek bir menü belirir:

```
KURYE MENÜSÜ (Hesap → Kurye Panelim):
├── 🟢 Çevrimiçi / 🔴 Çevrimdışı (tek tuş)
├── ☕ Moladayım (süre gir: "15 dk")
│   └── "15 dk sonra devam edeceğim" (otomatik bildirim)
├── 📊 Bugünkü Performans
│   ├── Tamamlanan sipariş: 12
│   ├── Toplam km: 45 km
│   ├── Kazanç: 360 ₺
│   └── Puan: 4.8 ⭐
├── 📅 Çalışma Takvimi
│   ├── Bu hafta: 32 saat
│   ├── Bu ay: 128 saat
│   └── Ortalama: 8 saat/gün
└── ⚙️ Ayarlar
    ├── Servis dışı günler
    ├── Bildirim tercihleri
    └── Ödeme hesabı
```

Bu menü sayesinde:
- Kurye ne zaman molaya çıktı, ne zaman döndü → kayıt altında
- Kim ne kadar çalıştı, nerede çalıştı, ne kadar kazandı → sistem biliyor
- Zaman içinde performans takibi mümkün

### 10.2 Kurye Puanlama ve Sınıflandırma

```
KURYE PUAN SİSTEMİ:
├── 4.5+:  ELİT (öncelikli sipariş)
├── 4.0-4.4: STANDART (normal dağıtım)
├── 3.0-3.9: İZLEME (sınırlı sipariş)
└── <3.0: PASİF (eğitim sonrası tekrar değerlendirme)
```

### 10.3 Mobing Önleme Sistemi

Kuryelerin karşılaştığı mobing durumları sistem tarafından tespit edilir:

```
MOBİNG TESPİT MEKANİZMALARI:
├── ⏱️ SÜRE BAZLI
│   ├── Sistem hesaplanan süre gösterilir
│   ├── Müşteri "gecikti" şikayeti yaparsa
│   ├── Sistem kendi süresi ile karşılaştırma yapar
│   ├── Kurye sistem süresine uyduysa şikayet reddedilir
│   ├── Kurye sistem süresini aştıysa neden sorulur
│   └── Haklı neden (trafik/hava/restoran gecikmesi) → iptal
│
├── 💬 İLETİŞİM BAZLI
│   ├── Müşteri ağır küfür/kötü dil kullanırsa
│   ├── Otomatik tespit (kelime filtresi)
│   ├── Kurye anında bildirim atabilir
│   └── Müşteri geçici ban (24 saat - 7 gün)
│
├── 📍 KONUM BAZLI
│   ├── Kurye belirtilen adreste beklerse
│   ├── Müşteri gelmezse 5 dk bekleme süresi
│   ├── Geri sayım başlar (5 dk)
│   ├── Süre sonunda sipariş iptal
│   └── Müşteri ceza puanı alır
│
├── 💰 ÖDEME BAZLI
│   ├── Kapıda ödeme için müşteri önceden para bildirir
│   ├── Kurye üzerinde nakit taşımaz
│   └── Ödeme online alınır
│
└── 📞 DESTEK BAZLI
    ├── Kurye tek tuşla destek çağırabilir
    ├── Canlı destek 7/24
    └── Acil durum butonu (panik)
```

### 10.4 Kurye Gerçekçi Süre Koruması

```
KURYE KORUMA KURALLARI:
├── Sistem süresinden önce teslim → kurye avantajlı
├── Sistem süresine uygun teslim → nötr
├── Sistem süresinden geç teslim → neden açıklanmalı
├── Restoran kaynaklı gecikme → kurye sorumlu değil
├── Trafik/hava kaynaklı gecikme → otomatik onay
└── 3+ haksız ceza alan kurye → otomatik inceleme
```

### 10.5 Kurye Termal Çanta ve Donanım

| Donanım | Zorunlu | Açıklama |
|---------|---------|----------|
| Termal çanta (büyük) | Evet | Sıcak/soğuk ayrı bölme |
| Telefon tutucu | Evet | Direksiyon/gidon montajı |
| Taşınabilir şarj | Öneri | Telefon batarya desteği |
| Yağmurluk | Evet | Kurye konforu |
| Kask | Evet (motor) | Güvenlik |

---

## 11. QR KOD TESLİMAT ONAY SİSTEMİ

### 11.1 Sistem Akışı

```
QR ONAY AKIŞI:
SİPARİŞ OLUŞUR:
├── Müşteriye QR kod gönderilir
├── Sipariş detay sayfasında görünür
├── QR kod içinde:
│   ├── Sipariş ID (benzersiz)
│   ├── Zaman damgası (oluşturma anı)
│   ├── Müşteri ID (hash'lenmiş)
│   └── İmza (sistem tarafından doğrulanır)
│
KURYE TESLİM ANI:
├── Kurye "Teslim Et" butonuna basar
├── Müşteriden QR okutması istenir
├── Alternatif: Kurye 4 haneli SMS kodu girer
├── QR doğrulama:
│   ├── Sipariş ID eşleşiyor mu?
│   ├── Zaman damgası geçerli mi?
│   └── İmza doğrulandı mı?
│
BAŞARILI:
├── Sipariş "TESLİM EDİLDİ" statüsü
├── Teslim zamanı saniye hassasiyetiyle kaydedilir
├── Müşteri ve kurye bildirim alır
└── Puanlama ekranı açılır

BAŞARISIZ:
├── QR hatalı → 3 deneme hakkı
├── 3 başarısız → manuel destek çağrılır
└── SMS kodu alternatifi sunulur
```

### 11.2 Zaman Ölçümü ve Raporlama

```
ZAMAN RAPORU:
├── Sipariş oluşturma:    14:30:00
├── Restoran onay:        14:30:45 (+45 sn)
├── Hazırlık başlangıç:   14:31:12 (+27 sn)
├── Hazırlık tamam:       14:42:08 (+10 dk 56 sn)
├── Kurye teslim alma:    14:43:30 (+1 dk 22 sn)
├── Müşteriye teslim:     14:55:17 (+11 dk 47 sn)
├── ─────────────────────────────────────
└── TOPLAM SÜRE:          25 dk 17 sn

SAPMA ANALİZİ:
├── Sistem tahmini:      26 dk
├── Gerçek:              25 dk 17 sn
├── Fark:                -43 sn (%2.8 hata)
└── Değerlendirme:       Başarılı (hata <%10)
```

### 11.3 QR Kod Güvenlik Önlemleri

| Güvenlik Katmanı | Açıklama |
|-----------------|----------|
| Tek kullanımlık | Her QR kod tek kullanım |
| Zaman aşımı | 30 dk geçerlilik |
| İmza doğrulama | HMAC-SHA256 |
| Coğrafi sınır | Sadece teslimat adresi yakınında (50m) |
| Ekran görüntüsü koruma | QR ekran görüntüsü algılanırsa uyarı |
| Brute-force koruma | 3 başarısız deneme → blok |

---

## 12. AKILLI KAPIDA ÖDEME SİSTEMİ

### 12.1 Sistem Tanımı

Kapıda ödeme tamamen kalkmaz ancak **nakit emanet** tamamen kaldırılır. Müşteri önceden para bildirimi yapmak zorundadır.

```
KAPIDA ÖDEME AKIŞI:
├── Müşteri kapıda ödeme seçer
├── Müşteri NE KADAR ödeyeceğini bildirir
│   ├── Sipariş tutarı: 120 ₺
│   ├── Müşteri bildirimi: 150 ₺ (120 ₺ + 30 ₺ bozukluk)
│   └── Maksimum bildirim: Sipariş × 2 (240 ₺)
│
├── Bildirim onaylanır
├── Müşteri cüzdanından tutar bloke edilir
├── Kuryeye "Müşteri 150 ₺ hazırladı" bilgisi gider
│
├── TESLİM ANI:
│   ├── Müşteri parayı uzatır
│   ├── Kurye sisteme "Tahsilat Tamam" onayı verir
│   ├── Müşteri cüzdanından bloke düşer
│   └── Tutar kurye cüzdanına aktarılır
│
└── İHTİLAF DURUMU:
    ├── Müşteri daha az verdi → kurye reddedebilir
    ├── Müşteri daha çok verdi → sistem iade eder
    └── Çözümsüz → destek devreye girer
```

### 12.2 Neden Nakit Emanet Yok?

```
NAKİT EMANET YASAĞI NEDENLERİ:
├── Kurye üzerinde fazla nakit → güvenlik riski
├── Kurye gasp/soygun hedefi olabilir
├── Müşteri eksik/hatalı para verebilir
├── Bozuk para sorunu (para üstü)
├── Muhasebe karmaşası
└── Tüm ödemeler online izlenebilir
```

### 12.3 Ödeme Seçenekleri

| Yöntem | Kapıda | Online | Açıklama |
|--------|--------|--------|----------|
| Kredi Kartı (online) | - | ✓ | Anında ödeme |
| Cüzdan Bakiyesi | - | ✓ | Platform cüzdanı |
| Kapıda Nakit Bildirimli | ✓ | - | Önceden bildirim şart |
| Kapıda Kart (POS) | ✓ | - | Kurye yanında POS (opsiyonel) |
| Mobil Ödeme (QR) | ✓ | ✓ | FastPay/Apple Pay/Google Pay |

---

## 13. YERİNDE YEMEK ÖDEME SİSTEMİ (DINE-IN)

### 13.1 Sistem Tanımı

Restorana gidip yemek yiyen müşteri de **platform üzerinden ödeme** yapabilir. Bu hem müşteriye kolaylık hem restorana avantaj sağlar.

```
YERİNDE YEMEK AKIŞI:
MÜŞTERİ RESTORANA GİDER
         │
         ├── Masaya oturur
         ├── Yemek siparişi verir (restorana normal)
         ├── Yemeğini yer
         └── Hesap istediğinde:
              │
              ▼
ÖDEME YÖNTEMİ SEÇER:
├── A) PLATFORM ÜZERİNDEN ÖDE (teşvikli)
│   ├── Uygulamayı açar → "Restoranda Öde" butonu
│   ├── Restoranı bulur (QR okutur veya listeden seçer)
│   ├── Hesap tutarını görür (restoran girdi)
│   ├── Cüzdan/kart ile öder
│   ├── Anında puan kazanır 🎯
│   └── Dijital fiş gelir (e-Arşiv)
│
├── B) RESTORANA ELDEN ÖDE (klasik)
│   ├── Nakit veya restoran POS'u ile öder
│   ├── Puan KAZANAMAZ ❌
│   └── Fiş basılır
│
└── C) KARMA ÖDE
    ├── Kısım platform, kısım nakit
    └── Sadece platform kısmına puan
```

### 13.2 Müşteriyi Platformdan Ödemeye Teşvik

| Teşvik | Müşteri | Restoran |
|-------|---------|----------|
| **Puan** | Her platform ödemede **1 puan** | Her platform ödemede **1 puan** |
| **Komisyon** | - | Dine-in ödemelerde de **%2** (sabit, tüm kanallar aynı) |
| **Rozet** | "Sık Restoran Müşterisi" rozeti (10+ ödeme) | "Dijital Ödeme" rozeti (50+ platform ödeme alan) |
| **Sadakat** | Delivery + Dine-in puanları aynı cüzdanda | - |
| **Kampanya** | "Çifte puan" (restoran belirler) | Kampanya belirleme yetkisi |
| **Veri** | - | Müşteri verisi (kim, ne yemiş, ne sıklıkta) |

**Restorana %2 komisyon**: Dine-in ödemede de aynı oran uygulanır. Tüm kanallarda komisyon standardı korunur. Restoran yine kazanır: rakipler %25-30 alırken biz %2 alırız.

**Puanların maliyeti**: Yoktur. Müşteri puanlarını delivery'de kurye ücretinde kullanır. Restoran puanlarını komisyon düşüşünde veya premium hizmetlerde kullanır. 10 puan = 1 ₺ değerindedir.

### 13.3 Restoran Avantajları

```
RESTORAN NE KAZANIR?
├── Kasadaki iş yükü azalır (otomatik ödeme, para üstü derdi yok)
├── Nakit taşıma/emanet riski kalkar
├── Müşteri sadakat programı otomatik işler (platform halleder)
├── Dijital fiş (e-Arşiv) otomatik kesilir, muhasebe kolaylaşır
├── Tüm kanallarda aynı düşük komisyon (%2)
├── Müşteri verisi gelir (kim geliyor, ne yiyor, ne sıklıkta?)
└── Platformda "Bu restoranda ye" önerilerinde öne çıkma
```

### 13.3 Masa Sayısı Zorunluluğu

Dine-In hizmeti verecek her restoran, kurumsal hesap kaydı sırasında **masa sayısını** bildirmek zorundadır:

```
MASA SAYISI KURALI:
├── 🔢 Masa sayısı: Restoran profilinde zorunlu alan
├── 🏪 Sadece paket servis yapanlar: Masa sayısı = 0
├── 📈 Masa sayısı değişirse: Restoran güncellemeli
├── 🖨️ Her masaya: QR kod basılır (platform tarafından üretilir)
├── 🔄 Masa numaraları: 1'den başlar, sistem otomatik atar
└── ✅ Doğrulama: Platform masa sayısını denetler (fotoğraf/beyan)
```

### 13.4 QR Kod ile Masa ve Hesap

Her masada restorana özel QR kod bulunur:

```
QR KOD SİSTEMİ:
├── Müşteri QR okutur
├── Masa numarası otomatik belirlenir (Masa 5)
├── Restoranın o masaya ait hesabı görünür
│   ├── Sipariş edilen ürünler (restoran girer)
│   ├── Toplam tutar
│   └── Varsa kampanya/indirim
├── Müşteri onaylar → öder
└── Garson onayı gerekmez (otomatik)

ALTERNATİF: QR yoksa
├── Uygulamada "Restoran Bul" ile restoran seçilir
├── Tutar manuel girilir (restoran onayı gerekir)
└── Masa numarası manuel yazılır
```

### 13.5 Güvenlik ve Doğrulama

```
GÜVENLİK:
├── Müşteri ödeme yapınca restorana anlık bildirim
├── Restoran onayı gerekir (ödeme doğru mu?)
├── İhtilaf durumunda:
│   ├── Restoran "hesap yanlış" derse → düzeltme yapılır
│   ├── Müşteri "ben ödemedim" derse → kayıt incelenir
│   └── 3 taraf (müşteri + restoran + platform) çözümü
└──── Her işlem kayıt altında (tarih, saat, masa, ürünler)
```

---

## 14. ZORUNLU AKTİF MÜŞTERİ HİZMETLERİ

### 14.1 Kural

**Her restoran** büyük/küçük fark etmeksizin aktif bir müşteri hizmetleri numarası bildirmek zorundadır.

### 14.2 Şartlar

```
MÜŞTERİ HİZMETLERİ ŞARTLARI:
├── Numara: 7/24 ulaşılabilir olmalı
├── Cevap süresi: Maksimum 30 saniye
├── Kayıt: Tüm görüşmeler kaydedilir (7 gün saklama)
├── Dil: Türkçe (ek diller opsiyonel)
├── Çalışan: Konu hakkında eğitimli personel
├── Bildirim: Platforma entegre (sorun çözülemezse platform devreye girer)
└── Alternatif: WhatsApp Business / Telegram (opsiyonel)
```

### 14.3 Büyük vs Küçük Restoran

| Özellik | Büyük Restoran (10+ çalışan) | Küçük Restoran (<10 çalışan) |
|---------|------------------------------|------------------------------|
| Müşteri hizmeti | Ayrı departman | İşletme sahibi/kendisi |
| Cevap süresi | 10 sn | 30 sn |
| Dil desteği | 2+ dil | En az Türkçe |
| Entegrasyon | API/PBX | Telefon/WhatsApp |

### 14.4 Platform Müşteri Hizmetleri (Yedek)

Platform ayrıca **merkezi müşteri hizmetleri** sağlar:

```
PLATFORM MÜŞTERİ HİZMETLERİ:
├── 7/24 canlı destek
├── Sipariş sorunları
├── İade/şikayet yönetimi
├── Kurye şikayetleri
├── Ödeme sorunları
├── Teknik destek
└── Acil durum hattı (panik butonu)
```

---

## 15. RESTORAN SAHİBİ KURUMSAL PANELİ

### 15.1 Panel Özellikleri

Kurumsal panel, restoran sahibine tam kontrol sağlar:

```
KURUMSAL PANEL MENÜSÜ:
├── 📊 DASHBOARD
│   ├── Günlük/haftalık/aylık sipariş grafikleri
│   ├── Gelir tablosu (brüt/net/komisyon)
│   ├── Popüler ürünler sıralaması
│   ├── Müşteri yorumları (canlı akış)
│   ├── Kurye performansı (varsa özel kurye)
│   ├── Puan durumu (görsel/evrak/kamera)
│   └── Teslimat süresi raporu
│
├── 📋 SİPARİŞ YÖNETİMİ
│   ├── Aktif siparişler (canlı takip)
│   ├── Sipariş geçmişi (filtreli arama)
│   ├── İptal edilen siparişler
│   ├── İade talepleri
│   └── Şikayet yönetimi
│
├── 🍽️ MENÜ YÖNETİMİ
│   ├── Ürün ekle/düzenle/sil
│   ├── Kategori yönetimi
│   ├── Ürün görselleri
│   ├── Fiyat güncelleme (toplu/toplu)
│   ├── Stok yönetimi (opsiyonel)
│   ├── Tazelik süresi tanımlama
│   └── Menü aktivasyon/deaktivasyon
│
├── 📸 GÖRSEL YÖNETİMİ
│   ├── Zorunlu görsel durumu
│   ├── Yeni görsel yükleme
│   ├── Eski görsel uyarıları
│   └── Görsel kalite puanı
│
├── 🎥 KAMERA YÖNETİMİ
│   ├── Canlı yayın durumu
│   ├── Kamera ekle/kaldır
│   ├── Yayın geçmişi
│   └── Puan katkısı
│
├── 📄 EVRAK YÖNETİMİ
│   ├── Evrak durumu
│   ├── Yeni evrak yükleme
│   ├── Süresi dolan evraklar
│   └── Doğrulama durumu
│
├── 💰 FİNANS
│   ├── Gelir tablosu
│   ├── Komisyon raporu
│   ├── Haftalık/aylık özet
│   ├── Cüzdan bakiyesi
│   ├── Para çekme talebi
│   └── Vergi raporu (e-Arşiv entegrasyonu)
│
├── 👥 KULLANICI YÖNETİMİ
│   ├── Yetkili kullanıcı ekleme
│   ├── Rol bazlı yetkilendirme
│   ├── Çalışan yönetimi
│   └── İzin takibi
│
├── ⚙️ AYARLAR
│   ├── Çalışma saatleri
│   ├── Servis bölgesi
│   ├── Bildirim tercihleri
│   ├── Ödeme ayarları
│   └── API entegrasyonları
│
└── 📞 DESTEK
    ├── Canlı destek
    ├── Sık sorulan sorular
    ├── Eğitim videoları
    └── Bildirim merkezi
```

### 15.2 Rol Bazlı Yetkilendirme

```
YETKİ SEVİYELERİ:
├── 🏢 SAHİP
│   ├── Tüm yetkiler
│   ├── Finansal işlemler
│   ├── Kullanıcı yönetimi
│   └── Hesap silme/devretme
│
├── 👨‍💼 MÜDÜR
│   ├── Sipariş yönetimi
│   ├── Menü yönetimi
│   ├── Müşteri hizmetleri
│   └── Raporlama
│
├── 👨‍🍳 ŞEF
│   ├── Menü yönetimi
│   ├── Stok takibi
│   ├── Tazelik yönetimi
│   └── Kamera yönetimi
│
├── 📸 FOTOĞRAFÇI
│   ├── Sadece görsel yükleme
│   └── Sadece görsel güncelleme
│
└── 👀 GÖZLEMCİ
    ├── Sadece görüntüleme
    └── Rapor indirme
```

---

## 16. SİPARİŞ YÖNETİMİ VE CANLI TAKİP

### 16.1 Sipariş Yaşam Döngüsü

```
SİPARİŞ DURUM MAKİNESİ:
MÜŞTERİ SEPETİ
   │
   ▼
SİPARİŞ OLUŞTURULDU ──────────────────────────────────┐
   │                                                    │
   ▼                                                    │
RESTORAN ONAYI ──── REDDET ──► İPTAL EDİLDİ ──────────┤
   │ (onay süresi: max 2 dk)                           │
   ▼                                                    │
HAZIRLANIYOR                                            │
   │                                                    │
   ▼                                                    │
HAZIR (paketleme tamam)                                 │
   │                                                    │
   ▼                                                    │
KURYE YOLA ÇIKTI ─────────────────────────────────────┤
   │ (canlı takip başlar)                               │
   ├── Hava durumu bildirimi (yağmur varsa)            │
   ├── Trafik bildirimi (yoğunluk varsa)               │
   └── Kurye konumu canlı (müşteriye açık)              │
   │                                                    │
   ▼                                                    │
TESLİM EDİLDİ (QR ile onay) ──────────────────────────┤
   │                                                    │
   ▼                                                    │
PUANLAMA EKRANI                                         │
   │                                                    │
   ▼                                                    │
SİPARİŞ TAMAMLANDI ◄───────────────────────────────────┘
```

### 16.2 Müşteri Canlı Takip Ekranı

```
CANLI TAKİP EKRANI:
╔════════════════════════════╗
║   🍽️ SİPARİŞ #1234        ║
║                            ║
║   📍 DURUM:                ║
║   ✅ Sipariş alındı        ║
║   🔄 Hazırlanıyor...       ║
║   ⏳ Kurye bekleniyor       ║
║   🛵 Kurye yolda            ║ ← ŞU AN
║   📦 Teslim edildi          ║
║                            ║
║   🕐 TAHMİNİ TESLİMAT      ║
║   14:58 (8 dk kaldı)       ║
║                            ║
║   🌧️ HAVA DURUMU           ║
║   Hafif yağmur (+%15)      ║
║                            ║
║   🗺️ [Kurye konumu]        ║
║   ┌────────────────────┐   ║
║   │     🛵 → 🏠         │   ║
║   │    2.3 km / 8 dk   │   ║
║   └────────────────────┘   ║
║                            ║
║   📞 Kurye: Ali (5.0 ⭐)  ║
║   💬 Mesaj gönder          ║
╚════════════════════════════╝
```

### 16.3 Sipariş İptal Kuralları

| Durum | İptal Eden | Ceza/İade |
|-------|-----------|-----------|
| Restoran onayı öncesi | Müşteri | Tam iade, ceza yok |
| Restoran onayı sonrası | Müşteri | %50 iade, kalan restorana |
| Hazırlık başladı | Müşteri | İade yok, tam ödeme |
| Restoran kaynaklı iptal | Restoran | Tam iade + %10 ceza |
| Kurye bulunamadı | Sistem | Tam iade |
| Teslimat süresi aşımı | Müşteri | Tam iade + %20 kupon |

---

## 17. CÜZDAN VE ÖDEME SİSTEMİ (TAKSİ İLE ORTAK)

### 17.1 Ortak Altyapı

Yemek sistemi, taksi sistemi ile aşağıdaki ortak altyapıyı kullanır:

```
ORTAK BİLEŞENLER:
├── 💰 Cüzdan Sistemi (taksi ile aynı)
│   ├── Bakiye yönetimi
│   ├── Para yükleme/çekme
│   ├── Havale/EFT
│   ├── Kart bağlama
│   ├── Otomatik ödeme
│   └── İşlem geçmişi
│
├── ⭐ Puanlama Motoru (taksi ile aynı)
│   ├── Çift yönlü puanlama
│   ├── Ağırlıklı ortalama
│   ├── Puan geçmişi
│   ├── İtiraz yönetimi
│   └── Ceza sistemi
│
├── 🗺️ Harita ve Konum (taksi ile aynı)
│   ├── Google Maps entegrasyonu
│   ├── Canlı takip
│   ├── Rota optimizasyonu
│   ├── Bölge yönetimi
│   └── Adres doğrulama
│
├── 📱 Bildirim Sistemi (taksi ile aynı)
│   ├── Push bildirim
│   ├── SMS
│   ├── E-posta
│   ├── WhatsApp (opsiyonel)
│   └── In-app bildirim
│
└── 🔐 Güvenlik Katmanı (taksi ile aynı)
    ├── JWT yetkilendirme
    ├── 2FA
    ├── Oturum yönetimi
    ├── İmza doğrulama
    └── Şifreleme
```

### 17.2 Yemek Özel Ödeme Akışı

```
YEMEK ÖDEME AKIŞI:
SİPARİŞ TUTARI HESAPLAMA:
├── Ürün toplamı:         100 ₺
├── Kurye ücreti:          20 ₺
├── Hava durumu ek ücret:  +3 ₺ (yağmur)
├── Paketleme ücreti:      +2 ₺
├── ──────────────────────────
└── TOPLAM:               125 ₺

ÖDEME YÖNTEMİ SEÇİMİ:
├── Cüzdan bakiyesi (varsa)
├── Kredi kartı (online)
├── Kapıda nakit (bildirimli)
├── Kapıda kart (POS)
└── Bölünmüş ödeme (cüzdan + kart)

TAHSİLAT:
├── Online: Anında çekim
├── Kapıda nakit: Bloke → teslimde çözüm
├── Kapıda kart: Bloke → teslimde çekim
└── İptal durumunda: Anında iade (24 saat içinde)
```

---

## 18. VERİTABANI ŞEMASI

### 18.1 Tablo Listesi

```sql
-- ============================================
-- TEMEL ŞEMA: yemek_sistemi
-- ============================================

-- RESTORAN ANA TABLOSU
CREATE TABLE yemek_restoran (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kurumsal_hesap_id   UUID NOT NULL REFERENCES kurumsal_hesap(id),
    unvan               VARCHAR(255) NOT NULL,
    marka_adi           VARCHAR(150) NOT NULL,
    telefon             VARCHAR(20) NOT NULL,
    email               VARCHAR(255) NOT NULL,
    web_sitesi          VARCHAR(255),
    mutfak_turu         VARCHAR(50) NOT NULL,     -- Türk, İtalyan, Çin, vs.
    fiyat_araligi       VARCHAR(10) NOT NULL,     -- ₺, ₺₺, ₺₺₺
    servis_tipi         VARCHAR(50) NOT NULL,     -- paket, restoran_ici, ikisi_de
    calisma_saatleri    JSONB NOT NULL,           -- gün bazlı {pazartesi: {acilis: "09:00", kapanis: "22:00"}}
    servis_yaricap      INTEGER NOT NULL,         -- km cinsinden
    konum               GEOGRAPHY(POINT) NOT NULL,
    adres              TEXT NOT NULL,
    adres_tarifi       TEXT,
    aktif               BOOLEAN DEFAULT true,
    kayit_tarihi        TIMESTAMPTZ DEFAULT NOW(),
    guncelleme_tarihi   TIMESTAMPTZ DEFAULT NOW(),
    pasif_nedeni       TEXT,                      -- neden pasif olduğu
    CONSTRAINT fk_kurumsal FOREIGN KEY (kurumsal_hesap_id) REFERENCES kurumsal_hesap(id)
);

-- RESTORAN BELGELERİ
CREATE TABLE yemek_restoran_belge (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    belge_tipi          VARCHAR(50) NOT NULL,     -- vergi_levhasi, hijyen, ruhsat, vb.
    dosya_yolu          TEXT NOT NULL,
    dogrulama_durumu    VARCHAR(20) DEFAULT 'beklemede', -- beklemede, onaylandi, reddedildi, sure_doldu
    yukleme_tarihi      TIMESTAMPTZ DEFAULT NOW(),
    gecerlilik_tarihi   DATE,
    puan                INTEGER DEFAULT 0,
    dogrulama_notu     TEXT,
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id)
);

-- RESTORAN GÖRSELLERİ
CREATE TABLE yemek_restoran_goruntu (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    kategori            VARCHAR(50) NOT NULL,     -- dis_cephe, salon, mutfak, cevre, tuvalet, otopark
    dosya_yolu          TEXT NOT NULL,
    cozunurluk          VARCHAR(20),
    cekim_tarihi        TIMESTAMPTZ,
    geotag              GEOGRAPHY(POINT),
    aktif               BOOLEAN DEFAULT true,
    yukleme_tarihi      TIMESTAMPTZ DEFAULT NOW(),
    son_kullanma        TIMESTAMPTZ,              -- 90 gün sonra
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id)
);

-- CANLI KAMERA
CREATE TABLE yemek_kamera (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    kamera_adi          VARCHAR(100),
    stream_url          TEXT NOT NULL,
    aktif               BOOLEAN DEFAULT false,
    cozunurluk          VARCHAR(20),
    son_yayin_tarihi    TIMESTAMPTZ,
    puan_katkisi        INTEGER DEFAULT 0,
    kayit_aktif         BOOLEAN DEFAULT true,
    olusturma_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id)
);

-- MENÜ KATEGORİLERİ
CREATE TABLE yemek_kategori (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    ad                  VARCHAR(100) NOT NULL,
    sira                INTEGER DEFAULT 0,
    aktif               BOOLEAN DEFAULT true,
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id)
);

-- MENÜ ÜRÜNLERİ
CREATE TABLE yemek_urun (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    kategori_id         UUID REFERENCES yemek_kategori(id),
    ad                  VARCHAR(200) NOT NULL,
    aciklama            TEXT,
    fiyat               DECIMAL(10,2) NOT NULL,
    indirimli_fiyat     DECIMAL(10,2),
    para_birimi         VARCHAR(3) DEFAULT 'TRY',
    hazirlik_suresi     INTEGER NOT NULL,         -- saniye cinsinden
    tazelik_omru        INTEGER,                  -- saniye cinsinden
    birim               VARCHAR(20) DEFAULT 'adet', -- adet, porsiyon, kg, lt
    stok                DECIMAL(10,2),            -- NULL = limitsiz
    goruntu_url         TEXT,
    aktif               BOOLEAN DEFAULT true,
    olusturma_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    guncelleme_tarihi   TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id),
    CONSTRAINT fk_kategori FOREIGN KEY (kategori_id) REFERENCES yemek_kategori(id)
);

-- ÜRÜN OPSİYON GRUPLARI (ör: boyut, ekstra malzeme)
CREATE TABLE yemek_urun_opsiyon_grubu (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    urun_id             UUID NOT NULL REFERENCES yemek_urun(id),
    ad                  VARCHAR(100) NOT NULL,     -- Boyut, Ekstra, İçecek
    zorunlu             BOOLEAN DEFAULT false,
    coklu_secim         BOOLEAN DEFAULT false,
    CONSTRAINT fk_urun FOREIGN KEY (urun_id) REFERENCES yemek_urun(id)
);

-- ÜRÜN OPSİYONLARI
CREATE TABLE yemek_urun_opsiyon (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grup_id             UUID NOT NULL REFERENCES yemek_urun_opsiyon_grubu(id),
    ad                  VARCHAR(100) NOT NULL,
    fiyat_farki         DECIMAL(10,2) DEFAULT 0,
    CONSTRAINT fk_grup FOREIGN KEY (grup_id) REFERENCES yemek_urun_opsiyon_grubu(id)
);

-- SİPARİŞ ANA TABLOSU
CREATE TABLE yemek_siparis (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    musteri_id          UUID NOT NULL REFERENCES bireysel_hesap(id),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    kurye_id            UUID REFERENCES kurye_hesap(id),
    durum               VARCHAR(30) DEFAULT 'olusturuldu',
    -- durum değerleri: olusturuldu, onaylandi, hazirlaniyor, hazir, yolda, teslim_edildi, iptal, iade
    siparis_tutari      DECIMAL(10,2) NOT NULL,
    kurye_ucreti        DECIMAL(10,2),
    komisyon            DECIMAL(10,2),
    toplam_tutar        DECIMAL(10,2) NOT NULL,
    odeme_yontemi       VARCHAR(30) NOT NULL,      -- cuzdan, kredi_karti, kapida_nakit, kapida_kart
    kapida_para_miktar  DECIMAL(10,2),             -- NULL = online ödeme
    teslimat_adresi     TEXT NOT NULL,
    teslimat_notu       TEXT,
    QR_kod              VARCHAR(255),
    QR_kod_suresi       TIMESTAMPTZ,
    olusturma_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    onay_tarihi         TIMESTAMPTZ,
    hazirlama_baslangic TIMESTAMPTZ,
    hazirlama_bitis     TIMESTAMPTZ,
    kurye_teslim_alma  TIMESTAMPTZ,
    teslim_tarihi       TIMESTAMPTZ,
    tahmini_sure        INTEGER,                   -- saniye (dinamik hesaplanan)
    guncel_tahmin       INTEGER,                   -- saniye (anlık güncellenen)
    CONSTRAINT fk_musteri FOREIGN KEY (musteri_id) REFERENCES bireysel_hesap(id),
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id),
    CONSTRAINT fk_kurye FOREIGN KEY (kurye_id) REFERENCES kurye_hesap(id)
);

-- SİPARİŞ ÜRÜNLERİ
CREATE TABLE yemek_siparis_kalem (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    siparis_id          UUID NOT NULL REFERENCES yemek_siparis(id),
    urun_id             UUID NOT NULL REFERENCES yemek_urun(id),
    ad                  VARCHAR(200) NOT NULL,     -- sipariş anındaki ad (fiyat değişse bile)
    birim_fiyat         DECIMAL(10,2) NOT NULL,
    miktar              INTEGER NOT NULL DEFAULT 1,
    toplam_fiyat        DECIMAL(10,2) NOT NULL,
    secilen_opsiyonlar  JSONB,                     -- [{grup: "boyut", secim: "büyük"}, ...]
    CONSTRAINT fk_siparis FOREIGN KEY (siparis_id) REFERENCES yemek_siparis(id),
    CONSTRAINT fk_urun FOREIGN KEY (urun_id) REFERENCES yemek_urun(id)
);

-- PUANLAMA
CREATE TABLE yemek_puan (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    siparis_id          UUID NOT NULL REFERENCES yemek_siparis(id),
    puan_veren          UUID NOT NULL,             -- kullanıcı ID'si
    puan_veren_tip      VARCHAR(20) NOT NULL,      -- musteri, restoran, kurye
    puan_alan           UUID NOT NULL,             -- kullanıcı ID'si
    puan_alan_tip       VARCHAR(20) NOT NULL,      -- musteri, restoran, kurye
    puan                DECIMAL(2,1) NOT NULL,     -- 1.0 - 5.0
    yorum               TEXT,
    kriterler           JSONB,                     -- {lezzeet: 4.5, porsiyon: 4.0, ...}
    olusturma_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_siparis FOREIGN KEY (siparis_id) REFERENCES yemek_siparis(id)
);

-- ZAMAN DAMGALARI (tazelik takibi)
CREATE TABLE yemek_zaman_damgasi (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    siparis_id          UUID NOT NULL REFERENCES yemek_siparis(id),
    urun_id             UUID NOT NULL REFERENCES yemek_urun(id),
    hazirlama_baslangic TIMESTAMPTZ NOT NULL,
    pisirme_tamam       TIMESTAMPTZ,
    paketleme           TIMESTAMPTZ NOT NULL,
    kurye_teslim        TIMESTAMPTZ,
    musteri_teslim      TIMESTAMPTZ,
    toplam_sure         INTEGER,                   -- saniye
    tazelik_derecesi    VARCHAR(20),               -- premium, standart, gec, gecikmis
    CONSTRAINT fk_siparis FOREIGN KEY (siparis_id) REFERENCES yemek_siparis(id),
    CONSTRAINT fk_urun FOREIGN KEY (urun_id) REFERENCES yemek_urun(id)
);

-- SÜRE HESAPLAMA LOG
CREATE TABLE yemek_sure_log (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    siparis_id          UUID NOT NULL REFERENCES yemek_siparis(id),
    tahmini_sure        INTEGER NOT NULL,          -- saniye
    guncel_sure         INTEGER NOT NULL,          -- saniye (anlık)
    trafik_durumu       VARCHAR(30),
    trafik_katsayi      DECIMAL(3,2),
    hava_durumu         VARCHAR(50),
    hava_katsayi        DECIMAL(3,2),
    mesafe              DECIMAL(5,2),              -- km
    hazirlik_suresi     INTEGER,                   -- saniye
    hesaplama_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_siparis FOREIGN KEY (siparis_id) REFERENCES yemek_siparis(id)
);

-- KURYE PROFİL UZANTISI (bireysel_hesap ile 1:1, ayrı kayıt yok)
-- Kullanıcı ana hesabında meslek="kurye" seçince bu kayıt oluşur
CREATE TABLE kurye_profil (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bireysel_hesap_id   UUID NOT NULL UNIQUE REFERENCES bireysel_hesap(id),
    ehliyet_turu        VARCHAR(10),                -- A2, B (NULL ise sadece yaya/bisiklet)
    sigorta_no          VARCHAR(50),
    saglik_raporu       TEXT,
    termal_canta_var    BOOLEAN DEFAULT false,
    deneme_siparis      INTEGER DEFAULT 0,
    mentor_kurye_id     UUID REFERENCES kurye_profil(id),
    olusturma_tarihi    TIMESTAMPTZ DEFAULT NOW(),
    uygunluk_durumu     VARCHAR(20) DEFAULT 'musait', -- musait, sipariste, donuste, mola, kapali
    mola_bitis          TIMESTAMPTZ,                -- NULL=molada değil
    son_konum           GEOGRAPHY(POINT),
    son_konum_guncelleme TIMESTAMPTZ,
    calisma_baslangic   TIMESTAMPTZ,                -- bugün ilk ne zaman çevrimiçi oldu
    bugun_siparis_sayisi INTEGER DEFAULT 0,
    bugun_kazanc        DECIMAL(10,2) DEFAULT 0,
    CONSTRAINT fk_bireysel FOREIGN KEY (bireysel_hesap_id) REFERENCES bireysel_hesap(id)
);

-- RESTORAN ÇALIŞANLARI (kurumsal panel kullanıcıları)
CREATE TABLE yemek_calisan (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    bireysel_hesap_id   UUID NOT NULL REFERENCES bireysel_hesap(id),
    rol                 VARCHAR(30) NOT NULL,      -- sahip, mudur, sef, fotografci, gozlemci
    aktif               BOOLEAN DEFAULT true,
    atama_tarihi        TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id),
    CONSTRAINT fk_bireysel FOREIGN KEY (bireysel_hesap_id) REFERENCES bireysel_hesap(id)
);

-- RESTORAN MÜŞTERİ HİZMETLERİ LOG
CREATE TABLE yemek_musteri_hizmet (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restoran_id         UUID NOT NULL REFERENCES yemek_restoran(id),
    musteri_id          UUID REFERENCES bireysel_hesap(id),
    siparis_id          UUID REFERENCES yemek_siparis(id),
    kanal               VARCHAR(30),               -- telefon, whatsapp, platform
    kayit_dosyasi       TEXT,
    baslama_zamani      TIMESTAMPTZ DEFAULT NOW(),
    bitis_zamani        TIMESTAMPTZ,
    cozum_durumu        VARCHAR(30),               -- beklemede, cozuldu, platforma_devredildi
    CONSTRAINT fk_restoran FOREIGN KEY (restoran_id) REFERENCES yemek_restoran(id),
    CONSTRAINT fk_musteri FOREIGN KEY (musteri_id) REFERENCES bireysel_hesap(id),
    CONSTRAINT fk_siparis FOREIGN KEY (siparis_id) REFERENCES yemek_siparis(id)
);

-- İNDEKS
CREATE INDEX idx_siparis_durum ON yemek_siparis(durum);
CREATE INDEX idx_siparis_musteri ON yemek_siparis(musteri_id);
CREATE INDEX idx_siparis_restoran ON yemek_siparis(restoran_id);
CREATE INDEX idx_siparis_tarih ON yemek_siparis(olusturma_tarihi);
CREATE INDEX idx_urun_restoran ON yemek_urun(restoran_id);
CREATE INDEX idx_goruntu_restoran ON yemek_restoran_goruntu(restoran_id);
CREATE INDEX idx_puan_siparis ON yemek_puan(siparis_id);
CREATE INDEX idx_kurye_konum ON kurye_hesap USING GIST(son_konum);
CREATE INDEX idx_restoran_konum ON yemek_restoran USING GIST(konum);
```

### 18.2 İlişki Diyagramı (Metin)

```
yemek_restoran ──1:N── yemek_restoran_belge
yemek_restoran ──1:N── yemek_restoran_goruntu
yemek_restoran ──1:N── yemek_kamera
yemek_restoran ──1:N── yemek_kategori
yemek_restoran ──1:N── yemek_urun
yemek_restoran ──1:N── yemek_siparis
yemek_restoran ──1:N── yemek_calisan
yemek_kategori ──1:N── yemek_urun
yemek_urun ──1:N── yemek_urun_opsiyon_grubu
yemek_urun_opsiyon_grubu ──1:N── yemek_urun_opsiyon
yemek_urun ──1:N── yemek_siparis_kalem
yemek_urun ──1:N── yemek_zaman_damgasi
yemek_siparis ──1:N── yemek_siparis_kalem
yemek_siparis ──1:N── yemek_puan
yemek_siparis ──1:N── yemek_zaman_damgasi
yemek_siparis ──1:N── yemek_sure_log
yemek_siparis ──1:N── yemek_musteri_hizmet
bireysel_hesap ──1:N── yemek_puan (puan_veren/puan_alan)
bireysel_hesap ──1:1── kurye_profil
kurye_profil ──1:N── yemek_siparis (kurye_id ile)
```

---

## 19. API ENDPOINT'LERİ

### 19.1 Restoran Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/restoran` | Yeni restoran kaydı |
| GET | `/api/v1/yemek/restoran/{id}` | Restoran detayı |
| PUT | `/api/v1/yemek/restoran/{id}` | Restoran güncelleme |
| DELETE | `/api/v1/yemek/restoran/{id}` | Restoran silme (pasif) |
| GET | `/api/v1/yemek/restoran/ara` | Restoran ara (filtreli) |
| GET | `/api/v1/yemek/restoran/yakin` | Yakındaki restoranlar (konum bazlı) |
| PUT | `/api/v1/yemek/restoran/{id}/calisma-saatleri` | Çalışma saatlerini güncelle |
| PUT | `/api/v1/yemek/restoran/{id}/servis-bolgesi` | Servis bölgesi güncelle |

### 19.2 Belge Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/restoran/{id}/belge` | Belge yükle |
| GET | `/api/v1/yemek/restoran/{id}/belgeler` | Belgeleri listele |
| GET | `/api/v1/yemek/restoran/{id}/belge/{belge_id}` | Belge detayı |
| DELETE | `/api/v1/yemek/restoran/{id}/belge/{belge_id}` | Belge sil |
| POST | `/api/v1/yemek/belge/dogrula/{belge_id}` | Belge doğrulama başlat |
| GET | `/api/v1/yemek/restoran/{id}/puan/evrak` | Evrak bazlı puan durumu |

### 19.3 Görsel Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/restoran/{id}/goruntu` | Görsel yükle |
| GET | `/api/v1/yemek/restoran/{id}/goruntuler` | Görselleri listele (kategori bazlı) |
| DELETE | `/api/v1/yemek/restoran/{id}/goruntu/{goruntu_id}` | Görsel sil |
| PUT | `/api/v1/yemek/restoran/{id}/goruntu/{goruntu_id}` | Görsel güncelle |
| GET | `/api/v1/yemek/restoran/{id}/goruntu/durum` | Zorunlu görsel durumu |

### 19.4 Kamera Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/restoran/{id}/kamera` | Kamera ekle |
| GET | `/api/v1/yemek/restoran/{id}/kameralar` | Kameraları listele |
| PUT | `/api/v1/yemek/restoran/{id}/kamera/{kamera_id}` | Kamera güncelle |
| DELETE | `/api/v1/yemek/restoran/{id}/kamera/{kamera_id}` | Kamera sil |
| GET | `/api/v1/yemek/restoran/{id}/kamera/{kamera_id}/yayin` | Canlı yayın URL'i |
| POST | `/api/v1/yemek/restoran/{id}/kamera/{kamera_id}/baslat` | Yayın başlat |
| POST | `/api/v1/yemek/restoran/{id}/kamera/{kamera_id}/durdur` | Yayın durdur |

### 19.5 Menü Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/restoran/{id}/kategori` | Kategori ekle |
| GET | `/api/v1/yemek/restoran/{id}/kategoriler` | Kategorileri listele |
| PUT | `/api/v1/yemek/restoran/{id}/kategori/{kat_id}` | Kategori güncelle |
| DELETE | `/api/v1/yemek/restoran/{id}/kategori/{kat_id}` | Kategori sil |
| POST | `/api/v1/yemek/restoran/{id}/urun` | Ürün ekle |
| PUT | `/api/v1/yemek/restoran/{id}/urun/{urun_id}` | Ürün güncelle |
| DELETE | `/api/v1/yemek/restoran/{id}/urun/{urun_id}` | Ürün sil |
| GET | `/api/v1/yemek/restoran/{id}/menu` | Tam menü getir (kategorili) |
| PUT | `/api/v1/yemek/restoran/{id}/urun/{urun_id}/stok` | Stok güncelle |
| POST | `/api/v1/yemek/restoran/{id}/urun/{urun_id}/opsiyon-grubu` | Opsiyon grubu ekle |
| POST | `/api/v1/yemek/urun/{urun_id}/opsiyon` | Opsiyon ekle |

### 19.6 Sipariş Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/siparis` | Sipariş oluştur |
| GET | `/api/v1/yemek/siparis/{id}` | Sipariş detayı |
| GET | `/api/v1/yemek/siparislerim` | Müşterinin siparişleri |
| GET | `/api/v1/yemek/restoran/{id}/siparisler` | Restoran siparişleri |
| PUT | `/api/v1/yemek/siparis/{id}/onay` | Sipariş onayla (restoran) |
| PUT | `/api/v1/yemek/siparis/{id}/red` | Sipariş reddet (restoran) |
| PUT | `/api/v1/yemek/siparis/{id}/iptal` | Sipariş iptal (müşteri) |
| PUT | `/api/v1/yemek/siparis/{id}/hazir` | Hazır bildirimi |
| PUT | `/api/v1/yemek/siparis/{id}/yola-cik` | Kurye yola çıktı |
| PUT | `/api/v1/yemek/siparis/{id}/teslim-et` | QR ile teslim et |
| POST | `/api/v1/yemek/siparis/{id}/qr-dogrula` | QR kod doğrula |
| GET | `/api/v1/yemek/siparis/{id}/canli-takip` | Canlı takip verisi |

### 19.7 Süre Hesaplama

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/sure/tahmin` | Süre tahmini hesapla |
| GET | `/api/v1/yemek/sure/hava-durumu` | Anlık hava durumu (konum bazlı) |
| GET | `/api/v1/yemek/sure/trafik-durumu` | Anlık trafik durumu |
| GET | `/api/v1/yemek/siparis/{id}/sure-log` | Süre hesaplama geçmişi |

### 19.8 Puanlama

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/siparis/{id}/puan` | Puan ver |
| GET | `/api/v1/yemek/restoran/{id}/puan` | Restoran puan detayı |
| GET | `/api/v1/yemek/kurye/{id}/puan` | Kurye puan detayı |
| GET | `/api/v1/yemek/musteri/{id}/puan` | Müşteri puan detayı |
| GET | `/api/v1/yemek/restoran/siralama` | Restoran sıralaması |

### 19.9 Kurye Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/kurye/kayit` | Kurye kaydı |
| GET | `/api/v1/yemek/kurye/{id}` | Kurye detayı |
| PUT | `/api/v1/yemek/kurye/{id}/konum` | Konum güncelle |
| PUT | `/api/v1/yemek/kurye/{id}/durum` | Müsaitlik durumu güncelle |
| GET | `/api/v1/yemek/kurye/yakindaki-siparisler` | Yakındaki siparişler |
| POST | `/api/v1/yemek/siparis/{id}/kurye-ata` | Kurye ata |
| POST | `/api/v1/yemek/kurye/{id}/mobing-bildirim` | Mobing bildirimi |

### 19.10 Ödeme

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/odeme/kapida-bildirim` | Kapıda ödeme bildirimi |
| GET | `/api/v1/yemek/cuzdan/bakiye` | Cüzdan bakiyesi |
| POST | `/api/v1/yemek/cuzdan/para-yukle` | Para yükle |
| POST | `/api/v1/yemek/cuzdan/para-cek` | Para çek (restoran/kurye) |

### 19.11 Müşteri Hizmetleri

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/yemek/musteri-hizmet/kayit` | Görüşme kaydı başlat |
| PUT | `/api/v1/yemek/musteri-hizmet/{id}/cozum` | Çözüm bildir |
| POST | `/api/v1/yemek/musteri-hizmet/platforma-devret` | Platforma devret |

---

## 20. AKIŞ DİYAGRAMLARI

### 20.1 Restoran Kayıt ve Aktivasyon

```
MÜŞTERİ: KURUMSAL HESAP AÇAR
         │
         ▼
RESTORAN: TEMEL BİLGİLERİ GİRER
         │
         ▼
RESTORAN: ZORUNLU BELGELERİ YÜKLER (vergi, ruhsat, hijyen...)
         │
         ▼
SİSTEM: BELGELERİ OTOMATİK DOĞRULAR (AI + OCR)
         │
         ├── Başarılı ──► AŞAMA 2: MANUEL KONTROL
         │                    │
         │                    ├── Onay ──► RESTORAN AKTİF
         │                    │              │
         │                    │              ▼
         │                    │         ZORUNLU GÖRSELLERİ
         │                    │         YÜKLEMESİ İSTENİR
         │                    │              │
         │                    │              ▼
         │                    │         6+ GÖRSEL TAMAM MI?
         │                    │              │
         │                    │         ├── Evet ──► PROFİL AKTİF
         │                    │         └── Hayır ──► SINIRLI MOD
         │                    │
         │                    └── Red ──► NEDEN BELİRTİLİR
         │                                  │
         │                                  7 GÜN SONRA
         │                                  TEKRAR BAŞVURU
         │
         └── Başarısız ──► 24 SAAT İÇİNDE
                           YENİDEN YÜKLEME HAKKI
```

### 20.2 Sipariş Oluşturma ve Teslimat

```
MÜŞTERİ: RESTORAN SEÇER
         │
         ├── Sıralama: Puan (4.5+ üstte)
         ├── Canlı kamera varsa +100 puan
         ├── Teslimat süresi gösterilir (dinamik)
         └── Menüye göz atar
         │
         ▼
MÜŞTERİ: SEPETİ OLUŞTURUR
         │
         ├── Ürün ekler (+ opsiyonlar)
         ├── Teslimat adresi girer
         └── Ödeme yöntemi seçer
         │
         ▼
MÜŞTERİ: SİPARİŞİ ONAYLAR
         │
         ▼
SİSTEM: DİNAMİK SÜRE HESAPLAR
         │
         ├── Hava durumu (Meteoroloji API)
         ├── Trafik durumu (Google Traffic)
         ├── Mesafe hesaplama
         ├── Restoran hazırlık süresi (geçmiş)
         └── Tahmini süre gösterilir
         │
         ▼
SİSTEM: SİPARİŞİ RESTORANA İLETİR
         │
         ▼
RESTORAN: 2 DAKİKA İÇİNDE ONAYLAR
         │
         ├── Onay ──► HAZIRLIK BAŞLAR
         │              │
         │              ▼
         │         SİSTEM: UYGUN KURYE ATA
         │              │
         │              ├── Puan (4.5+)
         │              ├── Mesafe (yakın)
         │              └── Müsaitlik (uygun)
         │              │
         │              ▼
         │         KURYE: RESTORANA GİDER
         │              │
         │              ▼
         │         RESTORAN: PAKETİ TESLİM EDER
         │              │
         │              ▼
         │         SİSTEM: ZAMAN DAMGASI (paketleme)
         │              │
         │              ▼
         │         KURYE: MÜŞTERİYE GİDER
         │              │
         │              ├── Canlı takip (müşteri)
         │              ├── Hava/trafik bildirimi
         │              └── Güncel süre gösterimi
         │              │
         │              ▼
         │         VARış: QR KOD OKUTMA
         │              │
         │              ├── Başarılı ──► TESLİM
         │              │                  │
         │              │                  ▼
         │              │             PUANLAMA EKRANI
         │              │                  │
         │              │                  ▼
         │              │             SİPARİŞ TAMAM
         │              │
         │              └── Başarısız ──► SMS KODU
         │                                    │
         │                                    ├── 3 deneme
         │                                    └── Başarısız ──► DESTEK
         │
         └── Red ──► İPTAL (+ neden)
                      │
                      ▼
                 MÜŞTERİYE BİLDİRİM
```

### 20.3 Kapıda Ödeme Akışı

```
MÜŞTERİ: KAPIDA NAKİT SEÇER
         │
         ▼
SİSTEM: PARA BİLDİRİMİ İSTER
         │
         ├── Sipariş tutarı: 120 ₺
         ├── Müşteri bildirir: 150 ₺ (120+30 bozuk)
         └── Maks: 240 ₺ (sipariş × 2)
         │
         ▼
MÜŞTERİ: ONAYLAR
         │
         ▼
SİSTEM: CÜZDANDAN BLOKE EDER (150 ₺)
         │
         ▼
KURYE: "MÜŞTERİ 150 ₺ HAZIRLADI" BİLGİSİ
         │
         ▼
KURYE: TESLİM ANI --- MÜŞTERİ PARAYI UZATIR
         │
         ├── Miktar doğru ──► KURYE ONAYLAR
         │                       │
         │                       ├── Bloke çözülür
         │                       ├── Tutar kurye cüzdanına
         │                       └── Sipariş tamam
         │
         ├── Miktar eksik ──► KURYE REDDEDER
         │                       │
         │                       └── Müşteri tamamlamalı
         │
         └── Miktar fazla ──► SİSTEM İADE EDER
                             │
                             └── Fark cüzdana iade
```

---

> 📝 **Not:** Bu doküman, TAKSI-SYSTEM-DESIGN.md ile aynı formatta hazırlanmıştır. Yemek sistemi, taksi altyapısındaki cüzdan, puanlama, canlı takip ve harita sistemlerini ortak kullanır. Yeni modüller eklendikçe doküman güncellenecektir.
