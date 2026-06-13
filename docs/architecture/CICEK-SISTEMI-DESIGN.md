# 🌸 ÇİÇEK SİSTEMİ - KAPSAMLI TASARIM DOKÜMANI

> **TÜM PLATFORM İÇİN ORTAK KURALLAR:** Bu modül, [MASTER-PLAN.md](MASTER-PLAN.md) ve [TAXI-SYSTEM-DESIGN.md](TAXI-SYSTEM-DESIGN.md)'de belirtilen ortak platform kurallarına (adres/konum zorunlu, 1 işlem = 1 yorum hakkı, 3 seçenekli oylama, yorum silinemez, anti-troll, %2 komisyon, puan = sıralama) tabidir.

---

## 📋 İÇİNDEKİLER

1. [Çiçek Eko-Sistemi Mimarisi](#1-çiçek-eko-sistemi-mimarisi)
2. [Hesap Türleri ve Kayıt](#2-hesap-türleri-ve-kayıt)
3. [Tedarik Zinciri (4 Kademe)](#3-tedarik-zinciri-4-kademe)
   - [Kurye Entegrasyonu → KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md)
4. [Çiçekçi (Perakende) Modülü](#4-çiçekçi-perakende-modülü)
5. [Toptancı Modülü](#5-toptancı-modülü)
6. [Üretici (Çiftçi) Modülü](#6-üretici-çiftçi-modülü)
7. [Malzeme Tedarikçileri Modülü](#7-malzeme-tedarikçileri-modülü)
8. [Sipariş ve Teslimat Süreci](#8-sipariş-ve-teslimat-süreci)
9. [Komisyon Yapısı](#9-komisyon-yapısı)
10. [Özel Gün Takvimi ve Hatırlatma](#10-özel-gün-takvimi-ve-hatırlatma)

---

## 1. ÇİÇEK EKO-SİSTEMİ MİMARİSİ

### 1.1 Zincir Yapısı

```
                    ┌──────────────────────────┐
                    │      MÜŞTERİ (SİPARİŞ)     │
                    │   Bireysel hesap ile alır  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    ÇİÇEKÇİ (PERAKENDE)    │
                    │   Kurumsal / Bireysel     │
                    │   Buket hazırlar, satar   │
                    └────────────┬─────────────┘
                                 │
                    ═════════════╪══════════════════
                    │            │                │
                    ▼            ▼                 ▼
        ┌──────────────┐ ┌────────────┐ ┌──────────────────┐
        │  TOPLANCI     │ │ MALZEMECİ   │ │  DİĞER ÇİÇEKÇİLER │
        │  Toptan çiçek │ │ Kağıt, saksı│ │  Stok takası      │
        │  alır/satar   │ │ kurdele vb  │ │                    │
        └──────┬───────┘ └────────────┘ └──────────────────┘
               │
               ▼
        ┌──────────────┐
        │  ÜRETİCİ      │
        │  (Çiftçi)     │
        │  Tarla/sera   │
        └──────────────┘
```

### 1.2 Platformdaki Yeri

| Kademe | Hesap Türü | Rol | Örnek |
|--------|-----------|-----|-------|
| **1** | Bireysel | Çiçek Üreticisi (Çiftçi) | Tarla/sera sahibi |
| **2** | Kurumsal | Toptancı / Komisyoncu | Hal, toptan dağıtımcı |
| **3** | Kurumsal / Bireysel | Çiçekçi (Perakende) | Dükkan, online satıcı |
| **3b** | Bireysel / Kurumsal | Malzeme Tedarikçisi | Kağıt, saksı, kurdele |
| **4** | Bireysel | Müşteri | Son kullanıcı |

---

## 2. HESAP TÜRLERİ VE KAYIT

### 2.1 Çiçek Üreticisi (Çiftçi) Kaydı

**Bireysel hesap içinde** ek rol: `cicek_ureticisi`

| Belge | Zorunlu | Açıklama |
|-------|---------|----------|
| Kimlik | Evet | TC/YK |
| Çiftçi Belgesi | Evet | Tarım Bakanlığı |
| Arazi/Sera Tapu | Evet | Üretim alanı kanıtı |
| İlaç Kullanım Raporu | Evet | Bitki koruma kaydı |
| Su Analiz Raporu | Evet | Sulama suyu kalitesi |
| Hijyen Sertifikası | Evet | Temel gıda hijyeni |

**Profil bilgileri:**
- Üretim türü: Kesme çiçek, saksı çiçeği, fide, tohum
- Üretim kapasitesi: adet/ay
- Üretim alanı: dönüm/m²
- Sertifikalar: Organik, İyi Tarım, GlobalGAP
- Hasat takvimi: Hangi ayda ne var

### 2.2 Toptancı Kaydı

**Kurumsal hesap** olarak açılır.

| Belge | Açıklama |
|-------|----------|
| Vergi Levhası | Toptan ticaret yetkisi |
| İşletme Ruhsatı | Hal kaydı / depo ruhsatı |
| Soğuk Hava Depo Belgesi | Varsa |
| Nakliye Ruhsatı | Çiçek taşıma aracı |

### 2.3 Çiçekçi (Perakende) Kaydı

**Kurumsal hesap** veya **Bireysel hesap + Esnaf rolü**.

| Belge | Açıklama |
|-------|----------|
| İşletme Ruhsatı | Belediye onaylı |
| Vergi Levhası | Esnaf/Kurumsal |
| Hijyen Sertifikası | Bitki hijyeni |
| Nakliye Belgesi | Varsa teslimat aracı |

**Dükkan Açma Süreci:**
```
ADIM 1: Bireysel hesap aç (yoksa)
ADIM 2: "Çiçekçi Dükkanı Aç" butonu
├── Dükkan adı, adresi, konumu
├── Çalışma saatleri (gün bazlı)
├── Teslimat bölgesi (km çapı)
├── Hazırlık süresi (buket yapımı, dakika cinsinden)
├── Dükkan fotoğrafları (en az 3)
└── Belgeleri yükle

ADIM 3: Onay süreci (ortalama 24-48 saat)
ADIM 4: Dükkan açılır → ürün ekleyebilir
```

**Dükkan Aktif / Pasif Durumu ve Zaman Çizelgesi:**
```
Çiçekçi dükkanı, fiziksel bir işletme olduğu için açılış/kapanış durumu kritiktir.
Ancak dükkan KAPALI olsa bile, müşteri zaman çizelgesinden ileri tarihli sipariş verebilir.

═══════════════════════════════════════════════════════════════
  DÜKKANIN 3 DURUM SEVİYESİ:
═══════════════════════════════════════════════════════════════

  1️⃣ 🟢 AÇIK (Aktif + Çalışma Saati İçinde)
  ├── Dükkan çalışıyor, çiçekçi dükkanda
  ├── Anlık sipariş alınabilir (bugün teslim)
  ├── Kurye hemen atanabilir
  ├── Müşteri görür: "🟢 Açık · Hemen sipariş verebilirsin"
  └── ⏰ Çalışma saati: 09:00-21:00 · Kalan: 4 saat

  2️⃣ 🟡 ÇALIŞMA SAATİ DIŞI (Aktif ama saatler geçti)
  ├── Dükkan aktiftir, çiçekçi yarın açacaktır
  ├── Anlık teslimat MÜMKÜN DEĞİL
  ├── Müşteri görür: "🟡 Şu an kapalı · Yarın 09:00'da açılır"
  ├── 📅 ÖN SİPARİŞ ALINIR (yarın veya ileri tarih)
  │   ├── Müşteri zaman çizelgesinden seçer
  │   ├── Seçenekler: Yarın 09:00 / 10:00 / 11:00 ...
  │   └── Sistem, bir sonraki açılış saatini otomatik önerir
  └── Müşteriye gösterim:
      ┌──────────────────────────────────────┐
      │  🟡 Gül Bahçesi Çiçekçilik            │
      │  Şu an kapalı · 09:00'da açılır       │
      │                                       │
      │  📅 Ön sipariş verebilirsin:          │
      │  ┌──────────────────────────────────┐│
      │  │ Yarın 10:00 — ⏱️ 30 dk hazırlık  ││
      │  │ Pazartesi 14:00 — Özel sipariş   ││
      │  │ 1 Ay sonra — Düğün paketi        ││
      │  └──────────────────────────────────┘│
      │                                       │
      │  [📅 Zaman Çizelgesinden Sipariş Ver] │
      └──────────────────────────────────────┘

  3️⃣ 🔴 PASİF (Manuel kapalı, çiçekçi kapattı)
  ├── Çiçekçi kendisi kapattı (tatil, hastalık, tadilat)
  ├── Anlık sipariş MÜMKÜN DEĞİL
  ├── 📅 ÖN SİPARİŞ YİNE ALINIR (zaman çizelgesiyle)
  │   ├── Müşteri en az 1 gün sonrasına sipariş verebilir
  │   ├── Çiçekçi, kapalı olduğu günlerde otomatik pasif
  │   └── Sistem: "En erken [açılacağı tarih] teslim"
  ├── Neden pasif?
  │   ├── 🏖️ Tatil (tarih aralığı belirtir)
  │   ├── 🤒 Hastalık / Acil durum
  │   ├── 🔧 Tadilat / Taşınma
  │   └── 📦 Stok yetersiz (geçici)
  └── Müşteriye gösterim:
      ┌──────────────────────────────────────┐
      │  🔴 DÜKKAN ŞU AN KAPALI              │
      │  📅 Açılma: 15 Haziran Pazartesi     │
      │                                       │
      │  📅 Ön sipariş verebilirsiniz         │
      │  ┌──────────────────────────────────┐│
      │  │ 15 Haz Pzt · 10:00              ││
      │  │ 16 Haz Salı · 14:00             ││
      │  │ 📅 Özel gün siparişi            ││
      │  └──────────────────────────────────┘│
      │                                       │
      │  [📅 Zaman Çizelgesinden Sipariş Ver] │
      └──────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
  ZAMAN ÇİZELGESİ (Timeline) SİPARİŞ SİSTEMİ:
═══════════════════════════════════════════════════════════════
  Dükkanın durumu ne olursa olsun, müşteri HER ZAMAN
  zaman çizelgesinden ileri tarihli sipariş verebilir.

  ZAMAN ÇİZELGESİ:
  ├── 🟢 Bugün: ${available_today_slots}
  │   ├── Dükkan açıksa → anlık teslimat seçenekleri
  │   └── Dükkan kapalıysa → gösterilmez
  ├── 📅 Yarın: ${tomorrow_slots}
  │   ├── 09:00 · 10:00 · 11:00 · 12:00 · 13:00 ...
  │   └── Her saat başı slot
  ├── 📅 Bu Hafta: ${this_week_slots}
  │   ├── Pazartesi · Salı · Çarşamba ...
  │   └── Saat: 09:00-21:00 arası
  ├── 📅 Önümüzdeki Ay: ${next_month_slots}
  │   ├── Düğün, organizasyon, özel gün
  │   └── Kesin tarih seçimi
  └── 📅 Aylar Öncesi: ${advance_slots}
      ├── Sevgililer Günü, Anneler Günü
      └── Yıllık özel siparişler

  MÜŞTERİ AKIŞI:
  1. Dükkanı keşfeder (açık/kapalı fark etmez)
  2. Ürünü/buketi seçer
  3. 📅 "Zaman Çizelgesi" butonuna tıklar
  4. İstediği gün ve saati seçer
  5. Siparişi tamamlar
  6. Ödeme yapar
  7. ✅ Sipariş, seçilen zamana planlanır
  8. ⏰ Seçilen zamanda çiçekçi hazırlar / kurye gider

  NOT: Dükkan pasif olsa bile zaman çizelgesi üzerinden
  sipariş alınabilir. Kural: "Sipariş alınır, teslimat
  dükkanın açık olduğu zamana planlanır."

DÜKKAN AKTİF/PASİF API:
├── `GET /api/cicekci/{id}/durum` → {
│     durum: 'acik' | 'calisma_saati_disi' | 'pasif',
│     calisma_saatleri: {hafta_ici: '08:00-21:00', ...},
│     tatil_gunleri: ['2026-06-15', '2026-06-16'],
│     en_erken_teslimat: '2026-06-10T09:00'
│   }
├── `PUT /api/cicekci/{id}/durum` → aktif/pasif değiştir
├── `GET /api/cicekci/{id}/zaman-cizelgesi?tarih=2026-06-15`
│   → {musait_saatler: ['09:00','10:00',...], uyari: 'pazartesi'}
├── `POST /api/cicekci/{id}/siparis?tarih=2026-06-15&saat=10:00`
│   → Sipariş oluştur, seçilen zamana planla
└── Platform, dükkan pasifken bile zaman çizelgesinden sipariş alabilir

ÇALIŞMA SAATLERİ (gün bazlı):
├── Hafta içi: 08:00 - 21:00
├── Cumartesi: 09:00 - 18:00
├── Pazar: 10:00 - 16:00 (isteğe bağlı)
├── Özel gün: 14 Şubat, Anneler Günü → 08:00-23:00
└── Müşteriye göster: "🟢 Bugün 20:00'a kadar açık · ⏰ Kalan: 4 saat"

GEÇİCİ KAPANMA (Mola/Tatil):
├── Öğle molası: 13:00-14:00 (dükkan pasif değil, çalışma saati dışı sayılır)
├── Bayram tatili: gün bazlı kapatma → pasif
├── Acil durum: anında kapat (hastalık, elektrik kesintisi) → pasif
└── Müşteriye mesaj: "Bu dükkan [tarih] tarihine kadar kapalıdır, ön sipariş alınır"
```

**Hazırlık Süresi Zorunluluğu:**
```
Her çiçekçi, siparişin hazırlanma süresini belirtmek zorundadır:
├── ⏱️ Min: 15 dk (sadece paketleme)
├── ⏱️ Orta: 30 dk (buket düzenleme)
├── ⏱️ Uzun: 60 dk (özel tasarım buket)
├── ⏱️ Özel: 120+ dk (kurye ile teslimat, kurumsal siparişler)
└── Müşteri görür: "Siparişin hazırlanma süresi: ~30 dk"
```

> Hazırlık süresi, yemek sistemindeki gibi teslimat süresine eklenir: Toplam süre = Hazırlık + Kurye yolu. Hava durumu ve trafik de hesaba katılır.

### 2.4 Malzeme Tedarikçisi Kaydı

**Bireysel veya Kurumsal**, ürettiği malzemeye göre:

| Tedarikçi Türü | İzin/Belge |
|---------------|------------|
| Saksı Üreticisi | Sanayi sicil (seramik/plastik) |
| Kağıt/Ambalaj Üreticisi | Atık bildirimi, orman izni |
| Kurdele/Textil | Tekstil kaydı |
| Gübre/Toprak | Tarım Bakanlığı üretim izni |

---

## 3. TEDARİK ZİNCİRİ (4 KADEME)

### 3.1 Akış Diyagramı

```
ÜRETİCİ                   TOPLANCI                 ÇİÇEKÇİ                 MÜŞTERİ
────────                  ───────                  ───────                 ───────
Hasat eder                 Toplu alır               Stoklarını görür        Gezinir
Fotoğraf çeker             Sınıflandırır             Buket tasarlar          Seçer
Platforma yükler           Fiyatlandırır             Sipariş alır            Sipariş verir
Sipariş bekler             Satışa sunar              Kuryeye verir           Teslim alır
                            Stok takibi               Öder                    Yorum yapar
```

### 3.2 Her Kademede Platformun Rolü

- Her kademe arası işlem **platform üzerinden** yapılır
- Her işlemden **%2 komisyon** alınır (zincirdeki her kademede ayrı ayrı)
- Tüm ödemler online, nakit yok
- Kurye sistemi: Çiçekçi → Müşteri arası (teslimat)
- Toptancı → Çiçekçi arası (nakliye ayrı, opsiyonel)
- Üretici → Toptancı arası (üretici kendi gönderir veya platform kuryesi)

### 3.4 Kurye Entegrasyonu

Çiçek sistemi, **platformun bağımsız kurye havuzunu** kullanır. Kuryeler yemek, çiçek, market gibi tüm servislerden gelen teslimatları tek bir havuzda görür ve kabul/red eder.

> 📖 **Detaylı kurye sistemi:** [KURY-SISTEMI-DESIGN.md](KURY-SISTEMI-DESIGN.md) — bağımsız, tüm servislere hizmet veren ortak kurye havuzu.

```
KURYE AKIŞI (Çiçekçi → Müşteri):
├── Sipariş alınır → Çiçekçi hazırlamaya başlar
├── Platform ortak havuzdan en uygun kuryeyi bulur
│   ├── Kurye aynı anda yemek/çiçek/market teslimatı görebilir
│   ├── Kurye servis tercihine göre yönlendirilir
│   └── Kurye kabul ederse atama yapılır
├── Hazırlık bitince → Kuryeye bildirim → Alır → Müşteriye gider
└── Kurye, teslimat türüne göre farklı ücret alır

KURYE TÜRLERİ:
├── 🚲 Platform Kuryesi (ortak havuz, tüm servisler)
├── 🚗 Çiçekçinin Kendi Kuryesi (dükkan çalışanı, sadece çiçek)
└── 📦 Kargo (kurutulmuş/yapay çiçek, uzak mesafe için opsiyonel)
```

> **ÖNEMLİ:** Canlı çiçek teslimatında kurye bildirimine "Hassas Taşıma ⚠️" etiketi eklenir. Kurye ekranında "Kırılacak / Devrilecek — Dik taşıyın" uyarısı gösterilir. Çiçek teslimatları, yemek teslimatlarına göre +5₺ hassas taşıma primi alır.

### 3.5 Önceden Sipariş Sistemi (Pre-Order)

Çiçek sektöründe **önceden sipariş** standarttır. Düğün, nişan, yıldönümü, açılış gibi özel günler için aylar öncesinden sipariş verilebilir.

```
ÖNCEDEN SİPARİŞ ZAMAN DİLİMLERİ:
├── 🔴 Acil Teslimat: Bugün / 2 saat içinde (varsa stok)
├── 🟡 Kısa Süreli: 1-7 gün içinde
├── 🟢 Orta Süreli: 1-4 hafta içinde
├── 🔵 Uzun Süreli: 1-6 ay içinde (düğün, organizasyon)
└── 🟣 Yıllık Tekrarlı: Her yıl aynı tarihte (abonelik)

SİPARİŞ AKIŞI (Önceden):
├── Müşteri teslimat tarihini seçer (takvimden)
├── Çiçekçi siparişi alır, tarihi not alır
├── Sistem otomatik hatırlatma gönderir:
│   ├── Tarihe 7 gün kala: "Hazırlığa başla" uyarısı
│   ├── Tarihe 1 gün kala: "Yarın teslimat" hatırlatması
│   └── Teslimat günü: Hazırlık + kurye akışı başlar
├── Ödeme:
│   ├── Şimdi öde (tek seferde)
│   ├── Ön ödeme (%50) + teslimatta kalan (%50)
│   └── Tamamını teslimatta öde (kapıda nakit bildirimli)
└── İptal koşulları:
    ├── 30+ gün kala: Tam iade
    ├── 7-29 gün kala: %50 iade
    └── 7 günden az: İade yok (çiçekçi malzemeyi aldıysa)

TAKVİM ENTEGRASYONU:
├── Müşteri Google/Apple Takvim'e ekleyebilir
├── "Bu tarihte teslim edilecek" bildirimi
├── Çiçekçi takviminde otomatik blokaj
└── Platform, düğün sezonunda ön siparişleri öne çıkarır
```

### 3.6 Teslimat Süresi Gösterimi

**Yemek sistemindeki gibi**, çiçek siparişlerinde de teslimat süresi açıkça belirtilir:

```
TESLİMAT SÜRESİ HESABI:
├── ⏱️ Hazırlık Süresi (çiçekçinin seçtiği: 15/30/60/90 dk)
├── 🚲 Kurye Yolu (kuryenin çiçekçiye gelişi + müşteriye gidişi)
├── 🌧️ Hava Durumu Etkisi (yağmur/sis/karda +%15-30)
├── 🚦 Trafik Etkisi (yoğun saatlerde +%10-20)
└── ✅ TOPLAM TAHMİNİ SÜRE = Hazırlık + Kurye + Hava + Trafik

MÜŞTERİYE GÖSTERİM:
┌─────────────────────────────────────────────────┐
│  💐 Gül Bahçesi Çiçekçilik                      │
│                                                 │
│  ⏱️ Teslimat tahmini: ~45 dk                    │
│     ├── Hazırlık: 30 dk                        │
│     ├── Kurye yolu: 15 dk                      │
│     └── 🌧️ Yağmur +%15                         │
│                                                 │
│  🚲 Kurye: Mehmet · 4.8⭐ · 2 dk sonra gelir   │
└─────────────────────────────────────────────────┘
```

> Teslimat süresi, sepette ve sipariş onayında her zaman gösterilir. Müşteri süreyi görmeden sipariş veremez.

### 3.3 Stok Yönetimi

### 3.3 Stok Yönetimi

```
STOK ZİNCİRİ:
├── Üretici: Hasat miktarını girer (günlük/haftalık)
├── Toptancı: Stoktaki ürünleri listeler
├── Çiçekçi: Satın aldığı stoku görür, kendi vitrinine koyar
└── Müşteri: Çiçekçinin vitrinindeki ürünleri sipariş eder

SENKRONİZASYON:
├── Bir toptancıdan 5 çiçekçi sipariş verdiğinde
├── Stok otomatik düşer (çiçekçi bazında)
├── Toptancı stoku bitince tüm çiçekçilerde pasif olur
└── Üretici hasadı bitince toptancıda düşer
```

---

## 4. ÇİÇEKÇİ (PERAKENDE) MODÜLÜ

### 4.0 Hazır Ürün + Özel Sipariş (İkili Sistem)

Çiçekçi vitrini **iki modda** çalışır:

```
VİTRİN MODLARI:
├── 📦 HAZIR ÜRÜNLER (Önceden tasarlanmış buketler)
│   ├── Çiçekçi tarafından önceden hazırlanmış
│   ├── Stokta bekleyen veya talep üzerine yapılan
│   ├── Sabit fiyat, sabit içerik
│   ├── Hemen sipariş verilebilir
│   └── Kategori: doğum günü, sevgili, taziye...
│
└── ✏️ ÖZEL SİPARİŞ (Müşteri kendi tasarlar)
    ├── Müşteri adım adım kendi buketini oluşturur
    ├── En az 1 gün önceden sipariş (hazırlık süresi zorunlu)
    ├── Fiyat: seçilen ürünlere göre dinamik hesaplanır
    └── Her özel siparişe mesaj kartı zorunlu

MÜŞTERİ AKIŞI:
┌─────────────────────────────────────┐
│  VİTRİN                            │
│  ┌──────────────────────────────┐   │
│  │ [📦 Hazır Ürünler] [✏️ Özel] │   │
│  └──────────────────────────────┘   │
│                                     │
│  SEÇİM: 📦 Hazır                    │
│  → Ürün seç → Sepete ekle          │
│                                     │
│  SEÇİM: ✏️ Özel Sipariş            │
│  → 1️⃣ Tema seç                    │
│  → 2️⃣ Çiçek seç (en az 1)         │
│  → 3️⃣ Renk seç                    │
│  → 4️⃣ Boyut seç                   │
│  → 5️⃣ Ekstra: vazo/yeşillik/kurdele│
│  → 6️⃣ Mesaj kartı yaz (ZORUNLU)   │
│  → 7️⃣ Teslimat tarihi seç         │
│  → 💰 Fiyat göster → Sepete ekle   │
└─────────────────────────────────────┘
```

#### 4.0-a Özel Sipariş Detaylı Akış

```
ÖZEL SİPARİŞ ADIMLARI (Mobil/Web):

ADIM 1 - TEMA SEÇİMİ:
├── ❤️ Romantik
├── 🎂 Doğum Günü
├── 🕊️ Taziye
├── 👩 Anneler Günü
├── 🎓 Mezuniyet
├── 💍 Evlenme Teklifi
├── 🏢 Kurumsal
└── ✏️ Serbest Tasarım

ADIM 2 - ÇİÇEK SEÇİMİ (en az 1, en çok 5 tür, CANLI STOK):
├── 🌹 Gül (Kırmızı/Beyaz/Pembe/Sarı) × adet
│   └── 📦 Stok: 24 adet ✅
├── 🌷 Lale (Kırmızı/Sarı/Beyaz/Mor) × adet
│   └── 📦 Stok: 18 adet ✅
├── 🪷 Orkide (Beyaz/Mor/Pembe) × adet
│   └── 📦 Stok: 7 adet ⚠️
├── 🌸 Lilyum (Beyaz/Pembe) × adet
│   └── 📦 Stok: 3 adet 🔴
├── 🌼 Papatya × adet
│   └── 📦 Stok: 30 adet ✅
├── 💜 Karanfil × adet
│   └── 📦 Stok: 20 adet ✅
├── 🌻 Ayçiçeği × adet
│   └── 📦 Stok: 12 adet ✅
├── 💐 Kasımpatı × adet
│   └── 📦 Stok: 5 adet ⚠️
└── Her çiçek için:
    ├── Canlı stok sayısı gösterilir
    ├── Stok ≤ 5: ⚠️ uyarı (az stok)
    ├── Stok = 0: 🔴 tükenmiş (seçilemez)
    └── Müşteri stok kadar adet seçebilir

ADIM 3 - RENK PALETİ:
├── Kırmızı 🟥 | Pembe 🩷 | Beyaz ⬜
├── Sarı 🟨 | Mor 🟪 | Turuncu 🟧
├── Mavi 🟦 | Yeşil 🟩 | Karışık 🌈
└── Seçilen temaya göre önerilen renkler

ADIM 4 - BOYUT:
├── Küçük (20-25cm, tek kişilik) — +0₺
├── Orta (30-35cm, standart) — +50₺
├── Büyük (40-50cm, şaşaalı) — +120₺
└── Ekstra Büyük (50cm+, organizasyon) — +250₺

ADIM 5 - VAZO SEÇİMİ (isteğe bağlı, özel alt seçenekler):
├── 🏺 Vazo İstemiyorum — +0₺
├── 🏺 Sade Cam Vazo — +30₺
│   └── ⬜ Şeffaf / ⬜ Buzlu
├── 🏺 Boyalı Seramik Vazo — +60₺
│   └── 🟥 Kırmızı / 🩷 Pembe / ⬜ Beyaz / 🟦 Mavi
├── 🏺 Kristal Vazo — +100₺
│   └── ✨ Desenli / ✨ Sade
└── 🏺 El Yapımı Özel Vazo — +150₺ (çiçekçinin stoktaki el yapımı vazoları)

ADIM 6 - DİĞER EKSTRALAR:
├── 🌿 Yeşillik (okaliptüs/sarmaşık/deren) — +15₺
├── 🎀 Kurdele (saten/dantel/rafya) — +10₺
├── ✨ Işıklı süs — +25₺
└── 🧸 Oyuncak eklentisi — +40₺

ADIM 7 - MESAJ KARTI (ZORUNLU):
├── Kart tasarımı seç (şablonlar)
├── Notunu yaz (en az 10 karakter)
├── Dijital / Fiziksel kart seçimi
└── → Bu adım atlanamaz, çiçek kartsız anlamsızdır

ADIM 8 - TESLİMAT:
├── Hemen (hazırlık süresi kadar)
├── Tarihli (ileri bir tarih)
├── Ön sipariş (aylar öncesi)
└── Adres ve alıcı bilgisi

ADIM 9 - ÖDEME (ÖNCE ÖDEME, SONRA İŞLEM):
├── 💳 Ödeme alınmadan sipariş işleme alınmaz
├── Dinamik fiyat özeti (çiçekler + vazo + boyut + ekstralar)
├── Tahmini teslimat süresi
└── Ödeme yöntemi seç:
    ├── 💳 Kredi Kartı (tek çekim / taksit)
    ├── 👛 Platform Cüzdanı
    ├── 🏦 Havale/EFT
    └── 💵 Kapıda Nakit Bildirimli
```

#### 4.0-b Ödeme Öncelik Kuralı (Payment First Rule)

```
KURAL: Özel siparişlerde işlem sırası:

┌─────────────────────────────────────────────┐
│  SİPARİŞ AKIŞI:                             │
│                                              │
│  1️⃣ TASARIM → Müşteri buketi tasarlar       │
│  2️⃣ FİYATLANDIRMA → Sistem fiyatı hesaplar  │
│  3️⃣ ÖDEME → Müşteri ödemeyi yapar 💳       │
│  4️⃣ ONAY → Ödeme alınınca sipariş onaylanır ✅│
│  5️⃣ HAZIRLIK → Çiçekçi buketi hazırlar     │
│  6️⃣ TESLİMAT → Kurye teslim eder           │
└─────────────────────────────────────────────┘

ÖNEMLİ:
├── Ödeme alınmadan çiçekçiye bildirim gitmez
├── Ödeme alınmadan hazırlık başlamaz
├── Ödeme alınmadan stok rezervasyonu yapılmaz
├── Ödeme başarısız = sipariş iptal
└── Ödeme alındıktan sonra iptal/iade koşulları:
    ├── 30+ gün kala: %100 iade
    ├── 7-30 gün kala: %70 iade
    └── 7 günden az: iade yok (çiçekçi malzemeyi aldı)
```

#### 4.0-c Canlı Stok ve Rezervasyon Sistemi

```
CANLI STOK:
├── Her çiçek türü için anlık stok
├── Stok, saniyede güncellenir (WebSocket)
├── Müşteri seçim yaparken stok düşebilir
└── Stok biten çiçek gri gösterilir, seçilemez

STOK SEVİYELERİ:
├── 🟢 Yeterli Stok (10+ adet) → Yeşil
├── 🟡 Az Stok (1-9 adet) → Sarı uyarı
├── 🔴 Tükendi (0 adet) → Kırmızı, seçilemez
└── Seçilen adet kadar stok rezerve edilir

REZERVASYON SİSTEMİ:
├── Müşteri çiçeği sepete ekler → stoktan düşer
├── 15 dakika içinde ödeme yapılmazsa → stok geri açılır
├── Ödeme alınınca → kalıcı rezervasyon
├── Ödeme başarısız → anlık stok iadesi
└── Aynı çiçeği 2 müşteri aynı anda seçemez

VAZO STOK:
├── Her vazo türü için ayrı stok
├── El yapımı vazolar sınırlı sayıda
├── Mevsimlik vazolar (yazlık/kışlık)
└── Kristal vazo stok ile sınırlı
```

#### 4.0-b Hazır Ürün + Özel Sipariş Fiyat Karşılaştırma

```
ÖRNEK: Kırmızı Gül Buketi
┌──────────────────────┬────────────┬──────────────┐
│                      │  HAZIR 📦  │  ÖZEL ✏️     │
├──────────────────────┼────────────┼──────────────┤
│ 12 Kırmızı Gül       │ 250 ₺      │ 200 ₺        │
│ Boyut seçimi         │ 2 seçenek  │ 4 seçenek    │
│ Ekstra ekleme        │ ❌ Yok     │ ✅ Var       │
│ Mesaj kartı          │ İsteğe     │ Zorunlu      │
│ Teslimat             │ Hemen      │ 1 gün sonra  │
│ Fiyat aralığı        │ Sabit 250 ₺│ 200-450 ₺    │
└──────────────────────┴────────────┴──────────────┘
```

#### 4.0-c DB Şeması (Özel Sipariş için)

```sql
-- Özel sipariş tasarımı
ozel_siparis_tasarim (
  id, musteri_id, tema, boyut,
  cicekler_json,   -- [{"cicek_id":1,"adet":12,"renk":"kirmizi"}, ...]
  ekstralar_json,  -- ["vazo","kurdele","yesillik"]
  kart_notu, kart_tasarimi, kart_turu,
  toplam_fiyat, olusturma_tarihi
)

-- Özel sipariş → sipariş dönüşümü (onaylandığında)
ozel_siparis_siparis (
  id, tasarim_id, cicekci_id, musteri_id,
  teslimat_tarihi, teslimat_adresi,
  alici_adi, durum, odeme_turu
)
```

> **Not:** Özel siparişlerde hazırlık süresi, normal ürüne göre +1 gün eklenir. Çiçekçi, müşterinin tasarımını görür, stok durumuna göre onaylar veya revizyon önerir. Müşteri onayı olmadan sipariş kesinleşmez.

```
VİTRİN ÖĞELERİ:
├── 📸 Ürün fotoğrafı (en az 2, gerçek çiçek, stok fotoğraf yasak)
├── 💰 Fiyat
├── 📏 Boyut seçeneği (küçük/orta/büyük)
├── 🏷️ Kategori (doğum günü, sevgililer günü, cenaze, vb.)
├── 📝 Açıklama (içindeki çiçekler, renkler)
└── 🚚 Teslimat seçenekleri (bugün, yarın, tarihli)
```

### 4.1-a Ürün (Çiçek) Özellikleri ve Etiketleme

Her ürünün **çiçek isimleri** ve **çiçek özellikleri** açıkça belirtilmelidir. Müşteri ne aldığını bilmelidir.

```
ZORUNLU ÜRÜN ALANLARI:
├── 🌸 İçindeki Çiçekler (en az 1, en çok 10)
│   ├── Örn: "Kırmızı Gül, Beyaz Lilyum, Yeşillik"
│   └── Her çiçek için alt alanlar:
│       ├── İsim: "Gül"
│       ├── Renk: "Kırmızı"
│       ├── Adet: 12
│       └── Varyant: "Hollanda gülü"

├── 📏 Özellikler
│   ├── Boyut: "Küçük (25cm) / Orta (35cm) / Büyük (50cm)"
│   ├── Ağırlık: "1.2 kg"
│   ├── Vazo: "Dahil / Hariç"
│   ├── Ömür: "7-10 gün"
│   └── Koku: "Var / Yok / Hafif"

├── 🏷️ Etiketler
│   ├── Mevsim: "İlkbahar / Yaz / Sonbahar / Kış / Yıl boyu"
│   ├── Anlamı: "Aşk / Dostluk / Şükran / Başsağlığı"
│   ├── Bakım: "Kolay / Orta / Zor"
│   └── Alerjen: "Varsa uyarı"

└── 🌍 Menşei
    ├── "Hollanda" (ithal)
    ├── "Yerli" (Türkiye)
    └── Üretici adı (varsa)
```

**Örnek ürün kartı:**
```
┌──────────────────────────────────────────┐
│  🌹 12 Kırmızı Gül Buketi               │
│                                          │
│  İçindekiler:                            │
│  ├── 🌹 Kırmızı Gül × 12 (Hollanda)     │
│  ├── 🌿 Okaliptüs yeşillik × 3          │
│  └── 🎀 Kırmızı kurdele                  │
│                                          │
│  Özellikler:                             │
│  ├── Boyut: 40cm                         │
│  ├── Vazo: Hariç                         │
│  ├── Ömür: 7-10 gün                      │
│  └── Koku: Hafif gül kokusu             │
│                                          │
│  Anlamı: "Aşk ve tutku" ❤️              │
│  Mevsim: Yıl boyu                        │
└──────────────────────────────────────────┘
```

### 4.1-b Kapsamlı Çiçek Veritabanı (Platform Referans Kataloğu)

Platformda bulunan **tüm çiçek türleri**, özellikleri, anlamları, mevsimleri ve stok bilgileri:

```
═══════════════════════════════════════════════════════════════
  🌹 1. GÜL (Rosa)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Buket / Aranjman
  Köken:      İthal (Hollanda, Ekvador, Kenya) + Yerli (Isparta)
  Renk:       Kırmızı 🟥, Beyaz ⬜, Pembe 🩷, Sarı 🟨, Turuncu 🟧,
              Mor 🟪, Mavi 🟦 (boyalı), Siyah ⬛ (nadir)
  Anlamı:
  ├── Kırmızı: Aşk, tutku, romantizm ❤️
  ├── Beyaz:   Masumiyet, saflık, saygı 🤍
  ├── Pembe:   Beğeni, şükran, zarafet 🩷
  ├── Sarı:    Dostluk, mutluluk, neşe 💛
  ├── Turuncu: Enerji, coşku, sıcaklık 🧡
  ├── Mor:     Büyü, ihtişam, ilk görüşte aşk 💜
  └── Mavi:    Gizem, imkansız aşk 💙 (doğal mavi gül yoktur)
  Varyantlar:
  ├── Hollanda gülü (iri başlı, uzun sap 60-80cm)
  ├── Isparta gülü (kokulu, orta başlı 40-60cm)
  ├── Spray gül (dallı, çok başlı, mini)
  ├── Kokulu gül (İngiliz/David Austin gülü)
  └── Solmayan gül (özel işlem, yıllarca dayanır)
  Mevsim:     Yıl boyu (sera), Haziran-Ekim (tarla)
  Ömür:       5-12 gün (vazoda)
  Boy:        30-80 cm
  Bakım:      Orta (dikensiz varyantlar var)
  Koku:       Kırmızı/Pembe yoğun, Sarı/Beyaz hafif
  Menşei:     🇹🇷 Isparta (dünyanın en büyük gül yağı üreticisi)
              🇳🇱 Hollanda (kesme gül)
              🇪🇨 Ekvador (iri başlı)
  Türkiye üretim: Yıllık ~300 milyon dal

═══════════════════════════════════════════════════════════════
  🌷 2. LALE (Tulipa)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Soğanlı bitki
  Köken:      Türkiye (Osmanlı'dan dünyaya yayılmıştır)
  Renk:       Kırmızı, Sarı, Beyaz, Pembe, Mor, Turuncu, Siyah (nadir)
  Anlamı:     Aşk, zarafet, mükemmel sevgi 💕
  ├── Kırmızı: Gerçek aşk
  ├── Sarı:    Umutsuz aşk (eskiden), neşe (günümüz)
  ├── Beyaz:   Bağışlama, saygı
  ├── Mor:     Asalet, krallık
  └── Pembe:   İlgi, sevgi
  Varyantlar:
  ├── Tek lale (klasik, tek taç yaprak)
  ├── Çift lale (şakayık görünümlü)
  ├── Papağan lale (saçaklı yapraklar)
  └── Zambak çiçekli lale (sivri uçlu)
  Mevsim:     Mart-Mayıs (tarla), Kasım-Nisan (sera ithal)
  Ömür:       5-10 gün (vazoda)
  Boy:        10-70 cm
  Bakım:      Kolay
  Koku:       Genelde yok, bazı türlerde hafif
  Menşei:     🇹🇷 Türkiye (Kazdağları, Anadolu)
              🇳🇱 Hollanda (dünyanın en büyük lale üreticisi)
  Not:        Türkiye'nin sembol çiçeğidir. Her yıl İstanbul Lale Festivali.

═══════════════════════════════════════════════════════════════
  🪷 3. ORKİDE (Orchidaceae)
═══════════════════════════════════════════════════════════════
  Türü:       Salon bitkisi / Kesme çiçek (nadir)
  Köken:      Güneydoğu Asya, Güney Amerika, tropikal
  Renk:       Beyaz, Pembe, Mor, Sarı, Mavi (boyalı), Kaplan desenli
  Anlamı:     Zarafet, asalet, güzellik, aşk, bereket 💎
  ├── Beyaz:  Saflık, hayranlık
  ├── Pembe:  Sevgi, nezaket
  ├── Mor:    Asalet, saygı
  └── Sarı:   Dostluk, yeni başlangıç
  Varyantlar:
  ├── Phalaenopsis (kelebek orkide) — en yaygın, 6-8 hafta çiçekli
  ├── Cymbidium — büyük çiçekli, kesme çiçek
  ├── Dendrobium — dallı, çok çiçekli
  ├── Oncidium (dans eden hanım) — küçük sarı çiçekler
  └── Vanda — mor/beyaz, uzun ömürlü
  Mevsim:     Yıl boyu (sera)
  Ömür:       6-8 hafta (saksıda), 7-14 gün (kesme)
  Boy:        20-100 cm
  Bakım:      Orta-Zor (nem + ışık dengesi)
  Koku:       Bazı türlerde vanilya/çikolata kokusu
  Menşei:     🇹🇷 Türkiye (sahil bölgeleri, seralar)
              🇳🇱 Hollanda (kesme çiçek)
  Fiyat:      Saksıda 150-500₺, Kesme 40-120₺/dal
  Türkiye pazarı: En çok satılan saksı çiçeği, doğum günü hediyesi #1

═══════════════════════════════════════════════════════════════
  💐 4. KRİZANTEM / KASIMPATI (Chrysanthemum)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Bahçe bitkisi
  Köken:      Çin, Japonya, dünya geneli
  Renk:       Beyaz, Sarı, Pembe, Mor, Kırmızı, Turuncu, Yeşil
  Anlamı:     Uzun ömür, sadakat, neşe, hüzün (kültüre göre)
  ├── Beyaz:  Teselli, taziye, veda 🕊️
  ├── Sarı:   Mutluluk, dostluk
  ├── Pembe:  Sevgi, hayranlık
  ├── Kırmızı: Aşk, paylaşım
  ├── Mor:    Asalet, zenginlik
  └── Bordo:  Taziye, saygı
  Varyantlar:
  ├── Tek başlı (disbud) — büyük tek çiçek
  ├── Spray (dallı) — çok çiçekli dal
  ├── Papatya tipi — ince yapraklı
  └── Düğme tipi — mini toplar
  Mevsim:     Yaz sonu - Kış (Eylül-Ocak)
  Ömür:       10-20 gün (vazoda) — en dayanıklı kesme çiçek
  Boy:        30-100 cm
  Bakım:      Kolay
  Koku:       Hafif, keskin
  Menşei:     🇹🇷 Türkiye (yoğun üretim)
  Not:        En uzun ömürlü kesme çiçeklerdendir. Taziye çiçeği olarak
              bilinir ama renkli varyantları mutlu günlerde de kullanılır.

═══════════════════════════════════════════════════════════════
  💜 5. KARANFİL (Dianthus caryophyllus)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek
  Köken:      Akdeniz, Türkiye
  Renk:       Kırmızı, Pembe, Beyaz, Sarı, Mor, Yeşil, Bordo
  Anlamı:     Sevgi, hayranlık, şükran, gurur
  ├── Kırmızı: Hayranlık, derin aşk
  ├── Pembe:  Annelik, şükran (Anneler Günü #1 çiçeği)
  ├── Beyaz:  Saflık, masumiyet, iyi şans
  ├── Sarı:   Hayal kırıklığı (dikkat!)
  ├── Mor:    Kapris, düzensizlik
  └── Çizgili: Pişmanlık, red
  Varyantlar:
  ├── Standart karanfil (tek başlı, büyük)
  ├── Spray karanfil (dallı, minyatür)
  └── Yeşil karanfil (özel boya, St. Patrick's Day)
  Mevsim:     Yıl boyu (sera)
  Ömür:       7-14 gün (vazoda)
  Boy:        40-60 cm
  Bakım:      Kolay
  Koku:       Tatlı, karanfil baharatı benzeri
  Menşei:     🇹🇷 TÜRKİYE (dünyanın en büyük karanfil üreticilerinden)
  Türkiye ihracatı: 35 ülkeye, 80 milyon dal/yıl, 12 milyon dolar
  Not:        Türkiye'nin en çok üretilen ve ihraç edilen çiçeğidir.
              Anneler Günü'nde en çok satılan çiçek.

═══════════════════════════════════════════════════════════════
  🌸 6. LİLYUM / ZAMBAK (Lilium)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Soğanlı bitki
  Köken:      Asya, Avrupa, Kuzey Amerika
  Renk:       Beyaz, Pembe, Turuncu, Sarı, Kırmızı, Mor
  Anlamı:     Saflık, masumiyet, görkem, yeniden doğuş ✨
  ├── Beyaz:  Saflık, iffet (düğünlerde) 🤍
  ├── Pembe:  Zenginlik, refah
  ├── Turuncu: Tutku, enerji, nefret (dikkat!)
  ├── Sarı:   Neşe, arkadaşlık
  └── Kırmızı: Aşk, arzu
  Varyantlar:
  ├── Asya lilyum (erken çiçek, bol tomurcuk)
  ├── Oriental lilyum (geç çiçek, büyük, yoğun kokulu)
  ├── LA melez (Asya+Oriental, uzun ömürlü)
  ├── Trompet lilyum (uzun boru şeklinde çiçek)
  └── Calla Lily (Zantedeschia) — ayrı tür, zarif, 2 hafta dayanır
  Mevsim:     Nisan-Eylül
  Ömür:       7-14 gün (vazoda)
  Boy:        50-120 cm
  Bakım:      Orta (polen dökülmesine dikkat)
  Koku:       Oriental: Yoğun, sarhoş edici — Asya: Hafif
  Menşei:     🇹🇷 Türkiye (Karadeniz), 🇳🇱 Hollanda
  Dikkat:     Kediler için zehirlidir! Satışta uyarı zorunlu.
              Polenleri kıyafetlerde leke yapar.

═══════════════════════════════════════════════════════════════
  🌼 7. PAPATYA (Bellis perennis / Leucanthemum)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Kır çiçeği
  Köken:      Avrupa, Asya
  Renk:       Beyaz taç + Sarı merkez (klasik), Pembe, Kırmızı (gerbera)
  Anlamı:     Masumiyet, saflık, neşe, sadakat 🌞
  ├── Klasik: İyi kalpli, masumiyet
  ├── Mavi gözlü: Sabır, güzellik
  └── Gerbera: Neşe, mutluluk, sıcakkanlılık
  Varyantlar:
  ├── Kır papatyası (küçük, yabani)
  ├── Gerbera (büyük başlı, renkli) — ayrı bir tür
  ├── Sarı papatya (Anthemis)
  └── Mavi papatya (Felicia)
  Mevsim:     Mart-Temmuz
  Ömür:       5-10 gün (vazoda)
  Boy:        15-60 cm
  Bakım:      Kolay
  Koku:       Hafif, topraksı
  Menşei:     🇹🇷 Yerli
  Not:        Gerbera Türkiye'de 103 milyon adet/yıl üretilmektedir.
              En hızlı büyüyen çiçek segmenti (+%45.7).

═══════════════════════════════════════════════════════════════
  🌻 8. AYÇİÇEĞİ (Helianthus annuus)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek
  Köken:      Kuzey Amerika, yaygın Türkiye
  Renk:       Sarı taç + Kahverengi merkez (klasik)
              Kırmızımsı, Turuncu varyantlar
  Anlamı:     Mutluluk, sadakat, uzun ömür, pozitif enerji ☀️
  Varyantlar:
  ├── Standart ayçiçeği (tek başlı, büyük)
  ├── Spray ayçiçeği (dallı, çok çiçekli)
  └── Süs ayçiçeği (küçük başlı, renkli)
  Mevsim:     Haziran-Eylül
  Ömür:       5-10 gün (vazoda)
  Boy:        60-180 cm
  Bakım:      Kolay
  Koku:       Yok / Hafif bitkisel
  Not:        Pozitif mesaj için en iyi çiçek. Hastane ziyaretlerinde
              ve "geçmiş olsun" için idealdir.

═══════════════════════════════════════════════════════════════
  🌺 9. HÜSNÜYUSUF (Dianthus barbatus)
═══════════════════════════════════════════════════════════════
  Türü:       Kesme çiçek / Bahçe çiçeği
  Köken:      Güney Avrupa, Türkiye
  Renk:       Pembe, Kırmızı, Beyaz, Bordo, İki renkli
  Anlamı:     Zarafet, nezaket, kibarlık
  Mevsim:     Mayıs-Temmuz
  Ömür:       7-10 gün (vazoda)
  Boy:        30-60 cm
  Koku:       Hafif, tatlı
  Not:        Türkiye'nin yükselen ihracat çiçeği. Son 5 yılda
              ihracatı 3 katına çıktı.

═══════════════════════════════════════════════════════════════
  🌿 10. OKALİPTÜS (Eucalyptus)
═══════════════════════════════════════════════════════════════
  Türü:       Yeşillik / Dolgu malzemesi
  Köken:      Avustralya, Akdeniz iklimi
  Renk:       Mavimsi yeşil, Gri-yeşil
  Anlamı:     Koruma, şifa, güç
  Mevsim:     Yıl boyu
  Ömür:       10-21 gün (vazoda) — en dayanıklı yeşillik
  Boy:        40-100 cm
  Koku:       Ferah, okaliptüs, mentol
  Kullanım:   Buketlerde dolgu, aranjmanlarda temel yeşillik

═══════════════════════════════════════════════════════════════
  DİĞER ÖNEMLİ ÇİÇEKLER:
═══════════════════════════════════════════════════════════════
  🏵️ Şakayık (Peony) — Haziran, sadece 4-6 hafta, lüks düğün çiçeği
     Anlamı: Zenginlik, şeref, romantizm
     Ömür: 5-7 gün ⏳ kısa — Fiyat: 50-150₺/dal (yüksek)

  🌿 Lavanta (Lavender) — Haziran-Ağustos, koku terapi
     Anlamı: Sakinlik, huzur, sadakat
     Kullanım: Buket, kurutmalık, yağ, kese

  💜 Sümbül (Hyacinth) — Mart-Nisan, yoğun koku
     Anlamı: Oyun, şaka, üzüntü (Yunan mitolojisi)
     Renk: Mor, Pembe, Beyaz, Mavi

  🌸 Frezya (Freesia) — Nisan-Haziran, tatlı koku
     Anlamı: Masumiyet, dostluk, güven
     7-10 gün vazoda

  🌼 Nergis (Daffodil/Narcissus) — Şubat-Nisan, bahar müjdecisi
     Anlamı: Yeniden doğuş, umut, bencillik (mit)
     Dikkat: Kesildikten sonra 6 saat suda bekletilmeli (sümüksü özsu)

  🌷 İris / Süsen (Iris) — Nisan-Mayıs
     Anlamı: Bilgelik, cesaret, umut
     Fransa'nın sembol çiçeği (Fleur-de-lis)

  🌼 Kasımpatı / Krizantem (yukarıda detaylı)

  💐 Ortanca (Hydrangea) — Haziran-Eylül
     Anlamı: Samimiyet, derin duygular, güzellik
     Bol su ister, 7-14 gün vazoda

  🌺 Açelya (Azalea) — Nisan-Mayıs
     Anlamı: Ilımlılık, tutku, geçici aşk
     Saksı çiçeği

  🌷 Yıldız çiçeği (Dahlia) — Temmuz-Ekim
     Anlamı: İçsel güzellik, zarafet, bağlılık
     Her renkte var, 200+ tür

  ⚜️ Lisianthus / Eustoma — Yıl boyu
     Anlamı: Takdir, minnettarlık, karizma
     Gül benzeri, 7-14 gün vazoda

  🌹 Gardenya (Gardenia) — Mayıs-Temmuz
     Anlamı: Gizli aşk, saflık, neşe
     Yoğun yasemin kokusu, 25-30°C sever

  🌴 Starliçe / Cennet Kuşu (Strelitzia) — Yıl boyu
     Anlamı: Cennet, özgürlük, ihtişam
     Egzotik, tropikal, 2-3 hafta vazoda
```

### 4.1-c Vazo Çeşitleri ve Özellikleri

```
═══════════════════════════════════════════════════════════════
  🏺 VAZO KATALOĞU
═══════════════════════════════════════════════════════════════
  Tüm vazolar isteğe bağlıdır. Müşteri vazosuz da sipariş verebilir.

  1. CAM VAZO (en çok tercih edilen)
  ├── Malzeme:         Soda camı, kristal cam
  ├── Alt türler:
  │   ├── Şeffaf cam    — klasik, her çiçekle uyumlu
  │   ├── Buzlu cam     — modern, mat görünüm
  │   ├── Renkli cam    — yeşil, mavi, pembe tonları
  │   └── El yapımı cam — üfleme, özel desenli
  ├── Fiyat aralığı:   30-100₺
  ├── Stok takibi:     Her alt tür için ayrı stok
  └── Avantaj:         Çiçeği öne çıkarır, her dekorasyona uyar

  2. SERAMİK VAZO
  ├── Malzeme:         Kil, seramik, taş tozu
  ├── Alt türler:
  │   ├── Sade seramik   — mat, el yapımı hissi
  │   ├── Sırlı seramik  — parlak, renkli
  │   ├── Geometrik      — modern, köşeli tasarım
  │   └── El yapımı      — her biri benzersiz, sınırlı sayı
  ├── Fiyat aralığı:   50-150₺
  ├── Stok durumu:     El yapımı olanlar sınırlı (1-5 adet)
  └── Avantaj:         Sıcak, doğal görünüm, uzun ömürlü

  3. KRİSTAL VAZO
  ├── Malzeme:         Kurşunlu/kurşunsuz kristal
  ├── Alt türler:
  │   ├── Sade kristal   — ışıltılı, şeffaf
  │   ├── Desenli        — kesme kristal, pırıltılı
  │   └── Renkli kristal — amber, mavi tonlar
  ├── Fiyat aralığı:   100-300₺
  ├── Stok:            Sınırlı, özel üretim
  └── Avantaj:         Lüks görünüm, özel gün hediyesi

  4. PORSELEN VAZO
  ├── Malzeme:         Porselen, ince işçilik
  ├── Alt türler:
  │   ├── Beyaz porselen — zarif, minimalist
  │   ├── Desenli        — el işi desen, çiçek motifli
  │   └── Altın varaklı  — lüks, elit
  ├── Fiyat aralığı:   60-200₺
  └── Avantaj:         Zarif, sofistike, özel koleksiyon

  5. METAL VAZO
  ├── Malzeme:         Çelik, alüminyum, pirinç, bakır
  ├── Alt türler:
  │   ├── Mat metal     — endüstriyel, modern
  │   ├── Tel örgü      — hasır görünümlü, el yapımı
  │   └── Pirinç/bakır  — vintage, zamana bırakılmış
  ├── Fiyat aralığı:   40-120₺
  └── Avantaj:         Modern/endüstriyel dekorasyon, dayanıklı

  6. PİŞMİŞ TOPRAK VAZO
  ├── Malzeme:         Pişmiş kil, terakota
  ├── Fiyat aralığı:   25-80₺
  └── Avantaj:         Doğal, rustik, bahçe havası

  ───────────────────────────────────────────────────────
  VAZO STOK DURUMU GÖSTERGELERİ:
  ├── 🟢 Bol stok (10+ adet)
  ├── 🟡 Sınırlı (3-9 adet)
  ├── 🔴 Son 1-2 adet
  ├── ⚫ Tükendi
  └── 💎 El yapımı (sınırlı sayı, tekil ürün)
```


### 4.2 Buket Oluşturucu

Müşteri kendi buketini oluşturabilir:

```
BUKET TASARIMI:
├── 1️⃣ Çiçek seç (gül, lilyum, papatya, orkide...)
├── 2️⃣ Renk teması seç (kırmızı, pembe, beyaz, karışık)
├── 3️⃣ Boyut seç (küçük/orta/büyük)
├── 4️⃣ Ekstra: yeşillik, kurdele, saksı
├── 5️⃣ Mesaj kartı yaz (dijital/basılı)
├── 6️⃣ Teslimat tarihi seç
└── 7️⃣ Kart notu: ZORUNLU
```

### 4.2-a Mesaj Kartı (Not) Zorunluluğu

```
KURAL: Her çiçek siparişinde MESAJ KARTI yazılması zorunludur.
├── Çiçek, fiziksel olmayan bir hediyedir
├── Alıcı, çiçeğin KİMDEN geldiğini ancak kart sayesinde bilir
├── Kartsız çiçek siparişi alınamaz ✅
└── Sipariş onaylanmadan önce kart notu girilmiş olmalıdır

MESAJ KARTI ÖZELLİKLERİ:
├── ✍️ Zorunlu alan (en az 10 karakter)
├── 💳 Dijital kart (PDF, siparişe eklenir)
├── 🖨️ Fiziksel kart (çiçekçi basar, bukete iliştirir)
├── 🌐 Teslimat anında kurye kartı da teslim eder
├── 📸 Müşteri kart tasarımını seçebilir (hazır şablonlar)
└── 📜 Kart metni sipariş özetinde görünür (alıcı hariç)

MESAJ KARTI TASARIMLARI:
├── 💕 Romantik: "Seni seviyorum, iyi ki varsın"
├── 🎂 Doğum Günü: "Nice mutlu yıllara..."
├── 👩 Anneler Günü: "İyi ki annemsin..."
├── 🏥 Geçmiş Olsun: "Çok geçmiş olsun, seni seviyoruz"
├── 💼 Kurumsal: "Başarılarınızın devamını dileriz"
├── 🕊️ Taziye: "Başınız sağ olsun..."
└── ✏️ Boş şablon: "Kendi notunu yaz"

TEKNİK:
├── DB'de sipariş tablosunda `kart_notu` alanı (TEXT, NOT NULL)
├── `kart_tasarimi` alanı (şablon seçimi)
├── `kart_turu` alanı ('dijital' / 'fiziksel')
└── Sipariş API'sinde kart notu zorunlu parametre
```

> Bu kural, çiçekçi modülüne özeldir. Diğer modüllerde (takside, yemekte) kart zorunluluğu yoktur.

### 4.3 Özel Gün Kategorileri

```
ÖZEL GÜN PAKETLERİ:
├── ❤️ Sevgililer Günü (14 Şubat)
├── 👩 Kadınlar Günü (8 Mart)
├── 👩 Anneler Günü (Mayıs)
├── 👨 Babalar Günü (Haziran)
├── 🎂 Doğum Günü
├── 💍 Evlenme Teklifi
├── 🏥 Geçmiş Olsun
├── 🕊️ Taziye / Cenaze
├── 🎓 Mezuniyet
├── 🎊 Yeni İş / Açılış
└── 📦 Özel Gün Paketi (kullanıcı tanımlar)
```

### 4.4 Tazelik Garantisi (Fotoğraflı)

```
TAZELİK KURALLARI:
├── 📸 Çiçekçi, sipariş anında buketin fotoğrafını çeker
├── 🤖 AI ile tazelik kontrolü (solma, sararma, kırık dal)
├── ⏰ fotoğraf zaman damgası
├── ✅ Taze: gönder → Müşteriye gider
├── ❌ Değilse: Çiçekçi uyarılır, yeni buket hazırlar
└── 📋 Müşteri teslimatta fotoğrafla karşılaştırır
```

### 4.5 Puanlama ve Yorum

- Ortak platform kuralları geçerlidir
- 1 sipariş = 1 yorum hakkı
- 3 oylama: Beğendim 👍 / Pas ⏭️ / Kötü 👎
- Ek kriter: Tazelik puanı (sistem otomatik hesaplar)
- Ek kriter: Zamanında teslimat puanı

---

## 5. TOPLANCI MODÜLÜ

### 5.1 Toptancı Özellikleri

```
TOPLANCI PANELİ:
├── Üreticilerden ürün listeleme
├── Fiyatlandırma (kendi marjını ekler)
├── Minimum sipariş adedi (çiçekçiler için)
├── Stok yönetimi (çoklu üretici)
├── Çiçekçilere özel fiyat listesi
├── Soğuk hava deposu takibi
├── Sevkiyat yönetimi (kendi filosu / platform kuryesi)
└── Raporlama (en çok satan, fire oranı, vb.)
```

### 5.2 Çiçek Sınıflandırma

```
SINIFLANDIRMA:
├── 1. Sınıf: En kaliteli, tam açmış, hasarsız
├── 2. Sınıf: Küçük kusurlu, yarım açmış
├── 3. Sınıf: İndirimli, hızlı tüketilmeli
└── Fire: Satılamaz, atık
```

---

## 6. ÜRETİCİ (ÇİFTÇİ) MODÜLÜ

### 6.1 Üretici Paneli

```
ÜRETİCİ PANELİ:
├── 🌱 Hasat Takvimi
│   ├── Ne zaman hangi çiçeğin hasat dönemi?
│   ├── Güncel hasat durumu (kg/adet)
│   └── Gelecek hasat tahmini
├── 📸 Günlük fotoğraf
│   ├── Tarla/sera güncel durumu
│   └── Müşteri (toptancı) güveni için
├── 💰 Fiyat belirleme
│   ├── Sezonluk fiyat listesi
│   └── Minimum fiyat uyarısı
├── 📦 Sipariş yönetimi
│   ├── Toptancılardan gelen siparişler
│   ├── Hasat + paketleme + gönderim
│   └── Teslimat onayı
└── 📊 Raporlar
    ├── Aylık satış
    ├── Fire oranı
    └── Müşteri memnuniyeti
```

### 6.2 Hasat Takvimi Entegrasyonu

```
ÖRNEK TAKVİM:
┌────────────┬───────┬───────┬───────┬───────┬───────┐
│  ÇİÇEK     │ NİSAN │ MAYIS │ HAZİR │ TEMMU │ AĞUST │
├────────────┼───────┼───────┼───────┼───────┼───────┤
│ Gül        │   x   │   x   │   x   │   x   │   x   │
│ Lilyum     │       │   x   │   x   │   x   │       │
│ Papatya    │   x   │   x   │   x   │       │       │
│ Karanfil   │   x   │   x   │   x   │   x   │   x   │
└────────────┴───────┴───────┴───────┴───────┴───────┘
```

---

## 7. MALZEME TEDARİKÇİLERİ MODÜLÜ

### 7.1 Tedarikçi Türleri

| Tedarikçi | Ürün | Puanlama Kriteri |
|-----------|------|------------------|
| 📦 **Saksı Üreticisi** | Seramik, plastik, hasır, beton saksı | Kırılma oranı, desen kalitesi |
| 📦 **Kağıt/Ambalajcı** | Buket kağıdı, hediye kutusu, kurdele | Renk haslığı, dayanıklılık |
| 📦 **Çiçek Süngeri** | Su tutan sünger, strafor | Su tutma kapasitesi |
| 📦 **Tel/Çıta** | Buket teli, çıta, bant | Paslanma, esneklik |
| 📦 **Gübre/Toprak** | Saksı toprağı, sıvı gübre | Organik sertifika |
| 📦 **Kart/Matbaa** | Mesaj kartı, etiket, logo baskı | Baskı kalitesi |

### 7.2 Tedarikçi → Çiçekçi İlişkisi

```
TEDARİK SİPARİŞ AKIŞI:
├── Çiçekçi, malzeme tedarikçisinden doğrudan sipariş verir
├── Platform üzerinden %2 komisyon
├── Min. sipariş adedi (tedarikçi belirler)
├── Stok takibi (çiçekçinin deposu)
└── Otomatik yenileme (sünger, kağıt gibi sürekli tüketilenler)
```

---

## 8. SİPARİŞ VE TESLİMAT SÜRECİ

### 8.1 Müşteri Sipariş Akışı

```
ADIM 1: KEŞİF
├── 🟢 Aktif dükkanları keşfet (konum bazlı)
├── 🔴 Pasif dükkanlar: "Şu an kapalı" etiketiyle gösterilir
├── Kategorilere göz at (doğum günü, sevgili...)
├── Özel gün paketlerini gör
└── Kendi buketini oluştur

ADIM 2: SİPARİŞ
├── Çiçekçi seç (sadece aktif dükkanlar)
├── Ürün/Buket seç (hazır veya özel sipariş)
├── Boyut seç (küçük 150₺, orta 250₺, büyük 400₺)
├── Mesaj kartı yaz (ZORUNLU)
├── 📍 TESLİMAT ŞEKLİ SEÇ (ZORUNLU)
│   ├── 🚚 Kurye ile adresime gelsin
│   ├── 🏪 Dükkandan kendim alırım
│   └── 📍 Kuryeden belirlediğim noktada alırım
├── Teslimat adresi / buluşma noktası
├── Teslimat tarihi ve saati
└── Ödeme (cüzdan/kart/kapıda nakit bildirimli)

ADIM 3: HAZIRLIK
├── Çiçekçi siparişi alır
├── Dükkan aktif mi kontrol et
├── Buketi hazırlar
├── Fotoğraf çeker (tazelik kontrolü)
├── Paketler + mesaj kartı ekler
└── Kuryeye verir / Dükkana hazır koyar

ADIM 4: TESLİMAT
├── 🚚 Kurye ile: Kurye müşteriye gider
│   ├── QR kod / SMS yetki ile teslim
│   └── Müşteri teslim alır
├── 🏪 Dükkandan: Müşteri dükkana gelir
│   ├── QR kod okutur
│   └── Çiçeği teslim alır
├── 📍 Noktada: Müşteri kurye ile buluşur
│   ├── Canlı takip
│   └── Noktada teslim alır
├── Müşteri fotoğrafla karşılaştırır
└── Yorum/puan bırakır
```

### 8.2 Teslimat Şekilleri

Müşteri, çiçeği **3 farklı şekilde** teslim alabilir:

```
═══════════════════════════════════════════════════════════════
  🚚 TESLİMAT ŞEKLİ SEÇİMİ (ZORUNLU)
═══════════════════════════════════════════════════════════════
  Her siparişte müşteri teslimat şeklini seçmek ZORUNDADIR.
  Varsayılan: Kurye Teslimi

  1️⃣ KURYE İLE TESLİM (Varsayılan)
  ┌─────────────────────────────────────────────┐
  │  🚚 Kurye ile adresime teslim edilsin      │
  └─────────────────────────────────────────────┘
  ├── Kurye, çiçekçiden alır → müşterinin adresine gider
  ├── Teslimat adresi girilir (adres defterinden seç)
  ├── QR kod / SMS kod ile teslimat onayı
  ├── Müşteri kapıda teslim alır
  ├── Ek ücret: Kurye ücreti (mesafeye göre 15-40₺)
  └── NOT: Müşteri adreste yoksa → kurye bekler (5 dk) → arar → iade

  2️⃣ DÜKKANDAN TESLİM AL (Müşteri kendisi alır)
  ┌─────────────────────────────────────────────┐
  │  🏪 Dükkandan kendim alacağım              │
  └─────────────────────────────────────────────┘
  ├── Müşteri, çiçekçi dükkanına gidip teslim alır
  ├── Kurye ücreti YOK (0₺)
  ├── Müşteri, siparişi hazır olduğunda gelir
  ├── "Hazır" bildirimi → müşteriye SMS/push
  ├── Dükkanda QR kod okutarak teslim alır
  ├── Müşteri çiçeği görür, beğenmezse değiştirme hakkı (1 kez)
  └── NOT: Sipariş hazır olmadan dükkana gidilmez

  3️⃣ KURYEDEN TESLİM AL (Belirlenen noktada)
  ┌─────────────────────────────────────────────┐
  │  📍 Kuryeden belirlediğim noktada alacağım │
  └─────────────────────────────────────────────┘
  ├── Müşteri, kurye ile belirli bir noktada buluşur
  ├── Örn: "İş çıkışı metro çıkışında kuryeden alayım"
  ├── Müşteri, buluşma noktasını haritada işaretler
  ├── Kurye o noktaya gelir, müşteri teslim alır
  ├── Kurye ücreti: Normalin %50'si (kısa mesafe)
  ├── Müşteri kuryeyi canlı takip eder
  └── NOT: Müşteri buluşma noktasına gelmezse → kurye 5 dk bekler

  ───────────────────────────────────────────────────────────
  SEÇİM EKRANI (Mobil/Web):
  
  ┌──────────────────────────────────────────────┐
  │  📍 Teslimat Şekli                          │
  │                                              │
  │  ○ 🚚 Kurye ile adresime gelsin             │
  │       └── 📝 Adres: Moda, Kadıköy           │
  │       └── 💰 +25₺ kurye ücreti              │
  │                                              │
  │  ○ 🏪 Dükkandan kendim alırım              │
  │       └── 📍 Çiçekçi: 500m uzakta            │
  │       └── 💰 Kurye ücreti yok ✅             │
  │       └── ⏰ Hazır olunca gelirim            │
  │                                              │
  │  ○ 📍 Kuryeden noktada alırım               │
  │       └── 🗺️ Buluşma noktası seç            │
  │       └── 💰 +12₺ kurye ücreti (yarım)      │
  │       └── 📱 Kuryeyi canlı takip             │
  └──────────────────────────────────────────────┘
```

### 8.2-b Teslimat Zamanı Seçenekleri

| Seçenek | Açıklama | Ek Ücret | Hangi Teslimat Şekli |
|---------|----------|----------|----------------------|
| 🚚 Bugün Teslimat | 2 saat içinde | +20 ₺ | Kurye / Kuryeden Al |
| 📅 Tarihli Teslimat | İleri bir tarih seçimi | Yok | Tümü |
| ⏰ Randevulu Teslimat | Belirtilen saatte | +10 ₺ | Kurye / Kuryeden Al |
| 🎁 Sürpriz Teslimat | Alıcıya haber vermeden | +10 ₺ | Kurye |
| 🏪 Mağazadan Al | Hazır olunca gelirim | Yok | Dükkandan Al

### 8.3 Özel Gün Hatırlatıcı

```
HATIRLATICI SİSTEMİ:
├── Müşteri, takvimine özel günler ekler
│   ├── Eşinin doğum günü (14 Mayıs)
│   ├── Yıldönümü (5 Haziran)
│   └── Anneler Günü (Mayıs 2. Pazarı)
├── Sistem 7 gün kala anında bildirim gönderir
├── "Geçen sene X çiçekçisinden almıştın" hatırlatması
├── Tek tıkla aynı siparişi tekrarla
└── Her hatırlatmadan platform para kazanmaz (sadakat)
```

---

## 9. KOMİSYON YAPISI

### 9.1 Kademeli Komisyon

```
ZİNCİR BOYUNCA:
├── Üretici → Toptancı: %2
├── Toptancı → Çiçekçi: %2
├── Çiçekçi → Müşteri: %2
│
├── Malzeme Tedarikçisi → Çiçekçi: %2
│
└── ÖRNEK: 100₺'lik gül
    ├── Üretici satar: 30₺ → platform: 0.60₺
    ├── Toptancı satar: 60₺ → platform: 1.20₺
    ├── Çiçekçi satar: 100₺ → platform: 2.00₺
    └── TOPLAM PLATFORM: 3.80₺
```

### 9.2 Neden Düşük Komisyon İşe Yarar?

```
GELENEKSEL ÇİÇEKÇİ:
├── Toptancıdan alış: 60₺ (üretici 30₺)
├── Müşteriye satış: 150₺ (%150 marj)
├── Platform komisyonu: 3₺ (%2)
├── Çiçekçiye kalan: 87₺
└── Rakipler %25 komisyon alsa: Çiçekçiye 37₺ kalır

YANİ:
├── Çiçekçi %2 ile çok daha fazla kazanır
├── Veya daha düşük fiyat verip daha çok satar
└── Platform zincirin her halkasından kazanır
```

### 9.3 İndirim Politikası: Platform İndirim Yapmaz, Dükkan Sahibi Yapar

```
═══════════════════════════════════════════════════════════════════
  KRİTİK KURAL: Platform site genelinde İNDİRİM YAPMAZ.
═══════════════════════════════════════════════════════════════════

NEDEN?
├── Platform %2 komisyonla çalışır (rakipler %25-30)
├── %2'den indirim yapmak = zarar etmek
├── İndirim yapacak marjımız YOK
├── Bu bilinçli bir tercihtir
└── Düşük komisyon = zaten düşük fiyat

NASIL ÇALIŞIR?
├── Her ürünün fiyatını DÜKKAN SAHİBİ belirler
├── Dükkan sahibi KENDİ KAR MARJINDAN indirim yapabilir
├── Platform komisyonu SABİTTİR (%2), indirimden etkilenmez
├── Dükkan sahibi kampanya panelinden istediği ürüne indirim tanımlar
└── Müşteriye "🔥 Fırsat" etiketi olarak gösterilir

DÜKKAN SAHİBİ İNDİRİM PANELİ:
┌─────────────────────────────────────────────┐
│  🏪 Kampanya Yönetimi                       │
│                                             │
│  Platform %2 komisyon alır, indirimleri     │
│  sen belirlersin.                           │
│                                             │
│  ☑ 🔥 Mini Orkide Sepeti · %20 indirim     │
│    (Normal: 400₺ → Şimdi: 320₺)            │
│    ← Sen belirledin                         │
│                                             │
│  ☐ 🌹 Kırmızı Gül Buketi · 50₺ indirim     │
│    ← Pasif                                  │
│                                             │
│  [Yeni kampanya adı.............] [Ekle]    │
│                                             │
│  ℹ️ Platform indirim yapmaz. İndirim        │
│  tutarı senin kar marjından düşer.          │
│  %2 komisyon sabittir.                      │
└─────────────────────────────────────────────┘

RAKİPLERLE KARŞILAŞTIRMA:
┌─────────────────────┬───────────┬──────────┐
│                     │ Rakipler  │ Biz      │
├─────────────────────┼───────────┼──────────┤
│ Komisyon            │ %25-30    │ %2       │
│ Site-wide indirim   │ %20-50    │ YOK ❌   │
│ Dükkan indirimi     │ Kısıtlı   │ Tam yetki│
│ Müşteriye fiyat     │ Yüksek    │ Düşük    │
│ Çiçekçi karı        │ Düşük     │ Yüksek   │
└─────────────────────┴───────────┴──────────┘

ÖZET:
├── Platform asla "site geneli %20 indirim" yapmaz
├── Her dükkan sahibi kendi indirimini belirler
├── Düşük komisyon = düşük fiyat = mutlu müşteri
└── Çiçekçi kendi karını yönetir, platform karışmaz
```

---

## 10. ÖZEL GÜN TAKVİMİ VE HATIRLATMA

### 10.1 Türkiye Özel Gün Takvimi

| Tarih | Gün | Önerilen Kategori |
|-------|-----|-------------------|
| 14 Şubat | Sevgililer Günü | ❤️ Kırmızı gül, orkide |
| 8 Mart | Kadınlar Günü | 👩 Renkli buketler |
| Mayıs 2. Pazar | Anneler Günü | 👩 Pembe gül, lilyum |
| Haziran 3. Pazar | Babalar Günü | 👨 Orkide, erkek çiçeği |
| 12-18 Mayıs | Vakıflar Haftası | 🏢 Ofis çiçeği |
| 29 Ekim | Cumhuriyet Bayramı | 🇹🇷 Kırmızı-beyaz |
| 10 Mayıs | Anneler Günü (alternatif) | 👩 Karışık buket |
| Yıl boyu | Doğum Günleri | 🎂 Müşteri tanımlar |
| Yıl boyu | Yıldönümleri | 💍 Müşteri tanımlar |

---

## 11. MÜŞTERİ YORUM + ÖDÜL SİSTEMİ (Purchase-to-Review)

### 11.1 Felsefe: "Önce Satın Al, Sonra Yorum Yap"

```
Yorum yapmak bir HAK'tır, satın alarak kazanılır.
Sadece doğrulanmış alışverişi olan kullanıcılar yorum yapabilir.
Bu sistem:
├── Sahte yorumları engeller
├── Güven oluşturur (her yorum "✅ Doğrulanmış" etiketli)
├── Müşteriyi sipariş sonrası etkileşimde tutar
└── Kaliteli geri bildirim sağlar
```

### 11.2 Yorum Akışı (Order-to-Review)

```
SİPARİŞ → ÖDEME → HAZIRLIK → FOTOĞRAF ONAYI → TESLİMAT → YORUM HAKKI
  1         2          3            4              5           6

ADIM 1: Müşteri sipariş verir + öder
ADIM 2: Çiçekçi hazırlar
ADIM 3: Fotoğraf çekilir → müşteri onaylar
ADIM 4: Kurye teslim eder
ADIM 5: Yorum ekranı AÇILIR (önceden görünmez)
ADIM 6: Müşteri yıldız verir + yorum yazar → ödül kazanır
```

### 11.3 Ödül Mekanizması (Rating-based Rewards)

| Müşteri Puanı | Ödül (Sadakat Puanı) | Mesaj |
|--------------|---------------------|-------|
| ⭐⭐⭐⭐⭐ (5 yıldız) | +25 puan | "Harika! 25 puan kazandınız 🎉" |
| ⭐⭐⭐⭐ (4 yıldız) | +25 puan | "Harika! 25 puan kazandınız 🎉" |
| ⭐⭐⭐ (3 yıldız) | +15 puan | "Teşekkürler! 15 puan kazandınız" |
| ⭐⭐ (2 yıldız) | +10 puan | "Geri bildiriminiz için teşekkürler" |
| ⭐ (1 yıldız) | +10 puan | "Geri bildiriminiz için teşekkürler" |

```
AMAÇ: Müşteriyi yorum yapmaya teşvik etmek
├── Yüksek puan = yüksek ödül (memnuniyeti pekiştir)
├── Düşük puan = düşük ödül (ama yine de teşekkür)
├── Puanlar → sadakat sisteminde birikir → indirim/bedava buket
└── Her siparişte harcanan her 25₺ = 1 puan (temel kazanç)
```

### 11.4 UI'da Görünüm

```
⭐ Müşteri Yorumları (4.9⭐ · 48 yorum)
┌─────────────────────────────────────┐
│ ✅ Sadece doğrulanmış alışverişi    │
│   olan kullanıcılar yorum yapabilir  │
├─────────────────────────────────────┤
│ 👩 Ayşe K. ✅ Doğrulanmış            │
│ ★★★★★                               │
│ "Harika bir buket!"                  │
├─────────────────────────────────────┤
│ 👨 Mehmet T. ✅ Doğrulanmış           │
│ ★★★★★                               │
│ "Sevgilim çok mutlu oldu 🌹"         │
└─────────────────────────────────────┘

YORUM EKRANI (sadece teslimattan sonra):
┌─────────────────────────────────────┐
│ ✅ Doğrulanmış Alışveriş            │
│ Bu siparişi satın aldığınız için    │
│ yorum yapmaya hak kazandınız.       │
│                                     │
│ Buket nasıldı?                      │
│ ☆ ☆ ☆ ☆ ☆  ← tıkla puan ver         │
│                                     │
│ [Yorumun...                    ]    │
│                                     │
│ [💬 Yorum Gönder · +10/25 Puan]     │
│ Yorumunuz adınızın baş harfiyle     │
│ yayınlanır.                         │
└─────────────────────────────────────┘
```

### 11.5 Kullanıcı Profilinde Yorum Geçmişi

Her kullanıcının profilinde:
- Toplam yorum sayısı
- Ortalama verdiği puan
- "Yardımcı" oyları (diğer kullanıcılar faydalı buldu mu?)
- En son yorumları

---

## 12. DB ŞEMASI (ÖZET)

```sql
-- Ana tablolar (detaylı şema DATABASE.md'de)

-- Çiçek üreticisi profili (bireysel_hesap 1:1)
cicek_ureticisi_profil (
  id, hesap_id, uretim_turu, kapasite, alan_buyuklugu,
  organik_sertifika, globalgap, hasat_takvimi_json
)

-- Toptancı profili (kurumsal_hesap 1:1)
toptanci_profil (
  id, hesap_id, depo_adresi, soguk_depo, min_siparis,
  sevkiyat_turu, calisma_bolgesi
)

-- Çiçekçi profili (kurumsal_hesap / bireysel + esnaf)
cicekci_profil (
  id, hesap_id, dukkan_adi, vitrin_fotografi,
  teslimat_secenekleri_json, calisma_saatleri,
  ozel_gun_paketleri_json, buket_tasarimlari_json
)

-- Malzeme tedarikçisi
malzeme_tedarikci (
  id, hesap_id, tedarik_turu, urun_listesi_json,
  min_siparis, sevkiyat_kosullari
)

-- Ürünler (çiçek)
cicek_urun (
  id, satici_id, satici_turu, isim, kategori,
  fiyat, boyut, stok_adet, fotograflar_json,
  tazelik_puani, mevsim_durumu, aktif
)

-- Sipariş zinciri
siparis_zinciri (
  id, urun_id, alici_id, alici_turu, satici_id,
  satici_turu, miktar, birim_fiyat, toplam,
  komisyon, durum, tarih
)

-- Özel gün hatırlatıcı
ozel_gun_hatirlatma (
  id, musteri_id, isim, tarih, tur, tekrar_yillik,
  onceki_siparis_id, aktif
)
```

---

> 📌 **Not:** Bu doküman çiçek modülünün kavramsal tasarımıdır. Detaylı API, DB şeması ve ön yüz akışları için ilgili alt dokümanlara bakınız. Tüm modüller platformun ortak altyapısını (kurye, ödeme, puanlama, cüzdan) kullanır.

---

## 12. ÇİÇEKÇİ ZORUNLU GÖRSEL SİSTEMİ

> Yemek sistemindeki 6+ zorunlu restoran görseline benzer şekilde, her çiçekçinin de belirli kategorilerde görsel yüklemesi zorunludur.

### 12.1 Zorunlu Görsel Kategorileri

Her çiçekçinin aşağıdaki **5 kategoride** en az 1'er fotoğraf yüklemesi zorunludur:

```
📸 ZORUNLU GÖRSELLER:
├── 1️⃣ DÜKKAN VİTRİNİ / DIŞ CEPHE
│   ├── Dükkanın sokak görünümü
│   ├── Tabela net okunur olmalı
│   └── Vitrin düzeni görünmeli
│
├── 2️⃣ ÇALIŞMA ALANI / ATÖLYE
│   ├── Buket hazırlama tezgahı
│   ├── Çiçek düzenleme alanı
│   └── Temizlik ve düzen görünür
│
├── 3️⃣ SOĞUK HAVA DEPOSU / STOK ALANI
│   ├── Çiçeklerin saklandığı alan
│   ├── Sıcaklık ve nem koşulları
│   └── Varsa soğutma sistemi
│
├── 4️⃣ TESLİMAT ARACI (varsa)
│   ├── Araç dış görünümü
│   ├── İç taşıma düzeni
│   └── Varsa soğutmalı bölme
│
└── 5️⃣ BUKET ÖRNEKLERİ (en az 3 farklı)
    ├── Farklı boy ve renklerde
    ├── Gerçek çiçek (stok fotoğraf yasak)
    └── Son 30 gün içinde çekilmiş
```

### 12.2 Görsel Kalite Standartları

| Kriter | Şart | Puan |
|--------|------|------|
| Minimum çözünürlük | 1920x1080 | - |
| Netlik | Bulanık olmayacak | +5/her net foto |
| Aydınlatma | Doğal/yapay yeterli ışık | +5 |
| Filtresiz | Orijinal renkler | +5 |
| Tarih damgası | Son 30 gün içinde çekilmiş | +10 |
| Geotag | Dükkan konumu eşleşiyor | +10 |

### 12.3 Görsel Eksiklik Durumları

| Durum | Yaptırım |
|-------|----------|
| 0-1 fotoğraf | Dükkan pasif, sipariş alınamaz |
| 2-3 fotoğraf | Sadece %50 kapasite sipariş |
| 4 fotoğraf | Tam kapasite, eksik kategoriler belirtilir |
| 5+ fotoğraf | Tam kapasite + öne çıkarma |

### 12.4 Periyodik Görsel Yenileme

Çiçekçilerin görsellerini **her 90 günde bir** yenilemesi zorunludur:

- Yenilenmeyen görseller eski olarak işaretlenir (-5 puan)
- 120 günü geçen görsel otomatik silinir
- Yenileme hatırlatması: 75., 80., 85. günlerde SMS/E-posta

---

## 13. CANLI KAMERA ENTEGRASYONU

### 13.1 Sistem Tanımı

Çiçekçiler, buket hazırlama alanında **canlı kamera** yayını açabilir. Tamamen opsiyoneldir ancak **+100 puan** bonusu sağlar.

### 13.2 Kamera Şartları

| Kriter | Zorunluluk |
|--------|-----------|
| Minimum çözünürlük | 720p (1280x720) |
| Minimum FPS | 15 |
| Ses | Sadece ortam sesi (mikrofon kapalı opsiyonel) |
| Kayıt saklama | Son 7 gün (sadece şikayet durumunda erişim) |
| Yayın gecikmesi | Maksimum 5 saniye |
| Çalışma saati | Dükkan açıkken yayın zorunlu |
| Kamera açısı | Tezgah ve buket hazırlama alanı net görünmeli |

### 13.3 Puan Katkısı

```
CANLI KAMERA PUAN HESABI:
├── Kamera var, aktif ve şartlara uygun:    +100 puan
├── Kamera var ama günde 1+ saat kapalı:    +50 puan
├── Kamera var ama günde 3+ saat kapalı:    +0 puan (ceza yok)
├── Kamera yok:                              +0 puan (ceza yok)
└── Kamera yayını kesintili/gecikmeli:       +25 puan
```

### 13.4 Müşteri Deneyimi

- Müşteri, sipariş öncesi canlı atölye izleyebilir
- Sipariş sonrası "Atölye Canlı" butonu ile yayına bağlanabilir
- Yayın sırasında ekran görüntüsü alınamaz (DRM koruması)
- Müşteri, yayında şikayet edecek bir durum görürse anlık bildirim gönderebilir

---

## 14. EVRAK BAZLI PUANLAMA (Çiçek Sistemi)

> ⚠️ **Görsel Zorunluluğu:** Sertifika ve izin evraklarının **fotoğrafı/tarayıcı görüntüsü** yüklenmelidir. Sadece evrak adı girmek puan kazandırmaz.

### 14.1 Puanlandırılabilir Evraklar

| Evrak | Puan | Açıklama |
|-------|------|----------|
| Hijyen Sertifikası (temel) | +25 | Zorunlu, gelirse puan |
| Soğuk Hava Depo Belgesi | +20 | Varsa |
| TSE Belgesi | +20 | Türk Standartları |
| Organik Çiçek Sertifikası | +25 | Organik üretim onayı |
| GlobalGAP Sertifikası | +30 | Uluslararası tarım standardı |
| İyi Tarım Uygulamaları | +20 | Tarım Bakanlığı onaylı |
| İşletme Sigorta Poliçesi | +20 | İş yeri sigortası |
| Ürün Sorumluluk Sigortası | +25 | Müşteriye karşı sorumluluk |
| Nakliye Ruhsatı | +15 | Çiçek taşıma aracı |
| Deprem Güvenlik Raporu | +10 | Yapı güvenliği |
| İSG (İş Sağlığı Güvenlik) | +15 | İş güvenliği raporu |
| Sürdürülebilirlik Raporu | +10 | Çevre dostu uygulamalar |
| Yerli Üretici İşbirliği Belgesi | +15 | Doğrudan üreticiden alım |

### 14.2 Toplam Evrak Puanı

```
TOPLAM PUAN: 0 - 230 arası
├── 0-50:     Başlangıç seviyesi 🟢
├── 51-100:   Standart çiçekçi 🟡
├── 101-150:  Güvenilir çiçekçi 🟠
├── 151-200:  Premium çiçekçi 🔵
└── 201+:     Elit çiçekçi 🟣
```

---

## 15. TAZELİK GARANTİSİ VE ZAMAN DAMGASI

### 15.1 Çiçek Tazeliği Sistemi

```
TAZELİK ZİNCİRİ:
├── 🌱 Üretici: Hasat zamanı damgası (AI ile doğrulama)
│   ├── Fotoğraf (hasat anı) + koordinat
│   └── Sistem: "⚠️ 3 gün önce hasat" uyarısı
│
├── 📦 Toptancı: Giriş zaman damgası
│   ├── Soğuk depoya giriş saati
│   └── Çıkış saati (çiçekçiye gönderim)
│
├── 🏪 Çiçekçi: Teslim alma + hazırlık damgası
│   ├── Toptancıdan alış saati
│   ├── Soğukta bekleme süresi
│   └── Buket hazırlama anı fotosu
│
└── 🚚 Müşteri: Teslim anı damgası (QR ile)
```

### 15.2 Tazelik Puanı ve Uyarılar

```
TAZELİK PUANI (Sistem otomatik hesaplar):
├── Hasat → Müşteri arası geçen süre
├── 0-24 saat:  🟢 Çok taze (100 puan)
├── 24-48 saat: 🟡 Taze (80 puan)
├── 48-72 saat: 🟠 Orta (60 puan)
├── 3-5 gün:    🔴 Dikkat (40 puan)
└── 5+ gün:     ⚫ Satılamaz (0 puan, otomatik pasif)

SİSTEM UYARILARI:
├── 72+ saat:  "Bu çiçek yakında solar, hızlı tüketin"
├── 5+ gün:    Çiçekçiye "Bu ürünü satamazsın" uyarısı
├── AI tazelik kontrolü:
│   ├── Solma, sararma, kırık dal tespiti
│   ├── Fotoğraf analizi (yapay zeka)
│   └── Taze değilse → Çiçekçiye "yenile" uyarısı
└── Müşteriye teslimatta:
    ├── "Bu çiçek 2 gün önce hasat edildi 🟡"
    └── Tahmini vazo ömrü: "7-10 gün"
```

### 15.3 Zaman Damgası Zinciri

```
ZAMAN DAMGASI KAYITLARI:
├── Hasat: {tarih, saat, koordinat, foto}
├── Toptancı giriş: {tarih, saat, depo_no}
├── Toptancı çıkış: {tarih, saat, araç_no}
├── Çiçekçi alış: {tarih, saat, çiçekçi_id}
├── Buket hazırlık: {tarih, saat, foto}
├── Paketleme: {tarih, saat}
├── Kurye alış: {tarih, saat}
└── Teslimat: {tarih, saat, QR_onay}

ZİNCİR KIRILIRSA:
├── Eksik damga → otomatik uyarı
├── 2+ eksik damga → puan kırılımı (-20)
├── Sahte damga → -50 puan + inceleme
└── Zincir tam → "✅ Tazelik Garantili" rozeti
```

---

## 16. ÇİFT YÖNLÜ PUANLAMA SİSTEMİ

### 16.1 Puanlama Üçgeni

Her sipariş sonrası **3 taraf** birbirini puanlar:

```
     MÜŞTERİ
     ╱       ╲
    ╱         ╲
ÇİÇEKÇİ ──── KURYE
```

| Gönderen | Alan | Puan Kriterleri |
|----------|------|----------------|
| Müşteri | Çiçekçi | Tazelik, sunum, tasarım, kart mesajı, zamanlama |
| Müşteri | Kurye | Hız, nezaket, paket durumu, iletişim |
| Çiçekçi | Müşteri | İletişim, adres doğruluğu, teslim alma hızı |
| Çiçekçi | Kurye | Bekleme süresi, paket taşıma kalitesi |
| Kurye | Çiçekçi | Hazırlık süresi, paketleme kalitesi |
| Kurye | Müşteri | Adres bulma kolaylığı, bekleme süresi |

### 16.2 Puan Aralığı ve Ağırlıklar

```
PUAN ARALIĞI: 1.0 - 5.0 (0.1 hassasiyet)

AĞIRLIKLI ORTALAMA HESABI (Çiçekçi):
├── Müşteri → Çiçekçi: %45
├── Kurye → Çiçekçi:    %15
├── Evrak bazlı puan:    %25
├── Canlı kamera:        %10
├── Tazelik puanı:       %5
└── TOPLAM:              %100
```

### 16.3 Puan Kuralları

- **Müşteri** puansız bırakırsa: 24 saat sonra varsayılan 4.0
- **Çiçekçi** puansız bırakırsa: 48 saat sonra varsayılan 4.0
- **Kurye** puansız bırakırsa: 12 saat sonra varsayılan 4.0
- Oy kullanmayan tarafın bir sonraki puanı %10 daha ağırlıklı

### 16.4 Sıralama (Reklam Satın Alınamaz)

```
SIRALAMA FORMÜLÜ:
├── Puan tabanlı (4.5+ → üst sıra)
├── Teslimat süresi (hızlı → üst sıra)
├── Görsel kalitesi (yüksek çöz. → öne çıkarma)
├── Canlı kamera (+100 puan avantaj)
├── Tazelik puanı (yüksek → üst sıra)
├── Aktif sipariş sayısı (popülerlik)
└── REKLAMLA SIRALAMA SATILMAZ
```

### 16.5 Puan Kırıcılar ve Cezalar

| İhlal | Puan Etkisi | Süre |
|-------|-----------|------|
| Solmuş çiçek gönderme | -2.0 | 30 sipariş |
| Eksik ürün (yanlış sayı) | -1.0 | 20 sipariş |
| Geç teslimat (%50 üzeri) | -0.5 | 20 sipariş |
| Kötü paketleme (ezik/devrik) | -0.7 | 25 sipariş |
| Müşteriye kötü davranış | -2.0 | 50 sipariş |
| Kart mesajı unutma | -1.5 | 15 sipariş |
| Sahte tazelik damgası | -5.0 (kalıcı ban) | Süresiz |
| Hijyen şikayeti (kanıtlı) | -3.0 | 100 sipariş |
| Kurye mobing | -1.5 | 40 sipariş |
| Fotoğrafta stok görsel kullanma | -1.0 | 20 sipariş |

---

## 17. DİNAMİK TESLİMAT SÜRESİ HESAPLAMA

### 17.1 Süre Bileşenleri

```
TESLİMAT SÜRESİ = HAZIRLIK + KURYE_TOP + HAVA + TRAFİK

HAZIRLIK SÜRESİ:
├── Hazır ürün: 15-30 dk (çiçekçinin belirlediği)
├── Özel sipariş: 60-120 dk (+1 gün ileri tarih)
├── Yoğunluk katsayısı: x1.0 (normal) / x1.5 (yoğun gün)
│   └── Örn: Sevgililer Günü, Anneler Günü
└── Çiçekçi geçmişine göre otomatik ayarlama
    ├── Son 10 sipariş ortalaması
    ├── Gecikme varsa +%10
    └── Hızlıysa -%5

KURYE TOPLAMA SÜRESİ:
├── Kuryenin çiçekçiye gelişi
├── Mesafe: kurye_konum → çiçekçi
├── Hava durumu: yağmur/sis/karda +%15-30
└── Trafik: yoğun saatlerde +%10-20

KURYE TESLİMAT SÜRESİ:
├── Çiçekçi → müşteri adresi
├── Mesafe hesaplama (harita API)
├── Hava durumu etkisi
├── Trafik durumu
└── Teslimat şekli:
    ├── Kurye adrese: normal
    ├── Kurye noktada: -%20 (kısa mesafe)
    └── Dükkandan al: 0 (kurye yok)
```

### 17.2 Süre Hesaplama API'si

```
GET /api/cicekci/{id}/teslimat-suresi?adres=...
Response:
{
  "hazirlik_dk": 25,
  "kurye_toplama_dk": 8,
  "kurye_teslimat_dk": 12,
  "hava_etkisi": 1.15,
  "trafik_etkisi": 1.1,
  "toplam_dk": 52,
  "guven_araligi": "45-60 dk",
  "uyari": "🌧️ Yağmur nedeniyle +%15 gecikme olabilir"
}
```

---

## 18. AKIŞ DİYAGRAMLARI

### 18.1 Çiçekçi Kayıt ve Aktivasyon

```
ÇİÇEKÇİ: KURUMSAL HESAP AÇAR / BİREYSEL + ESNAF ROLÜ
         │
         ▼
ÇİÇEKÇİ: TEMEL BİLGİLERİ GİRER (dükkan adı, adres, konum)
         │
         ▼
ÇİÇEKÇİ: ZORUNLU BELGELERİ YÜKLER (vergi, ruhsat, hijyen...)
         │
         ▼
SİSTEM: BELGELERİ OTOMATİK DOĞRULAR (AI + OCR)
         │
         ├── Başarılı ──► AŞAMA 2: MANUEL KONTROL (24-48 saat)
         │                    │
         │                    ├── Onay ──► DÜKKAN AKTİF (temel mod)
         │                    │              │
         │                    │              ▼
         │                    │         ZORUNLU GÖRSELLERİ YÜKLE
         │                    │         (5 kategori, en az 1'er)
         │                    │              │
         │                    │              ▼
         │                    │         5+ GÖRSEL TAMAM MI?
         │                    │              │
         │                    │         ├── Evet ──► TAM AKTİF
         │                    │         ├── 2-4 ──► SINIRLI MOD (%50)
         │                    │         └── 0-1 ──► PASİF (yükleme yap)
         │                    │
         │                    └── Red ──► NEDEN BELİRTİLİR
         │                                  │
         │                                  7 GÜN SONRA TEKRAR BAŞVURU
         │
         └── Başarısız ──► 24 SAAT İÇİNDE YENİDEN YÜKLEME HAKKI
```

### 18.2 Sipariş Oluşturma ve Teslimat

```
MÜŞTERİ: ÇİÇEKÇİ SEÇER
         │
         ├── Sıralama: Puan (4.5+ üstte)
         ├── Canlı kamera varsa +100 puan
         ├── Dükkan durumu: Açık / Çalışma Saati Dışı / Pasif
         ├── Teslimat süresi gösterilir (dinamik)
         └── Ürünlere göz atar (hazır / özel sipariş)
         │
         ▼
MÜŞTERİ: SEPETİ OLUŞTURUR
         │
         ├── Hazır ürün seçer veya özel buket tasarlar
         ├── Boyut seçer (küçük/orta/büyük)
         ├── Ekstra: vazo, yeşillik, kurdele, ışık
         ├── MESAJ KARTI YAZAR (ZORUNLU, en az 10 karakter)
         ├── Teslimat şekli seçer (kurye/dükkan/nokta)
         ├── Teslimat adresi girer
         └── Ödeme yöntemi seçer
         │
         ▼
MÜŞTERİ: SİPARİŞİ ONAYLAR + ÖDEME YAPAR
         │
         ▼
SİSTEM: DİNAMİK SÜRE HESAPLAR
         │
         ├── Hava durumu (Meteoroloji API)
         ├── Trafik durumu (Google Traffic)
         ├── Mesafe hesaplama
         ├── Çiçekçi hazırlık süresi (geçmiş veri)
         └── Tahmini süre gösterilir
         │
         ▼
SİSTEM: SİPARİŞİ ÇİÇEKÇİYE İLETİR
         │
         ▼
ÇİÇEKÇİ: SİPARİŞİ ALIR
         │
         ├── Onay ──► HAZIRLIK BAŞLAR
         │              │
         │              ▼
         │         BUKET HAZIRLANIR
         │              │
         │              ▼
         │         FOTOĞRAF ÇEKİLİR (tazelik kontrolü)
         │              │
         │              ├── AI: Taze ✅ → devam
         │              └── AI: Taze değil ❌ → yeniden hazırla
         │              │
         │              ▼
         │         MÜŞTERİYE FOTOĞRAF GÖNDERİLİR
         │              │
         │              ├── Onay → devam
         │              └── Red → çiçekçi düzeltir
         │              │
         │              ▼
         │         PAKETLENİR + MESAJ KARTI EKLENİR
         │              │
         │              ▼
         │         SİSTEM: UYGUN KURYE ATA
         │              │
         │              ├── Puan (4.5+)
         │              ├── Mesafe (yakın)
         │              └── Müsaitlik (uygun)
         │              │
         │              ▼
         │         KURYE: ÇİÇEKÇİDEN ALIR
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
         │         VARIŞ: QR KOD OKUTMA / SMS KODU
         │              │
         │              ├── Başarılı ──► TESLİM
         │              │                  │
         │              │                  ▼
         │              │             MÜŞTERİ: FOTOĞRAFLI
         │              │             KARŞILAŞTIRMA YAPAR
         │              │                  │
         │              │                  ▼
         │              │             PUANLAMA EKRANI (3 yönlü)
         │              │                  │
         │              │                  ▼
         │              │             SİPARİŞ TAMAM
         │              │
         │              └── Başarısız ──► SMS KODU (3 deneme)
         │                                    │
         │                                    └── Başarısız ──► DESTEK
         │
         ├── Red ──► İPTAL (+ neden)
         │              │
         │              ▼
         │         MÜŞTERİYE BİLDİRİM + İADE
         │
         └── Değişiklik ──► REVİZYON ÖNERİSİ
                            │
                            ├── Müşteri onayı → devam
                            └── Müşteri red → iptal
```

### 18.3 Zaman Çizelgesi (Timeline) Preorder Akışı

```
DÜKKAN DURUMU NE OLURSA OLSUN, MÜŞTERİ ÖN SİPARİŞ VEREBİLİR.

MÜŞTERİ: ZAMAN ÇİZELGESİNİ AÇAR
         │
         ▼
SİSTEM: DÜKKAN DURUMUNU KONTROL EDER
         │
         ├── 🟢 Açık → Bugün + İleri tarih gösterilir
         ├── 🟡 Çalışma Saati Dışı → Yarın + İleri tarih
         └── 🔴 Pasif → En erken açılış tarihi + sonrası
         │
         ▼
MÜŞTERİ: TARİH VE SAAT SEÇER
         │
         ├── Takvimden gün seçer
         ├── Saat seçer (09:00-21:00 arası, her saat başı)
         └── Sistem müsaitlik kontrolü yapar
         │
         ▼
MÜŞTERİ: SİPARİŞİ TAMAMLAR + ÖDER
         │
         ▼
SİSTEM: SEÇİLEN ZAMANA PLANLAR
         │
         ├── Çiçekçi takviminde blokaj
         ├── Otomatik hatırlatma:
         │   ├── 7 gün kala: "Hazırlığa başla"
         │   ├── 1 gün kala: "Yarın teslimat"
         │   └── Teslimat günü: hazırlık + kurye
         └── Müşteri takvimine ekleme (Google/Apple)
```

### 18.4 Özel Gün Sipariş Yoğunluğu Akışı

```
ÖZEL GÜN ÖNCESİ (7 GÜN KALA):
├── Sistem tüm çiçekçilere bildirim:
│   "Sevgililer Günü'ne 7 gün kaldı, stoklarınızı hazırlayın"
├── Ön siparişler aktifleşir
├── Fiyat artışı uyarısı (toptancıdan)
└── Ek kurye talebi (havuza)

ÖZEL GÜN (SABAH):
├── Çiçekçiler yoğunluk modunda
├── Hazırlık süresi otomatik +%50
├── Kurye öncelikli atama
└── Sipariş limiti: normalin 2 katı

ÖZEL GÜN (AKŞAM):
├── Yoğunluk azalır
├── Kalan stok için indirim (çiçekçi belirler)
└── Ertesi gün normal düzene dönüş
```

---

## 19. SİPARİŞ CANLI TAKİP SİSTEMİ

### 19.1 Müşteri Takip Ekranı

```
SİPARİŞ DETAYI:
┌─────────────────────────────────────┐
│  💐 Sipariş #1234                    │
│  🟢 Aktif · Tahmini: 15:30           │
├─────────────────────────────────────┤
│  📍 ADIM ADIM TAKİP:                 │
│                                      │
│  ✅ Sipariş Alındı   14:20           │
│  🔄 Buket Hazırlanıyor...            │
│     ⏳ Tahmini: 5 dk                 │
│  ⬜ Fotoğraf Çekilecek               │
│  ⬜ Kurye Yolda                       │
│  ⬜ Teslim Edildi                    │
├─────────────────────────────────────┤
│  👨‍🍳 Çiçekçi: Gül Bahçesi            │
│  🎯 Adres: Moda Cd. No:42            │
│  🚚 Kurye: Mehmet · 4.8⭐          │
│     📱 05XX XXX XX XX                │
└─────────────────────────────────────┘
```

### 19.2 Gerçek Zamanlı Bildirimler

| Aşama | Bildirim | Kanallar |
|-------|----------|----------|
| Sipariş alındı | "✅ Siparişiniz alındı" | Push, SMS |
| Hazırlık başladı | "👨‍🍳 Buketiniz hazırlanıyor" | Push |
| Fotoğraflandı | "📸 Buketinizin fotoğrafı çekildi, onaylayın" | Push, In-app |
| Onaylandı | "✅ Onaylandı, paketleniyor" | Push |
| Kurye yolda | "🚚 Kuryeniz yola çıktı" | Push, SMS |
| Teslim edildi | "✅ Teslim edildi · Yorum yapın" | Push, E-posta |

---

## 20. DB ŞEMASI (EKLER)

```sql
-- Çiçekçi görselleri (yemek sistemindeki restoran görsellerine benzer)
cicekci_goruntu (
  id, cicekci_id, kategori (vitrin/atolye/depo/arac/ornek),
  dosya_yolu, cozunurluk, cekim_tarihi, geotag,
  aktif, yukleme_tarihi, puan_katkisi
)

-- Canlı kamera kaydı
cicekci_kamera (
  id, cicekci_id, kamera_adi, cozunurluk,
  yayin_url, aktif_mi, son_kesinti_tarihi,
  calisma_saati_uyum_mu, puan_katkisi
)

-- Tazelik zaman damgası zinciri
tazelik_zinciri (
  id, siparis_id, asama (hasat/toptanci_al/toptanci_ver/cicekci_al/hazirlik/paket/kurye/teslimat),
  tarih_saat, koordinat, fotograf, dogrulandi_mi
)

-- Çiçekçi evrak puanı
cicekci_evrak_puan (
  id, cicekci_id, evrak_turu, puan, yukleme_tarihi,
  gecerlilik_tarihi, dogrulandi_mi, aktif
)

-- Puanlama (3 yönlü)
cicek_puan (
  id, siparis_id, puan_veren_id, puan_veren_tur (musteri/cicekci/kurye),
  puan_alan_id, puan_alan_tur (musteri/cicekci/kurye),
  puan (1.0-5.0), kriter_json, yorum, tarih
)

-- Sipariş canlı takip
siparis_takip (
  id, siparis_id, asama, baslama_tarihi, bitis_tarihi,
  tahmini_sure, guncel_durum, kurye_konum_json
)

-- Teslimat süresi logu
teslimat_sure_log (
  id, siparis_id, hesaplanan_sure, gercek_sure,
  hava_durumu, trafik_durumu, sapma_yuzde,
  iyilestirme_onerisi
)
```

---

## 21. API ENDPOINT'LERİ (EKLER)

### 21.1 Görsel Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/cicekci/{id}/goruntu` | Görsel yükle |
| GET | `/api/v1/cicekci/{id}/goruntuler` | Görselleri listele (kategori bazlı) |
| DELETE | `/api/v1/cicekci/{id}/goruntu/{goruntu_id}` | Görsel sil |
| GET | `/api/v1/cicekci/{id}/goruntu/durum` | Zorunlu görsel durumu |

### 21.2 Kamera Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/cicekci/{id}/kamera` | Kamera ekle |
| GET | `/api/v1/cicekci/{id}/kameralar` | Kameraları listele |
| PUT | `/api/v1/cicekci/{id}/kamera/{kamera_id}` | Kamera güncelle |
| DELETE | `/api/v1/cicekci/{id}/kamera/{kamera_id}` | Kamera sil |
| GET | `/api/v1/cicekci/{id}/kamera/{kamera_id}/yayin` | Canlı yayın URL |
| POST | `/api/v1/cicekci/{id}/kamera/{kamera_id}/baslat` | Yayın başlat |
| POST | `/api/v1/cicekci/{id}/kamera/{kamera_id}/durdur` | Yayın durdur |

### 21.3 Tazelik Zinciri

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/siparis/{id}/tazelik/ekle` | Zaman damgası ekle |
| GET | `/api/v1/siparis/{id}/tazelik/zincir` | Tazelik zincirini getir |
| GET | `/api/v1/urun/{id}/tazelik-puani` | Tazelik puanı sorgula |

### 21.4 Evrak Yönetimi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/cicekci/{id}/evrak` | Evrak yükle |
| GET | `/api/v1/cicekci/{id}/evraklar` | Evrakları listele |
| DELETE | `/api/v1/cicekci/{id}/evrak/{evrak_id}` | Evrak sil |
| GET | `/api/v1/cicekci/{id}/puan/evrak` | Evrak bazlı puan durumu |

### 21.5 Puanlama

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/siparis/{id}/puan` | Puan ver |
| GET | `/api/v1/cicekci/{id}/puan` | Çiçekçi puan detayı |
| GET | `/api/v1/siparis/{id}/puanlar` | Siparişe ait tüm puanlar |
| GET | `/api/v1/cicekci/siralama` | Çiçekçi sıralaması |

### 21.6 Teslimat Süresi

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/cicekci/{id}/sure/tahmin` | Süre tahmini hesapla |
| GET | `/api/v1/cicekci/{id}/sure/hava-durumu` | Anlık hava durumu |
| GET | `/api/v1/cicekci/{id}/sure/trafik-durumu` | Anlık trafik durumu |
| GET | `/api/v1/siparis/{id}/sure-log` | Süre hesaplama geçmişi |

### 21.7 Sipariş Canlı Takip

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| GET | `/api/v1/siparis/{id}/canli-takip` | Canlı takip verisi |
| PUT | `/api/v1/siparis/{id}/asama` | Aşama güncelle (çiçekçi/kurye) |
| POST | `/api/v1/siparis/{id}/fotograf-onay` | Fotoğraf onayı (müşteri) |
| PUT | `/api/v1/siparis/{id}/teslim-et` | QR ile teslim et |

