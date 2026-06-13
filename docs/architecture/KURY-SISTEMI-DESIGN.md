# 🚲 PLATFORM KURYE SİSTEMİ - BAĞIMSIZ TESLİMAT HAVUZU

---

## 📋 İÇİNDEKİLER

1. [Sistem Felsefesi](#1-sistem-felsefesi)
2. [Kurye Kaydı ve Zorunlu Belgeler](#2-kurye-kaydı-ve-zorunlu-belgeler)
3. [Kurye Durum Makinesi](#3-kurye-durum-makinesi)
4. [Çoklu Servis Yönlendirme (Yemek + Çiçek + Diğer)](#4-çoklu-servis-yönlendirme)
5. [Sipariş Anında Kurye Sorgulama](#5-sipariş-anında-kurye-sorgulama)
6. [Atama Algoritması ve Önceliklendirme](#6-atama-algoritması-ve-önceliklendirme)
7. [Çoklu Sipariş ve Zincirleme Teslimat](#7-çoklu-sipariş-ve-zincirleme-teslimat)
8. [Zaman Uyumsuzluğu Yönetimi](#8-zaman-uyumsuzluğu-yönetimi)
9. [Mola Yönetimi](#9-mola-yönetimi)
10. [Özel Teslimat Türleri](#10-özel-teslimat-türleri)
11. [Kurye Puanlama ve Ödül Sistemi](#11-kurye-puanlama-ve-ödül-sistemi)
12. [Ücretlendirme ve Ödeme](#12-ücretlendirme-ve-ödeme)
13. [Mobing Önleme ve Güvenlik](#13-mobing-önleme-ve-güvenlik)
14. [Kurye Mobil Uygulaması](#14-kurye-mobil-uygulaması)
15. [DB Şeması](#15-db-şeması)
16. [API Endpoint'leri](#16-api-endpointleri)

---

## 1. SİSTEM FELSEFESİ

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   BAĞIMSIZ KURYE HAVUZU — TEK HAVUZ, TÜM SERVİSLER             ║
║                                                                  ║
║   Kurye sistemi, platformdaki HİÇBİR servise bağlı değildir.   ║
║   Tek bir kurye havuzu, tüm servislere hizmet verir.            ║
║                                                                  ║
║   SERVİSLER:                                                     ║
║   🍽️ Yemek · 💐 Çiçek · 🚕 Taksi (opsiyonel)                 ║
║   📦 Paket · 🛒 Market · ve gelecekteki tüm modüller           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### 1.1 Temel İlkeler

```
🔑 İLKELER:
├── 1️⃣ Kurye bağımsızdır, hiçbir servise özel değildir
├── 2️⃣ Her kurye her servisten teslimat alabilir
├── 3️⃣ Teslimat türüne göre farklı ücretlendirme (çiçek=özen, yemek=hız)
├── 4️⃣ Kurye kendi tercihini yapar (servis bazlı kabul/red)
├── 5️⃣ Platform optimum dağıtımı yapar (yönlendirir, zorlamaz)
├── 6️⃣ Tüm servisler aynı kurye havuzundan beslenir
└── 7️⃣ Kurye müsaitlik durumunu kendi belirler
```

---

## 2. KURYE KAYDI VE ZORUNLU BELGELER

### 2.1 Ön Koşul

Her kurye öncelikle **Bireysel Hesap** açmak zorundadır. Bireysel hesap olmadan kurye kaydı yapılamaz.

### 2.2 Zorunlu Belgeler

| Belge | Açıklama | Geçerlilik Süresi |
|-------|----------|-------------------|
| **Kimlik** | TC Kimlik / Yabancı Kimlik | Süresiz |
| **Ehliyet** | En az Sınıf A1 (motosiklet) veya B (araba) | 10 yıl |
| **Adli Sicil Kaydı** | Temiz sabıka kaydı | 3 ay |
| **İkametgah Belgesi** | Adres teyidi | 1 yıl |
| **Vergi Mükellefiyeti** | Şahıs şirketi veya esnaf muafiyeti | 1 yıl |
| **SGK Kaydı** | İsteğe bağlı veya aktif sigorta | Süresiz |
| **Psikoteknik Raporu** | Psikolojik ve fiziksel yeterlilik | 2 yıl |
| **Termal Çanta Belgesi** | Varsa hijyen uygunluk | Yıllık |
| **Araç Ruhsatı** (araçlı kurye) | Ticari/Amatör | Yıllık |

### 2.3 Kurye Profil Fotoğrafları

```
FOTOĞRAF ŞARTLARI:
├── 1️⃣ ÖN (Yüz): Net, aydınlık, gözler ve yüz tam görünür
├── 2️⃣ ARKA: Sırt dönük, başın arkası görünür
├── 3️⃣ SOL YAN: Sol profilden çekilmiş, yüzün sol yanı görünür
│
└── Kurallar:
    ├── Arka fon düz (beyaz/açık renk)
    ├── Güneş gözlüğü, maske, aksesuar yasak (net yüz)
    ├── Son 6 ay içinde çekilmiş olmalı
    ├── Minimum 1920x1080 çözünürlük
    └── Biyometrik doğrulama (canlı fotoğraf çekimi)
```

### 2.4 Kurye Türleri

```
KURYE TÜRLERİ:
├── 🚲 Motosikletli Kurye (en yaygın, şehir içi)
│   ├── Hızlı, dar sokaklara girebilir
│   ├── Kapasite: 1-2 sipariş (çanta)
│   └── Uygun: Yemek, küçük çiçek, küçük paket
│
├── 🚗 Arabalı Kurye (geniş hacim)
│   ├── Yavaş ama büyük kapasite
│   ├── Soğutmalı bölme opsiyonel
│   └── Uygun: Büyük çiçek aranjmanı, çoklu sipariş
│
├── 🚶 Yaya Kurye (kısa mesafe)
│   ├── Maksimum 1 km yarıçap
│   ├── Kapasite: 1 sipariş
│   └── Uygun: Yakın mesafe yemek
│
├── 🚲 Bisikletli Kurye (çevreci)
│   ├── Orta hız, çevre dostu
│   └── Uygun: Kısa-orta mesafe
│
└── 🚐 Minibüs/Kamyonet (toplu teslimat)
    ├── Büyük hacimli organizasyon
    ├── Kapasite: 10+ sipariş
    └── Uygun: Kurumsal, düğün, organizasyon
```

### 2.5 Teslimat Yetenekleri (Kurye Bazında)

Her kurye hangi teslimat türlerini kabul ettiğini belirler:

```
KURYE YETENEKLERİ:
├── 🍽️ Yemek teslimatı: ✅ / ❌
│   └── Termal çanta var mı? ✅ / ❌
├── 💐 Çiçek teslimatı: ✅ / ❌
│   └── Hassas kargo ekipmanı var mı? ✅ / ❌
├── 📦 Paket teslimatı: ✅ / ❌
├── 🛒 Market teslimatı: ✅ / ❌
├── 🚕 Yolcu taşıma: ✅ / ❌ (taksi ruhsatı gerekli)
│
├── Maksimum paket boyutu: [küçük / orta / büyük]
├── Maksimum ağırlık: [kg]
└── Vardiya tercihi: [sabah / öğle / akşam / gece]
```

---

## 3. KURYE DURUM MAKİNESİ

```
                    ┌──────────────┐
                    │  ÇEVRİMDIŞI  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ÇEVRİMİÇİ   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼             ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  MÜSAİT  │ │ SİPARİŞTE│ │  PLANLI  │
        │bekliyor  │ │teslimde  │ │ rezerve  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             │            ▼            │
             │      ┌──────────┐       │
             │      │ DÖNÜŞTE  │       │
             │      │boşalıyor │       │
             │      └────┬─────┘       │
             │           │             │
             └───────────┴─────────────┘
                         │
                         ▼
                   ┌──────────┐
                   │   MOLA   │
                   └────┬─────┘
                        │
                        ▼
                   ┌──────────┐
                   │ÇEVRİMDIŞI│
                   └──────────┘
```

| Durum | Açıklama | Sistem Aksiyonu |
|-------|----------|-----------------|
| **Çevrimdışı** | Online değil, sipariş alamaz | Yok sayılır |
| **Çevrimiçi** | Sisteme bağlı, durum seçmemiş | Havuza ekle |
| **Müsait** | Beklemede, hemen çıkabilir | Tüm servisler için kullanılabilir |
| **Planlı/Rezerve** | X dk sonra müsait olacak | Gelecek siparişe ata |
| **Siparişte** | Teslimat yapıyor | Servis türü görünür |
| **Dönüşte** | Merkeze/müsait bölgeye dönüyor | Dönüş bitince müsait yap |
| **Mola** | "X dk sonra dönerim" | Süre bitince müsait yap |

---

## 4. ÇOKLU SERVİS YÖNLENDİRME

### 4.1 Kurye Ana Ekranı

Kurye, mobil uygulamasında tüm servislerden gelen teslimat taleplerini tek ekranda görür:

```
┌─────────────────────────────────────────────┐
│  09:41                          🔋 85%     │
│                                              │
│  🟢 MÜSAİT · Bugün 8 teslimat               │
│  💰 Bugün: 240₺ · Bu hafta: 1.240₺          │
├─────────────────────────────────────────────┤
│                                              │
│  🔔 GELEN TESLİMATLAR                        │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 🍽️ YEMEK · 4.2km · 25₺                 │ │
│  │  Kebapçı Mehmet → Moda Cd.              │ │
│  │  Hazırlık: 15 dk · Kurye: 5 dk         │ │
│  │  [ ✅ Kabul ]  [ ❌ Red ]               │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 💐 ÇİÇEK · 3.5km · 30₺ ⚠️ HASSAS      │ │
│  │  Gül Bahçesi → Fenerbahçe              │ │
│  │  Hazırlık: 25 dk · Kurye: 8 dk         │ │
│  │  [ ✅ Kabul ]  [ ❌ Red ]               │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 📦 MARKET · 2.8km · 20₺                │ │
│  │  Migros → Erenköy                      │ │
│  │  Hazırlık: 10 dk · Kurye: 4 dk         │ │
│  │  [ ✅ Kabul ]  [ ❌ Red ]               │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ─── DİĞER (2) ───                          │
│                                              │
│  [ 📋 Tümünü Gör ]                          │
└─────────────────────────────────────────────┘
```

### 4.2 Yönlendirme Kuralları

```
SİSTEM YÖNLENDİRME ÖNCELİKLERİ:
├── Kuryeye en yakın teslimat noktası
├── Servis bazlı: 🍽️ Yemek → hız öncelikli
│   └── Çiçek → özen/hassasiyet öncelikli
├── Kuryenin yetenekleri (çiçek ekipmanı var mı?)
├── Kurye puanı (yüksek puanlı kuryeye öncelik)
├── Teslimat süresi aciliyeti
└── Kurye geçmişi (hangi serviste daha başarılı?)
```

### 4.3 Kabul/Red Hakkı

```
KURYE KABUL/RED KURALLARI:
├── Kurye her teslimatı kabul veya red edebilir
├── Kabul → sipariş kuryeye atanır
├── Red → başka kuryeye yönlendirilir
├── Ret sebebi girilir (opsiyonel):
│   ├── Çok uzak
│   ├── Hassas taşıma ekipmanım yok
│   ├── O bölgeye gitmiyorum
│   └── Şu an müsait değilim
├── Sık red (%30+): Sistem önceliği düşürür
├── Sürekli red (%50+): Uyarı + puan kırılımı
└── Acil durum red (hastalık, kaza): Ceza yok
```

### 4.4 Servis Bazlı Kurye Tercihi

Kurye, hangi servislerden teslimat almak istediğini profilden belirler:

```
SERVİS TERCIHİ:
┌──────────────────────────────────┐
│  Kurye: Mehmet Yılmaz            │
│                                  │
│  Hangi servislerden teslimat     │
│  almak istersiniz?               │
│                                  │
│  ☑ 🍽️ Yemek (termal çantam var) │
│  ☑ 💐 Çiçek (hassas taşıma yap) │
│  ☐ 📦 Market                     │
│  ☐ 🚕 Yolcu Taşıma               │
│                                  │
│  Öncelikli servis: 🍽️ Yemek    │
│  (yüksek öncelikli servise       │
│   önce yönlendirilirsin)         │
│                                  │
│  [ 💾 Kaydet ]                   │
└──────────────────────────────────┘
```

---

## 5. SİPARİŞ ANINDA KURYE SORGULAMA

Müşteri siparişi **vermeden önce** sistem kurye durumunu sorgular:

```
MÜŞTERİ: SİPARİŞ ONAYLAMA EKRANINDA
         │
         ▼
SİSTEM: TÜM SERVİSLERDE KURYE TARAMASI
         │
         ├── Bölgedeki tüm müsait kuryeler
         │   ├── 🚲 Motosiklet (yemek/çiçek uygun)
         │   ├── 🚗 Araba (çiçek uygun + büyük boy)
         │   └── 🚶 Yaya (sadece yemek, yakın)
         │
         ├── Her kuryenin servis yeteneği kontrolü
         │   ├── Çiçek teslimatı: Hassas kargo uygun mu?
         │   ├── Yemek teslimatı: Termal çanta var mı?
         │   └── Boyut/ağırlık uygun mu?
         │
         ├── En uygun kurye seçilir
         │
         └── Müşteriye süre gösterilir
```

### 5.1 Kurye Bulunamazsa

```
KURYE BULUNAMADI:
├── Bölgede hiç müsait kurye yok
├── Müsait kuryeler var ama yetenek uyuşmazlığı
│   ├── Örn: Çiçek siparişi → sadece yemek kuryeleri var
│   └── Örn: Büyük boy çiçek → sadece motosiklet kuryeleri var
│
├── Sistem müşteriye bildirir:
│   ├── "⚠️ Şu an bölgenizde uygun kurye bulunamadı"
│   ├── "🕐 Tahmini bekleme: 30+ dakika (başka bölgeden gelecek)"
│   └── Alternatif:
│       ├── "Yine de sipariş ver" (bekleme listesi)
│       ├── "Planlı sipariş" (ileri bir saat seç)
│       └── "Vazgeç"
│
└── Yakın bölgeden kurye çağrılır (+ek ücret: 5-10₺)
```

---

## 6. ATAMA ALGORİTMASI VE ÖNCELİKLENDİRME

### 6.1 Puanlama Formülü

```
KURY_E PUANI = (MSF × 30) + (HIZ × 25) + (YET × 20) + (PUAN × 15) + (YUK × 10)

├── MSF = Mesafe Faktörü (kurye → işletme, km) — 0-100 arası
│   ├── 0-1 km: 100 puan
│   ├── 1-3 km: 75 puan
│   ├── 3-5 km: 50 puan
│   └── 5+ km:  25 puan
│
├── HIZ = Hazırlık Uyumu (kurye varışı, hazırlık zamanına uyuyor mu?)
│   ├── Tam uyum: 100 puan (kurye gelince hazır)
│   ├── ±5 dk:   75 puan
│   ├── ±10 dk:  50 puan
│   └── ±15+ dk: 25 puan
│
├── YET = Yetenek Uyumu (kuryenin bu teslimat türü için uygunluğu)
│   ├── Tam uygun + özel ekipman: 100 puan
│   ├── Uygun: 75 puan
│   ├── Kısmen uygun: 50 puan
│   └── Uygun değil: 0 puan (elenir)
│
├── PUAN = Kurye Puanı (müşteri ve işletme puanları ortalaması)
│   ├── 4.8+:  100 puan
│   ├── 4.5-4.7: 80 puan
│   ├── 4.0-4.4: 60 puan
│   └── 4.0-:    40 puan
│
└── YUK = Yük Faktörü (bölgedeki kurye yoğunluğu)
    ├── Çok kurye var: 100 puan (seçme şansı)
    ├── Normal: 75 puan
    ├── Az kurye: 50 puan
    └── Kritik: 25 puan (bulunanı ata)
```

### 6.2 Atama Karar Tablosu

| Durum | Karar | Müşteriye Gösterilen Süre |
|-------|-------|--------------------------|
| Kurye müsait, yetenek uygun, yakın | Doğrudan ata | Hazırlık + yol süresi |
| Kurye müsait ama yetenek uymaz | Başka kurye ara | Alternatif kurye süresi |
| Kurye meşgul, başkası var | Alternatif kurye ata | Alternatif kurye süresi |
| Kurye meşgul, alternatif yok, geciktirilebilir | Hazırlığı geciktir | Kurye varış süresi |
| Kurye meşgul, alternatif yok, geciktirilemez | İşletme bekle + kuryeyi bekle | Toplam süre (en kötü) |
| Hiç uygun kurye yok | Sipariş alınmaz | Bilgilendirme + alternatif |
| Kurye var ama servis tercihi kapalı | Servis açık kurye ara | - |

### 6.3 Atama Öncelik Sırası

```
1. ÖNCELİK: Yemek siparişleri (soğuma riski)
   ├── Sıcak yemek: +30 dk içinde teslim
   └── Soğuk/hızlı bozulur: Öncelikli

2. ÖNCELİK: Çiçek siparişleri (hassasiyet)
   ├── Hassas taşıma gerekli
   └── Belirli saatte teslim (özel gün)

3. ÖNCELİK: Market/Paket (esnek)
   └── Zaman daha esnek

4. ÖNCELİK: Planlı/Ön sipariş (en esnek)
   └── Saat bellidir, hazırlık önceden yapılır
```

---

## 7. ÇOKLU SİPARİŞ VE ZİNCİRLEME TESLİMAT

### 7.1 Aynı Anda Birden Çok Sipariş

Kurye, kapasitesi elverdiğince aynı anda birden çok sipariş taşıyabilir:

```
KAPASİTE YÖNETİMİ:
├── 🚲 Motosiklet: Maks 2 sipariş (çanta büyüklüğüne göre)
│   ├── 2 yemek (çantada üst üste)
│   ├── 1 büyük çiçek + 1 küçük yemek
│   └── 1 büyük çiçek (tek, hassas)
│
├── 🚗 Araba: Maks 5-10 sipariş (rota optimizasyonu)
│   ├── Çoklu yemek (termal bölmeli)
│   ├── Çoklu çiçek (sabit bölmeli)
│   └── Karışık (yemek + çiçek ayrı bölmelerde)
│
└── 🚶 Yaya/Bisiklet: Maks 1 sipariş
```

### 7.2 Zincirleme Teslimat (Kurye Meşgulken Yeni Sipariş)

Kurye bir teslimattayken yakındaki başka bir teslimat da kendisine atanabilir:

```
ZİNCİRLEME AKIŞI:
├── Kurye A, Teslimat 1'i yapıyor (Müşteri A'ya gidiyor)
├── Teslimat 2 geliyor (Müşteri B, A'ya yakın)
│
├── SİSTEM KONTROL EDER:
│   ├── Kurye A'nın rotası Müşteri B'ye uygun mu?
│   ├── Teslimat 2'nin hazır olma zamanı
│   └── Kurye A'nın kapasitesi var mı?
│
├── UYGUNSA:
│   ├── Kurye A'ya bildirim: "Yolda ek teslimat"
│   ├── Kurye A: Kabul/Red
│   └── Kabul → Teslimat 1'i bitir → Teslimat 2'ye git
│
└── DEĞİLSE:
    ├── Başka kurye ata
    └── Bekleme listesine ekle
```

### 7.3 Rota Optimizasyonu

```
ÇOKLU SİPARİŞ ROTA:
├── Başlangıç: Kurye konumu
├── Durak 1: İşletme A (yemek al)
├── Durak 2: Müşteri A (teslim et)
├── Durak 3: İşletme B (çiçek al)
├── Durak 4: Müşteri B (teslim et)
│
├── TOPLAM SÜRE: 45 dk
├── KAZANÇ: 25₺ + 30₺ = 55₺
├── YAKIT: 8₺
├── NET: 47₺ (tek siparişten ~%40 daha karlı)
└── Sistem en kısa rotayı otomatik hesaplar
```

---

## 8. ZAMAN UYUMSUZLUĞU YÖNETİMİ

### 8.1 İşletme Hazır Değilse

```
SENARYO: Kurye işletmeye vardı, sipariş henüz hazır değil
├── Kurye bekler (maks 5 dk)
├── 5 dk geçerse → kuryeye bekleme ücreti (2₺/dk)
├── 10 dk geçerse → kurye iptal edebilir
└── 15 dk geçerse → işletmeye ceza (-0.5 puan)
```

### 8.2 Kurye Gecikirse

```
SENARYO: Kurye yolda gecikti (trafik, hava)
├── 5 dk gecikme: Müşteriye bildirim + özür
├── 10 dk gecikme: Müşteriye yeni tahmini süre
├── 15+ dk gecikme: Müşteri iptal edebilir
└── Tazminat: Müşteriye 10₺ kupon (sistem karşılar)
```

### 8.3 Hazırlık Gecikirse (İşletme Kaynaklı)

```
SENARYO: İşletme hazırlık süresini aştı
├── Kurye beklemeye devam eder
├── Bekleme ücreti işletmeden kesilir
├── Müşteriye güncellenmiş süre gönderilir
└── İşletme ceza puanı (-0.3)
```

---

## 9. MOLA YÖNETİMİ

### 9.1 Mola Bildirimi

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
║   🍽️ Yemek kapalı        ║
║   💐 Çiçek kapalı         ║
║   📦 Market kapalı        ║
║                           ║
║   [ ✅ MOLA BAŞLA ]      ║
║   [ 🔄 Hazırım / İptal ] ║
╚═══════════════════════════╝
```

### 9.2 Mola Kuralları

```
MOLA KURALLARI:
├── Kurye süreyi KENDİSİ belirler
│   ├── Minimum: 1 dk
│   ├── Maksimum: 45 dk (üzeri çevrimdışı sayılır)
│   └── Varsayılan: 15 dk
│
├── Mola sırasında TÜM SERVİSLERDEN sipariş GELMEZ
│   ├── 🍽️ Yemek · 💐 Çiçek · 📦 Market
│   └── Acil durumda: "Acil sipariş var, çıkar mısın? (+%50 prim)"
│
├── Süre dolunca sistem otomatik hatırlatır
│   ├── ⏰ Bildirim: "Mola bitti, müsait misin?"
│   ├── Kurye: "Hazırım" → tüm servisler için müsait olur
│   ├── Kurye: "5 dk daha" → uzatır (1 kere)
│   └── Hiçbir şey yapmazsa → 5 dk sonra çevrimdışı
│
├── Mola sırasında konum paylaşımı devam eder (30 sn)
└── Kurye molayı erken bitirebilir: "Hazırım" butonu
```

### 9.3 Servis Bazlı Mola (Gelişmiş)

Kurye sadece belirli servisleri kapatabilir:

```
SERVİS BAZLI MOLA:
├── "Çiçek teslimatı almıyorum, yemek devam"
│   ├── 💐 Çiçek: KAPALI
│   └── 🍽️ Yemek: AÇIK
│
├── "Sadece market alıyorum"
│   ├── 🍽️ Yemek: KAPALI
│   ├── 💐 Çiçek: KAPALI
│   └── 📦 Market: AÇIK
│
└── Kurye panelinden tek tıkla aç/kapa
```

---

## 10. ÖZEL TESLİMAT TÜRLERİ

### 10.1 Hassas Teslimat (Çiçek)

```
ÇİÇEK TESLİMAT KURALLARI:
├── ⚠️ Kurye ekranında: "Kırılacak / Devrilecek" uyarısı
├── 📦 Dik taşıma zorunluluğu
├── 🌡️ Sıcak havalarda +%20 özen bonusu
├── 📐 Maksimum boy: 100cm (motosiklet için)
├── 🚗 Büyük aranjmanlar için araba kurye öncelikli
├── 💰 Ek ücret: +5₺ hassas taşıma
└── 📸 Teslimat anı fotoğrafı zorunlu
```

### 10.2 Sıcak Teslimat (Yemek)

```
YEMEK TESLİMAT KURALLARI:
├── 🔥 Termal çanta ZORUNLU (yemek için)
├── ⏱️ Maksimum teslimat süresi: 30 dk (sıcak kalma)
├── 🧊 Soğuk ürünler ayrı bölme
├── 📦 Dökülme/kokmaya karşı sızdırmaz paket
├── 💰 Normal ücret (ek ücret yok)
└── ❌ Termal çantasız kuryeye yemek atanmaz
```

### 10.3 Zamanında Teslimat (Özel Gün)

```
ÖZEL GÜN TESLİMAT KURALLARI:
├── ⏰ Tam saatinde teslim ZORUNLU (14 Şubat, Anneler Günü)
├── 🎯 Erken veya geç kabul edilmez
├── 💰 +%50 prim (yüksek risk)
├── 🚗 Öncelikli araçlı kurye
├── 🔔 Kuryeye 3 katı hatırlatma (1 gün/1 saat/15 dk kala)
├── ❌ Geç kalırsa: Tazminat + işletme cezası
└── ✅ Başarılı teslim: +20 bonus puan
```

---

## 11. KURYE PUANLAMA VE ÖDÜL SİSTEMİ

### 11.1 Puanlama (Çift Yönlü)

```
MÜŞTERİ → KURYE:
├── Hız (zamanında teslim)
├── Nezaket (güler yüz, iletişim)
├── Paket durumu (ezik/yırtık yok)
├── Doğruluk (doğru adres/kişi)
└── Genel memnuniyet

İŞLETME → KURYE:
├── Bekleme süresi (işletmede)
├── Paket taşıma kalitesi
├── İletişim (sipariş hazır değilse haber verme)
└── Profesyonellik

KURYE → MÜŞTERİ:
├── Adres bulma kolaylığı
├── Teslim alma hızı
├── Nezaket
└── İletişim (kapıda bekleme, arasa ulaşılabilirlik)

KURYE → İŞLETME:
├── Hazırlık süresi (gecikme var mı?)
├── Paketleme kalitesi
└── İletişim
```

### 11.2 Puan Aralığı

```
PUAN ARALIĞI: 1.0 - 5.0 (0.1 hassasiyet)
├── 4.8+:  Elit Kurye 👑
├── 4.5-4.7: Premium Kurye ⭐
├── 4.0-4.4: Standart Kurye ✅
├── 3.5-3.9: Geliştirilmeli ⚠️
└── 3.5-:    Riskli Kurye 🔴
```

### 11.3 Ödüller ve Avantajlar

| Puan Aralığı | Statü | Avantajlar |
|-------------|-------|-----------|
| 4.8+ | 👑 Elit | Öncelikli sipariş atama, +%10 ücret prim |
| 4.5-4.7 | ⭐ Premium | Erken sipariş görme, +%5 ücret prim |
| 4.0-4.4 | ✅ Standart | Normal atama |
| 3.5-3.9 | ⚠️ Düşük | Daha az sipariş, uyarı |
| 3.5- | 🔴 Riskli | Askıya alınma (eğitim + tekrar sınav) |

### 11.4 Puan Kırıcılar

| İhlal | Puan Etkisi | Süre |
|-------|-----------|------|
| Geç teslimat (%50 üzeri) | -0.5 | 20 sipariş |
| Kötü paket durumu (ezik) | -0.7 | 25 sipariş |
| Müşteriye kötü davranış | -2.0 | 50 sipariş |
| Siparişi düşürme/kırma | -3.0 | 100 sipariş + tazminat |
| Müşteriye hakaret | -5.0 | Kalıcı ban |
| Sahte teslimat bildirimi | -5.0 | Kalıcı ban |
| İşletmede beklemeyi red | -1.0 | 15 sipariş |
| Servis kısıtlamasını ihlal | -0.5 | 10 sipariş |

---

## 12. ÜCRETLENDİRME VE ÖDEME

### 12.1 Kurye Ücret Yapısı

```
KURYE ÜCRETİ = TABAN + MESAFE + SERVIS + PRIM

├── TABAN ÜCRET (her teslimat için):
│   ├── Kısa mesafe (0-2 km): 15₺
│   ├── Orta mesafe (2-5 km): 20₺
│   └── Uzun mesafe (5+ km): 25₺
│
├── MESAFE EK ÜCRETİ (km başına):
│   ├── 0-2 km: 2₺/km
│   ├── 2-5 km: 1.5₺/km
│   └── 5+ km: 1₺/km
│
├── SERVİS EK ÜCRETİ:
│   ├── 🍽️ Yemek: +0₺ (standart)
│   ├── 💐 Çiçek: +5₺ (hassas taşıma)
│   ├── 📦 Market: +0₺ (standart)
│   └── 🚕 Özel gün: +%50 prim
│
└── PRİM:
    ├── Yoğun saat (12:00-14:00 / 18:00-21:00): +%20
    ├── Gece (22:00-06:00): +%40
    ├── Yağmur/Kar: +%25
    └── Özel gün (14 Şubat, Anneler Günü): +%100
```

### 12.2 Örnek Hesaplamalar

```
ÖRNEK 1: Yemek, 3 km, öğle yoğunluğu
├── Taban: 20₺
├── Mesafe (3 km): 4.5₺
├── Servis: 0₺
├── Prim (yoğun saat +%20): 4.9₺
├── TOPLAM: 29.4₺
└── Müşteriden alınan: 25₺ (sistem sübvanse eder)

ÖRNEK 2: Çiçek, 4 km, yağmurlu
├── Taban: 20₺
├── Mesafe (4 km): 6₺
├── Servis (çiçek): 5₺
├── Prim (yağmur +%25): 7.75₺
├── TOPLAM: 38.75₺
└── Müşteriden alınan: 35₺ (sistem sübvanse eder)

ÖRNEK 3: Sevgililer Günü çiçek, 5 km
├── Taban: 25₺
├── Mesafe (5 km): 7.5₺
├── Servis (çiçek): 5₺
├── Prim (özel gün +%100): 37.5₺
├── TOPLAM: 75₺
└── Müşteriden alınan: 60₺ (sistem sübvanse eder)
```

### 12.3 Ödeme Döngüsü

```
ÖDEME AKIŞI:
├── Her teslimat sonrası ücret kurye cüzdanına eklenir
├── Günlük kazanç özeti (akşam 23:59'da)
├── Haftalık ödeme (Pazartesi 10:00)
│   ├── Minimum çekim: 50₺
│   ├── Maksimum çekim: limitsiz
│   └── IBAN'a havale (1-3 iş günü)
└── Anında çekim opsiyonu (7/24, %1 komisyon)
```

---

## 13. MOBİNG ÖNLEME VE GÜVENLİK

### 13.1 Mobing Bildirimi

```
KURYE MOBİNG BİLDİRİMİ:
├── Kurye, şu durumlarda bildirim yapabilir:
│   ├── Müşteri kötü davrandı / hakaret etti
│   ├── İşletme kuryeyi bekletti (10+ dk)
│   ├── İşletme kuryeye kötü davrandı
│   ├── Teslimat adresi güvenli değildi
│   └── Müşteri ödeme yapmadı / kaçtı
│
├── Bildirim anında platform yetkilisine düşer
│   ├── 15 dk içinde geri dönüş
│   ├── Kurye bilgileri gizli tutulur
│   └── İşletme/müşteri incelemeye alınır
│
└── Cezalar:
    ├── Müşteri hakareti: Uyarı + 1 ay oy hakkı kısıtlaması
    ├── İşletme mobingi: -1.0 puan + 1 hafta öne çıkarma kaybı
    └── Tekrar eden ihlal: Platformdan geçici/ kalıcı uzaklaştırma
```

### 13.2 Güvenlik Önlemleri

```
KURYE GÜVENLİĞİ:
├── 📱 Canlı konum takibi (kurye destek ekibi)
├── 🆘 Acil durum butonu (kurye ekranında)
│   ├── Basınca: En yakın polis merkezi + platform destek
│   └── Otomatik: Son bilinen konum + ses kaydı başlatma
├── 📋 Teslimat öncesi risk değerlendirmesi
│   ├── Gece teslimatı: 23:00-06:00 arası ek güvenlik
│   └── Yüksek riskli bölge uyarısı
├── 👥 Çift kurye modu (yüksek riskli teslimat)
└── 🏠 Teslimat adresi doğrulama (gerçek adres mi?)
```

### 13.3 Kurye Sigortası

```
SİGORTA KAPSAMI:
├── Zorunlu: Kaza sigortası (platform karşılar)
├── Zorunlu: Hırsızlık/soygun sigortası (platform karşılar)
├── İsteğe bağlı: Sipariş hasar sigortası
├── İsteğe bağlı: Gelir kaybı sigortası
└── Tüm kuryelere otomatik (aktif çalışırken geçerli)
```

---

## 14. KURYE MOBİL UYGULAMASI

### 14.1 Ana Ekran

```
┌─────────────────────────────────────────┐
│  KURYEM                             🔋  │
│                                          │
│  🟢 MÜSAİT · 5 teslimat görünüyor      │
│                                          │
│  📊 BUGÜN                               │
│  ├── Tamamlanan: 8 teslimat             │
│  ├── Toplam kazanç: 240₺                │
│  ├── Puan: 4.8 ⭐                   │
│  └── Çalışma: 4 saat 12 dk              │
│                                          │
│  ── YENİ TESLİMATLAR ──                 │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 🍽️ KEBAPÇI MEHMET                  │ │
│  │    → Moda Cd. No:42                │ │
│  │    📏 3.2 km · 💰 24₺              │ │
│  │    ⏱️ Hazırlık: 12 dk · Yol: 8 dk │ │
│  │    [ ✅ Kabul ]  [ ❌ Red ]         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 💐 GÜL BAHÇESİ ÇİÇEKÇİLİK   ⚠️     │ │
│  │    → Fenerbahçe Mah.               │ │
│  │    📏 4.1 km · 💰 35₺ (hassas +5) │ │
│  │    ⏱️ Hazırlık: 20 dk · Yol: 10 dk│ │
│  │    [ ✅ Kabul ]  [ ❌ Red ]         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ── AKTİF TESLİMATLARIM ──              │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 🟡 Teslimat #2341  (2 dk sonra)    │ │
│  │ 🍽️ Dürümcü Ali → Sahrayıcedit     │ │
│  │ 📍 Kurye: teslimatta              │ │
│  └────────────────────────────────────┘ │
│                                          │
│  [ ☕ Mola ] [ 📊 Rapor ] [ 👤 Profil ] │
└─────────────────────────────────────────┘
```

### 14.2 Teslimat Detay Ekranı

```
┌─────────────────────────────────────────┐
│  💐 TESLİMAT #4562                       │
│                                          │
│  ⚠️ HASSAS TAŞIMA · Kırılacak/Devrilecek│
│                                          │
│  ALINACAK:                               │
│  ├── 📍 Gül Bahçesi Çiçekçilik          │
│  │      Bağdat Cd. No:123               │
│  │      ⏱️ Hazırlık: 15 dk (12:30'da)   │
│  └── 📞 0532 XXX XX XX (çiçekçi)        │
│                                          │
│  TESLİMAT:                               │
│  ├── 📍 Aliye Yılmaz                     │
│  │      Fenerbahçe Mah. 412. Sk. No:7   │
│  │      📞 0541 XXX XX XX               │
│  └── 📝 Kart notu: "Seni seviyorum ❤️"  │
│                                          │
│  📐 BOYUT: 40cm (dik taşıma)            │
│  💰 KAZANÇ: 35₺ (taban 20₺ + mesafe     │
│       10₺ + hassas 5₺)                  │
│                                          │
│  🗺️ ROTA:                               │
│  ├── 🟢 Kurye konumu → çiçekçi (1.2km) │
│  ├── 🟡 Çiçekçi → müşteri (2.9km)      │
│  └── ⏱️ Toplam: 25 dk                   │
│                                          │
│  [ ✅ Teslim Aldım ]  [ 🆘 Yardım ]    │
└─────────────────────────────────────────┘
```

---

## 15. DB ŞEMASI

```sql
-- Kurye profili (her kurye için)
-- bireysel_hesap tabanlı, 1:1 ilişki
kurye_profil (
  id, hesap_id, kurye_turu, ehliyet_sinifi,
  termal_canta_var_mi, hassas_tasima_ekipmani_var_mi,
  max_paket_boyutu, max_agirlik,
  plaka, arac_tipi, arac_renk,
  calisma_saatleri_json,
  puan, puan_sayisi, statu, kayit_tarihi
)

-- Kurye servis tercihleri (hangi servislerden teslimat alır)
kurye_servis_tercih (
  id, kurye_id, servis_turu ('yemek'/'cicek'/'market'/'diger'),
  aktif_mi, oncelik_sirasi, ek_kosul_json
)

-- Kurye durum geçmişi
kurye_durum_log (
  id, kurye_id, durum ('musait'/'sipariste'/'donuste'/'mola'/'cevrimdisi'),
  servis_turu, baslama_zamani, bitis_zamani,
  konum_json, ek_bilgi
)

-- Teslimat ataması
kurye_teslimat_atama (
  id, kurye_id, siparis_id, servis_turu,
  teslimat_turu ('standart'/'hassas'/'sicak'/'ozel_gun'),
  atama_zamani, kabul_zamani, red_sebebi,
  teslim_alma_zamani, teslimat_zamani,
  hazirlik_suresi, yol_suresi, toplam_sure,
  ucret, prim, toplam_ucret
)

-- Kurye puanları (çift yönlü)
kurye_puan (
  id, teslimat_id, puan_veren_id, puan_veren_tur ('musteri'/'isletme'),
  puan_alan_id, puan_alan_tur ('kurye'/'musteri'/'isletme'),
  puan, kriter_json, yorum, tarih
)

-- Kurye kazanç kaydı
kurye_kazanc (
  id, kurye_id, teslimat_id, tarih,
  taban_ucret, mesafe_ucret, servis_ucret, prim_ucret,
  toplam_ucret, odendi_mi, odeme_tarihi
)

-- Kurye mola kaydı
kurye_mola (
  id, kurye_id, baslama_zamani, bitis_zamani,
  planlanan_sure, guncel_sure, konum, erken_bitti_mi
)

-- Mobing bildirimi
kurye_mobing_bildirim (
  id, kurye_id, bildiren_tur ('kurye'/'musteri'/'isletme'),
  hedef_tur, hedef_id, sebep, aciklama,
  durum ('incelemede'/'onaylandi'/'red'), cozum_tarihi
)
```

---

## 16. API ENDPOINT'LERİ

### 16.1 Kurye Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/kurye/kayit` | Kurye kaydı |
| GET | `/api/v1/kurye/{id}` | Kurye detayı |
| PUT | `/api/v1/kurye/{id}` | Kurye güncelle |
| PUT | `/api/v1/kurye/{id}/konum` | Konum güncelle |
| PUT | `/api/v1/kurye/{id}/durum` | Durum güncelle |
| PUT | `/api/v1/kurye/{id}/servis-tercih` | Servis tercihlerini güncelle |

### 16.2 Teslimat Atama

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| GET | `/api/v1/kurye/yakindaki-teslimatlar` | Yakındaki teslimatları listele |
| GET | `/api/v1/kurye/{id}/aktif-teslimatlar` | Aktif teslimatları listele |
| POST | `/api/v1/kurye/{id}/teslimat/{teslimat_id}/kabul` | Teslimatı kabul et |
| POST | `/api/v1/kurye/{id}/teslimat/{teslimat_id}/red` | Teslimatı reddet |
| POST | `/api/v1/kurye/{id}/teslimat/{teslimat_id}/teslim-al` | Teslim alındı bildirimi |
| POST | `/api/v1/kurye/{id}/teslimat/{teslimat_id}/teslim-et` | Teslim edildi bildirimi |

### 16.3 Mola

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/kurye/{id}/mola/basla` | Mola başlat |
| PUT | `/api/v1/kurye/{id}/mola/bitir` | Molayı bitir |
| PUT | `/api/v1/kurye/{id}/mola/uzat` | Molayı uzat |
| PUT | `/api/v1/kurye/{id}/servis/{servis}/kapat` | Servis bazlı kapat |

### 16.4 Puanlama

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/teslimat/{id}/puan` | Puan ver |
| GET | `/api/v1/kurye/{id}/puan` | Kurye puan detayı |
| GET | `/api/v1/kurye/siralama` | Kurye sıralaması (servis bazlı) |

### 16.5 Ödeme

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| GET | `/api/v1/kurye/{id}/kazanc` | Kazanç özeti |
| GET | `/api/v1/kurye/{id}/kazanc/gunluk` | Günlük kazanç |
| POST | `/api/v1/kurye/{id}/cuzdan/cek` | Cüzdandan para çek |

### 16.6 Güvenlik

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/kurye/{id}/mobing-bildirim` | Mobing bildirimi |
| POST | `/api/v1/kurye/{id}/acil-durum` | Acil durum bildirimi |
| GET | `/api/v1/kurye/{id}/guvenli-bolge` | Güvenli bölge sorgula |

---

## 17. DİĞER DOKÜMANLARLA İLİŞKİ

Bu doküman, platformdaki **tüm teslimat gerektiren servisler** için ortak kurye altyapısını tanımlar:

| Servis | Kurye Kullanımı | Özel Kurallar |
|--------|----------------|---------------|
| 🍽️ Yemek | Termal çanta zorunlu | Maks 30 dk teslimat |
| 💐 Çiçek | Hassas taşıma ekipmanı | Dik taşıma, fotoğraf |
| 📦 Market | Standart | Boyut/ağırlık sınırı |
| 🚕 Taksi | Yolcu taşıma ruhsatı gerekli | Ayrı modül |

> ⚠️ **ÖNEMLİ:** Bu doküman, [YEMEK-SISTEMI-DESIGN.md](YEMEK-SISTEMI-DESIGN.md) ve [CICEK-SISTEMI-DESIGN.md](CICEK-SISTEMI-DESIGN.md)'deki kurye bölümlerinin yerine geçer. Tüm servisler, kurye yönetimi için bu dokümana başvurur. Servis bazlı istisnalar (çiçek için dik taşıma, yemek için termal çanta) ilgili servis dokümanında belirtilir, kurye atama ve yönetim detayları bu dokümanda bulunur.
