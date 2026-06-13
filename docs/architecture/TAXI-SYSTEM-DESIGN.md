# 🚕 TAKSİ SİSTEMİ - KAPSAMLI TASARIM DOKÜMANI

---

## 📋 İÇİNDEKİLER

1. [Bireysel Hesap - Taksi Şöförü Kaydı](#1-bireysel-hesap---taksi-şöförü-kaydı)
2. [Araç (Ticari Plaka) Yönetimi](#2-araç-ticari-plaka-yönetimi)
3. [Çoklu Şöför Sistemi (Vardiya)](#3-çoklu-şöför-sistemi-vardiya)
4. [Araç Kiralama Sistemi](#4-araç-kiralama-sistemi)
5. [Araç Ortaklığı (Hisseli Plaka)](#5-araç-ortaklığı-hisseli-plaka)
6. [Sürücü-Araç Anlık Eşleşme Sistemi](#6-sürücü-araç-anlık-eşleşme-sistemi)
7. [Çift Yönlü Puanlama Sistemi](#7-çift-yönlü-puanlama-sistemi)
8. [Taksi Çağırma ve Eşleştirme Algoritması](#8-taksi-çağırma-ve-eşleştirme-algoritması)
9. [Fiyat Tahmin ve Rota Gösterim Sistemi](#9-fiyat-tahmin-ve-rota-gösterim-sistemi)
9.5 [Müşteri Özgün Rota Haritalama Sistemi](#95-müşteri-özgün-rota-haritalama-sistemi)
10. [Zorunlu Sistem Ödemesi (Cüzdan Sistemi)](#10-zorunlu-sistem-ödemesi-cüzdan-sistemi)
11. [Veritabanı Şeması (Yeni Tablolar)](#11-veritabanı-şeması-yeni-tablolar)
12. [API Endpoint'leri](#12-api-endpoint'leri)
13. [Akış Diyagramları](#13-akış-diyagramları)
14. [Müşteri Seyahat Taahhüt ve Erken İnme Sistemi](#14-müşteri-seyahat-taahhüt-ve-erken-inme-sistemi)
15. [Paylaşımlı Yolculuk ve Çoklu Yolcu Sistemi](#15-paylaşımlı-yolculuk-ve-çoklu-yolcu-sistemi)
16. [Başkasına Taksi Gönderme (Hediye Yolculuk) Sistemi](#16-başkasına-taksi-gönderme-hediye-yolculuk-sistemi)
17. [Konfor Tercih ve Bahşiş Sistemi](#17-konfor-tercih-ve-bahşiş-sistemi)
18. [Müşteri Çağrı İptal ve Binmeme Cezası](#18-müşteri-çağrı-i̇ptal-ve-binmeme-cezası)
19. [Bölgeler Arası Transfer Taksi ve Uzun Mesafe Sistemi](#19-bölgeler-arası-transfer-taksi-ve-uzun-mesafe-sistemi)
20. [Taksi Yolcu e-Kitap / e-Fatura / Yolculuk Raporu Sistemi](#20-taksi-yolcu-e-kitap--e-fatura--yolculuk-raporu-sistemi)
21. [Müşteri Taksi Terminali](#21-müşteri-taksi-terminali)
22. [Planlanmış Rotalar (Ön Rezervasyon)](#22-planlanmış-rotalar-ön-rezervasyon)
23. [Geliş Öncesi Karşılama Rezervasyonu (Terminal/Havalimanı)](#23-geliş-öncesi-karşılama-rezervasyonu-terminalhavalimanı)
24. [Acil Durum / Panik Butonu Sistemi](#24-acil-durum--panik-butonu-sistemi)
25. [Akaryakıt İndirim ve İstasyon Ağı](#25-akaryakıt-i̇ndirim-ve-i̇stasyon-ağı)
26. [Çekici / Yol Yardım ve Tamir Ağı](#26-çekici--yol-yardım-ve-tamir-ağı)
27. [Kaza / Hasar Bildirim Sistemi](#27-kaza--hasar-bildirim-sistemi)
28. [Vardiya Pazarı (Shift Marketplace)](#28-vardiya-pazarı-shift-marketplace)
29. [Dijital Bahşiş Sistemi](#29-dijital-bahşiş-sistemi)
30. [Günlük Gelir/Gider Defteri (Muhasebe)](#30-günlük-gelirgider-defteri-muhasebe)
31. [Otopark / Park İndirimleri](#31-otopark--park-i̇ndirimleri)
32. [Araç Yıkama ve Bakım İndirimleri](#32-araç-yıkama-ve-bakım-i̇ndirimleri)
33. [Kadın Yolcu Güvenlik Modu](#33-kadın-yolcu-güvenlik-modu)
34. [Mola Noktaları / Sosyal Alan Haritası](#34-mola-noktaları--sosyal-alan-haritası)
35. [Dil Rozetleri](#35-dil-rozetleri)
36. [Evcil Hayvan / Bebek Koltuğu / Engelli Filtresi](#36-evcil-hayvan--bebek-koltuğu--engelli-filtresi)
37. [Pos Cihazı / Kart Okuyucu Kiralama](#37-pos-cihazı--kart-okuyucu-kiralama)
38. [Plaka / Taksi Alım-Satım Platformu](#38-plaka--taksi-alım-satım-platformu)

---

## 1. BİREYSEL HESAP - TAKSİ ŞÖFÖRÜ KAYDI

### 1.1 Ön Koşul
Her taksi şöförü öncelikle **Bireysel Hesap** açmak zorundadır. Bireysel hesap olmadan taksi şöförü kaydı yapılamaz.

### 1.2 Zorunlu Belgeler

| Belge | Açıklama | Geçerlilik Süresi |
|-------|----------|-------------------|
| **Ehliyet** | En az Sınıf B, ticari taksi kullanmaya uygun | 10 yıl (duruma göre) |
| **Sürücü Belgesi (Resmi)** | Devletin istediği tüm sürücü belgeleri eksiksiz | 10 yıl |
| **Ticari Taksi Kullanım Belgesi** | Taksi hizmeti için özel izin | 5 yıl |
| **Psikoteknik Değerlendirme Raporu** | Psikolojik ve fiziksel yeterlilik | 2 yıl |
| **SRC Belgesi (Sürücü Davranışları)** | SRC-4 tipi (taksi/minibüs) | 5 yıl |
| **Adli Sicil Kaydı (Sabıka)** | Temiz sabıka kaydı | 3 ay |
| **Kimlik Fotokopisi** | TC Kimlik ön-arka | Süresiz |
| **İkametgah Belgesi** | Adres teyidi | 1 yıl |
| **Vergi Mükellefiyet Belgesi** | Bağlı olduğu vergi dairesi | 1 yıl |
| **SGK Hizmet Dökümü** | Aktif SGK durumu | 3 ay |

### 1.3 Şöför Profil Fotoğrafları

Şöförün profil sayfasında **3 adet fotoğraf** zorunludur:

```
FOTOĞRAF ŞARTLARI:
├── 1️⃣ ÖN (Yüz): Net, aydınlık, gözler ve yüz tam görünür
├── 2️⃣ ARKA: Sırt dönük, başın arkası görünür
├── 3️⃣ SOL YAN: Sol profilden çekilmiş, yüzün sol yanı görünür
│
└── Kurallar:
    ├── Arka fon düz (beyaz/açık renk)
    ├── Güneş gözlüğü, maske, şapka YASAK
    ├── Son 6 ay içinde çekilmiş olmalı
    └── Vesikalık formatında (4.5 × 6 cm)
```

### 1.4 Belge Yükleme ve Doğrulama Süreci

```
ADIM 1: Bireysel Hesap Aç (email/telefon + kimlik doğrulama)
        ↓
ADIM 2: "Taksi Şöförü Ol" butonuna bas
        ↓
ADIM 3: Profil Fotoğrafları
        ├── Ön yüz fotoğrafı yükle
        ├── Arka yüz fotoğrafı yükle
        ├── Sol yan fotoğrafı yükle
        └── Otomatik yüz tanıma kontrolü
        ↓
ADIM 4: Belge Yükleme Sayfası
        ├── Ehliyet yükle (ön-arka)
        ├── Sürücü belgesi yükle
        ├── Psikoteknik raporu yükle
        ├── SRC belgesi yükle
        ├── Sabıka kaydı yükle
        ├── TC Kimlik yükle (ön-arka)
        ├── Selfie (kimlik ile birlikte)
        ├── İkametgah yükle
        ├── Vergi mükellefiyet belgesi
        └── SGK hizmet dökümü
        ↓
ADIM 5: Yapay Zeka + Manuel Doğrulama
        ├── Yüz tanıma (selfie ↔ kimlik ↔ profil fotoğrafları)
        ├── Belge okunabilirliği kontrolü
        ├── Son kullanma tarihleri kontrolü
        ├── Sahte belge tespiti (AI)
        └── Devlet sistemleri entegrasyonu (opsiyonel)
        ↓
ADIM 6: Onay Mekanizması
        ├── ✅ ONAY: "Taksi Şöförü" rozeti aktif
        │   └── Onayı yapan: Sistem Admini veya yetkilendirilmiş kişi
        ├── ⏳ BEKLEMEDE: Manuel inceleme (24-48 saat)
        └── ❌ RED: Eksik belgeler bildirilir
        └── 🔄 İTİRAZ: Yeniden değerlendirme talebi
```

### 1.4 Belge Uyarı ve Yenileme Sistemi

```yaml
Belge Takip:
  - Her belgenin son kullanma tarihi sistemde kayıtlı
  - Bitiş tarihine 30 gün kala → Bildirim gider
  - Bitiş tarihine 7 gün kala → Uyarı (günlük bildirim)
  - Bitiş tarihi geçtiğinde → Taksi hizmeti durdurulur
  - Aktif edilmesi için yeni belge yüklenmesi gerekli

Belge Doğrulama Durumları:
  - ✅ GEÇERLİ: Belge tarihi içinde, doğrulanmış
  - ⏳ SÜRESİ DOLMAK ÜZERE: 30 gün kala
  - ❌ SÜRESİ DOLMUŞ: Hizmet durdurulur
  - 🔄 YENİLENİYOR: Yeni belge beklemede
```

### 1.5 Taksi Şöförü Profili (Dashboard)

```
┌─────────────────────────────────────────────────────────────────┐
│  🚕 Ahmet Yılmaz - Taksi Şöförü                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 BELGE DURUMU:                                               │
│  ├── ✅ Ehliyet: 10.06.2030 - Geçerli                          │
│  ├── ✅ Psikoteknik: 12.08.2027 - Geçerli                      │
│  ├── ✅ SRC Belgesi: 15.03.2029 - Geçerli                      │
│  ├── ✅ Adli Sicil: 01.01.2026 - Geçerli                        │
│  └── ⚠️ İkametgah: 20.01.2026 - 25 gün kaldı (Yenile!)        │
│                                                                 │
│  🚗 AKTİF ARAÇ:                                                 │
│  ├── Plaka: 34 TAK 1234                                         │
│  ├── Araç: 2023 Renault Megane                                 │
│  ├── Vardiya: Sabahçı (06:00-14:00)                             │
│  └── Şu an: Müsait ✅                                           │
│                                                                 │
│  ⭐ PUANLAR:                                                    │
│  ├── Sürüş Puanı: 4.8 ⭐ (156 değerlendirme)                   │
│  ├── Araç Puanı: 4.6 ⭐ (120 değerlendirme)                     │
│  └── Kombine Puan: 4.7 ⭐                                       │
│                                                                 │
│  💰 GÜNLÜK KAZANÇ:                                              │
│  ├── Bugün: 22 yolcu - 1.890 TL                                 │
│  ├── Kira: -250 TL                                               │
│  ├── Komisyon: -94 TL                                            │
│  └── Net: 1.546 TL                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. ARAÇ (TİCARİ PLAKA) YÖNETİMİ

### 2.1 Araç Sahipliği Türleri

```
ARAÇ SAHİPLİĞİ TÜRLERİ:
│
├── 1️⃣ TEK SAHİPLİ (Bireysel)
│   ├── 1 kişi aracın tam sahibi
│   ├── Kendi kullanır veya kiraya verir
│   └── Tüm gelir/sorumluluk tek kişide
│
├── 2️⃣ HİSSELİ / ORTAK (Çoklu Bireysel)
│   ├── 2 veya daha fazla kişi ortak
│   ├── Her biri belirli yüzdede hisse sahibi
│   ├── Örn: Ali %50, Mehmet %50
│   └── Kazanç hisse oranında paylaşılır
│
├── 3️⃣ KURUMSAL (Şirket)
│   ├── Firma adına kayıtlı
│   ├── Çalışan şöförler çalıştırabilir
│   ├── Raporlama ve muhasebe takibi
│   └── Birden fazla aracı olabilir
│
└── 4️⃣ KARMA (Karmaşık)
    ├── Örn: Şirket %50 + Ali %25 + Mehmet %25
    ├── Çoklu sahiplik + kurumsal iç içe
    └── Özel sözleşme yapısı
```

### 2.2 Araç Kayıt Bilgileri

```yaml
Araç Zorunlu Bilgiler:
  - Plaka Numarası: 34 TAK 1234 (eşsiz)
  - Plaka Tipi: Ticari Taksi
  - Ruhsat Bilgileri:
    ├── Ruhsat dosyası: SİSTEME YÜKLENMİŞ VE ONAYLANMIŞ OLMALI
    ├── Marka: Renault
    ├── Model: Megane
    ├── Yıl: 2023
    ├── Motor Hacmi: 1461cc
    ├── Motor Tipi: Dizel
    ├── Vites: Manuel / Otomatik
    ├── Renk: Beyaz
    └── Koltuk Kapasitesi: 4+1

  - Plaka: SİSTEMDE YAZMAK ZORUNDA
    └── Plaka, araç sayfasında ve tüm yolculuk kayıtlarında görünür

  - Sigorta Bilgileri:
    ├── Zorunlu Trafik Sigortası (Tarih)
    ├── Kasko (varsa)
    └── Ticari Taksi Sigortası

  - Araç Muayene Bilgisi:
    ├── Son Muayene Tarihi
    ├── Gelecek Muayene Tarihi
    └── Muayene Durumu: geçerli/geçersiz

  - Taksimetre Bilgisi:
    ├── Taksimetre Modeli
    ├── Son Kalibrasyon Tarihi
    └── Kalibrasyon Geçerlilik Tarihi

  - Periyodik Bakım Bilgileri:
    ├── Son Bakım Tarihi: 12.03.2026 ✅
    ├── Sonraki Bakım Tarihi: 12.09.2026
    ├── Bakım Türü: 30.000 km / 6 ay
    ├── Yapılan İşlemler: Yağ değişimi, filtre, fren balata
    └── Bakım Durumu: ✅ Güncel

  - Araç Takımı:
    ├── OBD Cihazı (anlık konum)
    ├── 🎥 Güvenlik Kamerası (ZORUNLU) — iç mekan kaydı
    ├── Taksimetre
    ├── Kart Okuyucu (opsiyonel)
    └── Acil Durum Butonu
```

### 2.3 Araç Güvenlik Kamerası Zorunluluğu

Sisteme kayıtlı HER TAKSİ araç içi güvenlik kamerası bulundurmak ZORUNDADIR. Bu kamera hem müşteri hem şöför güvenliği için tasarlanmıştır.

```
GÜVENLİK KAMERASI ZORUNLULUKLARI:
├── Fiziksel Kamera:
│   ├── Aracın iç mekanını tam gören bir noktada
│   ├── Ön koltuklar + arka koltuklar görünmeli
│   ├── Çözünürlük: En az 1080p
│   ├── Gece görüş (IR) özellikli
│   └── Sürekli kayıt (araç hareket halindeyken)
│
├── Kayıt Süresi:
│   ├── Minimum 7 gün kesintisiz kayıt saklama
│   ├── Her yolculuk kaydı otomatik işaretlenir
│   ├── Yolculuk kayıtları 30 gün saklanır
│   └── İhtilaf durumunda 90 güne kadar uzatılabilir
│
├── Sistem Entegrasyonu:
│   ├── Kamera sistemle uyumlu olmalı (API/bağlantı)
│   ├── Yolculuk başlayınca otomatik kayıt başlar
│   ├── Yolculuk bitince kayıt durur
│   └── Kayıtlar şifrelenir (sadece yetkili erişebilir)
│
└── Uyarı / İşaretleme:
    ├── Kamerası olmayan araç: "⚠️ Bu araçta güvenlik kamerası yok"
    ├── Müşteri çağrı anında bu uyarıyı görür
    ├── Sistem, kamerasız araçları düşük öncelikli eşleştirir
    └── 30 gün içinde kamera takmayan araç: SİSTEMDEN GEÇİCİ MEN
```

```
MÜŞTERİ EKRANI (Kamerasız Araç Uyarısı):
┌──────────────────────────────────────────────┐
│  🚗 34 TAK 5678  |  👤 Ali K.  4.2 ⭐      │
│                                              │
│  ⚠️ BU ARAÇTA GÜVENLİK KAMERASI YOKTUR      │
│  ┌──────────────────────────────────────┐    │
│  │  ❌ Araç içi güvenlik kamerası       │    │
│  │     bulunmamaktadır.                  │    │
│  │                                       │    │
│  │  🟢 Kameralı araç tercih edebilirsiniz│    │
│  └──────────────────────────────────────┘    │
│                                              │
│  [ YİNE DE BİN ]    [ KAMERALI ARAÇ BUL ]   │
└──────────────────────────────────────────────┘
```

### 2.4 Araç Fotoğrafları

Aracın sisteme **6 adet fotoğrafı** yüklenmelidir. Bu fotoğraflar araç sayfasında ve müşteri çağrı anında görünür.

```
ZORUNLU ARAÇ FOTOĞRAFLARI (6 Adet):
├── DIŞ CEPHE (4):
│   ├── 1️⃣ ÖN: Aracın ön cephesi, plaka net okunur
│   ├── 2️⃣ ARKA: Aracın arka cephesi, plaka net okunur
│   ├── 3️⃣ SAĞ YAN: Sağ taraftan çekim, tüm yan görünür
│   └── 4️⃣ SOL YAN: Sol taraftan çekim, tüm yan görünür
│
├── İÇ MEKAN (2):
│   ├── 5️⃣ ÖN KOLTUKLAR: Ön koltuklar, direksiyon, gösterge paneli
│   └── 6️⃣ ARKA KOLTUKLAR: Arka koltuklar, tavan, zemin
│
└── KURALLAR:
    ├── Tüm fotoğraflar güncel olmalı (son 1 ay)
    ├── Plaka her dış cephe fotoğrafında OKUNUR olmalı
    ├── Fotoğraflar gündüz, doğal ışıkta çekilmeli
    ├── Araç temiz olmalı (kiri/pası gizlemek yasak)
    └── Çözünürlük en az 1920×1080
```

### 2.5 Araç Sayfası (Dashboard)

```
┌─────────────────────────────────────────────────────────────────┐
│  🚗 34 TAK 1234                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📸 ARAÇ FOTOĞRAFLARI:                                         │
│  ┌──────┬──────┐  ┌──────┬──────┐                              │
│  │ ÖN   │ ARKA │  │ SAĞ  │ SOL  │                              │
│  │[📷]  │[📷]  │  │[📷]  │[📷]  │                              │
│  ├──────┴──────┤  ├──────┴──────┤                              │
│  │İÇ ÖN  │[📷] │  │İÇ ARKA│[📷] │                              │
│  └───────┴─────┘  └───────┴─────┘                              │
│                                                                 │
│  📋 ARAÇ BİLGİLERİ:                                             │
│  ├── Plaka: 34 TAK 1234                                        │
│  ├── Marka/Model: Renault Megane                               │
│  ├── Yıl: 2023 · Renk: Beyaz                                   │
│  ├── Yakıt: Dizel · Şanzıman: Otomatik                        │
│  ├── Ruhsat: ✅ YÜKLÜ VE ONAYLANMIŞ                            │
│  ├── Onay: Sistem Admin - 15.01.2026                           │
│  ├── 🎥 Güvenlik Kamerası: ✅ VAR (Onaylı)                     │
│  └── Puan: 4.6 ⭐ (120 değerlendirme)                           │
│                                                                 │
│  🔍 BELGE DURUMU:                                               │
│  ├── ✅ Sigorta: 15.09.2026 - 3 ay kaldı                       │
│  ├── ✅ Muayene: 12.04.2026 - Geçerli                          │
│  ├── ✅ Taksimetre Kalibrasyonu: 20.03.2026 - Geçerli          │
│  └── ⚠️ Kasko: 01.01.2026 - 2 ay geçmiş (YENİLET!)            │
│                                                                 │
│  🔧 PERİYODİK BAKIM:                                           │
│  ├── ✅ Son Bakım: 12.03.2026 (30.000 km)                      │
│  ├── ⏳ Sonraki Bakım: 12.09.2026                              │
│  └── İşlemler: Yağ, filtre, fren balata, rot balans            │
│                                                                 │
│  👤 AKTİF ŞÖFÖR BİLGİLERİ:                                     │
│  ├── 🧑 Ahmet Yılmaz                                           │
│  ├── 📷 [Profil Fotoğrafı]                                     │
│  ├── ⭐ Şöför Puanı: 4.8                                       │
│  ├── 🔹 Vardiya: Sabahçı (06:00-14:00)                        │
│  └── 📞 İletişim: 0XXX XXX XX XX                               │
│                                                                 │
│  👥 ATANMIŞ TÜM ŞÖFÖRLER:                                      │
│  ├── 🟢 Ahmet Yılmaz (Sabahçı - 06:00-14:00) - Aktif şu an     │
│  ├── 🟢 Mehmet Kaya (Akşamçı - 14:00-22:00) - Pasif             │
│  ├── 🟡 Ali Demir (Yedek/Hafta sonu) - Pasif                    │
│  └── [➕ Şöför Ekle]                                             │
│                                                                 │
│  📊 BUGÜNKÜ PERFORMANS:                                         │
│  ├── Toplam Yolculuk: 22                                        │
│  ├── Toplam Mesafe: 145 km                                      │
│  ├── Toplam Kazanç: 1.890 TL                                    │
│  ├── Kira Geliri: 250 TL (Akşamcıdan)                          │
│  └── Net: 2.140 TL                                              │
│                                                                 │
│  📅 VARDİYA TAKVİMİ:                                            │
│  │            PAZARTESİ SALI ÇARŞAMBA PERŞEMBE CUMA CUMARTESİ PAZAR
│  │  06:00-14:00 Ahmet    Ahmet   Ahmet    Ahmet    Ahmet   Ali   Ali
│  │  14:00-22:00 Mehmet   Mehmet  Mehmet   Mehmet   Mehmet  Ali   Ali
│  │  22:00-06:00   -        -       -         -       -      -     -
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.7 Trafik Muayene Otomatik Okuma ve Süre Takibi

Sisteme yüklenen trafik muayene belgesi, **sistem tarafından otomatik okunup analiz edilir**. Son geçerlilik tarihi çıkarılır ve bu tarih aşıldığında araç **güvenlik dışı** işaretlenerek aktif hizmetten düşürülür.

```
MUAYENE BELGESİ OTOMATİK ANALİZ:
├── ADIM 1: Araç sahibi muayene belgesini yükler (PDF/JPEG/PNG)
│
├── ADIM 2: Sistem OCR ile belgeyi okur
│   ├── Plaka bilgisi çıkarılır
│   ├── Muayene tarihi çıkarılır
│   ├── Son geçerlilik tarihi çıkarılır
│   ├── Muayene istasyonu bilgisi çıkarılır
│   └── Sonuç: Bilgiler doğrulandı mı? ✅ / ❌
│
├── ADIM 3: Sistem veritabanına kaydeder
│   ├── inspection_date: 12.03.2026
│   ├── inspection_expiry: 12.03.2027
│   └── inspection_status: 'valid'
│
├── ADIM 4: Günlük otomatik kontrol
│   ├── Her gece 00:00'da sistem tüm muayene tarihlerini tarar
│   ├── inspection_expiry < BUGÜN mü?
│   │   ├── EVET → Araç GÜVENLİK DIŞI işaretlenir
│   │   │   ├── is_active = FALSE
│   │   │   ├── status = 'inspection_expired'
│   │   │   └── Araç çağrı sisteminden düşer
│   │   └── HAYIR → Sorunsuz devam
│   │
│   └── 7 gün kala: UYARI bildirimi gönderilir
│       ├── "Muayeneniz 7 gün sonra sona erecek"
│       └── Araç sahibi + şöförler bildirim alır
│
└── ADIM 5: Yenileme
    ├── Araç sahibi yeni muayene belgesini yükler
    ├── Sistem tekrar OCR ile okur
    ├── Tarihler güncellenir
    └── Araç tekrar aktif olur
```

```
ARAÇ SAYFASI (Muayene Durumu):
┌──────────────────────────────────────────────┐
│  🔍 BELGE DURUMU:                            │
│  ├── ✅ Sigorta: 15.09.2027 - Geçerli        │
│  ├── ✅✅ Muayene: 12.03.2027 - Geçerli      │
│  │   └── (Sistem OCR ile okundu ✅)          │
│  ├── ✅ Taksimetre Kalibrasyonu: Geçerli     │
│  └── ⚠️ Kasko: 2 ay geçmiş                   │
│                                              │
│  ⏰ Yaklaşan Süreler:                        │
│  └── 🔔 Muayene: 7 gün kaldı → UYARI!       │
└──────────────────────────────────────────────┘
```

```
MÜŞTERİ EKRANI (Muayenesi Geçmiş Araç):
┌──────────────────────────────────────────────┐
│  🚗 34 TAK 5678                              │
│                                              │
│  ⛔ BU ARAÇ GÜVENLİK DIŞI                     │
│  ┌──────────────────────────────────────┐    │
│  │  ❌ Trafik muayenesi 15 gün önce      │    │
│  │     sona ermiştir.                    │    │
│  │                                       │    │
│  │  Bu araç geçici olarak sistemden      │    │
│  │  çıkarılmıştır.                       │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  [ BAŞKA ARAÇ BUL ]                          │
└──────────────────────────────────────────────┘
```

#### 2.7.1 Otomatik Kontrol Mekanizması

```yaml
Günlük Kontrol Sistemi:
  Zamanlama:
    - Her gece 00:00'da cron job çalıştırılır
    - Ayrıca her çağrı öncesi araç sorgusunda anlık kontrol
    - Muayene bitiş tarihi geçmişse anında devre dışı
  
  Aksiyonlar:
    30 gün kala:
      - Hatırlatma bildirimi (e-posta + SMS + uygulama)
      - "Muayeneniz 30 gün sonra sona erecek"
    
    7 gün kala:
      - Acil hatırlatma (SMS + arama)
      - "Muayeneniz 7 gün kaldı, lütfen yenileyin"
    
    Tarih geçince:
      - Araç OTOMATİK devre dışı
      - Tüm şöförlere bildirim
      - Araç sahibine ceza puanı (-2)
      - "Aracınız muayene eksikliği nedeniyle devre dışı"
    
    Yenileme:
      - Yeni belge yüklenir
      - OCR okur
      - Admin onayı (veya otomatik onay, OCR %100 eşleşirse)
      - Araç tekrar aktif
  
  Güvenlik:
    - OCR başarısız olursa manuel incelemeye yönlendirilir
    - Yanlış okuma durumunda admin düzeltebilir
    - Tüm okumalar loglanır (denetim için)
```

#### 2.7.2 Veritabanı

```sql
-- Mevcut alanlara ek olarak:
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    inspection_ocr_data       JSONB,         -- OCR çıktısı (tarih, istasyon, vs.)
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    inspection_last_checked   TIMESTAMP,     -- Son kontrol tarihi
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    inspection_warning_sent   INTEGER DEFAULT 0;  -- Kaç uyarı gönderildi

-- Otomatik kontrol logları
CREATE TABLE taxi_inspection_log (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    action              VARCHAR(30) NOT NULL,     -- ocr_read, warning_30d, warning_7d, auto_disabled, renewed
    old_expiry          DATE,
    new_expiry          DATE,
    ocr_confidence      DECIMAL(5,2),             -- OCR güven oranı %0-100
    is_auto             BOOLEAN DEFAULT TRUE,     -- Otomatik mi, manuel mi?
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inspection_log_vehicle ON taxi_inspection_log(vehicle_id);
```

#### 2.7.3 API

```
POST   /api/v1/taxi/vehicle/{vehicleId}/upload-inspection     # Muayene belgesi yükle + OCR
GET    /api/v1/taxi/vehicle/{vehicleId}/inspection-status     # Muayene durumu sorgula
POST   /api/v1/taxi/admin/inspection/{logId}/verify           # Admin OCR sonucunu onayla/düzelt
GET    /api/v1/taxi/admin/inspection/expired                  # Muayenesi geçmiş araçlar listesi
POST   /api/v1/taxi/admin/inspection/{vehicleId}/force-disable  # Admin manuel devre dışı
POST   /api/v1/taxi/admin/inspection/{vehicleId}/force-enable   # Admin manuel aktifleştir
```

---

### 2.8 Taksi Durakları (Durak Sistemi)

Taksiciler, sisteme kayıtlı taksilerini bağlı oldukları **taksi durağına** kaydedebilir. Duraklar, sistem tarafından oluşturulan lokasyonlardır ve her durak kendine bağlı araç/şöför listesine sahiptir.

#### 2.8.1 Durak Oluşturma ve Yönetim

```
DURAK OLUŞTURMA AKIŞI:
├── ADIM 1: Taksi sahibi, "Durak Oluştur" sayfasını açar
│
├── ADIM 2: Durak bilgilerini girer
│   ├── Durak Adı: "Kadıköy İskele Taksi Durağı"
│   ├── Adres: "Kadıköy İskele, 34710 Kadıköy/İstanbul"
│   ├── Konum (Harita): Sistem üzerinden işaretlenir
│   │   └── Haritada nokta seçilir veya adres girilir
│   ├── İl / İlçe: "İstanbul / Kadıköy"
│   ├── Telefon: "0216 XXX XX XX"
│   ├── Kapasite (opsiyonel): "20 araç"
│   └── Durak Türü: "İskele Durağı"
│
├── ADIM 3: Sistem onayı
│   ├── Admin durak lokasyonunu doğrular
│   ├── Aynı lokasyonda başka durak var mı? → Uyarı
│   └── Onay → Durak aktif
│
└── ADIM 4: Araçları durağa ekleme
    ├── Taksi sahibi kendi araçlarını durağa ekler
    ├── Her araç sadece BİR durağa bağlı olabilir
    └── Araçlar durağa bağlanınca çağrılarda durak adı görünür
```

#### 2.8.2 Durak Sayfası

```
DURAK SAYFASI:
┌──────────────────────────────────────────────┐
│  🏪 KADIKÖY İSKELE TAKSİ DURAĞI              │
├──────────────────────────────────────────────┤
│                                              │
│  📍 Konum: Kadıköy İskele, 34710 Kadıköy     │
│  📞 Telefon: 0216 XXX XX XX                  │
│  👤 Sorumlu: Ahmet Yılmaz                     │
│                                              │
│  ─── DURAĞA BAĞLI ARAÇLAR (12) ───          │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🚗 34 TAK 1234 ── Renault Megane        ││
│  │ ⛽ Dizel · ⭐ 4.6 · 👤 Mehmet Y.        ││
│  │ 🟢 Müsait                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🚗 34 TAK 5678 ── Toyota Camry          ││
│  │ ⚡ Elektrikli · ⭐ 4.8 · 👤 Ali K.      ││
│  │ 🟢 Müsait                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🚗 34 TAK 4321 ── Fiat Egea             ││
│  │ ⛽ LPG'li · ⭐ 4.2 · 👤 Ayşe K. 👩      ││
│  │ 🔴 Meşgul (Taksim)                       ││
│  └──────────────────────────────────────────┘│
│                                              │
│  🕐 Durak Mesai: 06:00 - 02:00              │
│  📊 Bugünkü Yolculuk: 47                    │
└──────────────────────────────────────────────┘
```

#### 2.8.3 Müşteri Çağrı Ekranında Durak Görünümü

Müşteri, yakındaki taksileri görürken **durak bilgisini** de görebilir ve dilerse belirli bir durağın taksilerini filtreleyebilir.

```
MÜŞTERİ EKRANI:
┌──────────────────────────────────────────────┐
│  🗺 YAKINDAKİ TAKSİLER                       │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🚗 34 TAK 1234  ── Renault Megane       ││
│  │ ⭐ 4.6 · 👤 Mehmet Y.                    ││
│  │ 📍 300 m · ⏱ 2 dk                        ││
│  │ 🏪 Kadıköy İskele Durağı                ││
│  │ 💰 Tahmini: 185 TL                        ││
│  │ [ ÇAĞIR ]                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🚗 34 TAK 5678  ── Toyota Camry         ││
│  │ ⭐ 4.8 · 👤 Ali K.                        ││
│  │ 📍 600 m · ⏱ 3 dk                        ││
│  │ 🏪 Moda Sahil Durağı                    ││
│  │ 💰 Tahmini: 195 TL                        ││
│  │ [ ÇAĞIR ]                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  🔽 DURAK FİLTRESİ:                          │
│  ┌──────────────────────────────────┐        │
│  │ ☐ Tümü                           │        │
│  │ ☐ Kadıköy İskele Durağı (5 araç) │        │
│  │ ☐ Moda Sahil Durağı (3 araç)     │        │
│  │ ☐ Feneryolu Durağı (2 araç)      │        │
│  └──────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

#### 2.8.4 Durak Kuralları

```yaml
Durak Sistemi Kuralları:
  Oluşturma:
    - Her durak sistem tarafından oluşturulur (kullanıcı oluşturamaz)
    - Taksi sahibi başvuru yapar, admin onaylar
    - Lokasyon: Sistem haritası üzerinde işaretlenir
    - Aynı noktada birden fazla durak olamaz
  
  Araç Bağlama:
    - Her araç sadece BİR durağa bağlı olabilir
    - Araç durağa bağlanınca çağrılarda durak adı görünür
    - Durak değişikliği: 30 günde 1 kez yapılabilir
    - Durağı olmayan araç: "Bağımsız Taksi" olarak işaretlenir
  
  Şöför Bağlama:
    - Şöför, aracın bağlı olduğu durağa otomatik bağlanır
    - Şöför birden fazla araç kullanıyorsa farklı durak olabilir
    - Şöför durak değiştirince araç bağlantısı güncellenir
  
  Çağrı Önceliği:
    - Müşteri durak filtrelemezse tüm yakın taksiler görünür
    - Müşteri durak seçerse sadece o durak taksileri
    - Duraktaki taksiler arasında sıra sistemi: En uzun bekleyen önce (varsayılan)
    - Durak yöneticisi sırayı manuel düzenleyebilir
```

#### 2.8.6 Durak Sıra Sistemi (Kuyruk Yönetimi)

Durak yöneticisi, durağa bağlı araçları **sıraya koyar**. Gelen çağrılar bu sıraya göre yönlendirilir.

```
DURAK SIRA SİSTEMİ MANTIĞI:
┌──────────────────────────────────────────────────────────────┐
│                      DURAK SIRASI                             │
│                                                              │
│  Sıra 1 → 🚗 34 TAK 1111  (En uzun bekleyen)                │
│  Sıra 2 → 🚗 34 TAK 2222                                     │
│  Sıra 3 → 🚗 34 TAK 3333                                     │
│  Sıra 4 → 🚗 34 TAK 4444                                     │
│  Sıra 5 → 🚗 34 TAK 5555  (En yeni gelen)                    │
│                                                              │
│  📞 Çağrı gelince → Sıra 1'deki araç yönlendirilir          │
│  ✅ Gönderildi → Sıradan çıkar, diğerleri bir kayar          │
│  🆕 Yeni araç geldi → Sıra sonuna eklenir                    │
│  🔄 Yönetici sırayı elle düzenleyebilir                      │
└──────────────────────────────────────────────────────────────┘
```

##### 2.8.6.1 Kuyruk Akışı

```
SIRA İŞLEYİŞİ:
├── DURAK DOLUMU:
│   ├── Araç durağa gelir → Sıra sonuna eklenir
│   ├── Araç GPS'i durak konumunda (100m içinde) → "Durakta" sayılır
│   ├── Araç pasifse sıraya girmez
│   └── Araç aktifse ve müsaitse sıraya eklenir
│
├── ÇAĞRI YÖNLENDİRME:
│   ├── Müşteri çağrı yapar (durak filtreli veya genel)
│   ├── Sistem, sıradaki 1. aracı seçer
│   │   ├── Araç müsait mi? → ✅ Yönlendir
│   │   │   └── Değilse → Sıradaki 2. araca bak
│   │   └── Sıradakilerin hiçbiri müsait değilse en yakın bağımsız taksi
│   ├── Araç yönlendirilince sıradan çıkar
│   └── Kalan araçlar bir sıra ilerler
│
├── YÖNETİCİ MÜDAHALESİ:
│   ├── Yönetici "Sırayı Düzenle" ekranından sırayı değiştirebilir
│   │   ├── Araç öne alınabilir (acil durum, VIP müşteri)
│   │   ├── Araç arkaya alınabilir (ceza, gecikme)
│   │   └── Araç sıradan çıkarılabilir (arıza, mola)
│   └── Her değişiklik loglanır
│
└── SIRADAN ÇIKMA:
    ├── Yolcu alınca → Otomatik çıkar
    ├── Pasif moda geçince → Otomatik çıkar
    ├── Araç duraktan 500m+ uzaklaşırsa → Otomatik çıkar
    ├── Yönetici çıkarırsa → Manuel
    └── Vardiya/çalışma saati bitince → Otomatik çıkar
```

##### 2.8.6.2 Yönetici Sıra Ekranı

```
DURAK YÖNETİCİ SIRALAMA EKRANI:
┌──────────────────────────────────────────────┐
│  🏪 KADIKÖY İSKELE DURAĞI — SIRA YÖNETİMİ   │
│                                              │
│  ┌──────── SIRA ─────────┐                   │
│  │ Sıra │ Araç    │ Durum│                   │
│  ├──────┼─────────┼──────┤                   │
│  │ 1 🥇 │34 TAK 1111│ 🟢  │  [⬆] [⬇] [🗑]  │
│  │ 2    │34 TAK 2222│ 🟢  │  [⬆] [⬇] [🗑]  │
│  │ 3    │34 TAK 3333│ 🟢  │  [⬆] [⬇] [🗑]  │
│  │ 4    │34 TAK 4444│ 🟢  │  [⬆] [⬇] [🗑]  │
│  │ 5    │34 TAK 5555│ 🟢  │  [⬆] [⬇] [🗑]  │
│  └──────┴─────────┴──────┘                   │
│                                              │
│  📊 Sıra İstatistik:                        │
│  ├─ Bekleyen araç: 5                        │
│  ├─ En uzun bekleyen: 34 TAK 1111 (45 dk)   │
│  ├─ Bugünkü yönlendirme: 23                 │
│  └─ Ortalama bekleme: 12 dk                 │
│                                              │
│  [ 🔄 SIRAYI KARIŞTIR ]  [ 💾 KAYDET ]      │
│                                              │
│  ℹ️ Yeni araç gelince otomatik sıra sonuna   │
│     eklenir. Çağrı gelince sıra-1 gider.    │
└──────────────────────────────────────────────┘
```

##### 2.8.6.3 Durak Sıra Kuralları

```yaml
Durak Sıra Sistemi Kuralları:
  Varsayılan Sıralama:
    - FIFO (First In, First Out): En önce gelen en önce gider
    - Sıra pozisyonu: Durağa geliş zamanına göre belirlenir
    - Gün sonu: Tüm sıra sıfırlanır (ertesi gün yeniden başlar)
  
  Yönetici Yetkileri:
    - Sırayı tamamen yeniden düzenleyebilir
    - Aracı sıranın herhangi bir pozisyonuna taşıyabilir
    - Aracı sıradan çıkarabilir
    - Sırayı "dondurup" tekrar başlatabilir
    - Tüm işlemler loglanır (denetim için)
  
  Otomatik Sıra Yönetimi:
    - Araç durağa 100m yaklaşınca sıraya eklenir
    - Araç duraktan 500m uzaklaşınca sıradan çıkar
    - Yolcu alan araç otomatik sıradan çıkar
    - Mola/arıza durumunda yönetici çıkarır
  
  Çağrı Yönlendirme:
    - Yeni çağrı → Sistem sıradaki 1. müsait aracı seçer
    - Sıradaki araç reddederse → 2. araca geçer, reddeden sıra sonuna
    - Müşteri durağı filtrelemişse → Sadece o durak sırası kullanılır
    - Müşteri duraksız aramışsa → Tüm yakın taksiler (sıra + bağımsız)
```

##### 2.8.6.4 Veritabanı

```sql
-- Durak sıra tablosu
CREATE TABLE taxi_station_queue (
    id                  UUID PRIMARY KEY,
    station_id          UUID NOT NULL REFERENCES taxi_stations(id) ON DELETE CASCADE,
    vehicle_id          UUID NOT NULL REFERENCES taxi_vehicles(id),
    driver_id           UUID NOT NULL REFERENCES taxi_drivers(id),
    
    queue_order         INTEGER NOT NULL,                     -- Sıra numarası (1, 2, 3...)
    joined_at           TIMESTAMP DEFAULT NOW(),              -- Sıraya giriş zamanı
    
    status              VARCHAR(20) DEFAULT 'waiting',        -- waiting, dispatched, skipped, removed
    dispatched_at       TIMESTAMP,                            -- Yönlendirilme zamanı
    dispatched_to       UUID REFERENCES taxi_ride_requests(id), -- Hangi çağrı için
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_station_queue_station ON taxi_station_queue(station_id, queue_order);
CREATE INDEX idx_station_queue_status ON taxi_station_queue(status);

-- Sıra değişiklik logları
CREATE TABLE taxi_station_queue_log (
    id                  UUID PRIMARY KEY,
    station_id          UUID REFERENCES taxi_stations(id),
    
    action              VARCHAR(30) NOT NULL,        -- reorder, add, remove, dispatch, skip
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    old_position        INTEGER,
    new_position        INTEGER,
    changed_by          UUID REFERENCES users(id),  -- Yönetici veya sistem
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_station_queue_log_station ON taxi_station_queue_log(station_id);
```

##### 2.8.6.5 API

```
DURAK SIRASI API:
POST   /api/v1/taxi/station/{stationId}/queue/add             # Aracı sıraya ekle
POST   /api/v1/taxi/station/{stationId}/queue/remove          # Aracı sıradan çıkar
POST   /api/v1/taxi/station/{stationId}/queue/reorder         # Sırayı yeniden düzenle
GET    /api/v1/taxi/station/{stationId}/queue                 # Sıra durumu
GET    /api/v1/taxi/station/{stationId}/queue/next            # Sıradaki araç
POST   /api/v1/taxi/station/{stationId}/queue/dispatch        # Sıradan aracı yönlendir
POST   /api/v1/taxi/station/{stationId}/queue/reset           # Sırayı sıfırla (gün sonu)
GET    /api/v1/taxi/station/{stationId}/queue/log             # Sıra değişiklik logları

ADMIN:
GET    /api/v1/taxi/admin/station/{stationId}/queue/stats     # Sıra istatistikleri
```

##### 2.8.6.6 Sıra Önceliği ve İstisnalar

```yaml
Öncelikli Yönlendirme:
  Normal Akış:
    - Çağrı → Sıra-1 gider (FIFO)
  
  İstisnalar:
    - Müşteri "Konforlu Taksi" seçmişse:
      └── Sıradaki en yüksek puanlı araç gider (sıra atlanabilir)
    
    - Müşteri "Yakıt Tipi" seçmişse:
      └── Sıradaki uygun yakıtlı ilk araç gider
    
    - Müşteri "Kadın Şöför" seçmişse:
      └── Sıradaki kadın şöförlü ilk araç gider
      └── Yoksa sıradaki ilk araca geç
    
    - VIP müşteri çağrısı:
      └── Sıra-1 gider (yönetici onayı gerekmez)
    
    - Acil durum / Yaşlı / Engelli müşteri:
      └── Yönetici sıradaki en uygun aracı manuel yönlendirir
  
  Ceza Sistemi:
    - Çağrıyı reddeden araç → Sıra sonuna (3 kere üst üste = gün boyu men)
    - Durağa geç gelen / sırayı ihlal eden → Yönetici arkaya atar
    - Sahte konumla sıraya giren → Sistem tespit eder, sıradan çıkarır
```

---

#### 2.8.7 Veritabanı

```sql
CREATE TABLE taxi_stations (
    id                  UUID PRIMARY KEY,
    name                VARCHAR(200) NOT NULL,
    owner_id            UUID REFERENCES users(id),             -- Taksi sahibi / sorumlu
    company_id          UUID REFERENCES company_profiles(id) NULL,
    
    address             TEXT NOT NULL,
    latitude            DECIMAL(10,7) NOT NULL,
    longitude           DECIMAL(11,7) NOT NULL,
    city                VARCHAR(100),
    district            VARCHAR(100),
    
    phone               VARCHAR(20),
    capacity            INTEGER DEFAULT 0,                     -- 0 = sınırsız
    station_type        VARCHAR(50),                           -- iskele, cadde, havalimanı, AVM, vb.
    
    opening_time        TIME DEFAULT '06:00',
    closing_time        TIME DEFAULT '02:00',
    
    status              VARCHAR(20) DEFAULT 'pending',         -- pending, active, suspended
    is_active           BOOLEAN DEFAULT TRUE,
    
    total_vehicles      INTEGER DEFAULT 0,
    total_trips_today   INTEGER DEFAULT 0,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_stations_location ON taxi_stations(latitude, longitude);
CREATE INDEX idx_stations_city ON taxi_stations(city, district);

-- Araç-Durak bağlantısı
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    station_id          UUID REFERENCES taxi_stations(id);
```

#### 2.8.8 API

```
POST   /api/v1/taxi/station/create                    # Durak başvurusu oluştur
GET    /api/v1/taxi/station/{stationId}                # Durak detayı
PUT    /api/v1/taxi/station/{stationId}/update         # Durak güncelle
POST   /api/v1/taxi/station/{stationId}/add-vehicle    # Araç durağa ekle
POST   /api/v1/taxi/station/{stationId}/remove-vehicle # Araç duraktan çıkar
GET    /api/v1/taxi/station/{stationId}/vehicles       # Duraktaki araçlar
GET    /api/v1/taxi/stations/nearby?lat=X&lng=Y&radius=Z  # Yakındaki duraklar
GET    /api/v1/taxi/stations/search?city=İstanbul&district=Kadıköy  # Durak ara

ADMIN:
POST   /api/v1/taxi/admin/station/{stationId}/approve   # Admin durak onayla
POST   /api/v1/taxi/admin/station/{stationId}/reject    # Admin durak red
POST   /api/v1/taxi/admin/station/{stationId}/suspend   # Admin durağı askıya al
```

---

## 3. ÇOKLU ŞÖFÖR SİSTEMİ (VARDİYA)

### 3.1 Vardiya Tipleri

```yaml
VARDİYA TÜRLERİ:
│
├── Tam Gün (Tek Şöför)
│   ├── 06:00 - 22:00 (16 saat)
│   └── Tüm kazanç tek şöföre
│
├── Çift Vardiya (En Yaygın)
│   ├── Sabahçı: 06:00 - 14:00 (8 saat)
│   ├── Akşamçı: 14:00 - 22:00 (8 saat)
│   └── Günlük kira sabah/akşam bölüşülür
│
├── Üçlü Vardiya
│   ├── Sabah: 06:00 - 12:00 (6 saat)
│   ├── Öğle: 12:00 - 18:00 (6 saat)
│   └── Akşam: 18:00 - 24:00 (6 saat)
│
├── Hafta Sonu / Yarı Zamanlı
│   ├── Sadece hafta sonu çalışan
│   ├── Haftada 2-3 gün çalışan
│   └── Yedek şöför (diğer şöför izinliyken)
│
└── Gece Vardiyası
    ├── 22:00 - 06:00 (8 saat)
    └── Özel tarife ile çalışma
```

### 3.2 Vardiya Atama Sistemi

```
KURALLAR:
├── Bir araca aynı anda sadece 1 şöför atanabilir
├── Vardiya saatleri çakışamaz
├── Her vardiya başında şöför kendini "aktif" yapmalı
├── Aktif olmayan şöför çağrı alamaz
├── Vardiya değişiklikleri en az 24 saat önce bildirilmeli
└── Yedek şöför sistemi:

ÖRNEK VARDİYA TAKVİMİ:
              Pazartesi   Salı      Çarşamba  Perşembe   Cuma      Cumartesi  Pazar
Sabah(06-14)  Ahmet       Ahmet     Ahmet     Ahmet      Ahmet     Mehmet     Mehmet
Akşam(14-22)  Mehmet      Mehmet    Mehmet    Mehmet     Mehmet    Ali        Ali
Gece(22-06)   Ali         Ali       -         -          Ali       -          -

YEDEK:
Veli (Tüm saatlerde yedek, izin durumunda devreye girer)
```

### 3.3 Vardiya Değiştirme / İzin Süreci

```
Şöför İzin İster:
    ↓
Sistem diğer şöförlere bildirim gönderir
("Perşembe sabahçı vardiyası boşaldı, talip var mı?")
    ↓
Yedek şöför veya başka şöför talip olur
    ↓
Onay süreci:
├── Araç sahibi onayı (gerekli)
├── Vardiya eşleşmesi
└── Kira düzenlemesi (kira var ise)
    ↓
Vardiya güncellenir
```

---

## 4. ARAÇ KİRALAMA SİSTEMİ

### 4.1 Kira Modelleri

| Kira Türü | Süre | Ödeme | Kiralayan | Kullanan |
|-----------|------|-------|-----------|----------|
| **Günlük Kira** | 1 gün | Günlük sabit ücret | Araç Sahibi | Şöför |
| **Vardiyalı Kira** | 8 saat | Vardiya başı sabit | Araç Sahibi | Şöför |
| **Haftalık Kira** | 7 gün | Haftalık sabit | Araç Sahibi | Şöför |
| **Aylık Kira** | 30 gün | Aylık sabit | Araç Sahibi | Şöför |
| **Komisyonlu Kira** | Değişken | % üzerinden | Araç Sahibi | Şöför |

### 4.2 Kira Anlaşması (Sistem Sözleşmesi)

```
┌─────────────────────────────────────────────────────────────────┐
│  📋 KİRA SÖZLEŞMESİ #K2026-00145                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  KİRALAYAN (ARAÇ SAHİBİ):                                       │
│  ├── Ad: Ahmet Yılmaz                                          │
│  ├── Üye No: 2026-0001-3847                                    │
│  └── Araç: 34 TAK 1234 - Renault Megane 2023                   │
│                                                                 │
│  KİRACI (ŞÖFÖR):                                                │
│  ├── Ad: Mehmet Kaya                                            │
│  ├── Üye No: 2026-0002-9156                                    │
│  └── Ehliyet: 10.06.2030                                       │
│                                                                 │
│  KİRA ŞARTLARI:                                                  │
│  ├── Kira Türü: Vardiyalı (Akşam 14:00-22:00)                  │
│  ├── Kira Ücreti: 200 TL / gün (KDV dahil)                    │
│  ├── Kira Ödeme: Günlük (otomatik kesinti)                     │
│  ├── KM Sınırı: Yok                                            │
│  ├── Çalışma Bölgesi: İstanbul Avrupa Yakası                    │
│  ├── Başlangıç: 01.01.2026                                      │
│  ├── Bitiş: 31.12.2026 (otomatik yenilenebilir)                │
│  └── Fesih Bildirimi: 15 gün önceden                           │
│                                                                 │
│  EK ŞARTLAR:                                                    │
│  ├── Araç hasarı durumunda şöför sorumlu (kasko muafiyeti kadar)│
│  ├── Trafik cezaları şöföre aittir                              │
│  ├── Araç bakımı kiralayana aittir                              │
│  ├── Aracın müsait olduğu saatler dışında kullanılamaz          │
│  └── Sigorta hasarsızlık indirimi %50 kiralayana ait           │
│                                                                 │
│  ✅ KİRALAYAN ONAYI: 01.01.2026                                 │
│  ✅ KİRACI ONAYI: 01.01.2026                                    │
│                                                                 │
│  💰 ÖDEME DURUMU: Otomatik ödeme aktif                          │
│  ├── Bugünkü Kira: 200 TL (Akşam kazancından kesilecek)        │
│  ├── Toplam Ödenen: 12.400 TL (62 gün)                         │
│  └── Gecikme: Yok                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Otomatik Kira Tahsilat Sistemi

```
ADIM 1: Şöför yolculuk yapar → Kazanç oluşur
        ↓
ADIM 2: Gün sonu veya vardiya sonu
        ↓
ADIM 3: Sistem otomatik hesaplar:
        ├── Toplam Kazanç: 800 TL
        ├── Kira: -200 TL (kira sözleşmesine göre)
        ├── Platform Komisyonu: -40 TL (%5)
        └── Şöför Net: 560 TL
        ↓
ADIM 4: Kira ücreti → Araç Sahibi hesabına aktarılır
        ↓
ADIM 5: Kalan tutar → Şöför hesabına aktarılır
        ↓
ADIM 6: Şöför bakiyesi < Kira günlük tutarı ise:
        ├── Şöför uyarılır ("Hesabınızda kira için yeterli bakiye yok")
        └── Ertesi gün kira 2 katına çıkar (gecikme cezası)
```

### 4.4 Kira Anlaşmazlık Çözümü

```
ANLAŞMAZLIK DURUMLARI:
├── Araç hasarlı teslim edilmişse
├── Kira ödemesi yapılmamışsa
├── Vardiya saatlerine uyulmamışsa
├── Araç kurallara uygun kullanılmamışsa
└── Sözleşme şartları ihlal edilmişse

ÇÖZÜM SÜRECİ:
1. Taraflar mesajlaşır (platform üzerinden)
2. Anlaşma sağlanamazsa platform arabuluculuk yapar
3. Kanıtlar değerlendirilir (fotoğraf, mesaj kaydı, GPS verisi)
4. Karar verilir (haklı/haksız)
5. Parasal çözüm yapılır (iade/kesinti)
```

---

## 5. ARAÇ ORTAKLIĞI (HİSSELİ PLAKA)

### 5.1 Ortaklık Modelleri

```yaml
EŞİT ORTAKLIK:
  ├── Ali: %50
  ├── Veli: %50
  ├── Kiralık: Vardiyalı (kira bedeli ortaklara paylaşılır)
  └── Kâr Dağıtımı: Kira geliri %50-%50 paylaşılır

EŞİT OLMAYAN ORTAKLIK:
  ├── Ali: %70
  ├── Veli: %30
  ├── Kiralık: Vardiyalı
  └── Kâr Dağıtımı: Kira geliri %70-%30 paylaşılır

KARMA ORTAKLIK:
  ├── Firma XYZ Ltd: %50
  ├── Ali: %30
  ├── Veli: %20
  ├── Kiralık: Değil (ortaklar kendisi kullanır)
  └── Kâr Dağıtımı: Kazanç oranında paylaşılır
```

### 5.2 Ortaklık Yönetim Paneli

```
┌─────────────────────────────────────────────────────────────────┐
│  📋 34 TAK 1234 - ORTAKLIK BİLGİLERİ                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HİSSEDARLAR:                                                   │
│  ┌──────┬────────────┬────────┬──────────────────┬──────────┐  │
│  │ #    │ Ad Soyad   │ Hisse  │ Rol              │ Durum    │  │
│  ├──────┼────────────┼────────┼──────────────────┼──────────┤  │
│  │ 1    │ Ali Yılmaz │ %40    │ Ortak + Şöför    │ ✅ Aktif │  │
│  │ 2    │ Veli Kaya  │ %30    │ Ortak (Kirada)  │ ✅ Aktif │  │
│  │ 3    │ Ayşe Demir │ %30    │ Ortak (Kirada)  │ ✅ Aktif │  │
│  └──────┴────────────┴────────┴──────────────────┴──────────┘  │
│                                                                 │
│  AYLIK KAZANÇ DAĞILIMI:                                         │
│  ├── Toplam Kira Geliri: 15.000 TL                              │
│  │   ├── Sabahçı (Ali): Kira ödemez (kendisi kullanır)         │
│  │   └── Akşamçı (Mehmet): Günlük 250 TL × 30 = 7.500 TL      │
│  │                                                              │
│  ├── Ali (%40): 7.500 × 0.40 = 3.000 TL                        │
│  ├── Veli (%30): 7.500 × 0.30 = 2.250 TL                       │
│  ├── Ayşe (%30): 7.500 × 0.30 = 2.250 TL                       │
│  └── Toplam: 7.500 TL                                           │
│                                                                 │
│  ANLAŞMA SÜRESİ: 01.01.2026 - 31.12.2026                       │
│  HER YILBAŞI OTOMATİK YENİLENİR                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. SÜRÜCÜ-ARAÇ ANLIK EŞLEŞME SİSTEMİ

### 6.1 Sürücü Koltuğunda Kim Var? Sistemi

```
KRİTİK KURAL: "Sürücü koltuğunda kim varsa, çağrıldığında o görünür."

NASIL ÇALIŞIR:
│
├── Her vardiya başında şöför "Vardiyaya Başla" butonuna basar
│   └── Sistem, o anda araca kimin atanmış olduğunu kaydeder
│
├── Eğer araç sahibi kendisi kullanıyorsa:
│   └── "Kendim Kullanıyorum" seçeneği ile aktif eder
│
├── Eğer kiracı kullanıyorsa:
│   └── Kira sözleşmesindeki vardiya saatine göre otomatik aktif
│
├── Eğer yedek şöför ise:
│   └── Sadece asil şöför pasifken aktif olabilir
│
└── Çağrı anında:
    ├── Sistem şöförün aktif/pasif durumunu kontrol eder
    ├── Aktif ise çağrıyı gönderir
    └── Pasif ise çağrı gönderilmez
```

### 6.2 Anlık Durum Makinesi

```
                    ┌──────────┐
                    │  BOŞTA   │
                    │ (Müsait) │
                    └────┬─────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ┌──────────┐          ┌──────────┐
       │ YOLCU    │          │ MOLA     │
       │ ALDI     │          │ (Aktif   │
       │          │          │  değil)  │
       └────┬─────┘          └────┬─────┘
            │                     │
            ▼                     │
       ┌──────────┐               │
       │ YOLCULUK │               │
       │ BAŞLADI  │               │
       └────┬─────┘               │
            │                     │
            ▼                     │
       ┌──────────┐               │
       │ YOLCULUK │               │
       │ BİTTİ    │               │
       └────┬─────┘               │
            │                     │
            └──────────┬──────────┘
                       │
                       ▼
                  ┌──────────┐
                  │  BOŞTA   │
                  │ (Müsait) │
                  └──────────┘

DURUM GEÇİŞ KURALLARI:
├── BOŞTA → YOLCU ALDI: Şöför çağrıyı kabul ettiğinde
├── YOLCU ALDI → MOLA: Şöför molaya ayrıldığında
├── YOLCU ALDI → YOLCULUK BAŞLADI: Yolcu bindiğinde
├── YOLCULUK BAŞLADI → YOLCULUK BİTTİ: Varış noktasına gelindiğinde
├── YOLCULUK BİTTİ → BOŞTA: Yolcu indiğinde
└── MOLA → BOŞTA: Şöför moladan döndüğünde
```

---

### 6.3 Şöför Aktif/Pasif Seçimi ve Konum Zorunluluğu

Sisteme kayıtlı her taksici, **aktif veya pasif** olarak sistemde görünmeyi seçebilir.

```
AKTİF / PASİF SEÇİMİ:
├── AKTİF (Çevrimiçi) 🟢
│   ├── Araç haritada görünür
│   ├── Çağrı almaya hazır
│   ├── KONUM AÇIK OLMALIDIR (GPS zorunlu)
│   └── "Müsait" durumda çağrı bekler
│
├── PASİF (Çevrimdışı) 🔴
│   ├── Araç haritada görünmez
│   ├── Çağrı almaz
│   ├── Konum bilgisi sistemde kayıtlıdır ama gizlidir
│   └── Şöför kendi isteğiyle pasif olur
│
└── GEÇİŞ:
    ├── Şöför uygulamadan tek tuşla aktif/pasif geçişi yapar
    ├── Vardiya saati geldiğinde otomatik "pasif → aktif" önerisi
    └── Vardiya saati bittiğinde otomatik "aktif → pasif" önerisi
```

#### Konum Zorunluluğu

AKTİF modda olan her şöförün **GPS konumu açık olmak zorundadır**.

```
KONUM KURALLARI:
├── AKTİF mod: GPS açık olmalı
│   ├── Konum kapatılırsa → sistem otomatik PASİF'e alır
│   ├── 30 saniyede bir konum güncellenir
│   └── Konum doğruluğu: ±10 metre
│
├── PASİF mod: GPS tercihe bağlı
│   └── Sistem pasifte konumu kaydetmez (gizlilik)
│
└── KONUM İZİN YOKSA:
    ├── Şöför AKTİF olamaz
    ├── Uyarı: "Aktif olmak için konum izni verin"
    └── Ayarlar sayfasına yönlendirilir
```

#### Şöför Uygulama Ana Ekranı

```
┌──────────────────────────────────────────────┐
│  🚕 34 TAK 1234  │  ⭐ 4.8                   │
│  Ahmet Yılmaz                                 │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │         🟢  AKTİF                    │    │
│  │         (Müsait)                     │    │
│  │         [Dokun → Pasif Yap]          │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  📍 Konum: Açık ✅                           │
│  ⏱ Bugün: 8 yolculuk, 520 TL               │
│                                              │
│  [ ÇAĞRI BEKLENİYOR ]                        │
│  ┌──────────────────────────────────────┐    │
│  │  Yolcu: Ahmet Yılmaz                 │    │
│  │  Mesafe: 500 m                       │    │
│  │  Rota: Kavacık → Taksim              │    │
│  │  [ KABUL ET ]  [ REDDET ]            │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

---

### 6.4 Araç QR Kod Sistemi

Sisteme kayıtlı her araç için **sistem tarafından eşsiz bir kare kod (QR)** oluşturulur. Müşteri, araca binmeden önce bu kodu okutarak aracı doğrular ve yolculuğu başlatır.

```
QR KOD YERLEŞİMİ:
┌──────────────────────────────────┐
│         🚗 34 TAK 1234          │
│                                  │
│   ┌─────┐         ┌─────┐      │
│   │ QR  │         │ QR  │      │
│   │ KOD │         │ KOD │      │
│   │ [SAĞ│         │[SOL]│      │
│   │ KAPI│         │KAPI │      │
│   └─────┘         └─────┘      │
│                                  │
│         ┌──────────┐            │
│         │   QR KOD  │            │
│         │  [İÇERİ]  │            │
│         └──────────┘            │
│         (Ön panel / orta konsol)│
└──────────────────────────────────┘

KOD İÇERİĞİ:
├── Araç ID (UUID)
├── Plaka Numarası
├── Sistem Doğrulama Kodu (şifreli)
└── Geçerlilik Süresi (dinamik, günlük yenilenir)
```

#### 6.4.1 Biniş Süreci (QR ile)

```
MÜŞTERİ BİNİŞ AKIŞI:
├── ADIM 1: Müşteri taksiyi çağırır
├── ADIM 2: Taksi gelir
│
├── ADIM 3: QR OKUTMA (BİNMEDEN ÖNCE)
│   ├── Müşteri, SAĞ veya SOL kapıdaki QR kodu okutur
│   ├── Uygulama: "34 TAK 1234 - Doğrulandı ✅"
│   │   └── "Bu, çağırdığınız araç. Lütfen binin."
│   └── Güvenlik: QR okunmazsa araç değişmiş olabilir → UYAR
│
├── ADIM 4: Müşteri biner
│
├── ADIM 5: İÇERİDEKİ QR (opsiyonel)
│   ├── Müşteri içerideki QR'ı okutursa yolculuk başlar
│   └── Veya direk "Yolculuk Başlat" butonuna basar
│
└── ADIM 6: Yolculuk başlar
```

#### 6.4.2 QR Kod Güvenlik Özellikleri

```yaml
QR Kod Güvenliği:
  Eşsizlik:
    - Her araç için TEK bir QR kodu
    - Sistem tarafından üretilir, değiştirilemez
    - Kopyalanırsa: Sadece o araç için geçerli
  
  Dinamik İçerik:
    - QR kod içindeki doğrulama kodu her gün yenilenir
    - Eski kod 24 saat sonra geçersiz olur
    - Sistem, aracın o anki aktif durumunu sorgular
  
  Doğrulama:
    - Müşteri okutur → Sistem sorgular:
      ├── Bu araç gerçekten bu müşteriye mi atandı?
      ├── Araç aktif mi?
      └── Müşteri doğru yerde mi?
    - Tüm cevaplar ✅ → "Binebilirsiniz"
    - Herhangi biri ❌ → "Uyarı: Araç eşleşmiyor!"
  
  Sahte QR Koruması:
    - QR kodu sadece sistem uygulaması okutabilir
    - Elle yazılan/çizilen QR kodlar geçersiz
    - QR basılı çıktı alınıp başka araca yapıştırılırsa:
      └── Plaka ve kod eşleşmez → sistem reddeder
```

#### 6.4.3 Veritabanı

```sql
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    qr_code             VARCHAR(64) UNIQUE;          -- QR kod içeriği (hash)
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    qr_code_updated_at  TIMESTAMP;                   -- Son QR yenileme

CREATE TABLE taxi_qr_log (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    trip_id             UUID REFERENCES taxi_trips(id),
    customer_id         UUID REFERENCES users(id),
    
    scan_location       VARCHAR(30) NOT NULL,         -- right_door, left_door, interior
    scan_result         BOOLEAN NOT NULL,             -- başarılı mı?
    ip_address          VARCHAR(45),
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_qr_log_vehicle ON taxi_qr_log(vehicle_id);
```

#### 6.4.4 API

```
POST   /api/v1/taxi/vehicle/{vehicleId}/qr-generate     # QR kod oluştur/yenile
POST   /api/v1/taxi/trip/{tripId}/qr-scan               # QR kod okut (biniş)
GET    /api/v1/taxi/vehicle/{vehicleId}/qr-status       # QR kod durumu
```

---

### 6.5 Anlık Durak / Sokak Çağrısı (QR ile Hızlı Biniş)

Bir müşteri, sistem taksisini **durağında veya sokakta görüp** anında binmek istediğinde, sistem üzerinden çağrı yapmadan doğrudan QR kod okutarak binebilir.

```
SENARYO:
├── Taksi: Bir durakta / sokakta bekliyor (AKTİF)
├── Müşteri: Taksinin yanından geçiyor
├── Müşteri: Araçtaki QR kodu (sistem logosu + köşedeki kod) görüyor
├── Müşteri: "Bu, sistem taksisi, hemen bineyim" diyor
├── Müşteri: QR kodu okutuyor
├── Sistem: Şöför AKTİF mi? → ✅ Onay
└── Müşteri: Çağrı yapmadan BİNİYOR
```

#### 6.5.1 Akış

```
ANLIK ÇAĞRI (QR İLE BİNİŞ) AKIŞI:
├── ADIM 1: Müşteri, araç kapısındaki QR kodu okutur
│   └── Uygulama açılır (veya açık değilse açılır)
│
├── ADIM 2: Sistem kontrolü
│   ├── Şöför AKTİF mi? → ✅ Devam
│   │   └── PASİF ise → ❌ "Şöför şu an müsait değil"
│   │       └── Müşteri binemez (sistem onay vermez)
│   ├── Araç müsait mi? → ✅ Devam
│   └── Müşteri uygun mu? → ✅ Devam
│
├── ADIM 3: Onay ve Biniş
│   ├── Sistem onay verir ✅
│   ├── "34 TAK 1234 - Binebilirsiniz"
│   └── Müşteri araca biner
│
├── ADIM 4: Yolculuk Başlangıcı
│   ├── Taksici, taksimetreyi AÇMAK ZORUNDADIR
│   ├── Taksimetre açma ücreti (açılış) tahakkuk eder
│   └── Yolculuk başlar
│
└── ADIM 5: Yolculuk Sonu
    ├── Müşteri nerede inerse insin (1 metre bile gitse)
    ├── AÇILIŞ ÜCRETİNİ ÖDEMEK ZORUNDADIR
    └── Ödeme: Sistem üzerinden otomatik
```

#### 6.5.2 Ücretlendirme Kuralı

```
TAKSİMETRE AÇILIŞ ÜCRETİ ZORUNLULUĞU:
├── Müşteri QR okutup onay aldı → BİNİŞ GERÇEKLEŞTİ
├── Taksici taksimetreyi açar → Açılış ücreti yazılır
│
├── MÜŞTERİ İSTERSE 1 METRE GİTSİN:
│   ├── Açılış ücreti ödemek zorundadır
│   ├── Örnek: Açılış: 25 TL + 1 metre: 1 TL = 26 TL
│   └── Müşteri tekrar inse bile bu ücreti öder
│
└── KURAL:
    ├── QR onay → Biniş → Taksimetre açma → En az açılış ücreti
    ├── Müşteri vazgeçerse (binmeden): Ceza uygulanır (Bölüm 18)
    └── Taksici taksimetre açmazsa: Şöför cezalandırılır (-1 puan)
```

#### 6.5.3 Taksici ve Müşteri Ekranı

```
TAKSİCİ EKRANI (Anlık Biniş) :
┌──────────────────────────────────────────────┐
│  🟢 AKTİF                                     │
│                                              │
│  📱 QR OKUTULDU: Müşteri biniyor            │
│  ┌──────────────────────────────────────┐    │
│  │  Müşteri: Ayşe Demir                 │    │
│  │  Yöntem: Anlık QR İle Biniş          │    │
│  │  📍 Anlık Konum: Bağdat Cad. No:123  │    │
│  │                                       │    │
│  │  ⏱ Taksimetre Açıldı ✅              │    │
│  │  └── Açılış: 25 TL                   │    │
│  │                                       │    │
│  │  [ YOLCULUK BAŞLADI ]                 │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘

MÜŞTERİ EKRANI:
┌──────────────────────────────────────────────┐
│  ✅ Biniş Onaylandı                          │
│                                              │
│  🚗 34 TAK 1234                             │
│  👤 Şöför: Mehmet Yılmaz                     │
│  ⭐ 4.8                                      │
│                                              │
│  📍 Nereye gidiyorsunuz?                     │
│  ┌──────────────────────────────────┐        │
│  │ [Hedef adres girin]              │        │
│  └──────────────────────────────────┘        │
│                                              │
│  veya [Taksimetreye bırak, yolda söylerim]  │
│                                              │
│  ⚠️ Not: Taksimetre açıldı (25 TL)          │
│  En az açılış ücretini ödersiniz.           │
└──────────────────────────────────────────────┘
```

#### 6.5.4 Kısıtlamalar

```yaml
Anlık QR Biniş Kuralları:
  Müşteri:
    - Sistemde kayıtlı olmalı (üye)
    - Yeterli bakiyesi olmalı (veya tanımlı kart)
    - Güvenilir müşteri puanı 2.5+ olmalı
    - Ceza durumu yoksa (Bölüm 18)

  Şöför:
    - AKTİF modda olmalı (pasifse müşteri binemez)
    - Araç müsait olmalı (yolcu yok)
    - Taksimetre açmak zorunda
    - Taksimetre açmazsa → -1 puan ceza

  Yolculuk:
    - Minimum ücret: Taksimetre açılış ücreti
    - Müşteri 1 metre gitse bile bu ücreti öder
    - Müşteri binip inmediyse → Bölüm 18 cezası
```

---

### 6.6 Taksi Bekleme Lokasyonu (Ben Buradayım)

Taksiciler, şehrin farklı noktalarında **bekleme lokasyonu** oluşturup "Ben buradayım" şeklinde işaretleme yapabilir. Bu, müşterilerin bekleyen taksileri haritada görmesini sağlar.

#### 6.6.1 Bekleme Lokasyonu Oluşturma

```
BEKLEME NOKTASI AKIŞI:
├── ADIM 1: Taksici, aktif modda haritada bir nokta seçer
│   └── "Burada Bekliyorum" butonuna basar
│
├── ADIM 2: Bekleme noktası bilgileri
│   ├── 📍 Konum: Haritadan seçilir (veya anlık GPS)
│   ├── 🏷️ Etiket (opsiyonel): "Mecidiyeköy üst geçit yanı"
│   ├── ⏱ Bekleme süresi: Ne kadar bekleyeceği
│   │   ├── "15 dk"
│   │   ├── "30 dk"  
│   │   ├── "1 saat"
│   │   └── "Belirsiz"
│   └── 📝 Not (opsiyonel): "Köşedeki kırmızı bina önü"
│
├── ADIM 3: Sistem kaydı
│   ├── Bekleme noktası sisteme kaydedilir
│   ├── Müşteri haritasında görünür hale gelir
│   └── "🟢 34 TAK 1234 burada bekliyor" bildirimi
│
└── ADIM 4: Taksi hareket edince
    ├── GPS değişimi algılanır (50m+)
    ├── "Hala bekliyor musunuz?" sorusu
    │   ├── EVET → Bekleme devam
    │   └── HAYIR → Bekleme noktası silinir
    └── Yolcu alınca → Bekleme otomatik silinir
```

#### 6.6.2 Taksici Ekranı

```
TAKSİCİ BEKLEME EKRANI:
┌──────────────────────────────────────────────┐
│  🟢 AKTİF — BEKLİYOR                         │
│                                              │
│  📍 Anlık Konum: Bağdat Cad. No:123          │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  📌 BEN BURADAYIM                        ││
│  │                                          ││
│  │  🗺 [Haritada nokta seçin]               ││
│  │                                          ││
│  │  🏷️ Etiket: [Maksimum 50 karakter]     ││
│  │                                          ││
│  │  ⏱ Bekleme Süresi:                       ││
│  │  ○ 15 dk  ○ 30 dk  ○ 1 saat  ○ Belirsiz ││
│  │                                          ││
│  │  [ ✅ BEN BURADAYIM ]                    ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ⚠️ Araç hareket edince bekleme otomatik     │
│     sonlanır veya onay sorulur.              │
│                                              │
│  [ 🟢 Aktif Bekliyorum ]  [ 🔴 Pasif Yap ] │
└──────────────────────────────────────────────┘
```

#### 6.6.3 Müşteri Ekranı

Müşteri haritada **bekleme noktasındaki taksileri** görür ve doğrudan çağırabilir.

```
MÜŞTERİ HARİTA EKRANI:
┌──────────────────────────────────────────────┐
│  🗺 YAKINDAKİ TAKSİLER                       │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🟢 34 TAK 1234                           ││
│  │ 📍 Bağdat Cad. (Bekliyor)                ││
│  │ ⭐ 4.6 · 👤 Mehmet Y.                    ││
│  │ ⏱ ~30 dk bekler                          ││
│  │ 💰 Tahmini: 185 TL                        ││
│  │ [ ÇAĞIR ]                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🟢 34 TAK 5678                           ││
│  │ 📍 Moda Sahil (Bekliyor)                 ││
│  │ ⭐ 4.8 · 👤 Ali K.                        ││
│  │ ⏱ ~15 dk bekler                          ││
│  │ 💰 Tahmini: 195 TL                        ││
│  │ [ ÇAĞIR ]                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 🔵 34 TAK 4321                           ││
│  │ ⏳ Yolculukta (Taksim yönü)              ││
│  │ ~8 dk sonra müsait                       ││
│  │ [ BEKLE ]                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  🔽 FİLTRE:                                  │
│  ┌──────────────────────────────────┐        │
│  │ ☐ Tümü                           │        │
│  │ ☐ 🟢 Bekleyenler (3)            │        │
│  │ ☐ 🔵 Yolculuktakiler (2)        │        │
│  │ ☐ 🟡 Yakında müsait (1)         │        │
│  └──────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

#### 6.6.4 Bekleme Noktası Kuralları

```yaml
Bekleme Noktası Kuralları:
  Oluşturma:
    - Sadece AKTİF moddaki taksiciler bekleme noktası oluşturabilir
    - Aynı anda sadece 1 bekleme noktası aktif olabilir
    - Bekleme noktası oluşturmak için araç müsait olmalı
  
  Süre Yönetimi:
    - Maksimum bekleme süresi: 2 saat
    - Belirsiz seçilirse: 2 saat sonra otomatik sonlanır
    - Süre bitince: Taksiciye sorulur "Devam?"
    - Yanıt yoksa: Bekleme silinir, varsayılan GPS konumuna döner
  
  Otomatik Silinme:
    - Araç 50 metreden fazla hareket ederse → Onay sorulur
    - Yolcu alınınca → Otomatik silinir
    - Pasif moda geçince → Otomatik silinir
    - Vardiya bitince → Otomatik silinir
  
  Müşteri Görünürlüğü:
    - Bekleme noktası müşteri haritasında özel simgeyle gösterilir
    - Müşteri "Bekleyenler" filtresiyle sadece bekleyen taksileri görebilir
    - Bekleme süresi dolan taksi haritadan kaybolur
  
  Konum Doğrulama:
    - GPS kapalıysa bekleme noktası oluşturulamaz
    - GPS ile işaretlenen nokta arasında 100m'den fazla fark varsa uyarı
    - Sahte konum işaretleme: Tespit edilince ceza (-2 puan)
  
  Beklememe Hakkı:
    - Şöför isterse bekleme noktasını iptal edebilir
    - Ancak bu bir CEZA puanı düşümü ile sonuçlanır
    - Ceza puanı, müşterinin alternatif taksi bulma zorluğuna göre belirlenir
    - Gündüz (kolay): -5 puan
    - Gece / zor durum: -100 puana kadar çıkabilir
    - Şöför cezayı kabul ederek müşteriyi bırakır
    - Beklememe durumunda sistem başka taksi yönlendirir
```

#### 6.6.5 Veritabanı

```sql
CREATE TABLE taxi_waiting_spots (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    latitude            DECIMAL(10,7) NOT NULL,
    longitude           DECIMAL(11,7) NOT NULL,
    label               VARCHAR(100),                    -- "Mecidiyeköy üst geçit yanı"
    
    duration_minutes    INTEGER DEFAULT 30,              -- 15, 30, 60, 120, 0=belirsiz
    started_at          TIMESTAMP DEFAULT NOW(),
    expires_at          TIMESTAMP,                       -- started_at + duration
    auto_cleared        BOOLEAN DEFAULT FALSE,
    
    status              VARCHAR(20) DEFAULT 'active',    -- active, expired, cleared
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_waiting_spots_active ON taxi_waiting_spots(status, expires_at);
CREATE INDEX idx_waiting_spots_location ON taxi_waiting_spots(latitude, longitude);
```

#### 6.6.6 API

```
POST   /api/v1/taxi/driver/waiting-spot/create         # Bekleme noktası oluştur
PUT    /api/v1/taxi/driver/waiting-spot/update          # Güncelle (süre uzat, etiket değiştir)
POST   /api/v1/taxi/driver/waiting-spot/clear           # Bekleme noktasını temizle
GET    /api/v1/taxi/driver/waiting-spot/status          # Kendi bekleme durumum
GET    /api/v1/taxi/waiting-spots/nearby?lat=X&lng=Y    # Yakındaki bekleyen taksiler
```

---

### 6.7 Yolculuk Sonrası Otomatik Görevlendirme

Bir taksi yolculuğunu tamamlayıp müşterisini bıraktığında, şöför hâlâ **aktif moddaysa** ve çağrı almaya müsaitse, sistem onu durağa dönmesini beklemeden **yeni bir göreve yönlendirebilir**.

#### 6.7.1 Yolculuk Sonrası Akış

```
YOLCULUK BİTTİ → OTOMATİK GÖREVLENDİRME:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────────┐                                               │
│  │  YOLCULUK    │                                               │
│  │  TAMAMLANDI  │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────┐                               │
│  │  Şöför hâlâ AKTİF modda mı?  │                               │
│  └──────┬───────────────┬───────┘                               │
│         │               │                                        │
│        EVET             │ HAYIR                                 │
│         │               ▼                                        │
│         ▼          ┌──────────────┐                             │
│  ┌────────────────┐ │  Pasif moda  │                             │
│  │ Sistem kontrolü │ │  geçildi    │                             │
│  │ yapar:          │ │  → Bekleme  │                             │
│  │ ✅ Aktif        │ └──────────────┘                             │
│  │ ✅ Müsait       │                                              │
│  │ ✅ GPS açık     │                                              │
│  └───────┬────────┘                                               │
│          │                                                        │
│          ▼                                                        │
│  ┌──────────────────────────────────┐                            │
│  │  Yakında bekleyen çağrı var mı?  │                            │
│  └──────┬──────────────────┬───────┘                            │
│         │                  │                                       │
│        EVET              HAYIR                                   │
│         │                  │                                       │
│         ▼                  ▼                                       │
│  ┌──────────────┐  ┌──────────────────┐                         │
│  │ Çağrıya yön- │  │ Bekleme noktasına │                         │
│  │ lendirilir   │  │ yönlendirilir     │                         │
│  │ (isterse    │  │ (en yakın durak   │                         │
│  │  kabul/red) │  │  veya bekleme     │                         │
│  └──────────────┘  │  noktası)         │                         │
│                    └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

#### 6.7.2 Pilot / Otomatik Görevlendirme

```
PİLOT GÖREVLENDİRME MODLARI:
├── MOD 1: Otomatik Kabul
│   ├── Şöför "Otomatik Kabul" modunu açmışsa
│   ├── Yolculuk biter bitmez sistem en yakın çağrıyı atar
│   ├── Şöför reddedemez (acil durum hariç)
│   └── Şöför: 15 sn içinde müdahale etmezse otomatik kabul
│
├── MOD 2: Öneri Modu
│   ├── Sistem çağrı önerisi gösterir
│   ├── "Yeni çağrı: Kadıköy → Taksim, 185 TL"
│   ├── Şöför kabul veya reddeder
│   ├── Reddederse: Başka çağrı gösterilir (maks 3 deneme)
│   └── Reddedince 5 dk bekleme (sürekli reddi engellemek için)
│
├── MOD 3: Durak Dönüş
│   ├── Şöför durağa dönmek istiyorsa
│   ├── Sistem çağrı göstermez, durağa yönlendirir
│   └── Durak sırasına eklenir (varsa)
│
└── MOD 4: Pasif
    ├── Şöför işi bırakıyorsa
    └── Pasif moda geçer, çağrı almaz
```

#### 6.7.3 Yolculuk Sonrası Şöför Ekranı

```
YOLCULUK SONRASI ŞÖFÖR EKRANI:
┌──────────────────────────────────────────────┐
│  ✅ YOLCULUK TAMAMLANDI                      │
│                                              │
│  📍 Varış: Taksim Meydanı                   │
│  💰 Ücret: 185 TL (bahşiş: 25 TL)           │
│  ⭐ Müşteri puanı: 4.5                       │
│                                              │
│  ───────────────────────────────────────     │
│                                              │
│  🟢 AKTİF — Çağrı almaya hazır              │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  📞 YENİ ÇAĞRI ÖNERİSİ                   ││
│  │                                          ││
│  │  📍 Şu an: Taksim                        ││
│  │  🎯 Çağrı: Taksim → Kadıköy (2 km)      ││
│  │  💰 Tahmini: 65 TL                       ││
│  │                                          ││
│  │  ⏱ Kabul için 15 saniyeniz var          ││
│  │                                          ││
│  │  [ ✅ KABUL ]  [ ❌ RED ]  [ ⏳ BEKLE ]  ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ 🤖      │ │ 📞      │ │ 🏪      │     │
│  │ Otomatik │ │ Çağrı   │ │ Durağa  │     │
│  │ Kabul   │ │ Ara     │ │ Dön    │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│                                              │
│  [ 🔴 PASİF YAP ]                            │
└──────────────────────────────────────────────┘
```

#### 6.7.4 Kesintisiz Görev Döngüsü

```
KESİNTİSİZ GÖREV DÖNGÜSÜ:
┌─────────────────────────────────────────────────────┐
│                                                      │
│  🚕 Yolculuk 1 → Tamamlandı                         │
│      ↓                                               │
│  🔄 Sistem yeni çağrı kontrolü                       │
│      ↓                                               │
│  🚕 Yolculuk 2 → Atandı                             │
│      ↓                                               │
│  🔄 Sistem yeni çağrı kontrolü                       │
│      ↓                                               │
│  🚕 Yolculuk 3 → Atandı                             │
│      .                                               │
│      .                                               │
│      ↓                                               │
│  🔴 Şöför pasif yapana kadar DEVAM                   │
│                                                      │
│  📈 Avantaj:                                         │
│  ├── Şöför boş beklemez, sürekli kazanır            │
│  ├── Müşteri beklemez, hızlı eşleşir                 │
│  └── Sistem verimliliği artar                        │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 6.7.5 Yolculuk Sonrası Otomatik Görevlendirme Kuralları

```yaml
Otomatik Görevlendirme Kuralları:
  Şartlar:
    - Şöför AKTİF modda olmalı
    - GPS konumu açık olmalı
    - Araç müsait olmalı (yolcu yok)
    - Şöför "Çağrı Almaya Hazır" durumunda olmalı
    - Son yolculuğun üzerinden en az 10 saniye geçmeli (güvenlik)

  Çağrı Eşleştirme:
    - Sistem mevcut konuma en yakın çağrıyı seçer
    - Çağrı şöföre 3 km mesafeye kadar olabilir
    - Şöför tercihleri (konfor, yakıt, cinsiyet) dikkate alınır
    - Müşteri puanı düşükse eşleştirme önceliği düşer

  Şöför Hakları:
    - Çağrıyı reddetme hakkı (günde maksimum 5 red)
    - 5. resten sonra 30 dk çağrı gösterilmez
    - Acil durumlarda "Pasif" butonu ile çıkış
    - Mola: "15 dk mola" butonu ile çağrıları durdurabilir

  Sistem Koruması:
    - Aynı noktada 5 dk içinde tekrar çağrı gelmez (spam koruma)
    - Şöför sürekli aynı bölgede kalıyorsa çağrı çeşitliliği sağlanır
    - Gece 00:00-06:00 arası çağrı mesafesi 5 km ile sınırlı
    - Tüm görevlendirmeler loglanır
```

#### 6.7.6 Veritabanı

```sql
-- Mevcut taxi_driver_status tablosuna ek:
ALTER TABLE taxi_driver_status ADD COLUMN IF NOT EXISTS
    auto_assign_mode       VARCHAR(20) DEFAULT 'suggest'; -- off, auto_accept, suggest, return_station

ALTER TABLE taxi_driver_status ADD COLUMN IF NOT EXISTS
    last_trip_ended_at     TIMESTAMP;                      -- Son yolculuk bitiş zamanı

ALTER TABLE taxi_driver_status ADD COLUMN IF NOT EXISTS
    reject_count_today     INTEGER DEFAULT 0;              -- Bugünkü red sayısı

ALTER TABLE taxi_driver_status ADD COLUMN IF NOT EXISTS
    last_reject_at         TIMESTAMP;                      -- Son reddetme zamanı
```

#### 6.7.7 API

```
POST   /api/v1/taxi/driver/auto-assign-mode          # Otomatik görevlendirme modu değiştir
GET    /api/v1/taxi/driver/auto-assign-status         # Mevcut durum
POST   /api/v1/taxi/driver/trip/{tripId}/complete     # Yolculuk tamamlandı + sonraki çağrıya hazır
POST   /api/v1/taxi/driver/next-ride                  # Sonraki yolculuğu iste (sıradaki çağrıyı al)
POST   /api/v1/taxi/driver/skip-ride                  # Çağrıyı atla

DRIVER PREFERENCES:
PUT    /api/v1/taxi/driver/auto-accept                # Otomatik kabul aç/kapa
PUT    /api/v1/taxi/driver/max-distance               # Maksimum çağrı mesafesi
POST   /api/v1/taxi/driver/take-break                 # Mola başlat (15/30/60 dk)
POST   /api/v1/taxi/driver/end-break                  # Molayı bitir
```

---

## 7. ÇİFT YÖNLÜ PUANLAMA SİSTEMİ

> ⚠️ **TÜM PLATFORM İÇİN ORTAK KURAL:** Bu bölümdeki puanlama kuralları (1 işlem = 1 yorum hakkı, 3 seçenekli oylama, yorum silinemez, anti-troll) **taksi, yemek ve diğer tüm platform servisleri için geçerlidir.** Ayrıca **adres ve konum bilgisi** her kullanıcı için zorunludur; adressiz/konumsuz hesap ile işlem yapılamaz. Detaylı uygulama farklılıkları ilgili servis dokümanında belirtilmiştir.

### 7.0 Platform Geneli Puanlama Kuralları

Aşağıdaki kurallar **tüm platform servisleri** (taksi, yemek, vb.) için aynen geçerlidir:

| Kural | Açıklama |
|-------|----------|
| **1 işlem = 1 yorum hakkı** | Platform üzerinden ödeme yapan kullanıcı, her işlem için **1 adet** yorum/puan hakkı kazanır. Platformdan ödemeyen (ör: üçüncü kişi adına alınan sipariş) yorum yapamaz. |
| **3 seçenekli oylama** | Beğendim 👍 (+1) / Pas ⏭️ (0 etki) / Kötü 👎 (-1). Klasik 1-5 yıldız sistemi **kullanılmaz**, bunun yerine bu 3 seçenek + opsiyonel yorum metni kullanılır. |
| **Yorum silinemez** | Ne hizmet sağlayıcı (şöför/restoran) ne de müşteri yorumunu silebilir. Sadece **platform yetkilisi** ihlal durumunda (küfür, hakaret, ticari ifşa) gizleyebilir. |
| **Anti-troll sistemi** | Bir kullanıcının oylarının %90+ olumsuz (Kötü 👎) ise **tüm oyları geçersiz** sayılır, istatistiklere eklenmez. Kullanıcı uyarılır, devamında hesap kısıtlanır. |
| **Puan = sıralama** | Hiçbir hizmet sağlayıcı (şöför/restoran) reklam vererek sıralamada yükselemez. Sıralama tamamen puana dayalıdır. |

> 📌 Taksi özelinde puanlama, bu ortak kuralların üzerine **ek detay kriterler** (sürüş kalitesi, davranış, temizlik vb.) ile genişletilmiştir. Aşağıdaki alt bölümler taksiye özgü detayları açıklar.

### 7.1 Felsefe: Müşteriye Kolay, Sistemde Detaylı

Puanlama sistemi **iki kademeli** çalışır:

```
KADEME 1 — MÜŞTERİ ANKETİ (2 Soru) 🧑‍✈️
├── Yolculuk sonunda müşteriye SADECE 2 soru sorulur:
│   ├── "Taksiden memnun kaldınız mız?" (1-5 ⭐)
│   └── "Taksiciden memnun kaldınız mı?" (1-5 ⭐)
│
├── Süre: 5 saniye (çok hızlı, yormaz)
└── Sonuç: Müşteri memnuniyetini basitçe ölçer

KADEME 2 — SİSTEM PUANLAMASI (Detaylı) ⚙️
├── Müşteriye sorulmaz, sistem ARKA PLANDA hesaplar
├── Kaynaklar:
│   ├── Araç sensörleri (GPS, hız, fren, korna)
│   ├── Yolcu anketinden çıkarım (dolaylı)
│   ├── Resmi trafik cezaları
│   └── Geçmiş istatistiksel veriler
│
├── Detaylı puanlar (7.9 - 7.17): Sadece sistem tarafından
│   hesaplanır, müşteri görmez
└── Sonuç: Kombine puana katkı sağlar
```

### 7.2 Müşteri Anketi (2 Soru)

Yolculuk bittiğinde müşteriye aşağıdaki ekran gösterilir:

```
┌──────────────────────────────────────────────┐
│  🚕 Yolculuk Tamamlandı                      │
│                                              │
│  Kadıköy → Taksim | 8.5 km | 167 TL          │
│  Şöför: Mehmet Y. | 34 ABC 123              │
│                                              │
│  ─── SADECE 2 SORU ───                      │
│                                              │
│  1️⃣ Taksiden memnun kaldınız mı?            │
│     (araç temizliği, konfor, koku)           │
│                                              │
│     ⭐⭐⭐⭐⭐                                │
│     (1-5 arası seçim)                        │
│                                              │
│  2️⃣ Taksiciden memnun kaldınız mı?          │
│     (güler yüz, sürüş, davranış)             │
│                                              │
│     ⭐⭐⭐⭐⭐                                │
│     (1-5 arası seçim)                        │
│                                              │
│  [ OYLA ]                                    │
│                                              │
│  📝 Yorum eklemek ister misiniz? (opsiyonel) │
│  ┌──────────────────────────────────┐        │
│  │                                  │        │
│  └──────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

Bu 2 soru, müşterinin **ortalama memnuniyetini** ölçer. Detaylı puanlar (7.9-7.17) buradan **dolaylı olarak** veya sistem sensörleriyle hesaplanır.

### 7.3 Detaylı Puanların Sistem Tarafından Hesaplanması

Müşterinin 2 soruya verdiği cevaplar + sistem verileri birleşerek detaylı puanları oluşturur:

```
ÖRNEK: Düşük Taksi Puanı (2 ⭐) Geldi
├── Sistem şu çıkarımları yapar:
│   ├── Yüksek ihtimal: Araç temiz değil
│   ├── Yüksek ihtimal: Araç kokusu var
│   └── Düşük ihtimal: Araç konforu kötü
│
├── Sistem sensörlerini kontrol eder:
│   ├── Son 10 yolculukta temizlik puanı: 4.2 (düşük ✅)
│   └── Koku şikayeti: 3 yolcu (✅ doğrulandı)
│
└── Araç İçi Temizlik Puanı (7.10): Otomatik düşürülür

ÖRNEK: Yüksek Şöför Puanı (5 ⭐) Geldi
├── Sistem şu çıkarımları yapar:
│   ├── Sürüş iyi olabilir
│   ├── Güler yüz iyi olabilir
│   └── Davranış iyi olabilir
│
├── Sistem sensörlerini kontrol eder:
│   ├── Son 20 yolculukta korna: 0 (✅)
│   ├── Hız ihlali: 0 (✅)
│   └── Yolcu yorumları: "Çok nazik" (✅)
│
└── Tüm şöför puanları olumlu etkilenir
```

### 7.4 Klasik Puanlama Kriterleri (Sistem Tarafı)

| Kriter | Ağırlık | 1 Yıldız | 5 Yıldız |
|--------|---------|----------|----------|
| **Sürüş Kalitesi** | %30 | Ani fren/sollama yok | Çok düzgün, güvenli |
| **Zamanında Gelme** | %20 | 20 dk gecikti | 3 dk içinde geldi |
| **İletişim** | %15 | Kaba, sessiz | Güleryüzlü, bilgilendirici |
| **Güvenli Sürüş** | %15 | Hız limiti aşar, telefonla konuşur | Çok güvenli |
| **Rota Bilgisi** | %10 | Yolu bilmez, sürekli navigasyon | Kestirme yollar bilir |
| **Yardımseverlik** | %10 | Bagaja yardım etmez | Çok yardımcı |

### 7.5 Araç Puanlama Kriterleri (Sistem Tarafı)

| Kriter | Ağırlık | 1 Yıldız | 5 Yıldız |
|--------|---------|----------|----------|
| **Araç Temizliği** | %30 | İçi pis, saç, çöp | Tertemiz, hijyenik |
| **Araç Kokusu** | %20 | Sigara kokar, çok kötü | Hafif güzel koku |
| **Araç Konforu** | %20 | Koltuklar rahatsız, süspansiyon kötü | Çok rahat |
| **Klima/Isıtma** | %15 | Çalışmıyor | Mükemmel çalışıyor |
| **Genel Bakım** | %15 | Ses gelir, kapı zor açılır | Pırıl pırıl, yeni gibi |

### 7.6 Kombine Puan Hesaplama

```
KOMBİNE PUAN FORMÜLÜ:

Kombine Puan = (Şöför Puanı × 0.60) + (Araç Puanı × 0.40)

ÖRNEK:
├── Şöför Puanı: 4.8
│   ├── Sürüş Kalitesi: 5.0
│   ├── Zamanında Gelme: 4.7
│   ├── İletişim: 4.9
│   ├── Güvenli Sürüş: 4.8
│   ├── Rota Bilgisi: 4.6
│   └── Yardımseverlik: 4.8
│
├── Araç Puanı: 4.6
│   ├── Araç Temizliği: 4.5
│   ├── Araç Kokusu: 4.7
│   ├── Araç Konforu: 4.6
│   ├── Klima/Isıtma: 4.8
│   └── Genel Bakım: 4.4
│
└── Kombine Puan = (4.8 × 0.60) + (4.6 × 0.40) = 2.88 + 1.84 = 4.72 ⭐
```

### 7.7 Sıralama Algoritması

```
ARAMA SIRALAMASINDA KULLANILAN KRİTERLER:
│
├── 1️⃣ Kombine Puan (%40)
│   ├── 5.0 → 100 puan
│   ├── 4.5 → 80 puan
│   └── 4.0 → 60 puan
│
├── 2️⃣ Toplam Yolculuk Sayısı (%20)
│   ├── 1000+ → 100 puan
│   ├── 500+ → 80 puan
│   └── 100+ → 50 puan
│
├── 3️⃣ Çağrı Kabul Oranı (%20)
│   ├── %95+ → 100 puan
│   ├── %80+ → 70 puan
│   └── %60+ → 40 puan
│
├── 4️⃣ Anlık Müsaitlik (%10)
│   └── Müsait → 100 puan, Meşgul → 0 puan
│
├── 5️⃣ Mesafe (%10)
│   ├── 0-500m → 100 puan
│   ├── 500m-1km → 80 puan
│   ├── 1-2km → 60 puan
│   ├── 2-5km → 40 puan
│   └── 5km+ → 20 puan
│
├── SIRALAMA = (Kombine Puan × 0.40) + (Yolcuk × 0.20) + (Kabul × 0.20) + (Müsait × 0.10) + (Mesafe × 0.10)
│
└── ÖRNEK:
    ├── Kombine: 4.72 → (94 × 0.40) = 37.6
    ├── Yolcuk: 156 → (78 × 0.20) = 15.6
    ├── Kabul: %92 → (92 × 0.20) = 18.4
    ├── Müsait: Evet → (100 × 0.10) = 10
    ├── Mesafe: 300m → (100 × 0.10) = 10
    └── TOPLAM: 91.6 PUAN → 1. SIRA
```

### 7.8 Çağrı Reddetme Cezaları

```
CEZA SİSTEMİ:
│
├── Her çağrı reddi → -1 puan (sürüş puanından düşer)
├── Günlük maksimum red: 3 (3. redden sonra ek ceza)
├── Aylık red limiti: 20 (aşarsa 1 gün hizmet durdurma)
│
├── Geçerli Ret Sebepleri: (Cezasız)
│   ├── Araç bakımda
│   ├── Sağlık sorunu
│   ├── Özel mazeret (bildirilmeli)
│   └── Yakıt alımı
│
├── Geçersiz Ret Sebepleri: (Ceza Puanı)
│   ├── "Kısa mesafe istemiyorum" → -1
│   ├── "Trafik sıkışık" → -1
│   ├── "Semti sevmiyorum" → -1
│   └── "Sebepsiz" → -2
│
├── Çağrıya Yanıt Vermeme (15 saniye timeout)
│   └── Otomatik ret sayılır → -1
│
└── ACİL DURUM: Kötü hava, doğal afet gibi durumlarda ceza sistemi devre dışı
```

---

### 7.9 Sürüş Kademe ve Konfor Onay Sistemi

#### 7.9.1 Sürüş Kademe Puanı (1-10)

Sürüş kalitesi, geleneksel 1-5 yıldızın ötesinde **1-10 arası detaylı bir kademe puanı** ile ölçülür. Bu puan, şöförün arabayı ne kadar **usta ve kademeli** kullandığını gösterir.

| Kademe | Seviye | Açıklama |
|--------|--------|----------|
| **10** | 🏆 Efsane Sürücü | Mükemmel akıcılık, sıfır ani hareket, yolcu hissetmez |
| **9** | 🥇 Usta Şöför | Çok düzgün, profesyonel, tüm virajları mükemmel alır |
| **8** | 🥈 Çok İyi | Hemen hemen hiç sarsıntı yok, çok konforlu |
| **7** | 🥉 İyi | Genelde düzgün, nadiren hafif ani fren |
| **6** | 👍 Orta-İyi | Çoğunlukla düzgün, bazen hafif sert kalkış |
| **5** | ➡️ Orta | Normal şehir içi sürüş, zaman zaman ani hareket |
| **4** | 👎 Orta-Kötü | Sık ani fren/kalkış, virajlarda sert |
| **3** | ❌ Kötü | Rahatsız edici sürüş, çok ani hareket |
| **2** | ❌❌ Çok Kötü | Sürekli sarsıntılı, güvensiz hissettirir |
| **1** | ⛔ Tehlikeli | Aşırı agresif, yolcu kendini güvende hissetmez |

```
PUANLAMA NASIL OLUŞUR:
├── Her yolculuk sonunda yolcu 1-10 arası sürüş puanı verir
│
├── Sürüş Puanı Kriterleri:
│   ├── 🏁 Kalkış: Ani kalkış mı? Kademeli mi? (1-10)
│   ├── 🛑 Fren: Ani fren mi? Yumuşak mı? (1-10)
│   ├── 🔄 Viraj: Sert dönüş mü? Akıcı mı? (1-10)
│   ├── ⚡ Hız Sabitleme: Sürekli gaz-fren mi? Dengeli mi? (1-10)
│   └── 🔊 Motor Ses: Zorlama var mı? Doğal akışta mı? (1-10)
│
├── Şöförün Sürüş Kademe Puanı = Son 100 yolculuğun ortalaması
│
└── Kademe Puanı, Kombine Puanda "Sürüş Kalitesi" alt kriterini besler:
    ├── Kademe 8-10 → Sürüş Kalitesi 5.0 ⭐
    ├── Kademe 6-7  → Sürüş Kalitesi 4.0 ⭐
    ├── Kademe 4-5  → Sürüş Kalitesi 3.0 ⭐
    ├── Kademe 2-3  → Sürüş Kalitesi 2.0 ⭐
    └── Kademe 1    → Sürüş Kalitesi 1.0 ⭐
```

#### 7.9.2 Konfor Onayı (Comfort Approval Badge)

Şöför **8.00 ve üzeri** Sürüş Kademe Puanına sahipse, **"✅ Konfor Onaylı"** rozeti kazanır. Bu rozet, arama sonuçlarında ve şöför profilinde görünür.

```
ROZET KURALLARI:
├── Minimum: Sürüş Kademe Puanı ≥ 8.00 (son 100 yolculuk ortalaması)
├── Ek şart: Son 100 yolculukta en az 80 adet sürüş puanı alınmış olmalı
│
├── ROZET AKTİF:
│   ┌─────────────────────────────────────────────────────┐
│   │  🚗 34 ABC 123  │  ⭐ 4.9  │  ✅ KONFOR ONAYLI     │
│   │  👤 Mehmet Y.   │  🏆 9.2  │  "Bu taksi konforlu"  │
│   └─────────────────────────────────────────────────────┘
│
├── ROZET PASİF (yüksek puan var ama yeterli oy yok): 
│   ┌─────────────────────────────────────────────────────┐
│   │  🚗 34 ABC 123  │  ⭐ 4.8  │  ⏳ Rozet için 18 oy  │
│   │  👤 Mehmet Y.   │  🏆 9.1  │  daha gerekli         │
│   └─────────────────────────────────────────────────────┘
│
├── ROZET KAYBI:
│   ├── Eğer puan 7.50'nin altına düşerse rozet gider
│   │   └── (8.00 kazanma eşiği, 7.50 kaybetme eşiği)
│   └── Rozet kaybından sonra tekrar kazanmak için
│       8.00 üstüne çıkıp 20 yolculuk daha yapmak gerekir
│
└── YOLCU GERİ BİLDİRİMİ:
    └── Yolculuk sonu ekranında:
        ┌──────────────────────────────────────────────┐
        │  ✅ BU TAKSİ KONFOLUYDU                       │
        │                                               │
        │  "Evet, bu taksi konforluydu" butonuna basın  │
        │  → Şöförün Konfor Onayına katkı sağlayın      │
        └──────────────────────────────────────────────┘
```

#### 7.9.3 Kombine Puan'a Etkisi

Sürüş Kademe Puanı, mevcut "Sürüş Kalitesi" kriterini (%30 ağırlık) besler. Konfor Onayı ise doğrudan puanı etkilemez ancak **sıralamada bonus** sağlar.

```
SIRALAMA BONUSU:
├── ✅ Konfor Onaylı şöförler: Kombine Puan'da +%5 bonus
│   └── Örnek: 4.72 → 4.72 × 1.05 = 4.96
│
├── Arama filtresi: Yolcu "Sadece Konfor Onaylı" seçeneği ile filtreleyebilir
│
└── Haritada: Konfor Onaylı taksiler özel simgeyle gösterilir
    └── 🚕 (normal) vs ⭐🚕 (konfor onaylı)
```

#### 7.9.4 Veritabanı Alanları

```sql
-- Mevcut taxi_drivers tablosuna ek alanlar
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    driving_tier        NUMERIC(2,1) DEFAULT 5.0;    -- Sürüş Kademe Puanı (1.0 - 10.0)
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    comfort_approved    BOOLEAN DEFAULT FALSE;        -- Konfor Onayı rozeti
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    comfort_approved_at TIMESTAMP;                    -- Rozet kazanma tarihi
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    total_driving_scores INTEGER DEFAULT 0;           -- Toplam sürüş puanı sayısı
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    last_100_driving_avg NUMERIC(3,1);               -- Son 100 sürüş ortalaması

-- Her yolculuğun sürüş kademe detayları
CREATE TABLE taxi_driving_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    -- 1-10 alt kriterler
    acceleration_score  NUMERIC(2,1) NOT NULL,        -- Kalkış kademeliliği
    braking_score       NUMERIC(2,1) NOT NULL,        -- Fren yumuşaklığı
    cornering_score     NUMERIC(2,1) NOT NULL,        -- Viraj akıcılığı
    speed_stability     NUMERIC(2,1) NOT NULL,        -- Hız sabitleme
    engine_smoothness   NUMERIC(2,1) NOT NULL,        -- Motor kullanımı
    
    -- Genel sürüş kademe puanı (5 alt kriterin ortalaması)
    overall_score       NUMERIC(2,1) NOT NULL,
    
    -- Konfor onayı
    passenger_confirmed_comfort BOOLEAN DEFAULT FALSE, -- Yolcu "Bu taksi konforlu" dedi mi?
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_driving_scores_driver ON taxi_driving_scores(driver_id);
CREATE INDEX idx_driving_scores_trip ON taxi_driving_scores(trip_id);
```

#### 7.9.5 API Endpoint'leri

```
GET    /api/v1/taxi/driver/{driverId}/driving-tier       # Sürüş Kademe Puanı
GET    /api/v1/taxi/driver/{driverId}/driving-history    # Sürüş puanı geçmişi
POST   /api/v1/taxi/trip/{tripId}/driving-score          # Yolculuk için sürüş puanı ver
POST   /api/v1/taxi/trip/{tripId}/confirm-comfort        # "Bu taksi konforlu" onayı
GET    /api/v1/taxi/search?comfort=true                  # Sadece konfor onaylı taksiler
```

---

### 7.10 Yoldaki Davranış ve Tutum Puanı

Sürüş tekniğinden (kademe/usta şöför) **tamamen ayrı** bir puandır. Şöförün yolda sergilediği davranış, diğer sürücülere saygı, trafik kurallarına uyum ve genel tutumunu ölçer.

```
SÜRÜŞ TEKNİĞİ (7.9) vs DAVRANIŞ (7.10):
├── Sürüş Kademe Puanı: Arabayı NASIL kullandığı
│   └── Ani fren mi? Kademeli kalkış mı? Viraj akıcı mı?
│
├── Davranış ve Tutum Puanı: Yolda NASIL DAVRANDIĞI
│   └── Korna çaldı mı? Küfür etti mi? Saygılı mı?
│
└── İkisi ayrı ayrı hesaplanır, kombine puana farklı etki eder
```

#### 7.10.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Trafik Kurallarına Uyum** | %25 | Kırmızı ışık, hız limiti, emniyet şeridi ihlali var mı? |
| **Diğer Sürücülere Saygı** | %20 | Sinyal kullanımı, yol verme, selektör yapmama |
| **Sakinlik / Öfke Kontrolü** | %20 | Trafikte sakin mi? Korna, küfür, el hareketi var mı? |
| **Yayalara Duyarlılık** | %15 | Yaya geçidinde yavaşlama, yayaya öncelik verme |
| **Yolcuya Karşı Tutum** | %10 | Yolcu varken diğer sürücülere bağırma/küfür |
| **Çevre Duyarlılığı** | %10 | Gereksiz korna, çevre kirliliği, egzoz |

```
PUANLAMA DETAYI:
├── 10: Örnek sürücü, trafikte melek gibi, herkese saygılı
├── 9: Çok kibar, asla sinyaliz sorunu yok
├── 8: Genelde sakin, nadiren hafif sinir
├── 7: Normal şehir içi davranış, ortalama
├── 6: Bazen sinirlenir ama kontrol eder
├── 5: Arada korna, hafif agresyon
├── 4: Sık sık korna, selektör, sinirlenme
├── 3: Diğer sürücülere bağırma, el hareketi
├── 2: Sürekli agresif, yayaları dikkate almaz
└── 1: Tehlikeli, saldırgan, trafik canavarı
```

#### 7.10.2 Otomatik Sensör ve Yolcu Puanı Karması

Davranış puanı **iki kaynaktan** beslenir:

```
PUAN KAYNAKLARI:
├── 1️⃣ YOLCU PUANI (%60)
│   └── Her yolculuk sonunda yolcu 1-10 arası değerlendirir:
│       "Şöför yolda nasıl davrandı?"
│       ├── Çok saygılı ve sakindi 😊 → 10
│       ├── Normal davrandı 😐 → 6-7
│       ├── Korna çaldı, sinirlendi 😠 → 3-4
│       └── Küfür etti, agresifti 🤬 → 1-2
│
└── 2️⃣ SİSTEM SENSÖRLERİ (%40) — Otomatik tespit
    ├── Sensör: Ani korna (telefon mikrofonu / araç sensörü)
    ├── Sensör: Sert fren / hızlı kalkış (araç telematiği)
    ├── Sensör: Hız limiti aşımı (GPS + hız verisi)
    ├── Sensör: Şerit ihlali (GPS rotası)
    └── Sistem bu verileri analiz eder:
        ├── 5+ korna → -1 puan
        ├── 3+ hız ihlali → -1 puan
        ├── Sert fren/kalkış → Sürüş Kademe'ye gider (buraya gitmez)
        └── Rapor: "Bu yolculukta 7 kez korna, 2 kez hız ihlali"
```

#### 7.10.3 Puanın Kombine Sisteme Etkisi

Mevcut "Sürüş Kalitesi" (%30) ikiye ayrılır:

```
GÜNCELLENMİŞ ŞÖFÖR PUANLAMA KRİTERLERİ:
┌──────────────────────────────────────────────────────┐
│  ESKİ: Sürüş Kalitesi %30                           │
│  YENİ: Sürüş Kalitesi (Teknik) %15 + Davranış %15   │
└──────────────────────────────────────────────────────┘

Kombine Puan = (Şöför Puanı × 0.60) + (Araç Puanı × 0.40)

Şöför Puanı:
├── Sürüş Kalitesi (Teknik - Kademe): %15
├── Yoldaki Davranış ve Tutum: %15
├── Zamanında Gelme: %20
├── İletişim: %15
├── Güvenli Sürüş: %15
├── Rota Bilgisi: %10
└── Yardımseverlik: %10
```

#### 7.10.4 Kötü Davranış Uyarı ve Ceza Sistemi

```
UYARI EŞİKLERİ:
├── Davranış Puanı 4.0-4.9 → ⚠️ SARI UYARI
│   ├── Sistemsel uyarı: "Sayın şöför, yolcular davranışınızdan
│   │   memnun değil, lütfen daha saygılı olun."
│   └── Etki: Yok (sadece uyarı)
│
├── Davranış Puanı 3.0-3.9 → 🟠 TURUNCU UYARI
│   ├── Sistem uyarısı
│   ├── 1 gün hizmet durdurma
│   └── Zorunlu: "Nezaket Eğitimi" modülü izleme
│
├── Davranış Puanı 2.0-2.9 → 🔴 KIRMIZI UYARI
│   ├── 3 gün hizmet durdurma
│   ├── Zorunlu: Yüz yüze eğitim
│   └── Yönetici onayı olmadan tekrar aktif olamaz
│
└── Davranış Puanı 1.0-1.9 → ⛔ KALICI UZAKLAŞTIRMA
    ├── Hesap dondurulur
    ├── İtiraz hakkı: 30 gün içinde dilekçe
    └── Geri dönüş: Ancak komisyon onayı ile
```

#### 7.10.5 Veritabanı Değişiklikleri

```sql
-- Mevcut taxi_drivers tablosuna ek alan
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    behavior_score      NUMERIC(2,1) DEFAULT 7.0;     -- Yoldaki Davranış Puanı (1.0-10.0)
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    behavior_warnings   INTEGER DEFAULT 0;              -- Alınan uyarı sayısı
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    behavior_suspended_until TIMESTAMP;                 -- Hizmet durdurma bitişi

-- Her yolculuğun davranış değerlendirmesi
CREATE TABLE taxi_behavior_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    -- Yolcu puanı (1-10)
    passenger_score     NUMERIC(2,1),                   -- Yolcunun verdiği puan
    
    -- Sistem sensör verileri
    horn_count          INTEGER DEFAULT 0,              -- Korna sayısı
    speed_violations    INTEGER DEFAULT 0,              -- Hız ihlali sayısı
    lane_violations     INTEGER DEFAULT 0,              -- Şerit ihlali sayısı
    system_penalty      NUMERIC(2,1) DEFAULT 0,         -- Sistem ceza puanı
    
    -- Hesaplanan toplam
    total_score         NUMERIC(2,1) NOT NULL,          -- (passenger_score × 0.6) + system_adj
    
    -- Yolcu yorumu (isteğe bağlı)
    passenger_comment   TEXT,
    behavior_flags      JSONB DEFAULT '[]',             -- ["agresif_korna", "hiz_ihlali"]
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_behavior_scores_driver ON taxi_behavior_scores(driver_id);
```

#### 7.10.6 API Endpoint'leri

```
GET    /api/v1/taxi/driver/{driverId}/behavior-score     # Davranış puanı
GET    /api/v1/taxi/driver/{driverId}/behavior-history   # Davranış geçmişi
POST   /api/v1/taxi/trip/{tripId}/behavior-score         # Yolculuk için davranış puanı ver
GET    /api/v1/taxi/driver/{driverId}/behavior-warnings  # Uyarı geçmişi
```

---

### 7.11 Karşılama Hizmeti Puanı (Kapı Açma / Müşteri Kabul)

Şöförün müşteriyi karşılama, kapı açma, bagaj yardımı ve ilk izlenim kalitesini ölçen **ayrı bir puandır**. Sürüşten, davranıştan ve araç temizliğinden bağımsızdır.

```
KARŞILAMA HİZMETİ = AYRI BİR PUAN (1-10)
├── Sürüş Kademe (7.9) ile ilgisi yok
├── Yoldaki Davranış (7.10) ile ilgisi yok
├── Araç Temizlik (7.12) ile ilgisi yok
└── Tamamen şöförün müşteriyi karşılama kalitesi
```

#### 7.11.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Kapı Açma** | %25 | İnip kapıyı açtı mı? Yoksa yolcu mu açtı? |
| **Selamlama** | %20 | Güleryüzlü "Hoş geldiniz" mi? Sessiz mi? |
| **Bagaj Yardımı** | %15 | Bagaj var mı? Yardım etti mi? |
| **İsim Teyit** | %15 | "Ahmet Bey siz misiniz?" diye sordu mu? |
| **İlk İzlenim** | %15 | Kılık kıyafet, bakım, gülümseme |
| **Bekletmeme** | %10 | Müşteri geldiğinde hazır mı? Bekletti mi? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: İner, kapıyı açar, güleryüzlü karşılar, 
│        bagaja yardım eder, isimle hitap eder
│
├── 7-8: Kapıyı içerden açar, güleryüzlü selamlar
│
├── 5-6: Sadece "Merhaba" der, ekstra hizmet yok
│
├── 3-4: Yolcuyu bekleterek biner, selam vermez
│
└── 1-2: Kaba davranır, kapıyı yüzüne kapatır, 
         bagajı beklemez
```

#### 7.11.2 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    welcome_score       NUMERIC(2,1) DEFAULT 7.0;     -- Karşılama Puanı (1.0-10.0)

CREATE TABLE taxi_welcome_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    door_opening        NUMERIC(2,1) NOT NULL,         -- Kapı açma
    greeting            NUMERIC(2,1) NOT NULL,         -- Selamlama
    luggage_help        NUMERIC(2,1) DEFAULT 0,        -- Bagaj yardımı
    name_confirmation   NUMERIC(2,1) NOT NULL,         -- İsim teyit
    first_impression    NUMERIC(2,1) NOT NULL,         -- İlk izlenim
    wait_time           NUMERIC(2,1) NOT NULL,         -- Bekletmeme
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_welcome_scores_driver ON taxi_welcome_scores(driver_id);
```

#### 7.11.3 API

```
GET    /api/v1/taxi/driver/{driverId}/welcome-score     # Karşılama puanı
POST   /api/v1/taxi/trip/{tripId}/welcome-score         # Karşılama puanı ver
```

---

### 7.12 Araç İçi Temizlik Puanı

Aracın **iç temizlik ve hijyen seviyesini** ölçen ayrı bir puandır. Mevcut Araç Puanı'ndaki "Temizlik" kriterinden bağımsız, daha detaylı ve ayrıştırılmış bir puandır.

```
ARAÇ TEMİZLİĞİ = AYRI BİR PUAN (1-10)
├── Koltuk temizliği
├── Zemin / paspas temizliği
├── Hava / koku
├── Cam / ayna temizliği
└── Genel hijyen
```

#### 7.12.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Koltuk Temizliği** | %25 | Leke, kırıntı, saç, tüy var mı? |
| **Zemin / Paspas** | %20 | Çamur, toz, çöp var mı? |
| **Koku** | %20 | Sigara, ter, parfüm kokusu? |
| **Cam / Ayna** | %15 | Parmak izi, buğu, leke var mı? |
| **Genel Düzen** | %10 | Eşyalar dağınık mı? Şişe, kağıt var mı? |
| **Hijyen Malzemesi** | %10 | Kolonya, mendil, el dezenfektanı var mı? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Tertemiz, hijyenik, kolonya ikramı, güzel koku
├── 8-9: Çok temiz, hafif ferah koku, düzenli
├── 6-7: Normal temiz, göze batan bir şey yok
├── 4-5: Hafif dağınık, tozlu, orta temiz
├── 2-3: Kirli, çöp var, kötü koku
└── 1: Çok kirli, hijyenik değil, rahatsız edici
```

#### 7.12.2 Araç Genel Puanına Etkisi

Mevcut Araç Puanlama kriterleri (7.5) güncellenir:

```
GÜNCELLENMİŞ ARAÇ PUANLAMA KRİTERLERİ:
┌──────────────────────────────────────────────────────┐
│  ESKİ: Araç Temizliği %30                           │
│  YENİ: Araç İçi Temizlik Puanı %20 (detaylı)       │
│        Araç Kokusu %15                              │
└──────────────────────────────────────────────────────┘

Araç Puanı:
├── Araç İçi Temizlik (detaylı 1-10): %20
├── Araç Kokusu: %15
├── Araç Konforu: %25
├── Klima/Isıtma: %20
└── Genel Bakım: %20
```

#### 7.12.3 Veritabanı

```sql
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    cleanliness_score   NUMERIC(2,1) DEFAULT 7.0;     -- İç temizlik puanı (1.0-10.0)

CREATE TABLE taxi_cleanliness_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    seat_cleanliness    NUMERIC(2,1) NOT NULL,         -- Koltuk temizliği
    floor_cleanliness   NUMERIC(2,1) NOT NULL,         -- Zemin temizliği
    smell_score         NUMERIC(2,1) NOT NULL,         -- Koku
    glass_cleanliness   NUMERIC(2,1) NOT NULL,         -- Cam temizliği
    general_order       NUMERIC(2,1) NOT NULL,         -- Genel düzen
    hygiene_items       NUMERIC(2,1) DEFAULT 0,        -- Hijyen malzemesi
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cleanliness_scores_vehicle ON taxi_cleanliness_scores(vehicle_id);
```

#### 7.12.4 API

```
GET    /api/v1/taxi/vehicle/{vehicleId}/cleanliness      # Temizlik puanı
POST   /api/v1/taxi/trip/{tripId}/cleanliness-score      # Temizlik puanı ver
```

---

### 7.13 İkram ve Nezaket Puanı (Kolonya / Şeker / Mendil)

Şöförün yolcuya **geleneksel Türk taksi ikramı** olan kolonya, şeker ve mendil sunmasını ölçen ayrı bir puandır.

```
İKRAM = AYRI BİR PUAN (1-10)
├── Karşılama (7.9) ile ilgisi yok
│   └── Kapı açmak ayrı, ikram ayrı
├── Araç Temizlik (7.10) ile ilgisi yok
└── Tamamen şöförün yolcuya sunduğu ikram kalitesi
```

#### 7.13.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Kolonya İkramı** | %40 | Yolculuk başında/bitiminde kolonya sundu mu? |
| **Şeker İkramı** | %25 | Şeker, naneli şeker, badem şekeri sundu mu? |
| **Mendil / Kağıt Mendil** | %20 | Yolcuya mendil uzattı mı? |
| **Su / İçecek** | %15 | Su, maden suyu gibi ekstra ikram var mı? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Kolonya + şeker + mendil + su, hepsi mevcut, 
│        güleryüzle sunuyor
│
├── 8-9: Kolonya + şeker + mendil, üçü de var
│
├── 6-7: Kolonya + mendil (şeker yok)
│
├── 4-5: Sadece kolonya (veya sadece mendil)
│
├── 2-3: Var ama sunmuyor, yolcu istemeli
│
└── 1: Hiçbir şey yok, ikram kültürü yok
```

#### 7.13.2 Yolcu Geri Bildirimi

Yolculuk sonunda yolcuya sorulur:

```
YOLCU EKRANI:
┌──────────────────────────────────────────────┐
│  Şöför size ikramda bulundu mu?              │
│                                              │
│  ☐ Kolonya 💧                                 │
│  ☐ Şeker 🍬                                  │
│  ☐ Mendil 🧻                                 │
│  ☐ Su 🚰                                     │
│  ☐ Hiçbiri ❌                                │
│                                              │
│  [ İkram Puanı Ver: 1-10 ]                   │
│                                              │
│  Ek Not:                                      │
│  ┌──────────────────────────────────┐        │
│  │ "Kolonyayı kendisi döktü, çok   │        │
│  │  nazikti, şeker de verdi"       │        │
│  └──────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

#### 7.13.3 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    hospitality_score   NUMERIC(2,1) DEFAULT 5.0;     -- İkram puanı (1.0-10.0)

CREATE TABLE taxi_hospitality_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    cologne_offered     BOOLEAN DEFAULT FALSE,         -- Kolonya sunuldu mu?
    candy_offered       BOOLEAN DEFAULT FALSE,         -- Şeker sunuldu mu?
    tissue_offered      BOOLEAN DEFAULT FALSE,         -- Mendil sunuldu mu?
    water_offered       BOOLEAN DEFAULT FALSE,         -- Su sunuldu mu?
    
    items_count         INTEGER DEFAULT 0,             -- Sunulan ikram sayısı
    overall_score       NUMERIC(2,1) NOT NULL,         -- 1-10 puan
    
    passenger_note      TEXT,                          -- Yolcu notu
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_hospitality_scores_driver ON taxi_hospitality_scores(driver_id);
```

#### 7.13.4 API

```
GET    /api/v1/taxi/driver/{driverId}/hospitality-score   # İkram puanı
POST   /api/v1/taxi/trip/{tripId}/hospitality-score       # İkram puanı ver
```

---

### 7.14 Bagaj Hizmeti Puanı

Şöförün müşterinin bagajını **araca yerleştirme ve indirme** hizmetini ölçen ayrı bir puandır. Karşılama (7.9) ile karıştırılmamalıdır — kapı açmak ayrı, bagaj ayrı bir hizmettir.

```
BAGAJ = AYRI BİR PUAN (1-10)
├── Binişte: Bagajı al → bagaja koy → yerleştir
├── İnişte: Bagajı aç → bagajı indir → müşteriye uzat
└── Müşterinin bagajı yoksa: Bu puan "N/A" olur, ortalamaya etki etmez
```

#### 7.14.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Bagajı Alma** | %25 | Müşterinin elinden bagajı aldı mı? "Ben alırım" dedi mi? |
| **Bagaja Yerleştirme** | %25 | Düzgün yerleştirdi mi? Ezilme/çizilme önlemi aldı mı? |
| **Bagajı İndirme** | %25 | İnişte bagajı indirip müşteriye uzattı mı? |
| **Özen / Dikkat** | %15 | Valizi yere atmak yerine özenle indirdi mi? |
| **Hız / Bekletmeme** | %10 | Bagaj işlemini hızlı yaptı mı, müşteriyi bekletti mi? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: İner, bagajı alır, özenle yerleştirir, inişte
│        indirir, müşteriye uzatır, teşekkür eder
│
├── 8-9: Bagajı alır ve yerleştirir, inişte indirir
│
├── 6-7: Bagajı alır ama yerleştirirken özensiz
│
├── 4-5: "Bagajı açar mısınız?" derse açar, kendisi
│        ilgilenmez
│
├── 2-3: Bagaj var ama ilgilenmez, müşteri kendi halleder
│
└── 1: Bagajı reddeder, "Bagaj yeri dolu" der
```

#### 7.14.2 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    luggage_score       NUMERIC(2,1) DEFAULT 5.0;     -- Bagaj puanı (1.0-10.0)

CREATE TABLE taxi_luggage_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    had_luggage         BOOLEAN DEFAULT FALSE,         -- Bagaj var mıydı?
    
    take_from_passenger NUMERIC(2,1) DEFAULT 0,        -- Müşteriden alma
    trunk_placement     NUMERIC(2,1) DEFAULT 0,        -- Bagaja yerleştirme
    take_from_trunk     NUMERIC(2,1) DEFAULT 0,        -- Bagajdan indirme
    care_attention      NUMERIC(2,1) DEFAULT 0,        -- Özen
    speed               NUMERIC(2,1) DEFAULT 0,        -- Hız
    
    overall_score       NUMERIC(2,1),                  -- (nullable, bagaj yoksa null)
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_luggage_scores_driver ON taxi_luggage_scores(driver_id);
```

#### 7.14.3 API

```
GET    /api/v1/taxi/driver/{driverId}/luggage-score      # Bagaj puanı
POST   /api/v1/taxi/trip/{tripId}/luggage-score          # Bagaj puanı ver
```

---

### 7.15 Güler Yüz ve Diğer Sürücülere Saygı Puanı

Şöförün yolculuk boyunca **güler yüzlü olması** ve **trafikte diğer araçlara saygılı davranmasını** ölçen ayrı bir puandır. Yoldaki davranış (7.8) genel trafik kurallarını ölçerken, bu puan özellikle **nezaket ve saygı** odaklıdır.

```
GÜLER YÜZ & SAYGI = AYRI BİR PUAN (1-10)
├── 7.8 (Yoldaki Davranış): Kural ihlali, korna, küfür → GENEL DAVRANIŞ
├── 7.13 (Güler Yüz & Saygı): Tebessüm, hal hatır, diğer sürücülere 
│   nazik işaret, teşekkür → NEZAKET & SAYGI
└── İkisi farklı boyutlar: Biri agresif olmamak, diğeri pozitif olmak
```

#### 7.15.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Güler Yüz** | %35 | Yolculuk boyunca tebessüm etti mi? Mutlu göründü mü? |
| **Diğer Sürücülere Saygı** | %30 | Yol verdi mi? Teşekkür etti mi? El işareti yaptı mı? |
| **Yolcuya İlgi** | %20 | "Yolculuk nasıl gidiyor?" gibi ilgi gösterdi mi? |
| **Teşekkür / Vedalaşma** | %15 | İnişte teşekkür etti mi? "İyi günler" dedi mi? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Sürekli gülümser, herkese yol verir, eliyle teşekkür
│        eder, yolcuyla sohbet eder, vedada teşekkür
│
├── 8-9: Çoğunlukla gülümser, saygılı, vedada teşekkür
│
├── 6-7: Zaman zaman gülümser, genelde saygılı
│
├── 4-5: Nötr ifade, ne güler ne asık, saygılı ama mesafeli
│
├── 2-3: Asık surat, diğer sürücülere sinirli hareketler
│
└── 1: Hiç gülümsemez, diğer sürücülere saygısız, 
│        teşekkür etmez, surat asar
```

#### 7.15.2 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    courtesy_score      NUMERIC(2,1) DEFAULT 7.0;     -- Güler yüz & saygı puanı (1.0-10.0)

CREATE TABLE taxi_courtesy_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    smiling_score       NUMERIC(2,1) NOT NULL,         -- Güler yüz
    respect_to_drivers  NUMERIC(2,1) NOT NULL,         -- Diğer sürücülere saygı
    passenger_interest  NUMERIC(2,1) NOT NULL,         -- Yolcuya ilgi
    farewell            NUMERIC(2,1) NOT NULL,         -- Teşekkür / vedalaşma
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_courtesy_scores_driver ON taxi_courtesy_scores(driver_id);
```

#### 7.15.3 API

```
GET    /api/v1/taxi/driver/{driverId}/courtesy-score     # Güler yüz & saygı puanı
POST   /api/v1/taxi/trip/{tripId}/courtesy-score         # Güler yüz & saygı puanı ver
```

---

### 7.16 Yayaya Yol Verme Puanı

Şöförün **yaya geçitlerinde, kavşaklarda ve kaldırım kenarlarında yayalara öncelik vermesini** ölçen ayrı bir puandır.

```
YAYAYA YOL VERME = AYRI BİR PUAN (1-10)
├── Yaya geçidinde durup yayayı geçirme
├── Kavşakta dönerken yayaya bakma
├── Kaldırıma yakın yerde yavaşlama
└── Yağmurda su sıçratmama
```

#### 7.16.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Yaya Geçidi** | %40 | Yaya geçidinde durup yayayı geçirdi mi? |
| **Kavşak Dönüş** | %25 | Sağa/sola dönerken yayaya baktı mı? |
| **Kaldırma Duyarlılığı** | %20 | Yayaya yakın yerlerde yavaşladı mı? |
| **Su Sıçratmama** | %15 | Su birikintisinde yavaşlayıp yayaya su sıçratmadı mı? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Her yaya geçidinde durur, göz teması kurar, 
│        eliyle işaret eder, su sıçratmaz
│
├── 8-9: Yaya geçidinde durur, dikkatli döner
│
├── 6-7: Çoğu yaya geçidinde durur, bazen geçer
│
├── 4-5: Bazen durur, genelde yayayı bekleterek geçer
│
├── 2-3: Nadiren durur, yayalar kaçışır
│
└── 1: Hiç durmaz, yayaya korna çalar, su sıçratır
```

#### 7.16.2 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    pedestrian_score    NUMERIC(2,1) DEFAULT 7.0;     -- Yaya puanı (1.0-10.0)

CREATE TABLE taxi_pedestrian_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    crosswalk_stop      NUMERIC(2,1) NOT NULL,         -- Yaya geçidi
    turn_awareness      NUMERIC(2,1) NOT NULL,         -- Kavşak dönüş
    sidewalk_care       NUMERIC(2,1) NOT NULL,         -- Kaldırım duyarlılığı
    splash_prevention   NUMERIC(2,1) NOT NULL,         -- Su sıçratmama
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pedestrian_scores_driver ON taxi_pedestrian_scores(driver_id);
```

#### 7.16.3 API

```
GET    /api/v1/taxi/driver/{driverId}/pedestrian-score    # Yaya puanı
POST   /api/v1/taxi/trip/{tripId}/pedestrian-score        # Yaya puanı ver
```

---

### 7.17 Trafik İşaretlerine Uyum Puanı (⚠️ En Önemli Puan Grubu)

Şöförün **trafik işaret ve levhalarına uyma disiplinini** ölçer. Bu puan grubu, diğer tüm puanlardan **daha yüksek öneme** sahiptir çünkü güvenlik, ceza ve hukuki sorumluluk doğrudan buna bağlıdır.

```
ÖNEM SIRASI:
├── 1. TRAFİK İŞARETLERİNE UYUM ⚠️ (EN ÖNEMLİ)
│   └── Güvenlik + Ceza + Sigorta + Hukuk
│
├── 2. Sürüş Kademe (7.9)
├── 3. Yayaya Yol Verme (7.16)
├── 4. Yoldaki Davranış (7.10)
└── Diğerleri...
```

#### 7.17.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Kırmızı Işık** | %30 | Kırmızı ışıkta durdu mu? Geçti mi? |
| **Hız Limiti** | %25 | Hız sınırına uydu mu? Radar/tablet var mı? |
| **Şerit / Emniyet Şeridi** | %15 | Sürekli orta şerit mi? Emniyet şeridini kullandı mı? |
| **Dur / Yol Ver / Park** | %15 | Dur levhasında durdu mu? Park yasağına uydu mu? |
| **Uyarı Levhaları** | %15 | Okul geçidi, yaya geçidi, tünel gibi uyarılara uydu mu? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Tüm kurallara harfiyen uyar, asla ihlal yapmaz,
│        örnek sürücü
│
├── 8-9: Çok nadir ihlal, genelde kusursuz
│
├── 6-7: Normal sürücü, bazen hız limiti aşar (5-10 km)
│
├── 4-5: Sık ihlal, radar cezası riski yüksek
│
├── 2-3: Sürekli kural ihlali, ehliyetine el konabilir
│
└── 1: Tüm kuralları hiçe sayar, tehlikeli sürüş
```

#### 7.17.2 Özel Önemi ve Ağırlığı

Bu puanın kombine puana etkisi diğerlerinden **daha fazladır**:

```
KOMBİNE PUANDA AĞIRLIK:
├── Normal puan: Her biri şöför puanının %10-15'i
│
├── Trafik İşaretlerine Uyum: Şöför puanının %25'i
│   └── (diğer her puandan 2 kat daha ağır)
│
└── CEZA BAĞLANTISI:
    ├── Kırmızı ışık ihlali tespiti → otomatik -2 puan
    ├── Hız limiti %50+ aşımı → otomatik -2 puan
    ├── Emniyet şeridi ihlali → otomatik -1 puan
    └── Sistem sensörleri + resmi trafik cezaları entegrasyonu
```

#### 7.17.3 Sistem Sensörleri ve Ceza Entegrasyonu

```
OTOMATİK TESPİT:
├── GPS + Hız Verisi: Anlık hız × limit kontrolü
│   ├── Limit +10 km → uyarı
│   ├── Limit +30 km → -1 puan
│   └── Limit +50 km → -2 puan + sistem bildirimi
│
├── Kamera / Sensör: Kırmızı ışık ihlali
│   └── Tespit → -2 puan
│
├── Resmi Trafik Cezaları Entegrasyonu:
│   ├── Sistem, şöförün resmi trafik cezalarını sorgular
│   ├── Her ceza → -1 puan
│   └── 3+ ceza / yıl → 1 gün hizmet durdurma
│
└── ACİL DURUM MUAFİYETİ:
    ├── Ambulans, itfaiye, polis gibi araçlara yol verme
    ├── Trafik kazasından kaçınma
    └── Yolcu acil sağlık durumu
```

#### 7.17.4 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    traffic_sign_score  NUMERIC(2,1) DEFAULT 7.0;     -- Trafik işaret puanı (1.0-10.0)
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    traffic_penalties   INTEGER DEFAULT 0;              -- Yıllık trafik cezası sayısı
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    last_penalty_date   DATE;                           -- Son ceza tarihi

CREATE TABLE taxi_traffic_sign_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    red_light           NUMERIC(2,1) NOT NULL,         -- Kırmızı ışık
    speed_limit         NUMERIC(2,1) NOT NULL,         -- Hız limiti
    lane_discipline     NUMERIC(2,1) NOT NULL,         -- Şerit
    stop_yield          NUMERIC(2,1) NOT NULL,         -- Dur / Yol ver
    warning_signs       NUMERIC(2,1) NOT NULL,         -- Uyarı levhaları
    
    system_detected_violations JSONB DEFAULT '[]',      -- Sistem tespitleri
    official_penalties  INTEGER DEFAULT 0,              -- Resmi ceza sayısı
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_traffic_sign_scores_driver ON taxi_traffic_sign_scores(driver_id);
```

#### 7.17.5 API

```
GET    /api/v1/taxi/driver/{driverId}/traffic-sign-score   # Trafik işaret puanı
POST   /api/v1/taxi/trip/{tripId}/traffic-sign-score       # Trafik işaret puanı ver
GET    /api/v1/taxi/driver/{driverId}/traffic-penalties    # Trafik cezaları
```

---

### 7.18 Kılık Kıyafet ve Kişisel İmaj Puanı

Şöförün **dış görünüş, kılık kıyafet düzeni ve kişisel bakımını** ölçen ayrı bir puandır.

```
KİŞİSEL İMAJ = AYRI BİR PUAN (1-10)
├── Kılık kıyafet: Temiz, ütülü, uygun giyim
├── Sakal tıraşı: Bakımlı, düzenli
├── Genel bakım: Saç, el, tırnak temizliği
└── Aksesuar: Kötü koku, aşırı parfüm, rahatsız edici detay
```

#### 7.18.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Kıyafet Temizliği** | %30 | Kirli, buruşuk, leke var mı? |
| **Sakal / Yüz Bakımı** | %25 | Sakal tıraşı olmuş mu? Bakımlı mı? |
| **Genel Temizlik** | %20 | Saç, el, tırnak temiz ve bakımlı mı? |
| **Koku / Parfüm** | %15 | Aşırı parfüm, ter kokusu, sigara kokusu var mı? |
| **Aksesuar / Detay** | %10 | Şapka, güneş gözlüğü içerde? Küpe, dövme rahatsız edici mi? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Takım elbise / temiz gömlek, traşlı, bakımlı, 
│        hafif hoş koku, profesyonel görünüm
│
├── 8-9: Temiz giyimli, traşlı, bakımlı
│
├── 6-7: Normal sokak kıyafeti, temiz, düzenli
│
├── 4-5: Dağınık, hafif kirli, sakal uzamış
│
├── 2-3: Kirli kıyafet, bakımsız, kötü koku
│
└── 1: Pasaklı, yırtık/kirli kıyafet, rahatsız edici görünüm
```

#### 7.18.2 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    appearance_score    NUMERIC(2,1) DEFAULT 7.0;     -- Kişisel imaj puanı (1.0-10.0)

CREATE TABLE taxi_appearance_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    clothing            NUMERIC(2,1) NOT NULL,         -- Kıyafet temizliği
    facial_hair         NUMERIC(2,1) NOT NULL,         -- Sakal / yüz bakımı
    cleanliness         NUMERIC(2,1) NOT NULL,         -- Genel temizlik
    scent               NUMERIC(2,1) NOT NULL,         -- Koku
    accessories         NUMERIC(2,1) NOT NULL,         -- Aksesuar / detay
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_appearance_scores_driver ON taxi_appearance_scores(driver_id);
```

#### 7.18.3 API

```
GET    /api/v1/taxi/driver/{driverId}/appearance-score    # Kişisel imaj puanı
POST   /api/v1/taxi/trip/{tripId}/appearance-score        # Kişisel imaj puanı ver
```

---

### 7.19 Araç İçi Deneyim Puanı (Konfor, Ses Yalıtımı, İnternet)

Aracın **yolculuk konforu, ses yalıtımı ve teknolojik imkanlarını** ölçen ayrı bir puandır. Araç temizliğinden (7.12) bağımsızdır — temizlik ayrı, deneyim ayrı.

```
ARAÇ İÇİ DENEYİM = AYRI BİR PUAN (1-10)
├── Konfor: Koltuk rahatlığı, süspansiyon, yol tutuş
├── Ses Yalıtımı: Dışarıdan ses geliyor mu? Motor sesi rahatsız ediyor mu?
├── İnternet / WiFi: Araçta WiFi var mı? Çalışıyor mu?
├── Şarj İmkanı: USB girişi, araç çakmağı var mı?
└── Klima / Isıtma: Yeterli mi? Hızlı mı?
```

#### 7.19.1 Puanlama Kriterleri (1-10)

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Koltuk Konforu** | %25 | Koltuk rahat mı? Uzun yolculukta sırt ağrısı yapar mı? |
| **Ses Yalıtımı** | %20 | Dışarıdan ses, motor sesi, rüzgar sesi geliyor mu? |
| **WiFi / İnternet** | %20 | Araçta internet var mı? Hızı yeterli mi? |
| **Şarj İmkanı** | %15 | USB, type-c, araç çakmağı mevcut ve çalışıyor mu? |
| **Klima / Isıtma** | %20 | Isıtma/soğutma yeterli mi? Hızlı etki ediyor mu? |

```
PUAN KARŞILAŞTIRMASI:
├── 10: Lüks koltuk, mükemmel yalıtım, hızlı WiFi, 
│        her koltukta şarj, klima kusursuz
│
├── 8-9: Rahat koltuk, iyi yalıtım, WiFi var, şarj var
│
├── 6-7: Normal taksi konforu, orta yalıtım, WiFi yok
│
├── 4-5: Sert koltuk, gürültülü, internet yok, şarj yok
│
├── 2-3: Rahatsız koltuk, çok gürültülü, klima zayıf
│
└── 1: Koltuk bozuk, gürültü dayanılmaz, klima çalışmıyor
```

#### 7.19.2 Araç Puanına Etkisi

Mevcut Araç Puanlama kriterleri (7.5) güncellenir:

```
GÜNCELLENMİŞ ARAÇ PUANLAMA:
┌──────────────────────────────────────────────────────┐
│  ESKİ: Araç Konforu %20 + Klima/Isıtma %15          │
│  YENİ: Araç İçi Deneyim Puanı %25 (detaylı)         │
│        Klima/Isıtma %15                              │
└──────────────────────────────────────────────────────┘

Araç Puanı:
├── Araç İçi Temizlik (7.12): %20
├── Araç Kokusu: %10
├── Araç İçi Deneyim (konfor, yalıtım, WiFi): %25
├── Klima/Isıtma: %15
└── Genel Bakım: %30
```

#### 7.19.3 Veritabanı

```sql
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    experience_score    NUMERIC(2,1) DEFAULT 6.0;     -- Araç içi deneyim puanı (1.0-10.0)
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    has_wifi            BOOLEAN DEFAULT FALSE;
ALTER TABLE taxi_vehicles ADD COLUMN IF NOT EXISTS
    has_usb_charging    BOOLEAN DEFAULT FALSE;

CREATE TABLE taxi_experience_scores (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    seat_comfort        NUMERIC(2,1) NOT NULL,         -- Koltuk konforu
    sound_insulation    NUMERIC(2,1) NOT NULL,         -- Ses yalıtımı
    wifi_quality        NUMERIC(2,1) DEFAULT 0,        -- WiFi kalitesi (0 = yok)
    charging_available  NUMERIC(2,1) NOT NULL,         -- Şarj imkanı
    ac_performance      NUMERIC(2,1) NOT NULL,         -- Klima performansı
    
    overall_score       NUMERIC(2,1) NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_experience_scores_vehicle ON taxi_experience_scores(vehicle_id);
```

#### 7.19.4 API

```
GET    /api/v1/taxi/vehicle/{vehicleId}/experience-score   # Araç içi deneyim puanı
POST   /api/v1/taxi/trip/{tripId}/experience-score         # Araç içi deneyim puanı ver
```

---

### 7.20 Müşteri (Yolcu) Puanlama Sistemi

Şöför de yolculuk sonunda **yolcuyu değerlendirme hakkına** sahiptir. Bu, çift yönlü puanlama sistemini tamamlar. Müşteri puanı **3 ana başlık** altında toplanır:

```
MÜŞTERİ PUANI = DAVRANIŞ × 0.50 + GÜVENİLİRLİK × 0.30 + DÜZEN × 0.20
```

#### 7.20.1 Müşteri Puanı Bileşenleri

**A) DAVRANIŞ (%50) — Yolculuk anındaki tutum**

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Nezaket** | %15 | Kibar mıydı? Selam verdi mi? Teşekkür etti mi? "İyi günler" dedi mi? |
| **Saygı / Sorunsuzluk** | %12 | Saygılı mı? Gereksiz tartışma çıkardı mı? Sözlü saldırı? |
| **Alkol / Madde Durumu** | %12 | Alkol kokusu var mı? Ayakta durmakta zorlanıyor mu? Araçta rahatsızlık yarattı mı? |
| **Genel Güvenlik** | %11 | Şöförü tehdit etti mi? Araca zarar verme riski? Şiddet eğilimi? |

**B) GÜVENİLİRLİK (%30) — Sözünde durma, kurallara uyma**

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Çağrıya Sadakat** | %10 | Çağırdı mı? Binmedi mi? Kaç kez çağırıp vazgeçti? |
| **Zamanında Olma** | %8 | Belirtilen noktada hazır mıydı? Taksiyi bekletti mi? |
| **Taahhüde Uyma** | %7 | Gideceği yerde mi indi? Erken inme hakkını kötüye kullandı mı? |
| **Ödeme Disiplini** | %5 | Ödemede sorun çıkardı mı? İtiraz/chargeback geçmişi? |

**C) DÜZEN (%20) — Araç içi düzen ve hijyen**

| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| **Araç Temizliği** | %10 | Araca kirli ayakkabıyla bindi mi? Çöp bıraktı mı? Döktü mü? |
| **Sigara / Yiyecek** | %5 | Araçta sigara içti mi? Yemek yedi mi? Kırıntı döktü mü? |
| **Eşya Düzeni** | %5 | Kişisel eşyasını dağıttı mı? Islak şemsiye ile bindi mi? |

```
PUAN KARŞILAŞTIRMASI (Toplam Müşteri Puanı):
├── 4.5 - 5.0 ⭐: ✅ VIP Yolcu
│   Kibar, saygılı, ayık, temiz, zamanında, sorunsuz
│   → Öncelikli eşleşme, en iyi taksiler
│
├── 3.5 - 4.4 ⭐: ✅ Normal Yolcu
│   Genelde iyi, ufak tefek kusurlar olabilir
│   → Standart eşleşme
│
├── 2.5 - 3.4 ⭐: ⚠️ Düşük Puanlı Yolcu
│   Sorunlu, gürültülü, bazen alkollü, dağınık
│   → Düşük öncelik, uzun bekleme
│
├── 1.5 - 2.4 ⭐: ⛔ Güvensiz Yolcu
│   Agresif, alkollü, araca zarar veren, çağrı sadakatsiz
│   → En düşük öncelik, 2x bekleme, bahşiş zorunlu
│
└── 1.0 - 1.4 ⭐: 🚫 Blokeli Yolcu
    Çok tehlikeli, şiddet eğilimli, sürekli sorun çıkaran
    → Geçici hesap dondurma + müşteri hizmetleri
```

#### 7.20.2 Şöför Geri Bildirim Ekranı

Yolculuk bittiğinde şöförün karşısına çıkar:

```
┌──────────────────────────────────────────────┐
│  🧑 Yolcuyu Değerlendir                     │
│                                              │
│  Yolcu: Ahmet Yılmaz                         │
│  Rota: Kadıköy → Taksim                      │
│                                              │
│  ─── DAVRANIŞ ───                           │
│  Nezaket:          ⭐⭐⭐⭐⭐                  │
│  Saygı/Sorunsuz:   ⭐⭐⭐⭐⭐                  │
│  Alkol/Madde:      ⭐⭐⭐⭐⭐ (ayık)           │
│  Güvenlik:         ⭐⭐⭐⭐⭐ (sorunsuz)       │
│                                              │
│  ─── GÜVENİLİRLİK ───                       │
│  Çağrı Sadakati:   ⭐⭐⭐⭐⭐                  │
│  Zamanında Olma:   ⭐⭐⭐⭐☆                   │
│                                              │
│  ─── DÜZEN ───                               │
│  Araç Temizliği:   ⭐⭐⭐⭐⭐                  │
│                                              │
│  Genel Puan: 4.8 ⭐                          │
│                                              │
│  Yorum (opsiyonel):                          │
│  ┌──────────────────────────────────┐        │
│  │ "Çok kibar bir yolcuydu,        │        │
│  │  sohbeti güzeldi."              │        │
│  └──────────────────────────────────┘        │
│                                              │
│  [ DEĞERLENDİR ]                             │
└──────────────────────────────────────────────┘
```

#### 7.20.3 Müşteri İçin Teşvik: Kendine Dikkat Etme Zorunluluğu

Müşteri, şöförün de kendisini değerlendirdiğini bildiği için **doğal olarak daha dikkatli** davranır. Bu karşılıklı puanlama sistemi sayesinde:

```
KARŞILIKLI GÜVENCE:
├── Müşteri bilir: Şöför de puan verecek
│   ├── Daha kibar davranır
│   ├── Aracı temiz kullanır
│   ├── Zamanında hazır olur
│   └── Alkol/sigara gibi rahatsızlıklardan kaçınır
│
└── Şöför bilir: Müşteri de puan verecek
    ├── Daha iyi hizmet sunar
    ├── Güler yüzlü olur
    └── Kurallara uyar

SONUÇ: İki taraf da birbirine saygılı olmak zorunda kalır.
Bu, sistemin kendi kendini denetlemesini sağlar.
```

#### 7.20.4 Yolcu Puanının Etkileri

Düşük yolcu puanı, müşterinin sistemdeki **erişim ve önceliğini** etkiler:

```
YOLCU PUAN KADEMELERİ:
├── 4.5 - 5.0 ⭐: ✅ VIP Yolcu
│   ├── Öncelikli eşleşme
│   ├── En iyi taksiler öncelikle ona gider
│   └── Acil çağrı önceliği
│
├── 3.5 - 4.4 ⭐: ✅ Normal Yolcu
│   └── Standart eşleşme
│
├── 2.5 - 3.4 ⭐: ⚠️ Düşük Puanlı Yolcu
│   ├── Eşleşme önceliği düşer
│   ├── Bekleme süresi artar (%30 daha uzun)
│   └── Taksiciler çağrıyı görünce reddedebilir (cezasız)
│
└── 1.0 - 2.4 ⭐: ⛔ Güvensiz Yolcu
    ├── Çağrı önceliği en düşük
    ├── Bekleme süresi 2 katına çıkar
    ├── Sadece düşük puanlı taksiler eşleşir
    └── Bahşiş teklifi zorunlu (en az %20 ek)
```

#### 7.20.5 Şöför Yorumu ve Uyarı Sistemi

```
YORUM VE UYARI MEKANİZMASI:
├── Olumlu Yorumlar:
│   ├── "Kibar yolcu, yine gelsin" → +0.1 puan
│   └── Sistemde görünür (yolcu profili)
│
├── Olumsuz Yorumlar:
│   ├── "Agresif davrandı" → -0.2 puan
│   ├── 3+ farklı şöför aynı şikayeti yaparsa → otomatik ikaz
│   └── "Araca zarar verdi" → hasar kaydı + ceza
│
└── Yalan Yorum Koruması:
    ├── Şöförün yorumu otomatik doğrulama geçer
    ├── 5'te 1 yolcu rastgele geri aranır (doğrulama)
    └── Yalan yorum tespiti → şöför -1 puan ceza
```

#### 7.20.6 Veritabanı

```sql
-- Müşteri puan bileşenleri
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    passenger_score       NUMERIC(2,1) DEFAULT 4.5;     -- Toplam müşteri puanı
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    passenger_behavior    NUMERIC(2,1) DEFAULT 4.5;     -- Davranış bileşeni
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    passenger_reliability NUMERIC(2,1) DEFAULT 4.5;     -- Güvenilirlik bileşeni
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    passenger_orderliness NUMERIC(2,1) DEFAULT 4.5;     -- Düzen bileşeni
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    passenger_tier        VARCHAR(30) DEFAULT 'normal';  -- vip, normal, low, blocked, suspended
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    total_driver_reviews  INTEGER DEFAULT 0;

CREATE TABLE taxi_passenger_reviews (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    passenger_id        UUID REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    -- Davranış (%50)
    politeness          NUMERIC(2,1) NOT NULL,         -- Nezaket
    respect             NUMERIC(2,1) NOT NULL,         -- Saygı
    alcohol_status      NUMERIC(2,1) NOT NULL,         -- Alkol durumu
    safety              NUMERIC(2,1) NOT NULL,         -- Güvenlik
    
    -- Güvenilirlik (%30)
    call_faithfulness   NUMERIC(2,1),                  -- Çağrı sadakati
    punctuality         NUMERIC(2,1),                  -- Zamanında olma
    commitment          NUMERIC(2,1),                  -- Taahhüt uyumu
    
    -- Düzen (%20)
    car_cleanliness     NUMERIC(2,1) NOT NULL,         -- Araç temizliği
    smoking_food        NUMERIC(2,1),                  -- Sigara/yiyecek
    item_order          NUMERIC(2,1),                  -- Eşya düzeni
    
    -- Hesaplanan puan
    behavior_score      NUMERIC(2,1),                  -- Davranış toplam
    reliability_score   NUMERIC(2,1),                  -- Güvenilirlik toplam
    orderliness_score   NUMERIC(2,1),                  -- Düzen toplam
    overall_score       NUMERIC(2,1) NOT NULL,         -- Genel toplam
    
    comment             TEXT,
    is_verified         BOOLEAN DEFAULT FALSE,
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_passenger_reviews_passenger ON taxi_passenger_reviews(passenger_id);
CREATE INDEX idx_passenger_reviews_driver ON taxi_passenger_reviews(driver_id);
```

#### 7.20.7 API

```
GET    /api/v1/taxi/passenger/{passengerId}/score         # Yolcu puanı
POST   /api/v1/taxi/trip/{tripId}/review-passenger        # Yolcuyu değerlendir
GET    /api/v1/taxi/passenger/{passengerId}/reviews       # Yolcu yorumları
GET    /api/v1/taxi/driver/{driverId}/given-reviews       # Şöförün verdiği yorumlar
```

---

## 8. TAKSİ ÇAĞIRMA VE EŞLEŞTİRME ALGORİTMASI

### 8.1 Çağırma Süreci (Adım Adım)

```
┌─────────────────────────────────────────────────────────────────┐
│                    TAKSİ ÇAĞIRMA AKIŞI                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Yolcu Konumunu Açar                                   │
│  ├── GPS otomatik algılama (tercihen)                           │
│  ├── Veya manuel konum girişi                                  │
│  └── Doğruluk: ±10 metre                                       │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Gidilecek Adres Girilir                               │
│  ├── Metin arama ("Kadıköy İskelesi")                          │
│  ├── Harita üzerinden işaretleme                               │
│  └── Favori adreslerden seçim                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Rota ve Ücret Tahmini Gösterilir                      │
│  ├── Haritada rota çizgisi                                     │
│  ├── Tahmini mesafe: 8.5 km                                    │
│  ├── Tahmini süre: 25 dakika                                   │
│  ├── Tahmini ücret: 95-110 TL                                  │
│  ├── Kullanılacak yol / güzergah                               │
│  └── Alternatif rotalar (varsa)                                │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: "Taksi Çağır" Butonu                                  │
│  ├── Yolcuya en yakın müsait taksiler bulunur                  │
│  └── Taksilere sırayla çağrı gider (en yakından başlayarak)   │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Taksilere Çağrı Gönderilir                            │
│  ├── 1. en yakın taksiye git (500m)                            │
│  │   ├── Ret (15 sn içinde yanıt yoksa) →                     │
│  │   └── Kabul → Eşleşme tamam!                                │
│  ├── 2. en yakın taksiye git (800m)                            │
│  │   ├── Ret →                                                  │
│  │   └── Kabul → Eşleşme tamam!                                │
│  ├── ... (en uzak mesafeye kadar)                              │
│  └── Hiçbiri kabul etmezse: "Müsait taksi bulunamadı"         │
│         │                                                      │
│         ▼                                                      │
│  ADIM 6: Eşleşme Sonrası                                       │
│  ├── Yolcu şunları görür:                                      │
│  │   ├── Şöför Adı: Ahmet Yılmaz                              │
│  │   ├── Şöför Puanı: 4.8 ⭐                                  │
│  │   ├── Araç Plaka: 34 TAK 1234                              │
│  │   ├── Araç Modeli: Renault Megane (Beyaz)                  │
│  │   ├── Araç Fotoğrafı                                       │
│  │   ├── Taksinin canlı konumu (haritada)                     │
│  │   ├── Tahmini varış süresi: 5 dakika                       │
│  │   └── Şöför telefonu (gizli, platform üzerinden arama)     │
│  │                                                             │
│  └── Şöför şunları görür:                                      │
│      ├── Yolcu Adı (ilk isim + soyisim baş harfi)             │
│      ├── Yolcu Puanı: 4.5 ⭐                                  │
│      ├── Alınacak Yer                                          │
│      ├── Gidilecek Yer                                         │
│      ├── Tahmini mesafe                                        │
│      └── Tahmini kazanç                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Eşleştirme Algoritması (Detay)

```
ESLEŞTİRME ALGORİTMASI:

function findNearestTaxi(passengerLocation, maxRadius = 10km):

    1. Yolcunun konumunu al
       ├── latitude, longitude
    
    2. Müsait taksileri bul (aktif + boşta durumda olanlar)
       ├── WHERE status = 'available'
       ├── AND ST_Distance(araç_konumu, yolcu_konumu) < maxRadius
       ├── ORDER BY mesafe ASC
    
    3. Mesafeye göre sırala (en yakından en uzağa)
       ├── Taksi 1: 300m (Ahmet - Puan: 4.8)
       ├── Taksi 2: 450m (Mehmet - Puan: 4.6)
       ├── Taksi 3: 1.2km (Ali - Puan: 4.9)
       └── Taksi 4: 2.5km (Veli - Puan: 4.2)
    
    4. Optimize edilmiş sıralama (mesafe + puan)
       ├── Her taksiye skor hesapla
       ├── Skor = (Mesafe Puanı × 0.50) + (Kombine Puan × 0.50)
       │
       ├── Taksi 1: Mesafe 300m → 100p, Puan 4.8 → 96p
       │       Skor = (100 × 0.5) + (96 × 0.5) = 98
       │
       ├── Taksi 2: Mesafe 450m → 90p, Puan 4.6 → 92p
       │       Skor = (90 × 0.5) + (92 × 0.5) = 91
       │
       ├── Taksi 3: Mesafe 1.2km → 70p, Puan 4.9 → 98p
       │       Skor = (70 × 0.5) + (98 × 0.5) = 84
       │
       └── Taksi 4: Mesafe 2.5km → 50p, Puan 4.2 → 84p
               Skor = (50 × 0.5) + (84 × 0.5) = 67
    
    5. En yüksek skordan başlayarak çağrı gönder
       ├── Taksi 1'e çağrı → Yanıt yok (15 sn timeout)
       ├── Taksi 2'ye çağrı → Ret (Kısa mesafe)
       ├── Taksi 3'e çağrı → KABUL!
       └── Eşleşme: Yolcu ↔ Ali (Taksi 3)
    
    6. Eşleşme anında bilgilendirme
       ├── Yolcu: Ali geldiğinde bildirilecek
       └── Ali: Yolcu konumuna yönlendirilecek

function calculateDistance(lat1, lon1, lat2, lon2):
    Haversine formülü ile iki nokta arası mesafe
```

### 8.3 Çağrıya Yanıt Vermeyen Şöförün Cezası

```
KRİTİK CEZA: Müşteri çağrısına yanıt vermeyen → Puan düşer!

KURAL:
├── Yolcu taksi çağırır → Sisteme çağrı düşer
├── En yakın 10 müsait taksinin hepsine çağrı gider
├── Her taksinin yanıtlaması için 15 saniye süre
│
├── TAKSİ ÇAĞRIYA YANIT VERMEZSE:
│   ├── 1. kez: -1 puan (uyarı)
│   ├── 2. kez: -1 puan (uyarı)
│   ├── 3. kez: -2 puan (günlük puan limiti aşıldı)
│   └── 5+ kez: O gün sistemden geçici men
│
├── TAKSİ ÇAĞRIYI REDDEDİVERSE:
│   ├── Kısa mesafe reddi: -1 puan + kabul oranı düşer
│   ├── Semt/rota reddi: -1 puan
│   └── Sebepsiz ret: -2 puan
│
└── YANIT VERMEMENİN YOLCU ÜZERİNDEKİ ETKİSİ:
    ├── Yolcu bekler
    ├── Yolcu sinirlenir
    ├── Sistem güvenilirliği azalır
    └── ÇÖZÜM: Otomatik olarak sıradaki taksiye geç!
```

### 8.7 Karşılıklı Taahhüt ve Bilgilendirme Sistemi

Müşteri bir taksi çağırdığında ve şöför bu çağrıyı kabul ettiğinde, **her iki taraf da bir taahhüde girer**. Sistem her iki tarafa da sonuçları ve riskleri önceden gösterir.

#### 8.7.1 Müşteri Taahhüdü

Müşteri çağrı yaparken şunu kabul eder:
- "Belirttiğim noktada olacağım"
- "Gecikirsem bekleme ücreti ödeyeceğim"
- "Gelmezsem ceza ödeyeceğim"

```
MÜŞTERİ ÇAĞRI ONAY EKRANI:
┌──────────────────────────────────────────────┐
│  📞 TAKSİ ÇAĞIRILIYOR                        │
│                                              │
│  📍 Sizi bekleyeceğim nokta:                 │
│  ┌──────────────────────────────────┐        │
│  │ Bağdat Cad. No:123              │        │
│  └──────────────────────────────────┘        │
│                                              │
│  ✅ Taksici seni almaya geliyor              │
│                                              │
│  ⚠️ TAAHHÜDÜNÜZ:                            │
│  ├─ ✅ Zamanında noktada olacağım           │
│  ├─ ✅ Gecikirsem bekleme ücreti öderim     │
│  │   └─ Gündüz: 72 TL/saat                  │
│  │   └─ Gece:  85 TL/saat                  │
│  └─ ❌ Gelmezsem ceza öderim                │
│      └─ (Bölüm 18 - mesafe bazlı ceza)      │
│                                              │
│  [ ✅ KABUL EDİYORUM, ÇAĞIR ]               │
└──────────────────────────────────────────────┘
```

#### 8.7.2 Şöför Taahhüdü

Şöför çağrıyı kabul ederken sistem ona şunu gösterir:

```
ŞÖFÖR ÇAĞRI KABUL EKRANI:
┌──────────────────────────────────────────────┐
│  📞 YENİ ÇAĞRI                              │
│                                              │
│  📍 Müşteri: Bağdat Cad. No:123             │
│  🎯 Hedef: Kadıköy                          │
│  💰 Tahmini: 185 TL                         │
│  📍 Uzaklık: 1.2 km                         │
│                                              │
│  ⚠️ BU ÇAĞRIYI KABUL EDERSEN:              │
│                                              │
│  Müşteri gecikirse (+5 dk):                 │
│  ├─ Bekleme ücreti işler → Sen kazanırsın  │
│  └─ Müşteri öder, sen beklersin            │
│                                              │
│  Müşteri hiç gelmezse:                      │
│  ├─ Mesafe bazlı ceza alırsın              │
│  └─ (Bölüm 18)                              │
│                                              │
│  Sen beklemez ve gidersen:                  │
│  ├─ Şu an: Gündüz, yoğun cadde             │
│  ├─ Müşterinin yeni taksi bulma oranı: %92 │
│  ├─ Gidersen kaybedeceğin puan: -5          │
│  └─ (Gece olsaydı: %15 → -100 puan)        │
│                                              │
│  [ ✅ KABUL ET ]    [ ❤️ REDDET ]          │
└──────────────────────────────────────────────┘
```

#### 8.7.3 Bekleme ve Puan Hesaplama Tablosu

```yaml
Karşılıklı Taahhüt Kuralları:
  Müşteri Tarafı:
    - Çağrı yaparken bekleme ücretini KABUL etmiş sayılır
    - Gecikirse bekleme ücreti otomatik işler
    - Gelmezse Bölüm 18 cezası uygulanır
    - Bekleme ücreti ücreti: İlk 5 dk ücretsiz (nezaket)
    - 5 dk sonrası: Saatlik ücret / 60 × dakika

  Şöför Tarafı:
    - Çağrıyı kabul ederken BEKLEMEYİ de kabul etmiş sayılır
    - Bekleme ücreti alacağı için beklemesi beklenir
    - Beklemez ve giderse DİNAMİK CEZA puanı düşer
    - Ceza hesaplaması:
      ├── Zorluk puanı = Müşterinin yeni taksi bulma olasılığı
      ├── Kolay (gündüz/şehir içi/yoğun):   -5 puan
      ├── Orta (akşam/normal):              -15 puan
      ├── Zor (gece/yağmur/tenha):          -50 puana kadar
      └── Çok zor (gece+yağmur+tenha):      -100 puana kadar
    
    - Şöför cezayı görür, kabul ederse puanı düşer
    - Şöför beklemeyi seçerse puan etkilenmez
    
  Bekleme Süresi Yönetimi:
    ├── 0-5 dk: Ücretsiz bekleme (nezaket süresi)
    ├── 5-15 dk: Bekleme ücreti başlar
    ├── 15-30 dk: Bekleme ücreti devam
    ├── 30+ dk: Sistem şöföre sorar
    │   ├── "Hâlâ bekliyor musunuz?"
    │   ├── EVET: Bekleme devam, ücret artar
    │   └── HAYIR: Şöför cezayı ödeyip gider
    └── Maksimum: 60 dk bekleme sonrası şöför cezasız iptal hakkı
```

#### 8.7.4 Müşteri Gecikme Takip Ekranı

```
MÜŞTERİ GECİKME TAKİBİ:
┌──────────────────────────────────────────────┐
│  🚗 TAKSİN BEKLİYOR                          │
│                                              │
│  👤 Mehmet Y.  ⭐ 4.6                        │
│  🚗 34 TAK 1234 — Renault Megane            │
│  📍 Bağdat Cad. No:123                      │
│                                              │
│  ⏱ Bekleme süresi: 8 dk                     │
│  ├─ İlk 5 dk: Ücretsiz ✅                   │
│  └─ 3 dk ücretli: 3.60 TL                   │
│                                              │
│  ⏳ Gecikme nedeni:                          │
│  ┌──────────────────────────────────┐        │
│  │ Trafikte kaldım, 5 dk içinde    │        │
│  │ geliyorum.                       │        │
│  └──────────────────────────────────┘        │
│                                              │
│  Güncel bekleme ücreti: 72 TL/saat          │
│                                              │
│  [ ✅ GELDİM, BİNİYORUM ]                   │
└──────────────────────────────────────────────┘
```

---

## 9. FİYAT TAHMİN VE ROTA GÖSTERİM SİSTEMİ

### 9.1 Fiyat Hesaplama Motoru

```
FİYAT = Açılış Ücreti + (Mesafe × KM Ücreti) + (Süre × Dakika Ücreti) + Varsa Ek Ücretler

ÖRNEK İSTANBUL TAKSİ ÜCRETİ:
├── Açılış Ücreti: 15 TL
├── KM Başına: 12 TL/km
├── Dakika Başına: 2 TL/dk (bekleme)
├── Minimum Ücret: 50 TL
│
├── HESAPLAMA (8.5 km, 25 dk):
│   ├── Açılış: 15 TL
│   ├── Mesafe: 8.5 × 12 = 102 TL
│   ├── Süre: 25 × 2 = 50 TL
│   ├── Toplam: 167 TL
│   └── Tahmin: 155-175 TL (trafik durumuna göre +/- %10)

DİNAMİK FAKTÖRLER:
├── Gece (22:00-06:00): %50 zamlı
├── Hafta sonu: %25 zamlı
├── Yoğun saat: %20 zamlı (08:00-10:00, 17:00-20:00)
├── Havalimanı: Sabit fiyat (ek ücret dahil)
└── Özel günler: %100 zamlı (yılbaşı, bayram, konser vb.)
```

### 9.2 Rota Gösterimi

```
YOLCU GÖRÜR:
┌─────────────────────────────────────────────────────────────────┐
│  📍 GİDİŞ: Kadıköy İskelesi                                    │
│  🎯 VARIŞ: Taksim Meydanı                                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   HARİTA                                │   │
│  │                                                         │   │
│  │   Kadıköy ──────────────┬──── Eminönü ───── Taksim     │   │
│  │         │                      │             │          │   │
│  │    ŞU AN: KADIKÖY       15 dk           10 dk           │   │
│  │                          2.5 km          3.5 km         │   │
│  │                                                         │   │
│  │   TOPLAM MESAFE: 8.5 km ● SÜRE: 25 dk ● ÜCRET: 167 TL │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🛣️ ROTA: E-5 Karayolu → Eminönü Köprüsü → Taksim             │
│  ⚠️ TRAFİK DURUMU: E-5 normal seyir                          │
│  🔄 ALTERNATİF ROTALAR:                                        │
│  ├── Sahil yolu (+3 km, +5 dk, +15 TL) - Trafiksiz            │
│  └── Bağdat Caddesi (+2 km, +10 dk, +20 TL) - Trafik var      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9.5 MÜŞTERİ ÖZGÜN ROTA HARİTALAMA SİSTEMİ

### 9.5.1 Amaç

Müşteri, adres yazmadan harita üzerinde serbestçe nokta belirleyip kendi rotasını oluşturur ve "buradan gitmek istiyorum" diyerek taksi çağırabilir. Bu sistem, özellikle:
- Adres tarifi zor olan noktalar (sahil, park, inşaat alanı, açık arazi)
- Toplanma noktaları (konser alanı, festival, stadyum çevresi)
- Standan/tezgahtan alışveriş yapıp gitmek isteyenler
- Tarif edilemeyen ara noktalar için kritiktir.

### 9.5.2 Terminal Tasarımı — Müşteri Ekranı (Gri Ton)

```
╔═══════════════════════════════════════════════════════════════╗
║  OZGUN ROTA CIZ  ·  Adim 2/4                                ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌───────────────────────────────────────────────────────┐   ║
║  │                   HARITA (Dokunmatik)                 │   ║
║  │                                                       │   ║
║  │         ▼ (Alis)                                      │   ║
║  │          ╭────────────────────╮                       │   ║
║  │         /     ● (Ara durak)   \                      │   ║
║  │        /      ROTA CIZGISI     \                     │   ║
║  │       /                          \                    │   ║
║  │      ╰────────────────────────────╯                   │   ║
║  │                      ▼ (Varis)                        │   ║
║  │                                                       │   ║
║  │  8.5 km  ·  25 dk  ·  145-165 TL                     │   ║
║  └───────────────────────────────────────────────────────┘   ║
║                                                               ║
║  ─── ROTA BILGISI ────────────────────────────────────────   ║
║                                                               ║
║  ▼ ALIS   »  Caddebostan Sahili (mavi semsiye)               ║
║  ● DURAK  »  Bostanci Migros                                 ║
║  ▼ VARIS  »  Bagdat Cad. No:123                              ║
║                                                               ║
║  ─── MUSTERI NOTU ────────────────────────────────────────   ║
║                                                               ║
║  ╔══════════════════════════════════════════════════════╗     ║
║  ║  Buradan gitmek istiyorum.                          ║     ║
║  ║  Mavi semsiyenin yanindayim, korna calmayin.       ║     ║
║  ╚══════════════════════════════════════════════════════╝     ║
║                                                               ║
║  ╔═════════════════════════════════════════════════════════╗  ║
║  ║  TAKSI CAGIR  ·  145-165 TL                           ║  ║
║  ╚═════════════════════════════════════════════════════════╝  ║
║                                                               ║
║  [▼Nokta ekle] [↻Sirala] [☆Favori] [✕Temizle]               ║
║                                                               ║
║  ─── SOHBET ──────────────────────────────────────────────   ║
║                                                               ║
║  ◈  Haritada alis noktani belirlemek icin istedigin           ║
║      yere uzun bas veya noktayi surukle.                      ║
║                                                               ║
║  ◆  Buradan gitmek istiyorum.                                 ║
║      ▼ Caddebostan Sahili · Mavi semsiyenin yani              ║
║                                                               ║
║  ◈  Varis noktani da belirle. Ara durak eklemek               ║
║      icin haritada orta noktaya uzun bas.                    ║
║                                                               ║
║  ◆  ✓ Alis: Sahil                                             ║
║      ● Ara: Bostanci Migros                                   ║
║      ▼ Varis: Bagdat Cad. No:123                              ║
║                                                               ║
║  ────────────────────────────────────────────────────────   ║
║  ▸ Not ekle (opsiyonel): mavi semsiyenin yanindayim...    ║
║  ────────────────────────────────────────────────────────   ║
║                                                               ║
║  [▦Rota]  [☆Favoriler]  [◷Gecmis]  [⚙Ayarlar]               ║
╚═══════════════════════════════════════════════════════════════╝
```

### 9.5.3 Nokta Belirleme Yöntemleri

| Yöntem | Açıklama | Kullanım |
|--------|----------|----------|
| **Uzun Basma** | Haritada 1sn basılı tut → nokta düşer | Alış, variş, ara durak |
| **Sürükle-Bırak** | Noktayı tutup sürükle → yeni konum | Hassas ayar |
| **Arama** | Adres/yer adı yaz → haritada bul | Bilinen yerler |
| **Anlık Konum** | "Bulunduğum yer" butonu | Hızlı alış |
| **Favoriler** | Kayıtlı adreslerden seç | Ev/iş/okul |
| **QR Kod** | Fiziksel konum QR'ını okut | Durak, mekan |

### 9.5.4 Çok Noktalı Rota (Multi-Leg)

Müşteri aynı yolculukta birden fazla durak ekleyebilir:

```
ÖRNEK: 3 Duraklı Rota
┌─────────────────────────────────────────────┐
│  📍 1. ALIŞ: Ev (Kadıköy)                   │
│  📍 2. DURAK: Çocuğu okula bırak            │
│  📍 3. DURAK: Kuru temizleme al             │
│  🎯 4. VARIŞ: İş (Levent)                   │
│                                              │
│  Her durakta 5 dk bekleme hakkı              │
│  Toplam: 22 km / 55 dk / 350 TL             │
└─────────────────────────────────────────────┘
```

**Kurallar:**
- Minimum 2 nokta (alış + variş), maksimum 10 nokta
- Her ara durakta 5 dk bekleme ücretsiz, sonrası bekleme ücreti
- Rota sırası değiştirilebilir (sürükle-bırak ile)
- Noktalar arası mesafe minimum 100m olmalı

### 9.5.5 "Buradan Gitmek İstiyorum" — Özel İstek Gönderme

Müşteri rotayı oluşturduktan sonra sisteme **özel bir istek notu** ile gönderebilir:

```
MÜŞTERİ İSTEĞİ:
┌──────────────────────────────────────────────┐
│  📝 "Buradan gitmek istiyorum"               │
│                                              │
│  Ek Not:                                     │
│  "Sahil kenarındayım, mavi şemsiyenin        │
│   yanında bekliyorum. Korna çalmanıza        │
│   gerek yok, görüyorum."                    │
│                                              │
│  🚗 Tercih: Standart / Konfor / VIP         │
│  💰 Bahşiş: +20 TL (ön bahşiş)              │
│                                              │
│  [ GÖNDER → TAKSİ ARIYOR ]                   │
└──────────────────────────────────────────────┘
```

**Sistem Akışı:**
```
ADIM 1: Müşteri haritada noktaları belirler
ADIM 2: Rota çizgisi oluşturulur (harita API)
ADIM 3: Fiyat tahmini hesaplanır
ADIM 4: Müşteri istek notu yazar (opsiyonel)
ADIM 5: "Gönder" butonuna basar
ADIM 6: Sistem rotayı + notu eşleştirme motoruna gönderir
ADIM 7: En uygun şöför eşleştirilir
        ├── Şöför görür: "Müşteri özel rota tanımladı"
        ├── Şöför görür: Müşteri notu
        ├── Şöför görür: Rota çizgisi + noktalar
        └── Şöför kabul eder veya reddeder
ADIM 8: Müşteri şöför bilgisi + canlı takip alır
```

### 9.5.6 Şöför Tarafı Görünümü

```
ŞÖFÖR ÇAĞRI KARTI — ÖZGÜN ROTA:
┌─────────────────────────────────────────────────────┐
│  🚕 YENİ ÇAĞRI — ÖZEL ROTA                         │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │  📍 ALIŞ 🌊 Caddebostan Sahili              │    │
│  │  🎯 VARIŞ 📍 Bağdat Cad. No:123             │    │
│  │  🛑 ARA: Bostancı Migros                    │    │
│  │  ─────────────────────────────────          │    │
│  │  📏 12.5 km │ ⏱ 35 dk │ 💰 195-215 TL      │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  📝 MÜŞTERİ NOTU:                                   │
│  "Buradan gitmek istiyorum, mavi şemsiyenin         │
│   yanındayım, sahil kenarı."                        │
│                                                     │
│  👤 Müşteri: Ayşe Y. ⭐ 4.8 (Onurlu Müşteri)       │
│                                                     │
│  🗺️ [ HARİTADA GÖSTER ]                             │
│                                                     │
│  [ ❌ REDDET ]                 [ ✅ KABUL ET ]      │
└─────────────────────────────────────────────────────┘
```

### 9.5.7 Veritabanı Şeması

```sql
-- Müşteri özgün rotaları
CREATE TABLE customer_custom_routes (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES individual_users(id),
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    route_name          VARCHAR(100),                -- "Sahil rotam" gibi
    is_favorite         BOOLEAN DEFAULT FALSE,        -- Sık kullanılanlara ekle
    total_distance_km   NUMERIC(6,2),                -- Toplam mesafe
    total_duration_min  INTEGER,                      -- Toplam süre
    estimated_fare      NUMERIC(10,2),               -- Tahmini ücret
    waypoints           JSONB NOT NULL                -- Tüm noktalar
);

-- Rota noktaları (her rota için 2-10 nokta)
CREATE TABLE customer_route_waypoints (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id            UUID NOT NULL REFERENCES customer_custom_routes(id) ON DELETE CASCADE,
    sequence_no         INTEGER NOT NULL,             -- Sıra (1=alış, 2..n-1=ara, n=varış)
    point_type          VARCHAR(10) CHECK (point_type IN ('pickup', 'stop', 'destination')),
    latitude            NUMERIC(10,7) NOT NULL,
    longitude           NUMERIC(10,7) NOT NULL,
    address_text        TEXT,                          -- Tersine çevrilmiş adres
    place_name          VARCHAR(200),                  -- "Caddebostan Sahili"
    customer_note       TEXT,                          -- Müşteri notu (opsiyonel)
    stop_duration_min   INTEGER DEFAULT 0,             -- Ara durak bekleme süresi
    UNIQUE(route_id, sequence_no)
);

-- Rota bazlı çağrı talepleri
CREATE TABLE route_based_requests (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES individual_users(id),
    route_id            UUID REFERENCES customer_custom_routes(id),
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    customer_note       TEXT,                          -- "Buradan gitmek istiyorum..."
    comfort_level       VARCHAR(20) DEFAULT 'standard',
    tip_amount          NUMERIC(10,2) DEFAULT 0,
    status              VARCHAR(20) DEFAULT 'pending', -- pending, matched, cancelled, completed
    matched_driver_id   UUID REFERENCES taxi_driver_profiles(id),
    trip_id             UUID REFERENCES taxi_trips(id),
    request_polyline    TEXT                           -- Rota çizgisi (encoded polyline)
);

CREATE INDEX idx_custom_routes_customer ON customer_custom_routes(customer_id);
CREATE INDEX idx_route_waypoints_route ON customer_route_waypoints(route_id);
CREATE INDEX idx_route_requests_customer ON route_based_requests(customer_id);
CREATE INDEX idx_route_requests_status ON route_based_requests(status);
```

### 9.5.8 API Endpoint'leri

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| POST | `/api/v1/taxi/custom-route/create` | Yeni özgün rota oluştur |
| GET | `/api/v1/taxi/custom-route/{id}` | Rota detayı |
| PUT | `/api/v1/taxi/custom-route/{id}` | Rotayı güncelle (nokta ekle/sil/sırala) |
| DELETE | `/api/v1/taxi/custom-route/{id}` | Rotayı sil |
| GET | `/api/v1/taxi/custom-route/list` | Müşterinin rotaları (favoriler + geçmiş) |
| POST | `/api/v1/taxi/custom-route/{id}/favorite` | Sık kullanılanlara ekle/çıkar |
| POST | `/api/v1/taxi/custom-route/geocode` | Koordinat → adres çevir (reverse geocode) |
| POST | `/api/v1/taxi/custom-route/estimate` | Rota için fiyat tahmini |
| POST | `/api/v1/taxi/custom-route/request` | "Buradan gitmek istiyorum" gönder |
| POST | `/api/v1/taxi/custom-route/request/{id}/cancel` | İsteği iptal et |

### 9.5.9 Kullanım Senaryoları

**Senaryo 1: Sahilden taksi çağırma**
> Müşteri Caddebostan sahilinde oturuyor, adres tarif edemiyor. Haritada bulunduğu noktaya uzun basar, "Sahil, mavi şemsiye yanı" notu ekler, variş noktasını Bağdat Caddesi olarak belirler. Şöför haritada tam noktayı görür.

**Senaryo 2: Çok duraklı günlük plan**
> Müşteri evden çıkıp çocuğu okula bırakacak, kuru temizleme alacak, sonra işe gidecek. 4 noktalı rota oluşturur, her durak için bekleme süresi tanımlar. Tek taksiyle tüm günlük işlerini halleder.

**Senaryo 3: Konser/maç çıkışı buluşma**
> 4 arkadaş ayrı yerlerden gelecek, önce Ali'yi al, sonra Veli'yi al, sonra stadyuma git. "Ali şu köşede, Veli marketin önünde" notlarıyla rotayı tarif ederler.

**Senaryo 4: "Buradan gitmek istiyorum" — acil çağrı**
> Müşteri cadde kenarında yürürken aniden taksiye ihtiyaç duyar. Telefonu çıkarır, haritada bulunduğu nokta otomatik alınır, "Buradan gitmek istiyorum" yazıp gönderir. Adres yazmaya gerek kalmaz.

### 9.5.10 Kullanıcı Arayüzü Akışı

```
MÜŞTERİ AKIŞI:
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ ANA      │    │ HARİTA   │    │ NOKTA    │    │ ROTA     │    │ TAKSİ    │
│ EKRAN    │───▶│ AÇILIR   │───▶│ BELİRLE  │───▶│ ONAYLA   │───▶│ GELİYOR  │
│          │    │          │    │ (uzun    │    │ + NOT    │    │          │
│ "Taksi   │    │ Tam      │    │  bas)    │    │ YAZ      │    │ Canlı    │
│  Çağır"  │    │ ekran    │    │          │    │          │    │ takip    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │
                     ▼
              ┌──────────────┐
              │ NOKTA EKLE   │
              │ (opsiyonel)  │
              │              │
              │ En fazla 10  │
              │ nokta        │
              └──────────────┘
```

---

## 10. ZORUNLU SİSTEM ÖDEMESİ (CÜZDAN SİSTEMİ)

### 10.1 Ödeme Zorunluluğu

```
KRİTİK KURAL: Tüm ödemeler SİSTEM ÜZERİNDEN yapılmak zorundadır!
├── Nakit ödeme KABUL EDİLMEZ
├── Elden ödeme KABUL EDİLMEZ
├── Havale/EFT KABUL EDİLMEZ
└── SADECE SİSTEM CÜZDANI veya SİSTEME TANIMLI KART

NEDEN ZORUNLU?
├── Güvenlik (dolandırıcılık önleme)
├── Komisyon tahsilatı
├── Vergi raporlaması
├── Anlaşmazlık çözümü
├── Puanlama sistemi
└── Şöför güvencesi (herkes kazancını alır)
```

### 10.2 Cüzdan Sistemi

```yaml
KULLANICININ SİSTEM CÜZDANI OLMAK ZORUNDADIR:

Cüzdan Tipleri:
  - Bireysel Cüzdan (her kullanıcı için)
  - Şöför Cüzdanı (kazançların toplandığı)
  - Kurumsal Cüzdan (firmalar için)

Bakiye Yükleme Yöntemleri:
  - Kredi Kartı (Visa, Mastercard, Troy)
  - Banka Kartı
  - Havale/EFT (IBAN'a)
  - Papara, ininal vb. dijital cüzdanlar
  - Mobil Ödeme (Turkcell, Vodafone, Türk Telekom)

Para Çekme:
  - Şöför: Kazancını banka hesabına çekebilir
  - Yolcu: Yükleme yaptığı kadar kullanabilir
  - İade: İptal durumunda cüzdana otomatik iade
```

### 10.3 Ödeme Akışı

```
ADIM 1: Yolcu Biner
        ↓
ADIM 2: Şöför "Yolculuk Başlattı" → Taksimetre açılır
        ↓
ADIM 3: Sistem yolcunun cüzdanından veya tanımlı kartından
        gidiş ücretini bloke eder (emanete alır)
        ├── Minimum tutar bloke: Tahmini ücret + %20
        └── Örnek: 167 TL + %20 = 200 TL bloke
        ↓
ADIM 4: Yolculuk devam eder → Gerçek zamanlı takip
        ├── Taksimetre sürekli güncellenir
        └── Tahmini ücret gerçekçi ücrete dönüşür
        ↓
ADIM 5: Varış Noktasına Gelindi
        ├── Şöför "Yolculuğu Bitir" butonuna basar
        └── Nihai ücret hesaplanır
        ↓
ADIM 6: Sistem Otomatik Ödemeyi Çeker
        ├── Bloke tutarın tamamı çekilmez
        ├── Sadece gerçek ücret çekilir (Örn: 175 TL)
        ├── Fazla bloke (25 TL) → Cüzdana otomatik iade
        └── Ek ücret varsa → Karttan otomatik çekim (ek yetki)

ADIM 7: Komisyon Dağıtılır
        ├── Toplam: 175 TL
        ├── Platform Komisyonu (%5): -8.75 TL
        ├── Araç Kira (varsa): -200 TL (aylık/çekilir)
        └── Şöför Kazancı (+ Platform cüzdanına): 166.25 TL

ADIM 8: Makbuz ve Fatura
        ├── Dijital makbuz yolcuya gönderilir
        ├── Fatura (talep edilirse) e-posta ile gönderilir
        └── Şöför günlük kazanç raporu hazırlanır
```

### 10.4 Ödeme Ekranları

```
YOLCU ÖDEME ÖN İZLEME:
┌─────────────────────────────────────────────────────────────────┐
│  💳 ÖDEME BİLGİLERİ                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  YOLCULUK: Kadıköy → Taksim                                    │
│  MESAFE: 8.5 km                                                │
│  SÜRE: 28 dakika                                                │
│                                                                 │
│  📄 ÜCRET DÖKÜMÜ:                                               │
│  ├── Açılış: 15.00 TL                                          │
│  ├── Mesafe: 102.00 TL (8.5 km × 12 TL)                        │
│  ├── Süre: 56.00 TL (28 dk × 2 TL)                             │
│  ├── Yoğun Saat (+%20): 34.60 TL                               │
│  └── TOPLAM: 207.60 TL                                         │
│                                                                 │
│  💳 ÖDEME YÖNTEMİ:                                              │
│  ├── 💳 Kredi Kartı: Visa **** 1234                             │
│  ├── 💰 Cüzdan Bakiyesi: 450 TL                                │
│  └── Seçilen: Kredi Kartı                                      │
│                                                                 │
│  [ÖDEMEYİ ONAYLıYORUM]                                         │
│  → Yolculuk başladığında ödeme otomatik çekilecektir.          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

YOLCU YOLCULUK BİTTİ:
┌─────────────────────────────────────────────────────────────────┐
│  ✅ YOLCULUK TAMAMLANDI                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🚕 34 TAK 1234 - Ahmet Yılmaz                                 │
│  📍 Kadıköy → Taksim                                           │
│                                                                 │
│  💰 ÖDEME:                                                      │
│  ├── Toplam Ücret: 207.60 TL                                   │
│  ├── Ödeme: Kredi Kartı (Visa **** 1234)                       │
│  └── Durum: ✅ Ödendi                                           │
│                                                                 │
│  📄 MAKBUZ: [Görüntüle]                                        │
│                                                                 │
│  ⭐ PUANLAMA (ZORUNLU):                                         │
│  ┌─────────────────────────────────────────────────────┐       │
│  │  ŞÖFÖR PUANLA                                        │       │
│  │  ├── Sürüş Kalitesi:     ⭐⭐⭐⭐☆ (4)              │       │
│  │  ├── Zamanında Gelme:    ⭐⭐⭐⭐⭐ (5)             │       │
│  │  ├── İletişim:           ⭐⭐⭐⭐☆ (4)              │       │
│  │  └── Profesyonellik:     ⭐⭐⭐⭐⭐ (5)             │       │
│  │                                                     │       │
│  │  ARAÇ PUANLA                                          │       │
│  │  ├── Temizlik:           ⭐⭐⭐⭐☆ (4)              │       │
│  │  ├── Koku:               ⭐⭐⭐⭐⭐ (5)             │       │
│  │  ├── Konfor:             ⭐⭐⭐⭐⭐ (5)             │       │
│  │  └── Klima/Isıtma:       ⭐⭐⭐⭐⭐ (5)             │       │
│  │                                                     │       │
│  │  Yorum (opsiyonel): [___________________________]          │       │
│  │                                                     │       │
│  │  [PUANLAMAYI GÖNDER]                               │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
│  ⚠️ NOT: Puanlama yapılmadan yeni taksi çağıramazsınız!        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.5 Şöför Kazanç Raporu

```
┌─────────────────────────────────────────────────────────────────┐
│  💰 Ahmet Yılmaz - Bugünkü Kazanç (12.06.2026)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┬──────────┬──────────┬──────────────────────┐  │
│  │ Saat         │ Nereden  │ Nereye   │ Ücret │ Kesintiler  │  │
│  ├──────────────┼──────────┼──────────┼───────┼─────────────┤  │
│  │ 06:15-06:35  │ Kadıköy  │ Bostancı │ 85 TL │ -4.25 TL    │  │
│  │ 06:40-07:10  │ Bostancı │ Üsküdar  │ 120 TL│ -6 TL       │  │
│  │ 07:15-07:50  │ Üsküdar  │ Taksim   │ 175 TL│ -8.75 TL    │  │
│  │ 08:00-08:30  │ Taksim   │ Beşiktaş │ 95 TL │ -4.75 TL    │  │
│  │ 08:40-09:15  │ Beşiktaş │ Kadıköy  │ 160 TL│ -8 TL       │  │
│  │ ...          │ ...      │ ...      │ ...   │ ...         │  │
│  ├──────────────┼──────────┼──────────┼───────┼─────────────┤  │
│  │ TOPLAM       │ 22 yolcu │ 145 km   │ 1,890 │ -94.50 TL   │  │
│  └──────────────┴──────────┴──────────┴───────┴─────────────┘  │
│                                                                 │
│  GELİR: 1,890.00 TL                                              │
│  KOMİSYON (%5): -94.50 TL                                       │
│  KİRA (Vardiyalık): -200.00 TL                                  │
│  NET KAZANÇ: 1,595.50 TL                                        │
│  ÖDENECEK (Hesaplara aktarıldı): 1,595.50 TL                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. VERİTABANI ŞEMASI (YENİ TABLOLAR)

### 11.1 Şöför Belgeleri

```sql
-- Taksi şöförü belgeleri
CREATE TABLE taxi_driver_documents (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    
    -- Ehliyet
    drivers_license_front   VARCHAR(500),             -- Ehliyet ön yüz
    drivers_license_back    VARCHAR(500),             -- Ehliyet arka yüz
    drivers_license_number  VARCHAR(50),
    drivers_license_class   VARCHAR(10),              -- B, B1 vb.
    drivers_license_issue   DATE,                     -- Veriliş tarihi
    drivers_license_expiry  DATE,                     -- Bitiş tarihi
    drivers_license_status  VARCHAR(20) DEFAULT 'pending', -- pending, verified, expired, rejected
    
    -- Psikoteknik
    psychotechnical_url     VARCHAR(500),
    psychotechnical_date    DATE,
    psychotechnical_expiry  DATE,
    psychotechnical_status  VARCHAR(20) DEFAULT 'pending',
    
    -- SRC Belgesi
    src_certificate_url     VARCHAR(500),
    src_certificate_number  VARCHAR(50),
    src_certificate_type    VARCHAR(20),              -- SRC-4
    src_certificate_expiry  DATE,
    src_certificate_status  VARCHAR(20) DEFAULT 'pending',
    
    -- Adli Sicil
    criminal_record_url     VARCHAR(500),
    criminal_record_date    DATE,
    criminal_record_expiry  DATE,
    criminal_record_status  VARCHAR(20) DEFAULT 'pending',
    
    -- İkametgah
    residence_doc_url       VARCHAR(500),
    residence_address       TEXT,
    residence_status        VARCHAR(20) DEFAULT 'pending',
    
    -- Vergi
    tax_certificate_url     VARCHAR(500),
    tax_office              VARCHAR(200),
    tax_number              VARCHAR(50),
    tax_status              VARCHAR(20) DEFAULT 'pending',
    
    -- Genel Durum
    verification_status     VARCHAR(20) DEFAULT 'pending', -- pending, verified, rejected
    verification_note       TEXT,                     -- Red sebebi veya not
    verified_by             UUID REFERENCES users(id), -- Admin onaylayan
    verified_at             TIMESTAMP,
    
    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);
```

### 11.2 Araç (Ticari Plaka) Tablosu

```sql
-- Ticari araç / taksi plakası
CREATE TABLE taxi_vehicles (
    id                  UUID PRIMARY KEY,
    
    -- Araç Sahipleri
    ownership_type      VARCHAR(30) NOT NULL,         -- individual, shared, corporate
    
    -- Plaka Bilgileri
    plate_number        VARCHAR(20) UNIQUE NOT NULL,  -- 34 TAK 1234
    plate_city          VARCHAR(50),                  -- İstanbul
    plate_type          VARCHAR(30) DEFAULT 'taxi',   -- taxi, minibus, commercial
    
    -- Araç Bilgileri
    brand               VARCHAR(100) NOT NULL,        -- Renault
    model               VARCHAR(200) NOT NULL,        -- Megane
    year                INTEGER NOT NULL,             -- 2023
    color               VARCHAR(50),
    engine_type         VARCHAR(20),                  -- diesel, gasoline, electric, hybrid
    transmission        VARCHAR(20),                  -- manual, automatic
    seating_capacity    INTEGER DEFAULT 4,
    
    -- Ruhsat
    registration_doc    VARCHAR(500),
    registration_number VARCHAR(100),
    
    -- Sigorta
    insurance_url       VARCHAR(500),
    insurance_type      VARCHAR(50),                  -- traffic, comprehensive, commercial
    insurance_start     DATE,
    insurance_expiry    DATE,
    insurance_status    VARCHAR(20) DEFAULT 'pending',
    
    -- Muayene
    inspection_url      VARCHAR(500),
    inspection_date     DATE,
    inspection_expiry   DATE,
    inspection_status   VARCHAR(20) DEFAULT 'pending',
    
    -- Taksimetre
    taximeter_model     VARCHAR(100),
    taximeter_calibration_date DATE,
    taximeter_calibration_expiry DATE,
    
    -- OBD / GPS
    obd_device_id       VARCHAR(100),                 -- GPS takip cihazı
    obd_last_ping       TIMESTAMP,                    -- Son ping
    obd_status          VARCHAR(20) DEFAULT 'offline',
    
    -- Fotoğraflar
    photo_url           VARCHAR(500),                 -- Kapak fotoğrafı
    photos              JSONB DEFAULT '[]',
    
    -- Durum
    is_active           BOOLEAN DEFAULT TRUE,
    is_available        BOOLEAN DEFAULT TRUE,         -- Müsait mi?
    status              VARCHAR(20) DEFAULT 'active',  -- active, maintenance, inactive, retired
    
    -- Puan
    rating_avg          DECIMAL(3,2) DEFAULT 0,
    rating_count        INTEGER DEFAULT 0,
    
    -- İstatistikler
    total_trips         INTEGER DEFAULT 0,
    total_distance_km   DECIMAL(12,2) DEFAULT 0,
    total_earnings      DECIMAL(14,2) DEFAULT 0,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.3 Araç Sahipliği (Ortaklık)

```sql
-- Araç sahipleri ve hisse oranları
CREATE TABLE taxi_vehicle_owners (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    user_id             UUID REFERENCES users(id),            -- Gerçek kişi
    company_id          UUID REFERENCES company_profiles(id) NULL, -- Tüzel kişi
    
    ownership_percent   DECIMAL(5,2) NOT NULL,                -- %50, %30 gibi
    ownership_type      VARCHAR(30),                          -- owner, lessor, both
    is_primary_owner    BOOLEAN DEFAULT FALSE,                -- Ana sahip
    
    role                VARCHAR(30) DEFAULT 'owner',          -- owner, co_owner, company
    
    -- Ortaklık Sözleşmesi
    agreement_url       VARCHAR(500),                         -- İmzalı sözleşme
    agreement_start     DATE,
    agreement_end       DATE,
    
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(vehicle_id, user_id)
);
```

### 11.4 Araç - Şöför Atama (Vardiya)

```sql
-- Araç-şöför vardiya atamaları
CREATE TABLE taxi_driver_assignments (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    driver_id           UUID REFERENCES users(id),            -- Şöför
    assigner_id         UUID REFERENCES users(id),            -- Atamayı yapan
    
    -- Vardiya Bilgileri
    shift_type          VARCHAR(30) NOT NULL,                 -- full_day, morning, evening, night, weekend, custom
    shift_start         TIME NOT NULL,                        -- 06:00
    shift_end           TIME NOT NULL,                        -- 14:00
    shift_days          JSONB NOT NULL,                       -- [1,2,3,4,5,6,7] (Pazartesi=1)
    
    -- Yetki Türü
    assignment_type     VARCHAR(30) NOT NULL,                 -- primary, rental, substitute, temporary
    
    -- Kira (eğer kiralık ise)
    rental_agreement_id UUID REFERENCES taxi_rental_agreements(id) NULL,
    
    -- Durum
    is_active           BOOLEAN DEFAULT TRUE,
    is_current_driver   BOOLEAN DEFAULT FALSE,                -- Şu an aktif sürücü mü?
    
    -- Zaman
    effective_from      DATE NOT NULL,
    effective_until     DATE,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(vehicle_id, driver_id, shift_type, shift_start)
);
```

### 11.5 Kira Sözleşmeleri

```sql
-- Araç kiralama sözleşmeleri
CREATE TABLE taxi_rental_agreements (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    lessor_id           UUID REFERENCES users(id),            -- Kiralayan (araç sahibi)
    lessee_id           UUID REFERENCES users(id),            -- Kiracı (şöför)
    
    -- Kira Türü
    rental_type         VARCHAR(30) NOT NULL,                 -- daily, shiftly, weekly, monthly, commission
    
    -- Kira Ücreti
    rental_amount       DECIMAL(10,2) NOT NULL,              -- Günlük/vardiya ücreti
    rental_currency     VARCHAR(3) DEFAULT 'TRY',
    payment_frequency   VARCHAR(20) DEFAULT 'daily',          -- daily, weekly, monthly
    payment_method      VARCHAR(30) DEFAULT 'auto_deduct',    -- Otomatik kesinti
    
    -- Kira Şartları
    km_limit            DECIMAL(10,2) NULL,                  -- Günlük km limiti
    km_overage_rate     DECIMAL(8,2) NULL,                   -- Limit aşımı ücreti/km
    service_area        JSONB DEFAULT '[]',                   -- Çalışma bölgesi
    work_hours_start    TIME,                                 -- Çalışma başlangıç
    work_hours_end      TIME,                                 -- Çalışma bitiş
    
    -- Depozito
    deposit_amount      DECIMAL(10,2) DEFAULT 0,
    deposit_paid        BOOLEAN DEFAULT FALSE,
    
    -- Sözleşme
    contract_url        VARCHAR(500),                         -- İmzalı sözleşme PDF
    contract_start      DATE NOT NULL,
    contract_end        DATE,
    auto_renew          BOOLEAN DEFAULT TRUE,
    
    -- Durum
    status              VARCHAR(20) DEFAULT 'active',         -- active, suspended, expired, terminated
    
    -- Ödeme Bilgileri
    total_paid          DECIMAL(14,2) DEFAULT 0,
    last_payment_date   DATE,
    next_payment_date   DATE,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.6 Şöför Anlık Durum

```sql
-- Şöförün anlık durumu (online/offline/müsait vb.)
CREATE TABLE taxi_driver_status (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),    -- Şu an hangi araçta
    
    -- Durum
    status              VARCHAR(30) NOT NULL DEFAULT 'offline', -- offline, available, busy_on_trip, on_break, maintenance
    is_available        BOOLEAN DEFAULT FALSE,               -- Çağrı almaya müsait mi?
    is_online           BOOLEAN DEFAULT FALSE,               -- Sisteme bağlı mı?
    
    -- Konum
    current_latitude    DECIMAL(10,8),
    current_longitude   DECIMAL(11,8),
    location_updated_at TIMESTAMP,
    
    -- Mevcut Yolculuk
    current_trip_id     UUID REFERENCES taxi_trips(id) NULL,
    trip_started_at     TIMESTAMP,
    
    -- Vardiya
    current_shift_id    UUID REFERENCES taxi_driver_assignments(id) NULL,
    shift_started_at    TIMESTAMP,
    shift_end_at        TIMESTAMP,
    
    -- Bugünkü İstatistikler
    today_trips         INTEGER DEFAULT 0,
    today_earnings      DECIMAL(12,2) DEFAULT 0,
    today_distance_km   DECIMAL(10,2) DEFAULT 0,
    
    -- Uygulama
    app_version         VARCHAR(20),
    device_type         VARCHAR(20),                          -- ios, android
    battery_level       INTEGER,                              -- 0-100
    
    -- Otomatik Kabul
    auto_accept         BOOLEAN DEFAULT FALSE,
    max_accept_distance INTEGER DEFAULT 5,                    -- km
    
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.7 Yolculuk Çağrıları

```sql
-- Çağrı logları (kim çağırdı, hangi taksilere gitti, sonuç)
CREATE TABLE taxi_ride_requests (
    id                  UUID PRIMARY KEY,
    passenger_id        UUID REFERENCES users(id),
    
    -- Konum
    pickup_latitude     DECIMAL(10,8) NOT NULL,
    pickup_longitude    DECIMAL(11,8) NOT NULL,
    pickup_address      TEXT,
    dropoff_latitude    DECIMAL(10,8) NOT NULL,
    dropoff_longitude   DECIMAL(11,8) NOT NULL,
    dropoff_address     TEXT,
    
    -- Tahmin
    estimated_distance  DECIMAL(8,2),
    estimated_duration  INTEGER,
    estimated_fare_min  DECIMAL(10,2),
    estimated_fare_max  DECIMAL(10,2),
    
    -- Rota
    route_polyline      TEXT,                                 -- Rota çizgisi (encoded polyline)
    route_instructions  JSONB DEFAULT '[]',                   -- Yol tarifleri
    
    -- Çağrıya Giden Taksiler
    notified_drivers    JSONB DEFAULT '[]',                   -- [{driver_id, distance, response}]
    accepted_driver_id  UUID REFERENCES users(id) NULL,
    accepted_at         TIMESTAMP,
    response_time_seconds INTEGER,                            -- Kabul süresi
    
    -- Durum
    status              VARCHAR(30) DEFAULT 'pending',        -- pending, accepted, declined, expired, cancelled
    cancel_reason       TEXT,
    cancelled_by        VARCHAR(20),                          -- passenger, system
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.8 Yolculuk Tablosu (Gelişmiş)

```sql
-- Yolculuk (mevcut taxi_trips tablosunun gelişmiş hali)
CREATE TABLE taxi_trips (
    id                  UUID PRIMARY KEY,
    request_id          UUID REFERENCES taxi_ride_requests(id),
    
    -- Taraflar
    passenger_id        UUID REFERENCES users(id),
    driver_id           UUID REFERENCES users(id),            -- Şöför
    vehicle_id          UUID REFERENCES taxi_vehicles(id),    -- Araç
    
    -- Yolculuk Bilgileri
    pickup_latitude     DECIMAL(10,8),
    pickup_longitude    DECIMAL(11,8),
    pickup_address      TEXT,
    dropoff_latitude    DECIMAL(10,8),
    dropoff_longitude   DECIMAL(11,8),
    dropoff_address     TEXT,
    
    -- Rota (Gerçek)
    distance_km         DECIMAL(8,2),
    duration_minutes    INTEGER,
    route_taken         JSONB DEFAULT '[]',                  -- GPS noktaları
    
    -- Ücret
    base_fare           DECIMAL(8,2) DEFAULT 0,
    distance_fare       DECIMAL(8,2) DEFAULT 0,
    time_fare           DECIMAL(8,2) DEFAULT 0,
    surge_multiplier    DECIMAL(3,2) DEFAULT 1.00,
    surge_amount        DECIMAL(8,2) DEFAULT 0,
    extra_fees          JSONB DEFAULT '{}',                  -- {toll: 15, bridge: 10}
    total_fare          DECIMAL(10,2),
    currency            VARCHAR(3) DEFAULT 'TRY',
    
    -- Ödeme
    payment_method      VARCHAR(50),                         -- card, wallet
    payment_status      VARCHAR(20) DEFAULT 'pending',       -- pending, authorized, captured, refunded
    payment_gateway_ref VARCHAR(255),
    payment_held_fare   DECIMAL(10,2),                       -- Bloke edilen tutar
    
    -- Komisyon
    commission_rate     DECIMAL(5,2) DEFAULT 5.00,
    commission_amount   DECIMAL(10,2),
    driver_earning      DECIMAL(10,2),
    rental_cost         DECIMAL(10,2) DEFAULT 0,             -- Kira kesintisi
    
    -- Zaman
    requested_at        TIMESTAMP,
    accepted_at         TIMESTAMP,
    driver_arrived_at   TIMESTAMP,                            -- Şöför geldi
    started_at          TIMESTAMP,                            -- Yolculuk başladı
    completed_at        TIMESTAMP,                            -- Yolculuk bitti
    
    -- Durum
    status              VARCHAR(30) DEFAULT 'requested',     -- requested, accepted, driver_arrived, in_progress, completed, cancelled, refunded
    
    -- İptal
    cancellation_reason TEXT,
    cancelled_by        VARCHAR(20),
    
    -- Puanlama
    driver_rated        BOOLEAN DEFAULT FALSE,
    vehicle_rated       BOOLEAN DEFAULT FALSE,
    driver_rating       INTEGER CHECK(driver_rating BETWEEN 1 AND 5),
    vehicle_rating      INTEGER CHECK(vehicle_rating BETWEEN 1 AND 5),
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.9 Puanlama Tablosu

```sql
-- Çift yönlü puanlama (şöför + araç)
CREATE TABLE taxi_ratings (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    reviewer_id         UUID REFERENCES users(id),            -- Yolcu
    driver_id           UUID REFERENCES users(id),            -- Puanlanan şöför
    vehicle_id          UUID REFERENCES taxi_vehicles(id),    -- Puanlanan araç
    
    -- Şöför Puanları
    driving_quality     INTEGER CHECK(driving_quality BETWEEN 1 AND 5),
    punctuality         INTEGER CHECK(punctuality BETWEEN 1 AND 5),
    communication       INTEGER CHECK(communication BETWEEN 1 AND 5),
    safe_driving        INTEGER CHECK(safe_driving BETWEEN 1 AND 5),
    route_knowledge     INTEGER CHECK(route_knowledge BETWEEN 1 AND 5),
    helpfulness         INTEGER CHECK(helpfulness BETWEEN 1 AND 5),
    
    driver_avg          DECIMAL(3,2),                         -- Otomatik hesaplanır
    
    -- Araç Puanları
    vehicle_cleanliness     INTEGER CHECK(vehicle_cleanliness BETWEEN 1 AND 5),
    vehicle_smell           INTEGER CHECK(vehicle_smell BETWEEN 1 AND 5),
    vehicle_comfort         INTEGER CHECK(vehicle_comfort BETWEEN 1 AND 5),
    vehicle_ac              INTEGER CHECK(vehicle_ac BETWEEN 1 AND 5),
    vehicle_condition       INTEGER CHECK(vehicle_condition BETWEEN 1 AND 5),
    
    vehicle_avg         DECIMAL(3,2),                         -- Otomatik hesaplanır
    
    -- Kombine
    combined_score      DECIMAL(3,2),                         -- (driver_avg × 0.6) + (vehicle_avg × 0.4)
    
    -- Yorum
    comment             TEXT,
    driver_response     TEXT,                                 -- Şöför cevap verebilir
    response_date       TIMESTAMP,
    
    -- Fotoğraflar
    photos              JSONB DEFAULT '[]',
    
    is_visible          BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(trip_id, reviewer_id)
);
```

### 11.10 Yolcu Cüzdanı

```sql
-- Kullanıcı cüzdanı
CREATE TABLE user_wallets (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    
    -- Bakiye
    balance             DECIMAL(14,2) DEFAULT 0,              -- Kullanılabilir bakiye
    blocked_balance     DECIMAL(14,2) DEFAULT 0,              -- Bloke edilmiş (yolculuk sırasında)
    
    -- Ödeme Yöntemleri
    default_payment     VARCHAR(30) DEFAULT 'wallet',         -- wallet, card
    saved_cards         JSONB DEFAULT '[]',                   -- [{card_token, last_four, brand}]
    
    -- Limitler
    daily_limit         DECIMAL(14,2) DEFAULT 1000,
    monthly_limit       DECIMAL(14,2) DEFAULT 10000,
    current_daily_spent DECIMAL(14,2) DEFAULT 0,
    current_monthly_spent DECIMAL(14,2) DEFAULT 0,
    
    -- Durum
    is_active           BOOLEAN DEFAULT TRUE,
    is_frozen           BOOLEAN DEFAULT FALSE,
    frozen_reason       TEXT,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Cüzdan hareketleri
CREATE TABLE wallet_transactions (
    id                  UUID PRIMARY KEY,
    wallet_id           UUID REFERENCES user_wallets(id),
    user_id             UUID REFERENCES users(id),
    
    -- İşlem Türü
    transaction_type    VARCHAR(30) NOT NULL,                 -- deposit, withdrawal, payment, refund, commission, rental
    related_trip_id     UUID REFERENCES taxi_trips(id) NULL,
    
    -- Tutar
    amount              DECIMAL(14,2) NOT NULL,
    fee                 DECIMAL(10,2) DEFAULT 0,
    net_amount          DECIMAL(14,2),
    currency            VARCHAR(3) DEFAULT 'TRY',
    balance_before      DECIMAL(14,2),
    balance_after       DECIMAL(14,2),
    
    -- Ödeme Yöntemi
    payment_method      VARCHAR(50),
    gateway_reference   VARCHAR(255),
    
    -- Durum
    status              VARCHAR(20) DEFAULT 'pending',        -- pending, completed, failed, refunded
    description         TEXT,
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 11.11 Çağrı Red Logları

```sql
-- Çağrı reddi logları (ceza puanı için)
CREATE TABLE call_rejection_log (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES users(id),
    request_id          UUID REFERENCES taxi_ride_requests(id),
    
    rejection_type      VARCHAR(30),                          -- timeout, manual_reject, auto_decline
    rejection_reason    TEXT,                                  -- Kullanıcı tarafından belirtilmişse
    calculated_distance DECIMAL(8,2),                          -- Yolcu mesafesi
    estimated_fare      DECIMAL(10,2),                         -- Tahmini ücret
    
    is_penalty          BOOLEAN DEFAULT TRUE,                  -- Ceza puanı kesildi mi?
    penalty_points      INTEGER DEFAULT 0,                     -- Kaç puan kesildi
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 12. API ENDPOINT'LERİ

### 12.1 Şöför Yönetimi

```
POST   /api/v1/taxi/driver/apply               # Taksi şöför başvurusu
GET    /api/v1/taxi/driver/status               # Başvuru durumu
POST   /api/v1/taxi/driver/documents            # Belge yükle
GET    /api/v1/taxi/driver/documents            # Belgeleri listele
DELETE /api/v1/taxi/driver/documents/:id        # Belge sil
PUT    /api/v1/taxi/driver/documents/:id/renew  # Belge yenile
GET    /api/v1/taxi/driver/profile              # Şöför profilim
PUT    /api/v1/taxi/driver/profile              # Profili güncelle
```

### 12.2 Araç Yönetimi

```
POST   /api/v1/taxi/vehicles                   # Araç ekle
GET    /api/v1/taxi/vehicles                    # Araçlarım listesi
GET    /api/v1/taxi/vehicles/:id                # Araç detayı
PUT    /api/v1/taxi/vehicles/:id                # Araç güncelle
DELETE /api/v1/taxi/vehicles/:id                # Araç sil
POST   /api/v1/taxi/vehicles/:id/owners         # Ortak ekle
DELETE /api/v1/taxi/vehicles/:id/owners/:ownerId # Ortak çıkar
PUT    /api/v1/taxi/vehicles/:id/owners/:ownerId # Hisse güncelle
POST   /api/v1/taxi/vehicles/:id/documents      # Araç belgesi yükle
GET    /api/v1/taxi/vehicles/:id/statistics     # Araç istatistikleri
```

### 12.3 Vardiya ve Atama

```
POST   /api/v1/taxi/assignments                 # Vardiya ata
GET    /api/v1/taxi/assignments                 # Vardiyaları listele
PUT    /api/v1/taxi/assignments/:id             # Vardiyayı güncelle
DELETE /api/v1/taxi/assignments/:id             # Vardiyayı kaldır
POST   /api/v1/taxi/assignments/:id/swap        # Vardiya değiştir
POST   /api/v1/taxi/assignments/:id/leave       # Vardiyadan izin al
GET    /api/v1/taxi/assignments/available       # Yedek şöför bul
POST   /api/v1/taxi/assignments/substitute      # Yedek ata
POST   /api/v1/taxi/driver/start-shift          # Vardiyaya başla
POST   /api/v1/taxi/driver/end-shift            # Vardiyayı bitir
```

### 12.4 Kiralama

```
POST   /api/v1/taxi/rental-agreements           # Kira sözleşmesi oluştur
GET    /api/v1/taxi/rental-agreements           # Kira sözleşmelerim
GET    /api/v1/taxi/rental-agreements/:id       # Sözleşme detay
PUT    /api/v1/taxi/rental-agreements/:id       # Sözleşme güncelle
DELETE /api/v1/taxi/rental-agreements/:id       # Sözleşme feshet
PUT    /api/v1/taxi/rental-agreements/:id/approve # Sözleşmeyi onayla
GET    /api/v1/taxi/rental-agreements/:id/payments # Ödeme geçmişi
```

### 12.5 Taksi Çağırma ve Yolculuk

```
GET    /api/v1/taxi/nearby                     # Yakın taksileri listele
POST   /api/v1/taxi/request                    # Taksi çağır
GET    /api/v1/taxi/request/:id                # Çağrı durumu
POST   /api/v1/taxi/request/:id/cancel         # Çağrıyı iptal et
GET    /api/v1/taxi/request/:id/estimate       # Ücret tahmini
POST   /api/v1/taxi/request/:id/accept         # Çağrıyı kabul et (şöför)
POST   /api/v1/taxi/request/:id/reject         # Çağrıyı reddet (şöför)

POST   /api/v1/taxi/trip/:id/start            # Yolculuğa başla
POST   /api/v1/taxi/trip/:id/end              # Yolculuğu bitir
GET    /api/v1/taxi/trip/:id                  # Yolculuk detayı
POST   /api/v1/taxi/trip/:id/rate-driver      # Şöför puanla
POST   /api/v1/taxi/trip/:id/rate-vehicle     # Araç puanla
```

### 12.6 Ödeme

```
GET    /api/v1/wallet                          # Cüzdan bilgileri
POST   /api/v1/wallet/deposit                  # Bakiye yükle
POST   /api/v1/wallet/withdraw                 # Para çek
POST   /api/v1/wallet/card/add                 # Kart ekle
DELETE /api/v1/wallet/card/:id                 # Kart sil
GET    /api/v1/wallet/transactions             # İşlem geçmişi
GET    /api/v1/wallet/trip/:id/payment         # Yolculuk ödemesi
```

### 12.7 Admin

```
GET    /api/v1/admin/taxi/drivers              # Şöför listesi
GET    /api/v1/admin/taxi/drivers/:id          # Şöför detay
PUT    /api/v1/admin/taxi/drivers/:id/verify   # Şöför onayla
PUT    /api/v1/admin/taxi/drivers/:id/reject   # Şöför reddet
POST   /api/v1/admin/taxi/drivers/:id/suspend  # Şöför askıya al
GET    /api/v1/admin/taxi/vehicles             # Araç listesi
PUT    /api/v1/admin/taxi/vehicles/:id/verify  # Araç onayla
GET    /api/v1/admin/taxi/trips                # Tüm yolculuklar
GET    /api/v1/admin/taxi/reports              # Raporlar
```

---

## 13. AKIŞ DİYAGRAMLARI

### 13.1 Genel Taksi Çağırma Akışı

```
YOLCU                          SİSTEM                          TAKSİLER
  │                              │                              │
  ├── Konum açar ──────────────► │                              │
  │                              │                              │
  ├── Gidilecek yeri girer ────► │                              │
  │                              ├── Rota hesapla ──────────── │
  │                              ├── Fiyat tahmin et           │
  │                              │                              │
  │◄── Rota + Fiyat göster ───── │                              │
  │                              │                              │
  ├── [Taksi Çağır] butonu ────► │                              │
  │                              ├── En yakın müsait taksileri bul
  │                              │                              │
  │                              ├── Taksi 1'e çağrı gönder ──►│
  │                              │        (800m, Puan: 4.8)     │
  │                              │◄──── Sinyal yok (timeout) ── │
  │                              │                              │
  │                              ├── Taksi 2'ye çağrı gönder ──►│
  │                              │        (1.2km, Puan: 4.9)    │
  │                              │◄──── KABUL! (3 sn) ───────── │
  │                              │                              │
  │◄── Eşleşme bilgisi ───────── │                              │
  │    Ahmet Yılmaz              │                              │
  │    34 TAK 1234               │                              │
  │    Tahmini varış: 4 dk       │                              │
  │                              │                              │
  │◄── Taksi haritada ────────── │                              │
  │    Canlı takip               │                              │
  │                              │                              │
  ├── Biner ────────────────────►│                              │
  │                              │◄── Yolculuk başlat ──────────│
  │                              │                              │
  │                              ├── Ödeme bloke (200 TL)      │
  │                              │                              │
  ├── Yolculuk sırasında ───────►│                              │
  │                              ├── Taksimetre canlı           │
  │                              │                              │
  ├── Varış ────────────────────►│                              │
  │                              │◄── Yolculuk bitir ──────────│
  │                              │                              │
  │                              ├── Nihai ücret hesapla (175 TL)
  │                              ├── Kalan bloke iade (25 TL)  │
  │                              ├── Komisyon kes (8.75 TL)    │
  │                              ├── Şöför kazancını aktar     │
  │                              │                              │
  │◄── Ödeme alındı (175 TL) ──  │                              │
  │                              │                              │
  │◄── PUANLA (ZORUNLU!) ───────│                              │
  │    Şöför + Araç puanla       │                              │
  │                              │                              │
  └── Puanlama tamam ──────────► │                              │
```

### 13.2 Çoklu Vardiya Yönetim Akışı

```
ARAÇ SAHİBİ                    SİSTEM                          ŞÖFÖRLER
  │                              │                              │
  ├── Araç ekle ───────────────► │                              │
  │    (34 TAK 1234)             │                              │
  │                              ├── Araç kaydı oluştu         │
  │                              │                              │
  ├── Vardiya ata ─────────────► │                              │
  │    Sabah: Ahmet (06-14)      │                              │
  │    Akşam: Mehmet (14-22)     │                              │
  │                              ├── Vardiyalar oluşturuldu    │
  │                              │                              │
  │                              │◄── Sabahçı başladı          │
  │                              │    Ahmet - Vardiyada (06:00)│
  │                              │    Durum: Müsait            │
  │                              │                              │
  │                              │    (Öğlen)                   │
  │                              │                              │
  │                              │◄── Akşamcı başladı          │
  │                              │    Mehmet - Vardiyada (14:00)
  │                              │    Durum: Müsait            │
  │                              │                              │
  │                              │◄── Sabahçı bitti            │
  │                              │    Ahmet - Vardiya bitti    │
  │                              │    Günlük kazanç: 1.890 TL  │
  │                              │                              │
  │◄── Kira geliri aktarıldı ────│                              │
  │    Sabah kirası: 0 TL        │                              │
  │    (Ahmet araç sahibi)       │                              │
  │                              │                              │
  │                              │◄── Akşamcı bitti            │
  │                              │    Mehmet - Vardiya bitti   │
  │                              │    Günlük kazanç: 1.200 TL  │
  │                              │                              │
  │◄── Kira geliri aktarıldı ────│                              │
  │    Akşam kirası: 200 TL      │                              │
  │                              │                              │
  └── Günlük rapor al ─────────►│                              │
      Toplam: 200 TL kira geliri │                              │
```

---

## 14. MÜŞTERİ SEYAHAT TAAHHÜT VE ERKEN İNME SİSTEMİ

### 14.1 Temel Kural: Seyahat Taahhüdü

Yolcu taksi çağırırken **gideceği yeri (hedef adresi)** belirtmek zorundadır. Bu adres, fiyat tahmini ve eşleştirme için kullanılır. Yolcu bu adrese gitmeyi **taahhüt etmiş** sayılır.

```
ÇAĞRI ANI:
├── Yolcu konumunu açar
├── Yolcu gideceği adresi girer → TAAHHÜT OLUŞUR
├── Sistem fiyat tahminini hesaplar (hedef adrese göre)
├── Taksi eşleşmesi yapılır
└── Yolculuk başlar
```

### 14.2 Normal Durum: Erken İnme ve Ödeme

Yolcu, taahhüt ettiği yerden **önce** inmek isterse (ör: yolda bir yerde inmek), sadece **indiği mesafe kadar** ödeme yapar. Bu normal bir durumdur ve cezai işlem uygulanmaz.

```
ÖRNEK:
├── Çağrı: Kadıköy → Taksim (8.5 km, tahmini 167 TL)
├── Yolcu bindi, Beşiktaş'ta inmek istedi (5.2 km)
├── Ödeme: Sadece 5.2 km ücreti = 102 TL
├── Kalan mesafe (3.3 km) iptal
└── Sonuç: Normal işlem, ceza yok
```

### 14.3 Aylık Erken İnme Hakkı (1 Hak / Ay)

Her yolcuya **ayda 1 kez** erken inme hakkı tanınır. Bu hak kullanıldığında, yolcu taahhüt ettiği yerden önce inse dahi sadece gittiği mesafe kadar öder. Bu hak **takvim ayı bazında** sıfırlanır.

```
KURAL:
├── Her ayın 1'inde hak yenilenir
├── Kullanılmayan hak devretmez
├── Hak sadece erken inme durumunda tükenir
└── Hak kullanıldığında ödeme: sadece gidilen mesafe
```

### 14.4 Kötüye Kullanım Tespiti ve Onurlu Müşteri Puanı

Eğer bir yolcu **yıl içinde 3 farklı ayda** erken inme hakkını kullanırsa (yani 3 ay üst üste veya toplam 3 ayda), bu durum **sistem tarafından kötüye kullanım** olarak işaretlenir.

```
TETİKLEYİCİ:
├── Yıl içinde 3 farklı ayda erken inme hakkı kullanımı
├── (Ocak + Mart + Mayıs gibi farklı aylar)
└── Her ay 1'er kere kullanım yeterli
```

Bu durumda:

```
SONUÇ:
├── Yolcunun "Onurlu Müşteri Puanı" düşer
├── Yolcu "Onurlu Müşteri" statüsünü kaybeder
├── Sistem, yolcuya uyarı bildirimi gönderir
│   └── "Sayın yolcu, sık sık erken inme talebinde bulunduğunuz için
│        onurlu müşteri puanınız düşürülmüştür."
└── Artık yeni bir kural devreye girer (bkz. 14.5)
```

### 14.5 Onurlu Müşteri Statüsü Kaybı Sonrası Ödeme Kuralı

Onurlu müşteri statüsünü kaybeden yolcu, **nerede inerse insin**, ilk çağırdığı ve taahhüt ettiği **gideceği mesafenin ücretini ödemek zorundadır**.

```
ÖRNEK (Onurlu Müşteri Kaybı Sonrası):
├── Çağrı: Kadıköy → Taksim (8.5 km, tahmini 167 TL)
├── Yolcu bindi, 500 metre sonra inmek istedi
├── ÖDENECEK: 167 TL (tam taahhüt edilen mesafe!)
├── Yolcu 500 metre gitse bile tam ücret öder
└── Sebep: Yolcu taahhüt sistemini kötüye kullanmıştır
```

### 14.6 Onurlu Müşteri Puanı ve Statü Detayları

```yaml
Onurlu Müşteri Puanı (0-100):
  Başlangıç: 100 (yeni her yolcu)
  
  Puan Kırma:
    - Her erken inme hakkı kullanımı: -5 puan
    - Yıl içinde 3. ay erken inme: -30 puan (statü kaybı tetiklenir)
    - Her ek erken inme (4. ay+): -10 puan
  
  Puan Kazanma:
    - Kesintisiz 6 ay erken inmesiz: +20 puan
    - Her tamamlanmış yolculuk: +1 puan (günde max 5)
    - 100 yolculuk tamamlama: +10 puan
  
  Statü Seviyeleri:
    - 80-100: Onurlu Müşteri ✅ — Ayda 1 erken inme hakkı var
    - 50-79: Standart Müşteri ⚠️ — Ayda 1 erken inme hakkı var
    - 0-49: Güvensiz Müşteri ❌ — Erken inme hakkı YOK, taahhüt ücreti ÖDEMEK ZORUNDA

  Statü Geri Kazanma:
    - Güvensiz → Standart: 6 ay erken inmesiz + puan 50+ olduğunda
    - Standart → Onurlu: 12 ay erken inmesiz + puan 80+ olduğunda
```

### 14.7 Yolcu Uyarı ve Bilgilendirme Sistemi

```
ERKEN İNME ANINDA:
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️ ERKEN İNME UYARISI                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Sayın Ahmet Yılmaz,                                            │
│                                                                 │
│  Taksim yerine Beşiktaş'ta inmek istediniz.                     │
│                                                                 │
│  Bu ay erken inme hakkınız: 1/1 (KULLANDINIZ)                   │
│  Bu yıl erken inme yaptığınız ay: 2 (Mart, Mayıs)              │
│                                                                 │
│  ⚠️ Yıl içinde 3. ay erken inme yaparsanız:                    │
│     "Onurlu Müşteri" statünüzü kaybeder ve                      │
│     taahhüt ettiğiniz mesafenin tamamını ödemek zorunda         │
│     kalırsınız.                                                 │
│                                                                 │
│  ✅ BUGÜNKÜ ÖDEME: Sadece Beşiktaş'a kadar (5.2 km) = 102 TL  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 14.8 Yeni Veritabanı Tablosu

```sql
-- Müşteri taahhüt ve onurlu müşteri takibi
CREATE TABLE customer_commitment_tracking (
    id                  UUID PRIMARY KEY,
    user_id             UUID REFERENCES users(id) UNIQUE,
    
    -- Onurlu Müşteri Puanı
    honorable_score     INTEGER DEFAULT 100 CHECK(honorable_score BETWEEN 0 AND 100),
    honorable_status    VARCHAR(30) DEFAULT 'honorable',  -- honorable, standard, untrusted
    status_changed_at   TIMESTAMP,
    
    -- Erken İnme İstatistikleri
    early_drop_current_month INTEGER DEFAULT 0,           -- Bu ay kullanılan erken inme
    early_drop_monthly_reset DATE,                        -- Sıfırlanma tarihi (ayın 1'i)
    early_drop_months       JSONB DEFAULT '[]',           -- ["2026-01", "2026-03", "2026-05"]
    early_drop_total        INTEGER DEFAULT 0,            -- Toplam erken inme sayısı
    
    -- Ceza Durumu
    is_penalized        BOOLEAN DEFAULT FALSE,            -- Taahhüt ücreti ödeme zorunluluğu var mı?
    penalty_until       DATE,                             -- Ceza bitiş tarihi (null = kalıcı)
    penalized_at        TIMESTAMP,
    
    -- İstatistikler
    total_trips         INTEGER DEFAULT 0,
    completed_trips     INTEGER DEFAULT 0,
    consecutive_months_clean INTEGER DEFAULT 0,           -- Kesintisiz temiz ay
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 14.9 API Endpoint'leri

```
GET    /api/v1/taxi/customer/status           # Onurlu müşteri durumu
GET    /api/v1/taxi/customer/history          # Erken inme geçmişi
GET    /api/v1/taxi/customer/monthly-rights   # Kalan aylık haklar
```

---

## 15. PAYLAŞIMLI YOLCULUK VE ÇOKLU YOLCU SİSTEMİ

### 15.1 Temel Kural: Grup ile Biniş

Bir müşteri, **kendisi dahil 3 veya daha fazla kişi** ile taksiye bindiğinde (yani 1'den fazla ek yolcu), bu yolculuk **"Paylaşımlı Yolculuk"** statüsüne geçer. Bu statü, taksicinin rota boyunca diğer müşterileri de almasına izin verir.

```
GRUP BİNİŞİ:
├── Müşteri: 1 kişi + 2+ arkadaş/aile = TOPLAM 3+ KİŞİ
├── Çağrı: Kadıköy → Taksim
├── Statü: PAYLAŞIMLI YOLCULUK
├── Taksici, Kadıköy → Taksim rotasında
│   diğer müşterileri alabilir
└── Bu hak, belirlenen rotanın SONUNA KADAR devam eder
```

### 15.2 Taksicinin Yolcu Alma Yetkisi

Yolculuk paylaşımlı statüde olduğunda, taksici **belirlenen rota üzerinde** diğer müşterileri alma hakkına sahiptir. Bu yetki **rota sonuna kadar** devam eder.

```
TAKSİCİ YETKİSİ:
├── Rota: Kadıköy → Taksim (E-5 karayolu)
│
├── Yetki 1: Kadıköy'den sonra gelen yolcuları alabilir
│   └── Örnek: Bostancı'da bir yolcu alır
│
├── Yetki 2: Zincirlikuyu'da başka yolcu alabilir
│
├── Yetki 3: Taksim'e kadar her noktada yolcu alabilir
│
└── SINIR: Taksim'e varıldığında yetki biter
    └── Yeni yolcular için yeni çağrı gereklidir
```

### 15.3 Grup Müşterinin Erken İnme Durumu

Paylaşımlı yolculukta grup müşteri erken inmek isterse:

```
DURUM 1: Grup erken iner, taksici rotaya devam eder
├── Grup: Kadıköy → Taksim çağırdı
├── Grup Beşiktaş'ta indi (erken inme)
├── Taksici, diğer yolcularla Taksim'e devam eder
├── Ödeme için grup: Erken inme kuralları geçerli
│   └── (bkz. Bölüm 14 - aylık hak, puan vs.)
└── Taksici: Yolcu kaybı yok, diğer yolcularla devam

DURUM 2: Tüm yolcular erken iner
├── Yolculuk sonlanır
└── Yeni yolcular için yeni çağrı gereklidir
```

### 15.4 Ücretlendirme Modeli

Paylaşımlı yolculukta her yolcu grubu **kendi bindiği noktadan indiği noktaya kadar** olan mesafe için ücretlendirilir.

```
ÜCRETLENDİRME ÖRNEĞİ:
├── Rota: Kadıköy → Taksim (8.5 km)
│
├── Grup A (Asıl çağıran): Kadıköy → Beşiktaş (5.2 km)
│   └── Öder: 5.2 km ücreti (grup toplamı / grup kişi sayısı)
│
├── Yolcu B: Bostancı → Taksim (6.0 km)
│   └── Öder: 6.0 km ücreti
│
├── Yolcu C: Zincirlikuyu → Taksim (2.1 km)
│   └── Öder: 2.1 km ücreti
│
└── Toplam Taksi Geliri: 5.2 + 6.0 + 2.1 = 13.3 km ücreti
```

### 15.5 Paylaşımlı Yolculuk Akışı

```
ÇAĞRI ANI:
├── Yolcu gideceği yeri girer
├── Yolcu "Yolcu Sayısı" seçer: 1 / 2 / 3 / 4+
│
├── EĞER yolcu sayısı ≥ 3 İSE:
│   ├── Sistem: "Bu yolculuk paylaşımlı olacaktır.
│   │   Taksici rota boyunca diğer yolcuları alabilir."
│   ├── Yolcu onaylar → Paylaşımlı statü aktif
│   └── Fiyat: Standart (paylaşımsız) fiyatın %70'i
│       (grup avantajı)
│
├── YOLCULUK SIRASINDA:
│   ├── Taksi uygulaması, rotadaki diğer yolculara
│   │   "Paylaşımlı taksi müsait" bildirimi gönderir
│   ├── İlgili yolcular çağrı yapar
│   ├── Taksici onaylar/durur ve alır
│   └── Sistem her yolcu için ayrı ücret hesaplar
│
└── YOLCULUK SONU:
    ├── Her yolcu kendi mesafesi kadar öder
    ├── Asıl çağıran grup: Erken inme kuralları geçerli
    └── Tüm ödemeler sistem üzerinden otomatik
```

### 15.6 Kısıtlamalar ve Kurallar

```yaml
Paylaşımlı Yolculuk Kuralları:
  Aktif Olma Şartı:
    - Asıl çağıran müşteri grubu ≥ 3 kişi olmalı
    - Araçta yeterli koltuk olmalı (4+1 veya 5+1)
  
  Taksici Yolcu Alma:
    - Sadece belirlenen rota üzerinde
    - Rota sonuna kadar geçerli
    - Taksici reddetme hakkına sahip (puan cezasız)
      - Sebep: "Araç kapasitesi dolu"
      - Sebep: "Rota dışı"
  
  Yolcu Hakları (Asıl Çağıran):
    - Gruptan biri erken inebilir (kalanlar devam eder)
    - Tüm grup erken inebilir (aylık hak + puan kuralları geçerli)
    - Paylaşımlı statüyü reddedemez (çağrı anında kabul etmiştir)
  
  Yolcu Hakları (Sonradan Binen):
    - Sadece bindiği noktadan itibaren ücret öder
    - Nerede ineceğini taahhüt eder
    - Erken inme hakkı: aylık hakları geçerli
```

### 15.7 Yeni Veritabanı Tablosu

```sql
-- Yolculuktaki yolcu gruplarını takip eder
CREATE TABLE trip_passengers (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    
    -- Yolcu / Grup Bilgisi
    passenger_type      VARCHAR(30) NOT NULL,  -- primary_group, additional
    group_size          INTEGER DEFAULT 1,      -- Gruptaki kişi sayısı
    is_primary          BOOLEAN DEFAULT FALSE,  -- Asıl çağıran mı?
    
    -- Biniş-İniş Bilgisi
    pickup_location     GEOGRAPHY(POINT),
    pickup_address      TEXT,
    dropoff_location    GEOGRAPHY(POINT),
    dropoff_address     TEXT,
    distance_km         NUMERIC(5,2),           -- Bu yolcunun mesafesi
    fare_amount         NUMERIC(10,2),          -- Bu yolcunun ücreti
    
    -- Ödeme Durumu
    payment_status      VARCHAR(30) DEFAULT 'pending',  -- pending, blocked, captured, refunded
    payment_id          UUID REFERENCES payments(id),
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- Paylaşımlı yolculuk ayarları
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    is_shared           BOOLEAN DEFAULT FALSE;
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    total_passengers    INTEGER DEFAULT 1;
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    primary_group_size  INTEGER DEFAULT 1;
```

### 15.8 API Endpoint'leri

```
POST   /api/v1/taxi/trip/{tripId}/passenger          # Yeni yolcu ekle (paylaşımlı)
GET    /api/v1/taxi/trip/{tripId}/passengers          # Yolculuktaki tüm yolcular
GET    /api/v1/taxi/nearby/shared                     # Yakındaki paylaşımlı taksiler
POST   /api/v1/taxi/trip/{tripId}/join               # Paylaşımlı taksiye katıl
```

---

## 16. BAŞKASINA TAKSİ GÖNDERME (HEDİYE YOLCULUK) SİSTEMİ

### 16.1 Temel Konsept

Bir müşteri, **kendisi gitmeden** bir tanıdığı için taksi çağırabilir. Müşteri:
- Taksiyi **kendisi çağırır** (kendi hesabından)
- **Gideceği rotayı belirler** (alış noktası → bırakış noktası)
- **Ücreti kendisi öder**
- Yolcu (tanıdık) sadece **biner ve iner**

```
HEDİYE YOLCULUK:
┌──────────────────────────────────────────────────┐
│  ÖDEYEN (Ali)  ───→  SİSTEM  ───→  YOLCU (Ayşe) │
│  ─ Çağrıyı yapar      ─ SMS/App      ─ Biner     │
│  ─ Rotayı girer       ─ Bildirim     ─ Gider     │
│  ─ Ücreti öder        ─ Eşleştirme   ─ İner      │
└──────────────────────────────────────────────────┘
```

### 16.2 Kullanım Senaryoları

```
SENARYO 1: Aile içi
├── Baba (ödeyen), çocuğu için taksi çağırır
├── Okul → Eve rotası
├── Çocuk sadece biner ve iner
└── Ödeme: Baba'nın cüzdanından

SENARYO 2: Firma / Kurum
├── Şirket (ödeyen), misafiri/müşterisi için taksi çağırır
├── Havalimanı → Otel rotası
├── Misafir sadece biner ve iner
└── Ödeme: Şirket hesabından (Kurumsal Hesap)

SENARYO 3: Arkadaş / Tanıdık
├── Arkadaş (ödeyen), başka bir arkadaşı için taksi çağırır
├── Ona özel sürpriz / yardım amaçlı
├── Yolcu sadece biner ve iner
└── Ödeme: Çağıranın cüzdanından
```

### 16.3 Çağrı Süreci

```
ÇAĞRI AKIŞI:
├── Ödeyen "Başkası İçin Taksi Çağır" seçeneğini seçer
│
├── ADIM 1: Yolcu Bilgileri
│   ├── Yolcu adı soyadı (zorunlu)
│   ├── Yolcu telefon numarası (zorunlu)
│   └── Not: Yolcunun üye olması gerekmez
│
├── ADIM 2: Rota Bilgileri
│   ├── Alış noktası (yolcunun bulunduğu yer)
│   ├── Bırakış noktası (gidilecek yer)
│   └── Sistem fiyat tahminini gösterir
│
├── ADIM 3: Ödeme Onayı
│   ├── Ödeyen fiyatı görür
│   ├── Ödeyen "Onayla ve Gönder" butonuna basar
│   ├── Tutar ödeyenin cüzdanında bloke edilir
│   └── Çağrı sisteme düşer
│
└── ADIM 4: Eşleşme ve Bildirim
    ├── Sistem en yakın müsait taksiciyi eşleştirir
    ├── Yolcuya SMS / App bildirimi gider:
    │   "Ayşe Hanım, Ali sizin için taksi çağırdı.
    │    Araç: 34 ABC 123, Şöför: Mehmet Yılmaz
    │    Sizi şuradan alacak: [konum]
    │    Gideceğiniz yer: [adres]"
    └── Taksiciye bildirim:
        "Yolcu: Ayşe (Ali adına çağrıldı)
         Alış: [konum], Bırakış: [adres]"
```

### 16.4 Yolcu (Binici) Deneyimi

```
YOLCU AKIŞI (uygulamasız yolcu):
├── SMS alır: "Ali sizin için taksi çağırdı"
├── SMS içinde:
│   ├── Taksi plakası ve modeli
│   ├── Şöför adı ve fotoğrafı (link)
│   ├── Canlı takip linki (aracı görebilir)
│   └── Tahmini varış süresi
│
├── Yolcu bekleme noktasına gider
│
├── Taksi gelir, yolcu biner
│
├── Yolculuk başlar
│   └── Yolcu rota değişikliği yapamaz (ödeyen belirledi)
│       └── İstisna: Acil durumda şöför ile iletişim
│
└── Yolculuk biter, yolcu iner
    └── Ödeme ile ilgili hiçbir işlem yapmaz
```

### 16.5 Ödeme ve Faturalama

```
ÖDEME DETAYLARI:
├── Ödeyen: Çağrı anında ücret bloke edilir
├── Bloke tutar: Tahmini ücret + %10 güvenlik marjı
│
├── Yolculuk TAMAMLANIRSA:
│   ├── Gerçek ücret hesaplanır
│   ├── Tahmini ücret > Gerçek ücret → fark iade
│   ├── Tahmini ücret < Gerçek ücret → fark blokeden çekilir
│   └── Ödeyene e-posta/SMS ile makbuz:
│       "Ali, Ayşe için çağırdığınız taksi yolculuğu tamamlandı.
│        Rota: [alış] → [bırakış]
│        Tutar: 187 TL
│        Kalan bakiye: 1.250 TL"
│
├── Yolculuk İPTAL EDİLİRSE:
│   ├── Yolcu binmeden iptal → tam iade
│   ├── Yolcu bindikten sonra iptal → kısmi iade
│   └── İptal sebebi ödeyene bildirilir
│
└── Fatura:
    ├── Bireysel ödeyen: Ödeme kanıtı e-posta ile
    ├── Kurumsal ödeyen: e-Fatura (Kurumsal Hesap ile)
    └── Fatura kesilen: Ödeyen (yolcu değil)
```

### 16.6 Kısıtlamalar ve Kurallar

```yaml
Hediye Yolculuk Kuralları:
  Ödeyen (Çağıran):
    - Geçerli bir hesabı olmalı (Bireysel veya Kurumsal)
    - Yeterli bakiyesi veya tanımlı kartı olmalı
    - Günde max 5 hediye yolculuk gönderebilir
    - Ayda max 20 hediye yolculuk gönderebilir
    - Yolculuk sırasında rota değişikliği talebinde bulunamaz
    - Yolculuğu ancak yolcu BİNMEDEN iptal edebilir
  
  Yolcu (Binici):
    - Üye olması gerekmez (telefon numarası yeterli)
    - Ödeme yapmaz
    - Rota değişikliği yapamaz
    - Erken inme hakkı: Standart kurallar geçerli
      - Ancak erken inme durumunda ödeyen bilgilendirilir
      - Erken inme puanı: YOLCU'ya işlenir (ödeyene değil)
    
  Şöför:
    - Yolcunun ödeyen adına geldiğini bilir
    - Yolcuya "Ali adına" olduğunu teyit eder
    - Standart yolcu haklarına sahiptir
    - Yolcu binmezse: iptal, ödeyene iade
```

### 16.7 Veritabanı Değişiklikleri

```sql
-- Mevcut taxi_trips tablosuna ek alanlar
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    trip_type           VARCHAR(30) DEFAULT 'self',  -- self, gift
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    payer_id            UUID REFERENCES users(id);  -- Ödeyen (kendisi için çağırdıysa = passenger)
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    passenger_name      VARCHAR(150);               -- Yolcu adı (üye değilse)
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    passenger_phone     VARCHAR(20);                -- Yolcu telefon
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    passenger_note      TEXT;                       -- Ödeyenin notu (isteğe bağlı)

-- Hediye yolculuk log tablosu
CREATE TABLE taxi_gift_rides (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id) UNIQUE,
    
    -- Ödeyen Bilgisi
    payer_id            UUID REFERENCES users(id) NOT NULL,
    payer_type          VARCHAR(30) DEFAULT 'bireysel',  -- bireysel, kurumsal
    
    -- Yolcu Bilgisi
    passenger_id        UUID REFERENCES users(id),        -- Üyeyse (nullable)
    passenger_name      VARCHAR(150) NOT NULL,
    passenger_phone     VARCHAR(20) NOT NULL,
    passenger_email     VARCHAR(255),                     -- İsteğe bağlı (makbuz için)
    
    -- Çağrı Detayları
    caller_note         TEXT,                             -- "Kızımı okuldan alıp eve bırakır mısın?"
    pickup_instruction  TEXT,                             -- "Beyaz bina önü, zil:3"
    
    -- İptal / İade
    cancel_reason       TEXT,
    refund_amount       NUMERIC(10,2),
    refund_status       VARCHAR(30) DEFAULT 'none',       -- none, pending, completed
    
    -- Zaman Bilgisi
    called_at           TIMESTAMP DEFAULT NOW(),
    trip_started_at     TIMESTAMP,
    trip_completed_at   TIMESTAMP,
    cancelled_at        TIMESTAMP,
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_gift_rides_payer ON taxi_gift_rides(payer_id);
CREATE INDEX idx_gift_rides_passenger_phone ON taxi_gift_rides(passenger_phone);
```

### 16.8 API Endpoint'leri

```
POST   /api/v1/taxi/gift/create                  # Hediye yolculuk çağır
GET    /api/v1/taxi/gift/list                     # Gönderdiğim hediye yolculuklar
GET    /api/v1/taxi/gift/{giftId}                 # Hediye yolculuk detayı
POST   /api/v1/taxi/gift/{giftId}/cancel          # Hediye yolculuğu iptal et (binmeden)
GET    /api/v1/taxi/gift/received                 # Adıma çağrılan yolculuklar
GET    /api/v1/taxi/gift/passenger/{phone}        # Telefon ile hediye sorgula (sms link)
POST   /api/v1/taxi/gift/{giftId}/rate            # Yolcu, hediye yolculuğu puanla
```

### 16.9 Güvenlik ve Doğrulama

```
DOĞRULAMA ADIMLARI:
├── Çağrı Anında:
│   ├── Ödeyenin kimliği doğrulanır (2FA opsiyonel)
│   ├── Limit kontrolü (günlük/aylık maksimum)
│   └── Bakiye / kart kontrolü
│
├── Yolcu Teslim Anında:
│   ├── Şöför, yolcuya adını sorar:
│   │   "Ayşe Hanım mısınız? Ali Bey sizin için çağırdı."
│   ├── Yolcu adını doğrular
│   ├── Şöför uygulamada "Yolcu Teslim Alındı" butonuna basar
│   └── Yolculuk başlar
│
├── SMS Doğrulama (opsiyonel):
│   ├── Yolcuya SMS ile 6 haneli kod gönderilir
│   ├── Yolcu kodu şöföre söyler
│   └── Şöför kodu uygulamaya girer → yolculuk başlar
│
└── Güvenlik Uyarıları:
    └── Şöför, yolcu adı/telefonu uyuşmazsa destek ekibine bildirir
```

### 16.10 Bildirim Şablonları

```
YOLCUYA SMS:
┌──────────────────────────────────────────────┐
│  🚕 Taksi Yolculuğunuz Hazır!               │
│                                              │
│  Merhaba Ayşe,                              │
│  Ali sizin için taksi çağırdı! 🎁           │
│                                              │
│  📍 Alış: Bağdat Cad. No:123, Kadıköy       │
│  📍 Bırakış: Taksim Meydanı                 │
│                                              │
│  🚗 Plaka: 34 ABC 123                       │
│  👤 Şöför: Mehmet Yılmaz                    │
│  ⭐ Şöför Puanı: 4.8                        │
│                                              │
│  🔗 Takip Linki: taksim.com/track/ABC123    │
│  ⏱ Tahmini Varış: 4 dakika                 │
│                                              │
│  Ödeme: Ali tarafından yapıldı ✅           │
│  Sadece binin ve keyfini çıkarın!           │
└──────────────────────────────────────────────┘

ÖDEYENE BİLDİRİM:
┌──────────────────────────────────────────────┐
│  ✅ Taksi Yolculuğu Tamamlandı              │
│                                              │
│  Merhaba Ali,                               │
│  Ayşe için çağırdığın yolculuk bitti.       │
│                                              │
│  📍 Rota: Kadıköy → Taksim (8.5 km)         │
│  💰 Tutar: 167 TL                           │
│  ⭐ Yolcu Puanı: 5.0                        │
│                                              │
│  Makbuz: taksim.com/receipt/ABC123          │
└──────────────────────────────────────────────┘
```

---

## 17. KONFOR TERCİH VE BAHŞİŞ SİSTEMİ

### 17.1 Puan = Konfor Seviyesi

Sistemdeki tüm puanlar doğrudan **konfor seviyesini** ifade eder. Yüksek puan = yüksek konfor.

```
PUAN - KONFOR EŞLEŞMESİ:
├── 10/10: 🏆 VIP Konfor — Sıfır kusur, lüks deneyim
├── 9/10:  🥇 Mükemmel Konfor
├── 8/10:  🥈 Çok İyi Konfor
├── 7/10:  🥉 İyi Konfor
├── 6/10:  👍 Orta-İyi Konfor
├── 5/10:  ➡️ Standart Konfor (ortalama taksi)
├── 4/10:  👎 Düşük Konfor
├── 3/10:  ❌ Kötü Konfor
├── 2/10:  ❌❌ Çok Kötü
└── 1/10:  ⛔ Berbat

KOMBİNE PUAN → KONFOR ETİKETİ:
├── 4.5 - 5.0 ⭐ → ⭐⭐⭐⭐⭐ Premium Konfor
├── 4.0 - 4.4 ⭐ → ⭐⭐⭐⭐ İyi Konfor
├── 3.0 - 3.9 ⭐ → ⭐⭐⭐ Standart
├── 2.0 - 2.9 ⭐ → ⭐⭐ Düşük Konfor
└── 1.0 - 1.9 ⭐ → ⭐ Kaçınılmalı
```

### 17.2 Konforlu Taksi / Şöför Tercihi

Müşteri, çağrı yaparken **minimum konfor seviyesi** belirleyebilir. Ayrıca araç **marka, model ve yakıt tipine** göre de filtreleme yapabilir.

```
ÇAĞRI EKRANI:
┌──────────────────────────────────────────────┐
│  📍 Nereye gidiyorsunuz?                     │
│  ┌──────────────────────────────────┐        │
│  │ Taksim Meydanı                   │        │
│  └──────────────────────────────────┘        │
│                                              │
│  🚗 ARAÇ TERCİHİ (opsiyonel)                 │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │ Marka: [ Tümü ▼ ]               │        │
│  │ ─────────────────────────────── │        │
│  │  ☐ Tüm Markalar                  │        │
│  │  ☐ Renault                       │        │
│  │  ☐ Toyota                        │        │
│  │  ☐ Volkswagen                    │        │
│  │  ☐ Hyundai                       │        │
│  │  ☐ Fiat                          │        │
│  │  ☐ Mercedes-Benz                 │        │
│  │  ☐ Diğer                         │        │
│  └──────────────────────────────────┘        │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │ Yakıt Tipi: [ Tümü ▼ ]          │        │
│  │ ─────────────────────────────── │        │
│  │  ☐ ⛽ Benzinli                   │        │
│  │  ☐ ⛽ Dizel (Mazotlu)            │        │
│  │  ☐ ⛽ LPG'li (Tüplü)             │        │
│  │  ☐ ⚡ Elektrikli                 │        │
│  │  ☐ 🔋 Hibrit (Benzin+Elektrik)  │        │
│  └──────────────────────────────────┘        │
│                                              │
│  ⭐ KONFOR TERCİHİ (opsiyonel)               │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │  ☐ Farketmez (en hızlı taksi)    │        │
│  │  ☐ ⭐⭐⭐ İyi Konfor (4.0+)      │        │
│  │  ☐ ⭐⭐⭐⭐ Premium (4.5+)       │        │
│  │  ☐ ⭐⭐⭐⭐⭐ VIP (5.0)          │        │
│  └──────────────────────────────────┘        │
│                                              │
│  👤 ŞÖFÖR TERCİHİ (opsiyonel)                │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │  Cinsiyet: [ Farketmez ▼ ]      │        │
│  │ ─────────────────────────────── │        │
│  │  ☐ Farketmez                     │        │
│  │  ☐ 👩 Kadın Şöför                │        │
│  │  ☐ 👨 Erkek Şöför                │        │
│  └──────────────────────────────────┘        │
│                                              │
│  🎯 Seçtiğiniz kriterlerde taksi             │
│     bulunamazsa bahşiş ile çağırabilirsiniz! │
│                                              │
│  [ TAKSİ ÇAĞIR ]                             │
└──────────────────────────────────────────────┘
```

Araç marka/model/yakıt bilgisi, müşterinin eşleştiği taksi ekranında da gösterilir:

```
EŞLEŞEN TAKSI EKRANI:
┌──────────────────────────────────────────────┐
│  🚗 TAKSİNİZ YOLDA                           │
│                                              │
│  🚗 34 TAK 5678                              │
│  ├─ Marka/Model: Renault Megane              │
│  ├─ Yıl: 2023                                │
│  ├─ Yakıt: Dizel                             │
│  ├─ Renk: Beyaz                              │
│  └─ ⭐ Kombine Puan: 4.6                     │
│                                              │
│  👤 Şöför: Mehmet Yılmaz  👨                │
│  ├─ ⭐ Şöför Puanı: 4.8                      │
│  └─ 📷 [Profil Fotoğrafı]                    │
│                                              │
│  📍 1.2 km uzaklıkta  |  ⏱ 3 dk            │
│                                              │
│  [ İPTAL ]    [ TAKİP ET ]                   │
└──────────────────────────────────────────────┘
```

### 17.3 Bahşiş Protokolü

Müşteri belirli bir konfor seviyesinde taksi bulamazsa veya çok beklemek istemezse, **bahşiş teklifi** yaparak taksiyi teşvik edebilir.

```
BAHŞİŞ PROTOKOLÜ AKIŞI:
├── Müşteri konfor tercihi yapar (örn: Premium 4.5+)
│
├── EŞLEŞME 1: Normal eşleşme dener
│   ├── Premium taksiler meşgulse → eşleşme olmaz
│   └── Sistem: "Bu seviyede taksi bulunamadı"
│
├── EŞLEŞME 2: Bahşiş teklifi ekranı
│   └── Müşteriye sorulur: "Bahşiş ekleyerek çağırmak ister misiniz?"
│
├── Müşteri bahşiş teklifini girer:
│   ┌──────────────────────────────────────────┐
│   │  💰 BAHŞİŞ EKLE                          │
│   │                                          │
│   │  Premium taksiler şu an meşgul.          │
│   │  Bahşiş ekleyerek öncelik kazanın!      │
│   │                                          │
│   │  Ekstra teklifiniz:                      │
│   │  ┌──────────────────────────────────┐    │
│   │  │ 50 TL       [ ✓ En Popüler]     │    │
│   │  │ 100 TL      [ ★ En İyi Değer]   │    │
│   │  │ 150 TL      [ ⚡ En Hızlı]      │    │
│   │  │ Özel: [________________] TL     │    │
│   │  └──────────────────────────────────┘    │
│   │                                          │
│   │  "Seni bekliyorum, gelirsen 50 TL       │
│   │   fazla vereceğim."                      │
│   │                                          │
│   │  [ BAHŞİŞ İLE ÇAĞIR ]                   │
│   └──────────────────────────────────────────┘
│
├── Bahşişli çağrı tüm müsait taksilere gider:
│   └── "Kadıköy → Taksim | +50 TL bahşiş | Premium tercih"
│
├── Taksici kabul ederse:
│   ├── Bahşiş tutarı bloke edilir (normal ücrete ek)
│   ├── Taksi yönlendirilir
│   └── Müşteriye bildirim: "Taksi bulundu! +50 TL bahşiş ile"
│
└── Yolculuk bitince:
    ├── Normal ücret + bahşiş otomatik çekilir
    ├── Bahşiş direkt şöföre aktarılır (sistem kesintisiz)
    └── Makbuz: "Ücret: 167 TL + Bahşiş: 50 TL = 217 TL"
```

### 17.4 Bahşiş Tipleri ve Limitler

```yaml
Bahşiş Protokolü Kuralları:
  Bahşiş Tipleri:
    - Zamanlı Bahşiş: "Gelirsen +50 TL" (standart)
    - Konfor Bahşişi: "Premium şöför arıyorum +100 TL"
    - Acil Bahşiş: "Hemen gelsin +150 TL"
    - Özel Bahşiş: Müşterinin girdiği tutar

  Limitler:
    - Minimum bahşiş: 10 TL
    - Maksimum bahşiş: 500 TL (güvenlik)
    - Maksimum bahşiş / oran: Normal ücretin %50'sini geçemez
    - Günlük max bahşiş harcaması: 1.000 TL

  Taksici Kabulü:
    - Taksici bahşiş teklifini görür ve kabul/red eder
    - Reddetme cezasız (bahşişli çağrıda)
    - Bahşiş: Normal ücrete ek, sistem komisyonu sadece normal ücretten

  İptal Durumu:
    - Müşteri iptal ederse: Bahşiş iade edilir
    - Taksici iptal ederse: Bahşiş iade + müşteriye 20 TL kupon
    - Yolcu binmezse: Bahşişin %50'si taksiciye kalır (bekleme tazminatı)
```

### 17.5 Bahşişin Puana Etkisi

```
BAHŞİŞ - PUAN İLİŞKİSİ:
├── Bahşiş alan şöför: Ek teşvik (puan etkisi yok)
│
├── Müşteri bahşiş verdiyse:
│   ├── "Bahşişli müşteri" rozeti kazanır
│   ├── Bir sonraki çağrıda öncelikli eşleşme
│   └── Taksiciler bahşiş veren müşterileri daha çok tercih eder
│
└── Sistem:
    ├── Bahşişten KDV alınmaz (doğrudan şöför geliri)
    ├── Sistem komisyonu sadece normal ücrete uygulanır
    └── Bahşişler kayıt altına alınır (vergi beyanı için)
```

### 17.6 Veritabanı

```sql
-- taxi_trips tablosuna bahşiş alanı
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    tip_amount          NUMERIC(10,2) DEFAULT 0;     -- Bahşiş tutarı
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    tip_status          VARCHAR(30) DEFAULT 'none';   -- none, offered, accepted, paid, refunded
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    comfort_preference  VARCHAR(30);                  -- Any, Good, Premium, VIP
ALTER TABLE taxi_trips ADD COLUMN IF NOT EXISTS
    comfort_min_score   NUMERIC(2,1);                 -- Min kombine puan (örn: 4.0)

-- Bahşiş teklifleri tablosu
CREATE TABLE taxi_tip_offers (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    
    customer_id         UUID REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    offered_amount      NUMERIC(10,2) NOT NULL,       -- Teklif edilen bahşiş
    tip_type            VARCHAR(30) NOT NULL,          -- time, comfort, urgent, custom
    tip_note            TEXT,                          -- "Seni bekliyorum, gelirsen 50 TL fazla"
    
    status              VARCHAR(30) DEFAULT 'offered', -- offered, accepted, rejected, paid, refunded
    responded_at        TIMESTAMP,
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tip_offers_trip ON taxi_tip_offers(trip_id);
CREATE INDEX idx_tip_offers_customer ON taxi_tip_offers(customer_id);

-- Müşteri bahşiş istatistiği
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    total_tips_given    NUMERIC(12,2) DEFAULT 0;      -- Toplam verilen bahşiş
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    tip_tier            VARCHAR(30) DEFAULT 'none';    -- none, tipper, big_tipper, whale
```

### 17.7 API Endpoint'leri

```
POST   /api/v1/taxi/search?comfort=4.5                         # Konfor tercihi ile ara
POST   /api/v1/taxi/search?brand=Renault&fuel=diesel&gender=male  # Marka/yakıt/cinsiyet filtreli ara
POST   /api/v1/taxi/trip/{tripId}/tip                  # Bahşiş teklifi yap
GET    /api/v1/taxi/trip/{tripId}/tip-status           # Bahşiş durumu
PUT    /api/v1/taxi/trip/{tripId}/tip/accept           # Taksici bahşişi kabul et
PUT    /api/v1/taxi/trip/{tripId}/tip/reject           # Taksici bahşişi reddet
GET    /api/v1/taxi/driver/tip-history                 # Taksici bahşiş geçmişi
GET    /api/v1/taxi/customer/tip-history               # Müşteri bahşiş geçmişi
```

### 17.8 Şöförler İçin Kalite Teşvik Mekanizması

Bu sistem, şöförlerde **"kaliteli olma isteği"** uyandırmak için tasarlanmıştır. Yüksek puan = yüksek kazanç dengesi doğal bir motivasyon oluşturur.

```
TEŞVİK ZİNCİRİ:
├── 1️⃣ Şöför puanını yükseltir
│   ├── Daha iyi sürüş (7.9)
│   ├── Daha saygılı davranış (7.10)
│   ├── Güler yüz (7.15)
│   ├── İkram (7.13)
│   └── Trafik kurallarına uyum (7.17)
│
├── 2️⃣ Yüksek puan = Yüksek konfor etiketi
│   └── 4.5+ ⭐ → Premium, 5.0 → VIP
│
├── 3️⃣ Premium/VIP etiketi = Daha fazla müşteri tercihi
│   └── Müşteriler "Konforlu Taksi" filtrelerini kullanır
│
├── 4️⃣ Yüksek talep = Bahşiş teklifleri
│   └── "Gelirsen +50 TL" → Şöför ekstra kazanır
│
└── 5️⃣ 👑 KALİTELİ ŞÖFÖR = DAHA FAZLA KAZANÇ
    ├── Normal ücret + Bahşiş
    ├── Daha az reddedilme (müşteri sizi bekler)
    ├── Sadık müşteri kitlesi
    └── Sistemde üst sıralarda görünme
```

### 17.9 Dinamik Konfor Fiyatlandırması (Eğrisel Artış Modeli)

#### 17.9.1 Felsefe

Sistemde popüler olmuş konforlu taksilerin ve şöförlerin doğal bir **talep primi** oluşur. Bu prim **lineer değil, eğrisel (non-linear)** olarak artar. Müşteri her konfor seviyesi için farklı bir artış oranı görür ve kendi kalite tercihini yapar.

```
EĞRİSEL ARTış MANTIĞI:
├── Düşük konfor (3.0-3.9): %0 — %5   → Hemen hemen aynı
├── Orta konfor  (4.0-4.4): %10 — %25 → Hafif artış
├── Yüksek konfor (4.5-4.9): %30 — %60 → Belirgin sıçrama
└── VIP / Mükemmel (5.0):   %75 — %100 → Üstel yükseliş
```

#### 17.9.2 Eğrisel Fiyat Formülü

```
FİYAT ARTIŞ FORMÜLÜ:

P = Kombine Puan (0.0 — 5.0 arası)(şöför puanı × 0.6 + araç puanı × 0.4)
T = Tavan katsayısı (maksimum artış yüzdesi, şehre göre değişir)

Eğrisel artış f(P) = T × (e^(1.2 × P / 5) - 1) / (e^1.2 - 1)

ÖRNEK TABLO (T = %100):
├── P = 3.0 (Standart):    %0   (referans fiyat)
├── P = 3.5:               %5
├── P = 4.0 (İyi):        %12
├── P = 4.3:              %25
├── P = 4.5 (Premium):    %38
├── P = 4.7:              %55
├── P = 4.9:              %82
└── P = 5.0 (VIP):        %100

GRAFİKSEL GÖSTERİM:
Artış %
│
100% ┤                                    ● VIP
 82% ┤                               ●
 55% ┤                         ●
 38% ┤                    ● Premium
 25% ┤              ●
 12% ┤         ● İyi
  5% ┤    ●
  0% ┤●───●────●────●────●────●────●────●────●────●  Puan
     3.0  3.2  3.4  3.6  3.8  4.0  4.2  4.4  4.6  4.8  5.0
```

#### 17.9.3 Müşteri Seçim Ekranı

Müşteri çağrı ekranında her konfor seviyesi için **farklı fiyat artışını görür** ve kendi bütçesine göre seçim yapar.

```
KONFOR FİYATLANDIRMA EKRANI:
┌──────────────────────────────────────────────┐
│  📍 Kadıköy → Taksim                        │
│  ├─ Tahmini mesafe:  8 km                    │
│  └─ Normal ücret:  185 TL                   │
│                                              │
│  ⭐ KONFOR SEVİYENİZİ SEÇİN                  │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  ○ Standart       185 TL  (%0)    ⭐⭐⭐  ││
│  │  ○ İyi Konfor    207 TL  (+%12)  ⭐⭐⭐⭐ ││
│  │  ○ Premium       255 TL  (+%38)  ⭐⭐⭐⭐⭐││
│  │  ○ VIP ⚡        370 TL  (+%100) 👑      ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Seçiminize göre ücret güncellenir.          │
│  Daha yüksek konfor = daha kaliteli araç+   │
│  şöför kombinasyonu.                         │
│                                              │
│  [ BU KONFORLA ÇAĞIR ]                      │
└──────────────────────────────────────────────┘
```

#### 17.9.4 Çoklu Araç Karşılaştırma

Müşteri aynı anda **farklı araç + şöför çiftlerini** fiyatlarıyla görebilir ve seçim yapabilir.

```
KARŞILAŞTIRMA EKRANI:
┌──────────────────────────────────────────────┐
│  🚗 YAKINDAKİ UYGUN TAKSİLER                 │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ ⭐⭐⭐⭐  İyi Konfor     (+%12)           ││
│  │ 🚗 34 TAK 1234  ── Renault Megane       ││
│  │    ⛽ Dizel · 2023 · Beyaz               ││
│  │ 👤 Mehmet Y.  👨 4.2 ⭐                 ││
│  │ 💰 207 TL  |  📍 1.2 km  |  ⏱ 3 dk     ││
│  │ [ SEÇ ]                                   ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ ⭐⭐⭐⭐⭐ Premium         (+%38) 🔥      ││
│  │ 🚗 34 TAK 5678  ── Toyota Camry         ││
│  │    ⚡ Elektrikli · 2024 · Beyaz          ││
│  │ 👤 Ali K.  👨 4.8 ⭐                     ││
│  │ 💰 255 TL  |  📍 2.5 km  |  ⏱ 5 dk     ││
│  │ [ SEÇ ]  ★ POPÜLER                       ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ ⭐⭐⭐⭐  İyi Konfor     (+%12)           ││
│  │ 🚗 34 TAK 4321  ── Fiat Egea            ││
│  │    ⛽ LPG'li · 2022 · Gri                ││
│  │ 👤 Ayşe K.  👩 4.6 ⭐                   ││
│  │ 💰 207 TL  |  📍 1.8 km  |  ⏱ 4 dk     ││
│  │ [ SEÇ ]  ⚡ Kadın Şöför                  ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ 👑 VIP Concierge          (+%100)        ││
│  │ 🚗 34 TAK 9999  ── Mercedes EQS        ││
│  │    ⚡ Elektrikli · 2025 · Siyah          ││
│  │ 👤 Ahmet S.  👨 5.0 ⭐                  ││
│  │ 💰 370 TL  |  📍 3.0 km  |  ⏱ 6 dk     ││
│  │ [ SEÇ ]  🔥 Sistemdeki en iyi eşleşme   ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ⚠️ Popüler araçların fiyatı talebe göre    │
│     anlık değişebilir.                       │
└──────────────────────────────────────────────┘
```

#### 17.9.5 VIP Concierge (En Yüksek Kademe)

VIP Concierge seviyesi, sistemdeki **en yüksek puanlı şöför + araç çiftlerine** aittir. Bu seviyeye ulaşmak için:

```yaml
VIP Concierge Eşikleri:
  Şöför:
    - Kombine puan: 4.9+ (11 boyutun tümünde 9+)
    - En az 500 tamamlanmış yolculuk
    - 30 günde sıfır iptal/red
    - Psikoteknik raporu güncel
    - Son 3 ay disiplin cezası yok
  
  Araç:
    - Araç puanı: 4.9+
    - 6 fotoğraf da onaylı
    - Ruhsat + periyodik bakım güncel
    - Tüm belgeler tam ve onaylı
    - Model yaşı: 5 yıldan yeni
  
  Eşleşme:
    - Şöför ve araç aynı kişiye ait (veya tam uyumlu kira)
    - Şöför o aracı son 90 günde en az 200 kez kullanmış
    - İkili uyum puanı 4.9+ (sistem hesaplar)
    - "Tam uyumlu taksi + taksici" sertifikası
```

```
VIP CONCIERGE ARAÇ PROFİLİ:
┌──────────────────────────────────────────────┐
│  👑 VIP CONCIERGE                            │
│                                              │
│  🚗 34 TAK 9999  |  Model: 2024             │
│  👤 Ahmet S.  |  ⭐ 5.0                      │
│                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Sürüş    │ │ Davranış │ │ Temizlik │     │
│  │ 10/10    │ │ 10/10    │ │ 10/10    │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ İkram    │ │ Kibar    │ │ Görünüm  │     │
│  │ 10/10    │ │ 10/10    │ │ 10/10    │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│                                              │
│  🏆 Sertifikalar:                            │
│  ├─ Tam Uyumlu Taksi + Taksici              │
│  ├─ VIP Concierge Onaylı                     │
│  └─ 500+ Yolculuk Tamamlandı                 │
│                                              │
│  💰 Fiyat: Normal ücret + %100               │
│  (kalite primi)                              │
└──────────────────────────────────────────────┘
```

#### 17.9.6 Zaman Planlamalı Konfor Tercihi

Müşteri önceden plan yaparken (Bölüm 22) konfor tercihini de belirleyebilir. Planlı rota + yüksek konfor kombinasyonunda **artış oranı sabitlenir** (anlık dalgalanmadan etkilenmez).

```
PLANLI ROTA + KONFOR TERCİHİ:
├── Müşteri: 3 bacaklı plan yapar
├── Konfor: Premium (+%38) seçer
│
├── Ücret:
│   ├── Bacak1: 65 TL × 1.30 (plan) × 1.38 (konfor) = 116.61
│   ├── Bacak2: 45 TL × 1.30 × 1.38 = 80.73
│   ├── Bacak3: 70 TL × 1.30 × 1.38 = 125.58
│   └── TOPLAM: 322.92 TL
│
└── Avantaj: Planlı konfor tercihinde artış oranı donar
    └── Anlık talep artsa bile müşteri aynı oranı öder
```

#### 17.9.7 Dinamik Talep Duyarlılığı

Popüler saatlerde konforlu araçların fiyat artışı **otomatik yükselir** (dynamic pricing overlay):

```
TALEP KATSAYISI (Dinamik):
├── Normal saat (10:00-16:00):   Talep × 1.0 (standart eğri)
├── Yoğun saat (07:00-10:00):    Talep × 1.2
├── Akşam (17:00-20:00):         Talep × 1.3
├── Gece (00:00-06:00):          Talep × 1.5
└── Özel gün/etkinlik:           Talep × 1.5 — 2.0

ÖRNEK:
├── Premium araç (4.5 puan): Normal eğri → +%38
├── Yoğun saatte: +%38 × 1.3 = +%49.4 → ~%50
└── Müşteri ekranda görür: "Bu araç şu an +%50"
```

#### 17.9.8 Kalite Teşvik Döngüsü

Bu fiyatlandırma modeli, taksicilerde **sürekli kalite iyileştirme motivasyonu** yaratır:

```
KALİTE TEŞVİK DÖNGÜSÜ:
┌─────────────────────────────────────────────────────┐
│                                                      │
│    Şöför kalitesini artırır                           │
│         ↓                                            │
│    Puanı yükselir (4.0 → 4.5 → 5.0)                 │
│         ↓                                            │
│    Konfor etiketi yükselir (İyi → Premium → VIP)    │
│         ↓                                            │
│    Fiyat artış oranı yükselir (+%12 → +%38 → +%100) │
│         ↓                                            │
│    Şöförün yolculuk başına geliri artar               │
│         ↓                                            │
│    Daha fazla müşteri tercih eder                     │
│         ↓                                            │
│    Şöför kalitesini daha da artırır...               │
│                                                      │
│    📈 Örnek Gelir Karşılaştırması:                   │
│    ├── Standart şöför (3.5p):  10 yolcu × 185TL    │
│    │   = 1.850 TL / gün                              │
│    ├── Premium şöför (4.7p):   10 yolcu × 287TL    │
│    │   = 2.870 TL / gün (+%55)                      │
│    └── VIP şöför (5.0p):       10 yolcu × 370TL    │
│        = 3.700 TL / gün (+%100)                     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 17.9.9 Kısıtlamalar ve Güvenceler

```yaml
Dinamik Konfor Fiyatlandırması Kuralları:
  Müşteri Hakları:
    - Fiyat artışı binmeden ÖNCE gösterilir (şeffaflık)
    - Müşteri artışı kabul etmezse standart çağrı yapabilir
    - Fiyat tahmini: Binmeden önce net ücret görülür
    - Tavan: Maksimum artış %100'ü geçemez (yasal sınır)

  Şöför Hakları:
    - Yüksek puan = otomatik yüksek artış (aktif onay gerekmez)
    - VIP Concierge etiketi başvuru + onay ile
    - Etiket haksız alınırsa: İptal + 30 gün men

  Sistem Koruması:
    - Talep kat sayısı günlük maksimum 2.0 ile sınırlı
    - Fiyat artışı 5 dk'da bir güncellenir
    - Manipülasyon tespit edilirse: Otomatik fiyat don durma
    - Tüm fiyat değişiklikleri loglanır

  Etik Kurallar:
    - Hiçbir şöför kendi puanını şişiremez
    - Sahte yolculukla puan yükseltme: Kalıcı ban
    - Müşteri onayı olmadan yüksek konforlu araç atanamaz
```

---

## 18. MÜŞTERİ ÇAĞRI İPTAL VE BİN MEME CEZASI

### 18.1 Temel Kural

Müşteri taksi çağırdıktan sonra **binmez veya vazgeçerse**, taksi o noktaya kadar gelmek için yakıt ve zaman harcamıştır. Bu bedel **müşteri tarafından karşılanmalıdır**.

```
KURAL:
├── Müşteri çağrı yapar → Taksi eşleşir → Taksi yola çıkar
├── Müşteri binmez / vazgeçer / gelmez
└── Müşteri, taksinin kendine geliş mesafesini öder
```

### 18.2 Ceza Hesaplama

```
CEZA FORMÜLÜ:
├── Ceza = Taksi'nin müşteriye geliş mesafesi × km başına ücret
│
├── Örnek:
│   ├── Taksi 2 km uzaktaydı → Ceza = 2 km × 20 TL = 40 TL
│   ├── Taksi 5 km uzaktaydı → Ceza = 5 km × 20 TL = 100 TL
│   └── Taksi 500 m uzaktaydı → Ceza = 0 (çok yakın, ceza yok)
│
├── Minimum eşik: 1 km'den uzaksa ceza uygulanır
│   └── 1 km altı → ceza yok (müşteri iptal edebilir)
│
└── Maksimum ceza: 150 TL (taksi çok uzaktan geliyorsa bile)
```

### 18.3 Tekrarlayan Binmeme Durumu

Arka arkaya binmeyen müşteriler için **kademeli ceza sistemi**:

```
TEKRARLAYAN İHLAL:
├── 1. İhlal (ayda 1.): Sadece geliş mesafesi ücreti
│
├── 2. İhlal (ayda 2.): Geliş mesafesi × 2
│
├── 3. İhlal (ayda 3. veya yılda 5.):
│   ├── Geliş mesafesi × 3
│   ├── Müşteri puanı -0.5 düşer
│   └── Sistem talepleri kısıtlanır
│
└── 5+ İhlal (yılda):
    ├── Müşteri "Güvensiz" statüye düşer
    ├── Bekleme süresi 2 katına çıkar
    └── Sadece ön ödemeli çağrı yapabilir
```

### 18.4 Müşteri Sistem Kısıtlamaları

Tekrarlayan binmeme durumunda sistem, müşterinin **çağrı önceliğini düşürür** ve **bekleme süresini artırır**:

```
SİSTEM KISITLAMALARI:
├── 1-2 ihlal: Normal işlem
│
├── 3 ihlal: ⚠️ Uyarı
│   ├── Çağrı önceliği düşer (arka sıraya alınır)
│   ├── Bekleme süresi %50 artar
│   └── Eşleşme sırasında en sona konur
│
├── 4 ihlal: 🔴 Kısıtlı
│   ├── Bekleme süresi 2 katına çıkar
│   ├── Sadece düşük puanlı taksiler eşleşir
│   ├── Çağrı öncesi uyarı: "Geçmişte 4 kez binmediniz"
│   └── Bahşiş zorunlu (%10)
│
└── 5+ ihlal: ⛔ Bloke
    ├── 1 gün çağrı yapamaz
    ├── Müşteri hizmetlerine yönlendirilir
    └── Aktif olmak için depozito yatırmalı (200 TL)
```

### 18.5 Müşteri Bilgilendirme Ekranı

```
ÇAĞRI İPTAL EKRANI:
┌──────────────────────────────────────────────┐
│  ⚠️ ÇAĞRI İPTAL                             │
│                                              │
│  Taksinin size geliş mesafesi: 2.3 km        │
│  Tahmini ceza: 46 TL                         │
│                                              │
│  Bu ay kullanım: 1/3 ihlal hakkı            │
│  (aylık 3 ihlalden sonra ek cezalar başlar) │
│                                              │
│  ❄️ 5 dk içinde ücretsiz iptal hakkınız var │
│                                              │
│  [ İPTAL ET ve CEZAYI ÖDE ]                  │
│  [ VAZGEÇ, TAKSİYİ BEKLE ]                   │
└──────────────────────────────────────────────┘

BİNMEME DURUMUNDA ŞÖFÖR BİLDİRİMİ:
┌──────────────────────────────────────────────┐
│  ✅ Müşteri binmedi                          │
│                                              │
│  Müşteri: Ahmet Yılmaz                       │
│  Size geliş mesafeniz: 2.3 km                │
│  Ceza: 46 TL (hesabınıza aktarılacak)       │
│                                              │
│  [ MÜŞTERİ BİNMEDİ ONAYLA ]                  │
└──────────────────────────────────────────────┘
```

### 18.6 Veritabanı

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    no_show_count       INTEGER DEFAULT 0;              -- Toplam binmeme sayısı
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    no_show_monthly     INTEGER DEFAULT 0;              -- Bu ayki binmeme
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    no_show_penalty_total NUMERIC(12,2) DEFAULT 0;      -- Ödenen toplam ceza
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    is_restricted       BOOLEAN DEFAULT FALSE;          -- Kısıtlı mı?
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    restricted_until    TIMESTAMP;                      -- Kısıtlama bitişi

-- Binmeme / iptal kayıtları
CREATE TABLE taxi_no_show_log (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    
    customer_id         UUID REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    driver_distance_km  NUMERIC(5,2) NOT NULL,          -- Taksi uzaklığı
    penalty_amount      NUMERIC(10,2) NOT NULL,         -- Ceza tutarı
    penalty_multiplier  INTEGER DEFAULT 1,              -- Kaç katı (tekrar)
    
    reason              VARCHAR(100),                    -- customer_cancel, no_show
    payment_status      VARCHAR(30) DEFAULT 'pending',   -- pending, paid
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_no_show_customer ON taxi_no_show_log(customer_id);
CREATE INDEX idx_no_show_driver ON taxi_no_show_log(driver_id);

-- Aylık sıfırlama (cron job)
-- Her ayın 1'inde: UPDATE users SET no_show_monthly = 0;
```

### 18.7 API

```
POST   /api/v1/taxi/trip/{tripId}/cancel              # Çağrı iptal (binmeden)
POST   /api/v1/taxi/trip/{tripId}/confirm-no-show      # Şöför: Müşteri binmedi onayı
GET    /api/v1/taxi/customer/no-show-history           # Müşteri binmeme geçmişi
GET    /api/v1/taxi/customer/restriction-status        # Kısıtlama durumu
```

---

## 📌 ÖNEMLİ NOTLAR

1. **Bireysel Hesap Ön Koşuldur**: Taksi şöförü olmak isteyen herkes öncelikle bireysel hesap açmak ve kimlik doğrulamasını tamamlamak zorundadır.

2. **Belgeler Zorunludur**: Hiçbir şöför belgeleri doğrulanmadan taksi hizmeti veremez. Tüm belgeler sisteme yüklenmeli ve onaylanmalıdır.

3. **Araç-Sürücü Dinamiği**: Aracı kim kullanıyorsa çağrı o kişiye gider. Araç sahibi kendisi de kullanabilir, kiraya da verebilir.

4. **Puanlama Sistemi**: Şöför ve araç ayrı ayrı puanlanır. Kombine puan sıralamayı belirler. Düşük puan = az iş.

5. **Çağrı Reddetme Cezası**: Kısa mesafe diye reddeden şöförler puan kaybeder. Bu sayede her yolcuya eşit hizmet garantilenir.

6. **Zorunlu Sistem Ödemesi**: Tüm ödemeler sistem üzerinden yapılır. Nakit ödeme kesinlikle yasaktır. Yolcuların cüzdan veya tanımlı kartı olmak zorundadır.

7. **Emanet Sistemi**: Ödeme yolculuk başında bloke edilir, yolculuk bitince otomatik çekilir. Bu sayede hem şöför hem yolcu güvendedir.

8. **Seyahat Taahhüt ve Erken İnme Sistemi**: Yolcu çağrı anında gideceği yeri taahhüt eder. Ayda 1 kez erken inme hakkı vardır. Yıl içinde 3 farklı ayda erken inme yapan yolcu "Onurlu Müşteri" statüsünü kaybeder ve taahhüt ettiği mesafenin tamamını ödemek zorunda kalır.

9. **Özgün Rota Haritalama Sistemi**: Müşteri adres yazmadan haritada serbestçe nokta belirleyip kendi rotasını oluşturabilir, "buradan gitmek istiyorum" notuyla taksi çağırabilir. 10 noktaya kadar ara durak eklenebilir.

9.5. **Paylaşımlı Yolculuk Sistemi**: Müşteri 2+ ek yolcu ile taksiye binerse (toplam ≥3 kişi), yolculuk paylaşımlı statüye geçer. Taksici, belirlenen rota sonuna kadar diğer yolcuları alabilir. Her yolcu kendi mesafesi kadar öder.

10. **Başkasına Taksi Gönderme (Hediye Yolculuk)**: Müşteri kendisi gitmeden bir tanıdığı için taksi çağırabilir, rotayı belirler ve ücreti kendisi öder. Yolcunun üye olması gerekmez; SMS ile bilgilendirilir.

11. **Puan = Konfor**: Sistemdeki tüm puanlar doğrudan konfor seviyesini ifade eder. Yüksek puan = yüksek konfor. Müşteriler konfor seviyesine göre filtreleme yapabilir.

12. **Bahşiş Protokolü**: Müşteri, konfor tercihi yapıp eşleşme bulamazsa bahşiş teklifi ile taksiciyi teşvik edebilir. Bahşiş doğrudan şöföre gider, sistem komisyonu sadece normal ücretten alınır. Bu sistem şöförlerde kaliteli olma isteği uyandırır.

13. **Müşteri Puanlaması (Çift Yön)**: Şöför de yolcuyu değerlendirir. Müşteri puanı = Davranış (%50) + Güvenilirlik (%30) + Düzen (%20). Düşük puanlı müşteriler daha uzun bekler, yüksek puanlılar öncelikli eşleşir.

14. **Araç İçi Deneyim Puanı**: Aracın konfor, ses yalıtımı, WiFi, şarj imkanı ve klima performansı ayrı bir puandır. Temizlikten bağımsız değerlendirilir.

15. **Kişisel İmaj Puanı**: Şöförün kılık kıyafet, sakal tıraşı, genel bakım ve kişisel hijyeni ayrı bir puandır.

16. **Müşteri Çağrı İptal / Binmeme Cezası**: Müşteri çağırıp binmezse taksinin geliş mesafesini öder. Tekrarlayan ihlallerde çağrı önceliği düşer, bekleme süresi artar.

17. **Bölgeler Arası Transfer Taksi**: Uzun mesafeli yolculuklarda müşteri ya tek taksi ile gidebilir ya da bölge sınırlarında taksi değiştirerek transfer yapabilir. Transfer seçeneğinde her bölgenin yerel şöförü kendi bölgesinde hizmet verir.

18. **Şöför Aktif/Pasif Seçimi**: Taksici aktif veya pasif modda olmayı seçer. Aktif modda GPS konumu açık olmak ZORUNDADIR. Konum kapatılırsa sistem otomatik pasife alır.

19. **Araç QR Kod Sistemi**: Her araç için sistem tarafından eşsiz QR kod oluşturulur. Müşteri binmeden önce araç sağ/sol kapısındaki veya içerideki QR kodu okutarak aracı doğrular ve yolculuğu başlatır.

20. **Anlık Durak/Sokak Çağrısı (QR Hızlı Biniş)**: Müşteri, sistem taksisini durakta/sokakta görüp çağrı yapmadan doğrudan QR okutarak binebilir. Şöför aktifse sistem onay verir. Biniş gerçekleşince taksimetre açılış ücreti zorunludur (1 metre gidilse bile).

21. **Müşteri Taksi Terminali**: Taksi sistemi, ana platform içinde bağımsız bir terminal (alt sistem) olarak çalışır. Müşteri taksi alanına girdiğinde terminal başlatılır, tüm taksi özellikleri aktif olur. Terminal bağımsız crash/state/resource yönetimine sahiptir.

22. **Planlanmış Rotalar (Ön Rezervasyon)**: Müşteri günlük akışına göre 12 saat - 30 gün öncesinden çok bacaklı plan yapabilir. Normal tarifeye %30 ek ücret uygulanır. Özel servis/periyot statüsündedir.

23. **Dinamik Konfor Fiyatlandırması (Eğrisel Artış)**: Popüler konforlu taksiler için talep primi eğrisel (non-linear) hesaplanır. Müşteri her konfor seviyesinin fiyat artışını görür (+%5 → +%100). VIP Concierge (+%100) sadece sistemdeki en yüksek puanlı şöför+araç çiftlerine verilir. Kalite teşvik döngüsü oluşturur.

24. **Araç İçi Güvenlik Kamerası Zorunluluğu**: Sisteme kayıtlı her taksinin araç içi güvenlik kamerası bulundurması ZORUNLUDUR. Kamerası olmayan araçlar sistem tarafından işaretlenir ve müşteriye "Bu araçta güvenlik kamerası yok" uyarısı gösterilir. 30 gün içinde takmayan araç geçici men edilir.

25. **Araç Marka/Model/Yakıt ve Şöför Cinsiyet Filtreleme**: Müşteri çağrı ekranında araç markası, model yılı, yakıt tipi (benzinli/dizel/LPG'li/elektrikli/hibrit) ve şöför cinsiyetine (kadın/erkek/farketmez) göre filtreleme yapabilir. Tüm bu bilgiler araç ve şöför kartlarında görünür.

26. **Trafik Muayene Otomatik Okuma ve Süre Takibi**: Sisteme yüklenen muayene belgesi OCR ile otomatik okunur, son geçerlilik tarihi çıkarılır. Tarih aşıldığında araç **güvenlik dışı** işaretlenerek otomatik devre dışı bırakılır. Her gece 00:00 cron job ile tüm araçlar taranır. 30/7 gün kala uyarı gönderilir.

27. **Taksi Durakları (Durak Sistemi)**: Sistem tarafından oluşturulan lokasyonlardaki duraklara araçlar ve şöförler bağlanabilir. Her araç tek durağa kayıtlı olur. Müşteri durak filtrelemesi yapabilir. Durak değişikliği 30 günde 1 kez.

28. **Taksi Bekleme Lokasyonu (Ben Buradayım)**: Taksiciler şehrin farklı noktalarında bekleme noktası oluşturup "Ben buradayım" işareti koyabilir. Müşteri haritada bekleyen taksileri görür ve doğrudan çağırabilir. GPS hareketinde otomatik sorgulanır.

29. **Durak Sıra Sistemi (Kuyruk Yönetimi)**: Durak yöneticisi araçları sıraya koyar, çağrılar sıraya göre yönlendirilir. FIFO varsayılan, yönetici sırayı elle düzenleyebilir. Reddeden araç sıra sonuna gider. Tüm işlemler loglanır.

30. **Yolculuk Sonrası Otomatik Görevlendirme**: Yolculuk bitince şöför aktifse sistem en yakın çağrıya yönlendirir (otomatik kabul, öneri veya durağa dönüş modu). Kesintisiz görev döngüsü ile şöför sürekli kazanır, müşteri beklemez.

31. **Geliş Öncesi Karşılama Rezervasyonu**: Müşteri başka şehirden yola çıkmadan önce varış noktasında kendisini bekleyecek taksi çağırabilir. Bekleme ücreti, aracın son 30 günlük ortalama saatlik kazancına göre hesaplanır (×0.80). İlk 15 dk ücretsiz. Rötar durumunda müşteri bilgilendirilir ve onayı alınır.

32. **Şöför Beklememe Hakkı ve Dinamik Ceza Puanı**: Şöför müşteriyi beklemeyi reddedebilir ancak bu bir ceza puanı düşümü ile sonuçlanır. Ceza, müşterinin alternatif taksi bulma zorluğuna göre belirlenir: gündüz -5 puan, gece/yağmur/tenha bölge gibi zor durumlarda -100 puana kadar çıkabilir. Şöför cezayı görüp onaylayarak müşteriyi bırakır, müşteri bekleme ücreti ödemez.

33. **Karşılıklı Taahhüt Sistemi**: Müşteri çağrı yaparken bekleme ücretini, şöför çağrıyı kabul ederken beklemeyi taahhüt eder. Sistem her iki tarafa da sonuçları önceden gösterir: müşteriye gecikme ücretini, şöföre beklememe cezasını ve müşterinin alternatif bulma olasılığını. İlk 5 dk bekleme ücretsizdir.

---

## 19. BÖLGELER ARASI TRANSFER TAKSİ VE UZUN MESAFE SİSTEMİ

### 19.1 Problem: Uzun Mesafe = Boş Dönüş

Bir müşteri Türkiye'nin bir ucundan diğer ucuna taksi ile gitmek istediğinde (örn: İstanbul → Antalya, 700+ km), taksici varış noktasında **geri dönüş müşterisi bulmakta zorlanır**. Bu durum taksici için ciddi kayıptır.

```
PROBLEM:
├── İstanbul → Antalya: 700 km, ~7 saat
├── Gidiş ücreti: ~8.000 TL
├── Dönüş: Büyük olasılıkla BOŞ
│   └── Kayıp: 700 km yakıt + 7 saat zaman = ~3.000 TL zarar
└── Taksici kârı: 8.000 - 3.000 - (masraflar) = ÇOK AZ
```

### 19.2 Çözüm: İki Seçenek

```
SEÇENEK 1: TEK TAKSİ (Tam Mesafe) 🚕
├── Aynı taksi, aynı şöför, İstanbul → Antalya
├── Artı: Kesintisiz yolculuk, tanıdık şöför
├── Eksi: Yüksek ücret, şöför dönüş sorunu
└── Fiyat: Normal km ücreti (uzun mesafe indirimi olabilir)

SEÇENEK 2: TRANSFER TAKSİ 🔄
├── İstanbul → Kocaeli sınırı: İstanbul taksicisi (1. taksi)
├── Kocaeli → Bilecik sınırı: Kocaeli taksicisi (2. taksi)
├── Bilecik → Eskişehir sınırı: Bilecik taksicisi (3. taksi)
├── Eskişehir → Antalya: Eskişehir + Afyon + Antalya taksicileri
│
├── Artı: Her şöför kendi bölgesinde, dönüş sorunu yok
├── Artı: Daha ekonomik (bölgesel fiyat farkı)
├── Eksi: Taksi değiştirme, bekleme
└── Fiyat: Bölgesel km ücreti (daha ucuz)
```

### 19.3 Transfer Sistemi Detayı

Sistem, Türkiye'yi **transfer bölgelerine** ayırır:

```
TRANSFER BÖLGELERİ (ÖRNEK):
├── Bölge 1: İstanbul (Avrupa) → İstanbul (Anadolu) sınırı
├── Bölge 2: İstanbul Anadolu → Kocaeli sınırı
├── Bölge 3: Kocaeli → Sakarya sınırı
├── Bölge 4: Sakarya → Düzce sınırı
├── Bölge 5: Düzce → Bolu sınırı
├── ...
└── Her bölgede sadece o bölgeye kayıtlı taksiciler hizmet verir
```

TRANSFER NOKTALARI: Şehirler arası otoyol gişeleri, benzin istasyonları, şehir giriş/çıkış noktaları.

```
TRANSFER AKIŞI:
├── Müşteri: İstanbul → Antalya
├── Sistem rota analizi yapar: 5 bölge, 4 transfer noktası
│
├── NOKTA 1: İstanbul Avrupa → Anadolu yakası gişeleri
│   ├── Taksi 1: İstanbul Avrupalı taksi (müşteriyi alır)
│   ├── Taksi 2: İstanbul Anadolulu taksi (müşteriyi devralır)
│   └── Müşteri: Arabadan iner, diğer arabaya biner
│
├── NOKTA 2: İstanbul Anadolu → Kocaeli gişeleri
│   ├── Taksi 2: Yolculuğa devam eder (bölge içi)
│   ├── (İstanbul Anadolu taksicisi Kocaeli'ye kadar gidebilir)
│   └── VEYA yeni Taksi 3: Kocaelili taksi devralır
│
├── ...
│
└── SON NOKTA: Antalya girişi
    └── Son taksi müşteriyi Antalya'da istediği adrese bırakır
```

### 19.4 Müşteri Seçim Ekranı

```
UZUN MESAFE ÇAĞRI EKRANI:
┌──────────────────────────────────────────────┐
│  📍 Nereye gidiyorsunuz?                     │
│  ┌──────────────────────────────────┐        │
│  │ İstanbul → Antalya (703 km)      │        │
│  └──────────────────────────────────┘        │
│                                              │
│  🚕 UZUN MESAFE SEÇENEKLERİ                 │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │ 🔄 TRANSFER TAKSİ (Önerilen)     │        │
│  │  ├── 4 transfer, 5 taksi         │        │
│  │  ├── ~6.500 TL (daha ekonomik)   │        │
│  │  ├── Her şöför kendi bölgesinde  │        │
│  │  └── Tahmini: 8 saat            │        │
│  └──────────────────────────────────┘        │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │ 🚕 TEK TAKSİ (Kesintisiz)        │        │
│  │  ├── Aynı şöför, aynı araç      │        │
│  │  ├── ~9.500 TL                   │        │
│  │  ├── Mola molaya gidebiliriz    │        │
│  │  └── Tahmini: 7 saat            │        │
│  └──────────────────────────────────┘        │
│                                              │
│  [ SEÇ ve ÇAĞIR ]                           │
└──────────────────────────────────────────────┘
```

### 19.5 Ücretlendirme

```yaml
Uzun Mesafe Ücretlendirme:
  Transfer Taksi:
    - Her bölge kendi km ücretini belirler
    - Bölge geçişlerinde bekleme ücreti yok (transfer anı)
    - Toplam: Bölge ücretleri toplamı
    - Uzun mesafe indirimi: %10-15 (normalden daha ucuz)
    - Örnek: 700 km × 9 TL/km = 6.300 TL (indirimsiz)
             6.300 × 0.90 = 5.670 TL (indirimli)

  Tek Taksi:
    - Normal km ücreti + dönüş güvencesi
    - Dönüş güvencesi: Toplam ücretin %20'si
    - Örnek: 700 km × 13 TL/km = 9.100 TL
             9.100 + 1.820 (%20 dönüş) = 10.920 TL

  Transfer Noktası Bekleme:
    - Transfer noktasında max 10 dk bekleme
    - 10 dk geçerse: yeni taksi bağımsız gelir
    - Müşteri kaynaklı gecikme: müşteri öder
    - Taksi kaynaklı gecikme: sistem karşılar
```

### 19.6 Şöför Bölge Kaydı

```sql
-- Şöförlerin çalışabileceği bölgeler
CREATE TABLE taxi_driver_regions (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    region_name         VARCHAR(100) NOT NULL,          -- "İstanbul Anadolu"
    region_boundary     GEOGRAPHY(POLYGON),             -- Bölge sınırı (GPS)
    max_distance_km     INTEGER DEFAULT 50,             -- Bölge dışı max mesafe
    
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_driver_regions_driver ON taxi_driver_regions(driver_id);

-- Transfer rotaları (sistem tarafından önceden tanımlanır)
CREATE TABLE taxi_transfer_routes (
    id                  UUID PRIMARY KEY,
    start_city          VARCHAR(100) NOT NULL,
    end_city            VARCHAR(100) NOT NULL,
    total_km            NUMERIC(6,1) NOT NULL,
    
    -- Rota adımları (JSON: [{"region":"İstanbul", "km":30}, ...])
    route_steps         JSONB NOT NULL,
    
    -- Transfer noktaları (GPS koordinatları)
    transfer_points     JSONB NOT NULL,
    
    estimated_duration  INTERVAL,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW()
);

-- Transfer yolculuk kaydı
CREATE TABLE taxi_transfer_trips (
    id                  UUID PRIMARY KEY,
    customer_id         UUID REFERENCES users(id),
    route_id            UUID REFERENCES taxi_transfer_routes(id),
    
    transfer_type       VARCHAR(30) NOT NULL,           -- single, transfer
    total_fare          NUMERIC(10,2) NOT NULL,
    discount_applied    NUMERIC(10,2) DEFAULT 0,
    
    status              VARCHAR(30) DEFAULT 'pending',  -- pending, active, completed
    
    -- Her segment için taksi kaydı
    segments            JSONB DEFAULT '[]',
    -- [{"trip_id": "...", "driver": "...", "region": "...", 
    --   "fare": 1200, "status": "completed"}, ...]
    
    created_at          TIMESTAMP DEFAULT NOW(),
    completed_at        TIMESTAMP
);

CREATE INDEX idx_transfer_trips_customer ON taxi_transfer_trips(customer_id);
```

### 19.7 API

```
POST   /api/v1/taxi/long-distance/estimate           # Uzun mesafe fiyat tahmini
POST   /api/v1/taxi/long-distance/book               # Uzun mesafe yolculuk oluştur
GET    /api/v1/taxi/long-distance/{id}/status        # Transfer durumu
GET    /api/v1/taxi/long-distance/regions            # Bölge listesi
GET    /api/v1/taxi/long-distance/routes             # Tanımlı rotalar
```

---

## 20. TAKSİ YOLCU e-KİTAP / e-FATURA / YOLCULUK RAPORU SİSTEMİ

*Bu bölüm yolculuk sonrası belge ve raporlama sistemini kapsayacaktır. İhtiyaca göre doldurulacaktır.*

---

## 21. MÜŞTERİ TAKSİ TERMİNALİ

### 21.1 Felsefe: Sistem İçinde Sistem

Taksi sistemi, ana platformun **içinde bağımsız bir terminal (alt sistem)** olarak çalışır. Müşteri, ana platform üzerinde gezinirken taksi alanına girdiğinde, tüm taksi özellikleri tek bir arayüz üzerinden aktif hale gelir. Bu, bir "mağaza içinde mağaza" veya "terminal içinde terminal" mantığıdır.

```
ANA PLATFORM (Web/Mobil Uygulama)
├── 🏠 Ana Sayfa
├── 👤 Hesabım
├── 💰 Ödemeler
│
├── 🚕 **TAKSİ TERMİNALİ** ← Müşteri bu alana girdiğinde
│   ├── 📞 Çağrı / Hızlı Biniş (QR)
│   ├── 🚗 Araç / Şöför Bilgisi
│   ├── ⭐ Değerlendirme
│   ├── 💳 Ödeme / Bahşiş
│   ├── 📜 Yolculuk Geçmişi
│   ├── 🎁 Hediye Yolculuk
│   ├── 👥 Paylaşımlı Yolculuk
│   └── ⚙️ Tercihler (Konfor, Bahşiş, vs.)
│
├── 📦 Diğer Hizmetler
└── ❓ Yardım
```

### 21.2 Terminal Mimarisi

```yaml
Taksi Terminali Mimarisi:
  Bağımsız Modül:
    - Kendi iç router'ı (alt navigasyon)
    - Kendi state yönetimi (global'den izole)
    - Kendi API servis katmanı
    - Terminal açıkken ana platform API'sine yük bindirmez
  
  Aktivasyon:
    - Müşteri taksi alanına girer → Terminal başlatılır
    - Terminal başlatılınca:
      ├── Mevcut konum alınır
      ├── Yakındaki araçlar yüklenir (şöför aktifse)
      ├── Müşterinin bakiyesi kontrol edilir
      ├── Müşteri puanı ve ceza durumu kontrol edilir
      └── Terminal arayüzü gösterilir
    
    - Terminal kapatılınca (başka sayfaya geçince):
      ├── State temizlenir
      ├── API bağlantıları kesilir
      └── Kaynaklar serbest bırakılır
  
    Özellik:
      - Terminal, ana platformdan bağımsız crash/göçük yönetimi
      - Terminal hata verse bile ana platform çalışmaya devam eder
```

### 21.3 Müşteri Navigasyonu

```
TAKSİ TERMİNALİNE GİRİŞ ÇIKIŞ:
├── GİRİŞ YOLLARI:
│   ├── 1️⃣ Ana menü → "Taksi" butonu
│   ├── 2️⃣ QR kod okutma (doğrudan terminali açar)
│   ├── 3️⃣ Push bildirim (çağrıya yanıt)
│   └── 4️⃣ Derin bağlantı (link ile doğrudan terminal)
│
├── TERMİNAL İÇİ GEZİŞ:
│   └── Alt navigasyon:
│       ├── 🏠 Terminal Ana Sayfa (harita + çağrı)
│       ├── 📞 Çağrılarım
│       ├── ⭐ Değerlendirmelerim
│       └── 👤 Profil / Tercihler
│
└── ÇIKIŞ:
    ├── "Ana Sayfa" butonu
    ├── Geri butonu (terminali kapatır)
    └── 5 dakika hareketsizlik → otomatik terminal kapanışı
```

### 21.4 Terminal Ana Ekranı

```
TAKSİ TERMİNALİ ANA EKRANI:
┌──────────────────────────────────────────────┐
│  🚕 TAKSİ                           [✕ Kapat]│
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │          🗺 HARİTA / KONUM              ││
│  │                                          ││
│  │          🚗 🚗 🚗                       ││
│  │        🚗        🚗                      ││
│  │       🚗   📍    🚗                      ││
│  │        🚗        🚗                      ││
│  │          🚗 🚗 🚗                       ││
│  │  (Yakındaki aktif taksiler)              ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  📍 Nereye?                     [🔍 Ara] ││
│  └──────────────────────────────────────────┘│
│                                              │
│  ⚡ Hızlı İşlemler:                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ 📞 Çağrı │ │ 📷 QR    │ │ 🎁 Hediye│     │
│  │  Yap     │ │ Okut     │ │  Gönder  │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ 💰 Bakiye │ │ ⭐ Puanım│ │ 📜 Geçmiş│     │
│  │  125 TL  │ │  4.8     │ │  Yolc.  │     │
│  └──────────┘ └──────────┘ └──────────┘     │
│                                              │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│  🏠 Ana Sayfa  📞 Çağrılar  ⭐ Puan  👤 Profil │
└──────────────────────────────────────────────┘
```

### 21.5 Terminal Özellik Matrisi

```yaml
Terminal İçi Özellikler:
  Çağrı İşlemleri:
    - Yeni çağrı oluşturma (adres + hedef)
    - Aktif çağrı takibi
    - Çağrı iptal
    - Anlık QR biniş (çağrısız)
  
  Araç/Şöför:
    - Atanan araç bilgisi
    - Şöför profili (ad, puan, fotoğraf)
    - Araç plaka ve model
    - Gerçek zamanlı konum takibi
  
  Ödeme:
    - Bakiye görüntüleme
    - Kart ekleme/çıkarma
    - Bakiye yükleme
    - Bahşiş ekleme
    - Ödeme geçmişi
  
  Değerlendirme:
    - Puanlama (2 soru: taksi + şöför)
    - Puan geçmişi
    - Müşteri puanım
  
  Hedef/Geçmiş:
    - Adres girme
    - Sık gidilen yerler (ev, iş)
    - Yolculuk geçmişi
    - Fatura/e-kitap görüntüleme
  
  Tercihler:
    - Konfor seviyesi (1-5)
    - Bahşiş yüzdesi/sabiti
    - Ödeme yöntemi varsayılan
    - Bildirim tercihleri
```

### 21.6 Terminal API Kullanımı

```
Terminal API Servisleri:
├── /api/v1/taxi/terminal/init          → Terminal başlatma (konum, bakiye, durum)
├── /api/v1/taxi/terminal/status        → Terminal durumu
├── /api/v1/taxi/terminal/close         → Terminal kapatma
│
├── Terminal içi tüm çağrılar:
│   ├── /api/v1/taxi/trip/*            → Çağrı/yolculuk işlemleri
│   ├── /api/v1/taxi/payment/*         → Ödeme işlemleri
│   ├── /api/v1/taxi/rating/*          → Puanlama işlemleri
│   ├── /api/v1/taxi/vehicle/*         → Araç işlemleri
│   └── /api/v1/taxi/driver/*          → Şöför işlemleri
│
└── Terminal kapanınca:
    ├── Canlı bağlantılar kesilir (WebSocket)
    ├── Geçici önbellek temizlenir
    └── State sıfırlanır
```

### 21.7 Ana Platformdan Bağımsızlık

```yaml
Terminal Bağımsızlık Prensipleri:
  Crash Isolation:
    - Terminal'de oluşan bir hata ana platformu etkilemez
    - Terminal çökerse sadece taksi alanı kullanılamaz
    - Ana platform (profil, ödemeler, diğer servisler) çalışmaya devam eder
  
  State Isolation:
    - Terminal kendi state'ini yönetir (Redux store / Context)
    - Ana platform state'i terminal state'inden etkilenmez
    - Terminal kapanınca state otomatik temizlenir
  
  Resource Management:
    - Terminal açıkken WebSocket/SSE bağlantısı kurulur
    - Terminal kapanınca tüm bağlantılar kesilir
    - Harita API'si (Google Maps/Mapbox) sadece terminalde yüklenir
  
  Versioning:
    - Terminal kendi versiyonuna sahiptir
    - Ana platformdan bağımsız güncellenebilir
    - Geriye dönük uyumluluk sağlanır
  
  Load Balancing:
    - Terminal istekleri ayrı bir API gateway üzerinden yönlendirilir
    - Terminal trafiği ana platform trafiğinden ayrı ölçeklenir
    - Yüksek talep durumunda sadece terminal ölçeklenir
```

---

## 22. PLANLANMIŞ ROTALAR (ÖN REZERVASYON)

### 22.1 Felsefe

Müşteri, günlük hayat akışına göre **bir gün önceden** taksi çağırma planı yapabilir. Bu, sıradan bir taksi çağrısı değil, **özel rezervasyonlu servis** niteliğindedir. Müşteri birden fazla bacaklı (multi-leg) rotalar tanımlayabilir.

```
ÖRNEK PLAN:
├── Bacak 1: Sabah 07:30 → Ev (A) → İş (B)
├── Bacak 2: Öğlen 12:00 → İş (B) → Toplantı (C)
└── Bacak 3: Akşam 18:00 → Toplantı (C) → Ev (A)
```

### 22.2 Özellikler

```yaml
Planlanmış Rota Özellikleri:
  Zamanlama:
    - En az 12 saat önceden planlanmalı
    - Maksimum 30 gün sonrasına plan yapılabilir
    - Her bacak için ayrı saat ve adres tanımlanır
    - İptal: Planlanan saatten 2 saat öncesine kadar ücretsiz
    - 2 saat kala iptal: %50 ceza
    - 30 dk kala iptal: %100 ceza (tam ücret)
  
  Rota Yapısı:
    - Minimum 1 bacak, maksimum 5 bacak
    - Her bacak: kalkış noktası + varış noktası + saat
    - Bacaklar arası bekleme süresi minimum 30 dk
    - Aynı gün içinde tüm bacaklar tamamlanmalı
  
  Ücretlendirme:
    - Normal taksi ücreti × 1.30 (%30 fazla)
    - Hesaplama: Her bacak ayrı hesaplanır
    - Toplam = (Bacak1 ücreti + Bacak2 ücreti + ...) × 1.30
    - Bekleme ücreti: Bacaklar arası bekleme için 5dk ücretsiz
      Sonra her 10dk için normal tarife
  
  Ödeme:
    - Plan oluşturulurken tam ücret bloke edilir
    - Müşteri bakiyesi yeterli değilse plan oluşturulamaz
    - İptal durumunda bloke çözülür (ceza kesintisiyle)
    - Yolculuk tamamlanınca bloke çözülür + gerçek ücret tahsil edilir
```

### 22.3 Akış

```
PLANLI ROTA AKIŞI:
├── ADIM 1: Müşteri plan oluşturur
│   ├── Tarih seçer (en az 12 saat sonrası)
│   ├── Bacakları tanımlar (A→B, C→D, ...)
│   ├── Her bacak için saat + adres girer
│   └── Tercihler (konfor, araç tipi) ekler
│
├── ADIM 2: Sistem hesaplama
│   ├── Her bacak için tahmini mesafe hesaplanır
│   ├── Normal ücret hesaplanır
│   ├── %30 eklenir → Toplam ücret
│   └── Müşteriye gösterilir: "Toplam: XXX TL"
│
├── ADIM 3: Onay ve bloke
│   ├── Müşteri onaylar
│   ├── Bakiye yeterli mi? → ✅ Bloke edilir
│   │   └── Yetersizse ❌ "Bakiyeniz yetersiz"
│   └── Plan kaydedilir, şöför ataması bekler
│
├── ADIM 4: Şöför ataması (ön rezervasyon)
│   ├── Planlanan saatten 1 saat önce şöför atanır
│   ├── Atama: En yakın/uygun şöför
│   │   └── Tercih: Yüksek puanlı şöför öncelikli
│   ├── Şöför bildirim alır
│   └── Şöför kabul/red:
│       ├── Kabul → "Planınız onaylandı ✅"
│       └── Red → Başka şöför atanır
│
├── ADIM 5: Bacak 1 başlar
│   ├── Şöför belirtilen saatte kalkış noktasında olur
│   ├── Müşteri biner
│   ├── QR okutur (veya normal çağrı gibi)
│   └── Yolculuk başlar
│
├── ADIM 6: Bacak 1 biter
│   ├── Müşteri iner
│   ├── Ödeme: Bu bacak için tahsilat
│   └── Bir sonraki bacağa hazırlık
│
├── ADIM 7: Bacak 2 başlar (bekleme varsa)
│   ├── Bekleme süresi işler
│   ├── Şöför bekler (veya başka şöför gelir)
│   └── Bacak 2 devam eder...
│
└── ADIM 8: Tüm bacaklar tamamlanır
    ├── Bloke çözülür
    ├── Gerçek ücret tahsil edilir
    └── Müşteri değerlendirme yapar
```

### 22.4 Müşteri Planlama Ekranı

```
PLANLAMA EKRANI:
┌──────────────────────────────────────────────┐
│  📅 PLANLANMIŞ ROTA REZERVASYONU              │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│                                              │
│  Tarih: [  15 Haziran 2026  ] 📅             │
│                                              │
│  ─── Bacak 1 ───                             │
│  ⏰ Saat: [  07:30  ]                        │
│  📍 Kalkış: [  Evim (Kayıtlı Adres)      ]  │
│  📍 Varış:  [  İşim (Kayıtlı Adres)      ]  │
│                                              │
│  ─── Bacak 2 ───                             │
│  ⏰ Saat: [  12:00  ]                        │
│  📍 Kalkış: [  İşim                      ]  │
│  📍 Varış:  [  Müşteri A. Şişli         ]  │
│                                              │
│  ─── Bacak 3 ───                             │
│  ⏰ Saat: [  18:00  ]                        │
│  📍 Kalkış: [  Müşteri A. Şişli         ]  │
│  📍 Varış:  [  Evim                     ]  │
│                                              │
│  [+ Bacak Ekle] (maks 5)                     │
│                                              │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│  Ücret Özeti:                                │
│  ├─ Bacak 1 (07:30): 65 TL × 1.30 =  84.50  │
│  ├─ Bacak 2 (12:00): 45 TL × 1.30 =  58.50  │
│  ├─ Bacak 3 (18:00): 70 TL × 1.30 =  91.00  │
│  ├─ Bekleme ücreti (tahmini):        12.00   │
│  └─ TOPLAM:                        246.00 TL │
│                                              │
│  [  ✅ ONAYLA ve BLOKE ET  ]                │
│                                              │
│  ⚠️ Bloke: 246.00 TL (bakiyeniz: 500.00 TL) │
└──────────────────────────────────────────────┘
```

### 22.5 Veritabanı

```sql
CREATE TABLE taxi_planned_routes (
    id                  UUID PRIMARY KEY,
    customer_id         UUID NOT NULL REFERENCES users(id),
    plan_date           DATE NOT NULL,                        -- planın yapıldığı gün
    route_date          DATE NOT NULL,                        -- yolculuk günü
    status              VARCHAR(20) DEFAULT 'pending',        -- pending, active, completed, cancelled
    
    total_legs          INTEGER NOT NULL CHECK(total_legs BETWEEN 1 AND 5),
    total_fee           DECIMAL(10,2) NOT NULL,               -- %30 ekli toplam
    blocked_fee         DECIMAL(10,2) NOT NULL,               -- bloke edilen tutar
    collected_fee       DECIMAL(10,2),                        -- gerçek tahsilat
    
    cancellation_time   TIMESTAMP,
    cancel_reason       VARCHAR(200),
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE taxi_route_legs (
    id                  UUID PRIMARY KEY,
    route_id            UUID NOT NULL REFERENCES taxi_planned_routes(id) ON DELETE CASCADE,
    leg_order           INTEGER NOT NULL CHECK(leg_order BETWEEN 1 AND 5),
    
    pickup_address      TEXT NOT NULL,
    pickup_lat          DECIMAL(10,7),
    pickup_lng          DECIMAL(10,7),
    dropoff_address     TEXT NOT NULL,
    dropoff_lat         DECIMAL(10,7),
    dropoff_lng         DECIMAL(10,7),
    
    scheduled_time      TIMESTAMP NOT NULL,                   -- planlanan saat
    actual_start_time   TIMESTAMP,                            -- gerçek başlangıç
    actual_end_time     TIMESTAMP,                            -- gerçek bitiş
    
    estimated_distance  DECIMAL(8,2),                         -- km
    estimated_fee       DECIMAL(10,2),                        -- normal ücret (x1.30 öncesi)
    actual_distance     DECIMAL(8,2),
    actual_fee          DECIMAL(10,2),                        -- gerçek ücret (x1.30 dahil)
    
    trip_id             UUID REFERENCES taxi_trips(id),       -- bağlı yolculuk
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    leg_status          VARCHAR(20) DEFAULT 'pending',        -- pending, waiting, active, completed, cancelled
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_planned_routes_customer ON taxi_planned_routes(customer_id);
CREATE INDEX idx_planned_routes_date ON taxi_planned_routes(route_date);
CREATE INDEX idx_route_legs_route ON taxi_route_legs(route_id);
```

### 22.6 API

```
POST    /api/v1/taxi/plan/create              # Plan oluştur (bacaklarla birlikte)
GET     /api/v1/taxi/plan/{planId}            # Plan detayı
GET     /api/v1/taxi/plan/my-plans            # Müşterinin tüm planları
PUT     /api/v1/taxi/plan/{planId}/update     # Plan güncelle (bacak ekle/çıkar)
DELETE  /api/v1/taxi/plan/{planId}/cancel     # Plan iptal
POST    /api/v1/taxi/plan/{planId}/pay        # Plan ödemesini yap (bloke)

GET     /api/v1/taxi/plan/available-drivers   # Plan için uygun şöförler
POST    /api/v1/taxi/plan/{planId}/assign     # Şöför ata (otomatik/manuel)

GET     /api/v1/taxi/plan/{planId}/leg/{legId}   # Bacak detayı
PUT     /api/v1/taxi/plan/{planId}/leg/{legId}   # Bacak güncelle

GET     /api/v1/taxi/plan/estimate            # Ücret tahmini (ön izleme)
```

### 22.7 Ücret Hesaplama Detayı

```yaml
Planlı Rota Ücretlendirme:
  Normal Taksi Ücreti (örnek):
    ├── Açılış: 25 TL
    ├── Mesafe: 20 TL/km
    └── Bekleme:  5 TL/dk (5dk ücretsiz)
  
  Planlı Rota Ücreti:
    ├── Her bacak NORMAL tarifeden hesaplanır
    ├── TOPLAM = (Bacak1 + Bacak2 + ... + Bekleme) × 1.30
    └── Örnek:
        ├── Bacak1: 65 TL  × 1.30 =  84.50
        ├── Bacak2: 45 TL  × 1.30 =  58.50
        ├── Bacak3: 70 TL  × 1.30 =  91.00
        ├── Bekleme: 10 TL × 1.30 =  13.00
        └── TOPLAM: 247.00 TL
  
  İptal Cezası:
    ├── 2+ saat kala: Ücretsiz
    ├── 30dk - 2 saat: %50 × Toplam
    └── 30dk dan az: %100 × Toplam
  
  Ek Hizmetler:
    ├── Her bacak için ayrı araç (isteğe bağlı): ×2.00
    ├── VIP araç (lüks segment): ×1.50
    └── Aynı şöför tüm bacaklar: ×1.00 (ek ücret yok)
```

### 22.8 Kısıtlamalar ve Kurallar

```yaml
Kurallar:
  Zamanlama:
    - En erken: 12 saat önceden
    - En geç: 30 gün sonrası
    - Bacak başına maksimum bekleme: 2 saat
    - Toplam plan süresi: Maksimum 12 saat (gece 22:00 - sabah 10:00 arası)
  
  Müşteri:
    - Güvenilir müşteri puanı 3.0+ olmalı
    - Son 30 günde iptal cezası yoksa
    - Yeterli bakiye (bloke için)
    - En fazla 3 aktif plan aynı anda
  
  Şöför:
    - En az 4.5 puan
    - En az 6 aylık sistem üyesi
    - Planlı rota onayı almış (özel eğitim)
    - Tüm bacaklarda müsait
  
  Ödeme:
    - Plan oluşturulurken tam bloke
    - Her bacak sonunda o bacak tahsil edilir
    - Bloke fazlası iade edilir
    - Bekleme ücreti bacak sonunda eklenir
```

---

## 23. GELİŞ ÖNCESİ KARŞILAMA REZERVASYONU (TERMİNAL/HAVALİMANI)

### 23.1 Felsefe

Müşteri, başka bir şehirden yola çıkmadan önce (uçak/otobüs/tren ile) **vardığı noktada kendisini bekleyecek bir taksi çağırabilir**. Müşteri "Yolculuğa çıkıyorum" işareti yaparak aracı önceden rezerve eder. Gecikme durumunda taksi mağdur olmasın diye **bekleme ücreti** sistemi devreye girer.

```
ÖRNEK SENARYO:
├── Müşteri: Ankara'dan İstanbul'a uçakla geliyor
├── Saat 14:00'te uçağa binmeden önce sisteme girer
├── "İstanbul'a geliyorum, havalimanında taksi beklesin" der
├── Sistem: "Uçağınız 16:30'da iniş yapacak, taksi 16:15'te orada"
├── Müşteri onaylar, rezervasyon oluşur
├── Uçak 2 saat rötar yapar → 18:30'da iner
├── Taksi 2 saat beklemiş olur
└── Müşteri: Normal ücret + 2 saat bekleme ücreti öder
```

### 23.2 Akış

```
KARŞILAMA REZERVASYONU AKIŞI:
├── ADIM 1: Müşteri "Yolculuğa Çıkıyorum" modunu açar
│   ├── Mevcut şehir: Ankara
│   ├── Varış şehri: İstanbul (Havalimanı)
│   ├── Ulaşım aracı: Uçak / Otobüs / Tren
│   ├── Tahmini varış: 16:30
│   ├── Uçuş/Sefer no (opsiyonel): "TK 1234"
│   └── Varış noktası: Sabiha Gökçen Havalimanı
│
├── ADIM 2: Sistem karşılama planı oluşturur
│   ├── Varış saatinden 15 dk önce taksi hazır (16:15)
│   ├── Taksi geliş süresi hesaba katılır
│   └── Müşteriye teklif sunulur
│
├── ADIM 3: Müşteriye bilgilendirme
│   ├── "Taksi 16:15'te sizi karşılayacak ✅"
│   ├── "Uçak rötar yaparsa: Her saat başı XXX TL bekleme ücreti"
│   ├── "İptal: En geç 1 saat öncesine kadar ücretsiz"
│   └── Müşteri onaylar
│
├── ADIM 4: Taksi ataması
│   ├── En yakın taksi havalimanına yönlendirilir
│   ├── Taksi varış noktasına 16:15'te gelir
│   └── Taksi bekleme moduna geçer
│
├── ADIM 5: Bekleme
│   ├── Taksi beklerken bekleme ücreti işlemeye başlar
│   ├── "Saat 16:30'u geçti → Bekleme ücreti: 85 TL/saat"
│   └── Müşteri uygulamadan anlık takip eder
│
└── ADIM 6: Müşteri gelir
    ├── Müşteri iniş yapar, bagaj alır, çıkışa gelir
    ├── QR okutur veya şöförü arar
    ├── Yolculuk başlar
    └── Ödeme: Normal ücret + bekleme ücreti
```

### 23.3 Bekleme Ücreti Hesaplama (Saatlik Kazanç Modeli)

Bekleme ücreti, taksicinin **ortalama saatlik kazancına** göre hesaplanır. Sistem her araç için otomatik bir bekleme ücreti çetveli çıkarır.

```
BEKLEME ÜCRETİ FORMÜLÜ:
├── Saatlik Bekleme Ücreti = (Son 30 günlük ortalama günlük kazanç / Ortalama çalışma saati) × 0.80
│
├── ÖRNEK HESAPLAMA:
│   ├── Araç son 30 günde: 18.000 TL kazanmış
│   ├── 25 gün çalışmış
│   ├── Günlük ortalama: 720 TL
│   ├── Günde ortalama 8 saat çalışmış
│   ├── Saatlik kazanç: 720 / 8 = 90 TL/saat
│   └── Bekleme ücreti: 90 × 0.80 = 72 TL/saat
│
├── MİNİMUM / MAKSİMUM:
│   ├── Minimum bekleme ücreti: 50 TL/saat
│   ├── Maksimum bekleme ücreti: 150 TL/saat
│   └── İlk 15 dk bekleme: ÜCRETSİZ (inis + bagaj süresi)
│
└── GÜNCELLEME:
    ├── Bekleme ücreti her gece otomatik yeniden hesaplanır
    ├── Son 30 günlük veri kullanılır
    └── Yeni araçlar için: Sistem ortalaması uygulanır
```

```
BEKLEME ÜCRETİ ÇETVELİ (ÖRNEK):
┌─────────────────────────────────────────────────┐
│  SAATLİK BEKLEME ÜCRETİ TABLOSU                 │
├─────────────────────────────────────────────────┤
│  Araç  │ Günlük Kazanç │ Saatlik │ Bekleme Ücreti│
├───────┼──────────────┼────────┼───────────────┤
│ TAK1111│ 850 TL/gün   │ 106 TL │  85 TL/saat   │
│ TAK2222│ 720 TL/gün   │  90 TL │  72 TL/saat   │
│ TAK3333│ 950 TL/gün   │ 119 TL │  95 TL/saat   │
│ TAK4444│ 600 TL/gün   │  75 TL │  60 TL/saat   │
│ TAK5555│ 1.100 TL/gün │ 138 TL │ 110 TL/saat   │
│─────────────────────────────────────────────────│
│ Sistem Ortalaması:  78 TL/saat                  │
└─────────────────────────────────────────────────┘
```

### 23.4 Müşteri Ekranları

```
"YOLCULUĞA ÇIKIYORUM" EKRANI:
┌──────────────────────────────────────────────┐
│  🧳 YOLCULUĞA ÇIKIYORUM                      │
│                                              │
│  📍 Şu an: Ankara                            │
│  🎯 Varış: İstanbul                          │
│                                              │
│  Ulaşım: ○ Uçak  ○ Otobüs  ○ Tren           │
│  Sefer no (opsiyonel): [ TK 1234     ]      │
│  Tahmini varış: [  16:30  ] 📅               │
│                                              │
│  📍 Sizi nerede karşılasın?                  │
│  ┌──────────────────────────────────┐        │
│  │ Sabiha Gökçen HAV - Dış Hatlar │        │
│  └──────────────────────────────────┘        │
│                                              │
│  🚗 Hedef noktanız:                          │
│  ┌──────────────────────────────────┐        │
│  │ Kadıköy, İstanbul                │        │
│  └──────────────────────────────────┘        │
│                                              │
│  [ KARŞILAMA PLANI OLUŞTUR ]                 │
└──────────────────────────────────────────────┘
```

```
KARŞILAMA ONAY EKRANI:
┌──────────────────────────────────────────────┐
│  ✅ KARŞILAMA PLANIN HAZIR                   │
│                                              │
│  🚗 34 TAK 1234 — Renault Megane            │
│  👤 Mehmet Y. ⭐ 4.6                         │
│                                              │
│  📍 Varış noktası: Sabiha Gökçen Havalimanı │
│  🕐 Taksi orada: 16:15                       │
│  ⏱ Uçağınız iniyor: 16:30                   │
│  🎯 Hedef: Kadıköy                           │
│                                              │
│  ─── ÜCRET DETAYI ───                      │
│  ├─ Normal yolculuk:              185 TL     │
│  ├─ Bekleme (ilk 15dk):          ÜCRETSİZ   │
│  ├─ Ek bekleme (sonraki her saat): 72 TL   │
│  └─ TOPLAM (tahmini):            185 TL     │
│                                              │
│  ⚠️ UÇAĞINIZ RÖTAR YAPARSA:                 │
│  ├─ 30 dk rötar: +0 TL (ilk 15dk ücretsiz) │
│  ├─ 1 saat rötar: +54 TL                    │
│  ├─ 2 saat rötar: +144 TL                   │
│  └─ 3 saat rötar: +216 TL                   │
│                                              │
│  "Uçağınızın rötar durumuna göre             │
│   bekleme ücreti işler. Onaylıyor musunuz?"  │
│                                              │
│  [ ✅ ONAYLIYORUM, ÇAĞIR ]  [ ❌ VAZGEÇ ]   │
└──────────────────────────────────────────────┘
```

```
RÖTAR TAKİP EKRANI:
┌──────────────────────────────────────────────┐
│  🧳 YOLCULUK TAKİBİ                          │
│                                              │
│  ✈️ TK 1234 — Ankara → İstanbul            │
│                                              │
│  🟢 Uçağınız zamanında: 16:30               │
│  ─────────────────────────────────────────   │
│                                              │
│  🚗 Taksi bekliyor: 34 TAK 1234             │
│  📍 Sabiha Gökçen - Dış Hatlar             │
│                                              │
│  ⏱ Bekleme süresi: 25 dk                    │
│  💰 Bekleme ücreti: 12 TL                    │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  ⏳ UÇAĞINIZ 25 DK ÖNCE İNDİ            ││
│  │  Çıkış kapısına gelmeniz yaklaşık       ││
│  │  15 dk sürecektir.                       ││
│  │  Bekleme ücreti: 0 TL (ilk 15 dk)      ││
│  └──────────────────────────────────────────┘│
│                                              │
│  📞 Şöför: "Merhaba, çıkıştayım, sizi      ││
│     bekliyorum."                             ││
└──────────────────────────────────────────────┘
```

### 23.5 Şöför Ekranı

```
ŞÖFÖR KARŞILAMA EKRANI:
┌──────────────────────────────────────────────┐
│  🟢 BEKLEME MODUNDA — KARŞILAMA              │
│                                              │
│  🧳 Müşteri: Ayşe Demir                      │
│  ✈️ TK 1234 — Ankara → İstanbul            │
│  🕐 İniş: 16:30  |  Bekleme başlangıcı: 16:15│
│  📍 Sabiha Gökçen - Dış Hatlar             │
│                                              │
│  ⏱ Bekleme süresi: 25 dk                    │
│  💰 Bekleme ücreti: 12 TL (72 TL/saat)      │
│  💰 Normal yolculuk: 185 TL                  │
│  ─────────────────────────────────────────   │
│  💰 TOPLAM TAHMİNİ: 197 TL                  │
│                                              │
│  🟢 Uçak zamanında indi                      │
│  📞 Müşteri: "Bagaj alıyorum, 10 dk"       │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  [ ✅ MÜŞTERİ GELDİ → YOLCULUĞU BAŞLAT ]││
│  │  [ ❌ İPTAL (müşteri gelmezse) ]        ││
│  └──────────────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

### 23.6 Bekleme Ücreti Hesaplama Detayı

```yaml
Bekleme Ücreti Hesaplama Kuralları:
  Veri Kaynağı:
    - Son 30 günlük çalışma istatistiği
    - Günlük kazanç / çalışılan gün sayısı
    - Günlük çalışma saati (sistem otomatik hesaplar)
    - Yeni araç (<10 gün): Sistem ortalaması kullanılır
  
  Formül:
    - Günlük Ortalama = Son 30 gün toplam kazanç / Çalışılan gün
    - Saatlik Kazanç = Günlük Ortalama / Ortalama çalışma saati
    - Bekleme Ücreti = Saatlik Kazanç × 0.80 (müşteri lehine %20 indirim)
  
  Ücretsiz Süre:
    - İlk 15 dk bekleme her zaman ücretsiz
    - Bu, iniş + yürüme + bagaj alma süresini kapsar
    - 15 dk'yı geçen her dakika için hesaplanır
  
  Tavan:
    - Maksimum bekleme: 4 saat (sonrası şöför iptal edebilir)
    - Maksimum bekleme ücreti: Tavan × saatlik ücret
    - Örnek: 4 saat × 72 TL = 288 TL bekleme ücreti
  
  Ödeme:
    - Bekleme ücreti ana yolculuk ücretine eklenir
    - Tek seferde tahsil edilir
    - Bekleme ücretinden sistem komisyonu alınmaz (tamamı şöföre)
  
  Şöför İsteği (Beklememe ve Ceza Puanı):
    - Şöför beklemek İSTEMEZSE bekleme ücreti uygulanmaz
    - Şöför: "Ben beklemem, başka araç çağırın" diyebilir
    - Bu durumda müşteri HİÇBİR bekleme ücreti ödemez
    - ANCAK şöförün bu kararı bir CEZA PUANI düşümü ile sonuçlanır
    - Sistem başka bir taksi yönlendirir (varsa)
    
    Ceza Puanı Hesaplama (Dinamik):
    ├── Ceza = Temel Ceza × Zorluk Katsayısı
    │
    ├── Temel Ceza: -5 puan
    │
    ├── Zorluk Katsayısı:
    │   ├── Gündüz (08:00-20:00):       ×1.0  → -5 puan
    │   ├── Akşam (20:00-00:00):        ×3.0  → -15 puan
    │   ├── Gece (00:00-06:00):         ×10.0 → -50 puan
    │   ├── Sabah erken (06:00-08:00):  ×5.0  → -25 puan
    │   ├── Yağmur/kar/kötü hava:       ×2.0  → Ek çarpan
    │   ├── Resmi tatil / özel gün:     ×3.0  → Ek çarpan
    │   ├── Şehir dışı / tenha bölge:   ×4.0  → Ek çarpan
    │   └── Müşteri engelli/yaşlı/çocuklu: ×2.0 → Ek çarpan
    │
    │   ÖRNEK HESAPLAMALAR:
    │   ├── Gündüz, güneşli, şehir içi:   -5 × 1.0 = -5 puan
    │   ├── Gece 02:00, yağmurlu:         -5 × 10 × 2 = -100 puan
    │   ├── Akşam 22:00, tatil günü:      -5 × 3 × 3 = -45 puan
    │   └── Sabah 07:00, tenha bölge:     -5 × 5 × 4 = -100 puan
    
    Maksimum Ceza: -100 puan (alt sınır)
    Minimum Ceza: -5 puan (üst sınır)
    
    Şöför cezayı görür ve kabul ederse işlemi onaylar
    "Bu müşteriyi bırakırsanız -45 puan kaybedersiniz. Onaylıyor musunuz?"
```

### 23.7 Rötar Durumu ve İptal

```
RÖTAR VE İPTAL YÖNETİMİ:
├── MÜŞTERİ İPTALİ:
│   ├── Varıştan 1 saat öncesine kadar: Ücretsiz iptal
│   ├── Varıştan 30 dk - 1 saat: %50 bekleme ücreti
│   │     (bu durumda taksi yola çıktıysa)
│   └── Varıştan 30 dk'dan az: Tam bekleme ücreti (1 saat)
│
├── RÖTAR DURUMU:
│   ├── Sistem (mümkünse) uçuş/sefer bilgisini API'den takip eder
│   ├── Rötar tespit edilince:
│   │   ├── Şöföre bildirim: "Uçak 1 saat rötarlı, bekle" 
│   │   ├── Müşteriye bildirim: "Uçağınız rötarlı, bekleme ücreti başladı"
│   │   └── Müşteri onayı istenir: "Beklemeye devam edelim mi?"
│   │       ├── EVET → Bekleme devam, ücret işler
│   │       └── HAYIR → İptal, sadece o ana kadar bekleme ücreti
│   └── Rötar yoksa: Normal akış devam
│
├── ŞÖFÖR İPTALİ:
│   ├── Şöför maksimum 15 dk bekler (müşteri gelmezse)
│   ├── 15 dk sonra "Müşteri gelmedi" bildirimi
│   ├── 15 dk bekleme ücreti müşteriden alınır (ücretsiz süre doldu)
│   └── Şöför yeni göreve yönlendirilir
│
└── MÜŞTERİ GELMEZSE:
    ├── 15 dk ücretsiz bekleme
    ├── 15 dk sonra her dk ücretli
    ├── 30 dk sonunda sistem şöföre "İptal et" önerir
    └── Müşteri: Bekleme ücreti + Bölüm 18 cezası
```

### 23.8 Veritabanı

```sql
CREATE TABLE taxi_arrival_bookings (
    id                  UUID PRIMARY KEY,
    customer_id         UUID NOT NULL REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    -- Yolculuk bilgisi
    departure_city      VARCHAR(100) NOT NULL,            -- Kalkış şehri
    arrival_city        VARCHAR(100) NOT NULL,            -- Varış şehri
    arrival_point       TEXT NOT NULL,                    -- Havalimanı / terminal / otogar
    arrival_point_lat   DECIMAL(10,7),
    arrival_point_lng   DECIMAL(11,7),
    destination_address TEXT,                             -- Nereye gidilecek
    destination_lat     DECIMAL(10,7),
    destination_lng     DECIMAL(11,7),
    
    -- Ulaşım
    transport_type      VARCHAR(20) NOT NULL,             -- flight, bus, train
    transport_code      VARCHAR(30),                      -- TK1234, sefer no
    
    -- Zamanlama
    estimated_arrival   TIMESTAMP NOT NULL,               -- Tahmini varış
    actual_arrival      TIMESTAMP,                        -- Gerçek varış
    driver_arrival      TIMESTAMP,                        -- Şöförün varışı
    waiting_started_at  TIMESTAMP,                        -- Bekleme başlangıcı
    waiting_ended_at    TIMESTAMP,                        -- Bekleme bitişi
    
    -- Ücret
    trip_fee            DECIMAL(10,2),                    -- Normal yolculuk ücreti
    waiting_fee_rate    DECIMAL(10,2),                    -- Saatlik bekleme ücreti
    waiting_minutes     INTEGER DEFAULT 0,                -- Ücretli bekleme (15dk sonrası)
    total_waiting_fee   DECIMAL(10,2),
    total_fee           DECIMAL(10,2),
    
    -- Durum
    status              VARCHAR(30) DEFAULT 'pending',    -- pending, waiting, active, completed, cancelled
    cancel_reason       VARCHAR(200),
    cancelled_by        VARCHAR(20),                      -- customer, driver, system
    
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_arrival_bookings_customer ON taxi_arrival_bookings(customer_id);
CREATE INDEX idx_arrival_bookings_status ON taxi_arrival_bookings(status);
CREATE INDEX idx_arrival_bookings_arrival ON taxi_arrival_bookings(estimated_arrival);
```

### 23.9 API

```
POST   /api/v1/taxi/arrival/create                    # Karşılama rezervasyonu oluştur
GET    /api/v1/taxi/arrival/{bookingId}                # Rezervasyon detayı
PUT    /api/v1/taxi/arrival/{bookingId}/update         # Güncelle (varış saati, adres)
POST   /api/v1/taxi/arrival/{bookingId}/cancel         # İptal
POST   /api/v1/taxi/arrival/{bookingId}/confirm        # Müşteri geldi onayı
POST   /api/v1/taxi/arrival/{bookingId}/no-show        # Müşteri gelmedi

GET    /api/v1/taxi/arrival/{bookingId}/waiting-status  # Bekleme durumu + ücret
GET    /api/v1/taxi/arrival/my-bookings                 # Müşterinin karşılama rezervasyonları

POST   /api/v1/taxi/arrival/{bookingId}/delay           # Rötar bildir (sistem/müşteri)
POST   /api/v1/taxi/arrival/{bookingId}/extend-waiting  # Bekleme süresi uzat

GET    /api/v1/taxi/driver/waiting-rate                 # Şöförün saatlik bekleme ücreti
```

### 23.10 Kısıtlamalar

```yaml
Karşılama Rezervasyonu Kuralları:
  Müşteri:
    - Sistemde kayıtlı ve aktif olmalı
    - Yeterli bakiye (minimum: normal ücret + 2 saat bekleme)
    - Güvenilir müşteri puanı 2.5+
    - Son 30 günde iptal cezası yok
  
  Şöför:
    - En az 4.0 puan
    - En az 30 günlük sistem üyesi
    - Bekleme ücreti hesaplanabilir (10+ gün veri)
    - Araç terminal/havalimanına ulaşabilir olmalı
  
  Zaman:
    - En erken: 2 saat önceden rezervasyon
    - En geç: 7 gün sonrasına rezervasyon
    - Maksimum bekleme: 4 saat
    - İptal: 1 saat öncesine kadar ücretsiz
  
  Ödeme:
    - Normal ücret + bekleme ücreti (varsa)
    - Bekleme ücreti sadece 15 dk sonrası için
    - Bekleme ücreti tavanı: 4 saatlik ücret
    - Ödeme yolculuk bitince tek seferde
  
  Beklememe Hakkı ve Ceza Puanı:
    - Şöför isterse beklemeyi reddedebilir (zorunlu değil)
    - Reddederse müşteriden HİÇBİR bekleme ücreti alınmaz
    - ANCAK şöför dinamik ceza puanı kaybeder:
      ├── Gündüz: -5 puan
      ├── Gece / zor durum: -100 puana kadar
      └── Hesaplama: Temel -5 × zorluk katsayısı
    - Şöför cezayı görüp onaylarsa işlem gerçekleşir
    - Sistem yeni bir taksi yönlendirir (varsa)
```

---

## 24. ACİL DURUM / PANİK BUTONU SİSTEMİ

### 24.1 Felsefe

Taksi şöförleri, özellikle gece vardiyasında, tek başına çalışırken soygun, sözlü/saldırı veya tehdit durumlarıyla karşılaşabilir. Bu sistem, şöförün **tek tuşla** anında yardım çağırmasını sağlar.

### 24.2 Panik Butonu Türleri

```
PANİK BUTONU TETİKLEME YÖNTEMLERİ:
├── 1️⃣ FİZİKSEL BUTON (Araç içi, direksiyon altı)
│   ├── Kablosuz, gizli konumlandırma
│   ├── Üzerine basınca sessiz modda sinyal
│   └── Şöförün fark edilmeden yardım çağırması
│
├── 2️⃣ UYGULAMA İÇİ BUTON
│   ├── Şöför uygulamasında büyük kırmızı buton
│   ├── "Aciliyet Seviyesi" seçimi: 1-2-3
│   ├── 3 saniye basılı tutunca tetiklenir (yanlışlıkla basmayı önler)
│   └── Sesli komut: "Yardım!" kelimesi algılanınca otomatik tetikleme
│
├── 3️⃣ AKILLI TETİKLEME (Otomatik)
│   ├── Araç anormal yavaşlama/durma → olası kavga/saldırı
│   ├── Şöförün telefonu/aleti aniden kapanırsa
│   ├── Araç rotasından çok saparsa (GPS)
│   ├── Belirli süre hareketsiz kalırsa (gece, tenha bölge)
│   └── Yüksek ses / bağırma (telefon mikrofonu)
│
└── 4️⃣ GİZLİ İŞARET
    ├── Şöför belirlenen bir kelimeyi söyler ("abi bakar mısın?")
    ├── Yolcuya belli etmeden yardım çağırma
    └── Sistem tanıdık olmayan rotayı kontrol eder
```

### 24.3 Akış

```
PANİK TETİKLENİNCE:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  🚨 PANİK BUTONU TETİKLENDİ                                  │
│                                                              │
│  ADIM 1: Sistem kaydı                                        │
│  ├── Şöför ID, Araç, Konum kaydedilir                       │
│  ├── Zaman damgası vurulur                                   │
│  └── Aciliyet seviyesi kaydedilir                           │
│                                                              │
│  ADIM 2: Bildirim zinciri başlar                             │
│  ├── 155 Polis İmdat (otomatik SMS + konum linki)            │
│  ├── En yakın polis noktası bildirilir                       │
│  ├── Durak yöneticisine bildirim                             │
│  ├── Diğer yakın taksicilere uyarı                           │
│  └── Sistem admin paneline düşer                             │
│                                                              │
│  ADIM 3: Canlı takip                                         │
│  ├── Araç GPS'i canlı paylaşıma açılır (gizli)              │
│  ├── Ses kaydı başlatılır (telefon mikrofonu)                │
│  ├── Kamera görüntüsü buluta akar                              │
│  └── 5 saniyede bir konum güncellenir                        │
│                                                              │
│  ADIM 4: Müdahale                                              │
│  ├── Polis/yakın taksiciler olay yerine yönlendirilir        │
│  └── Durum "güvenli" olana kadar sistem aktif kalır          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 24.4 Şöför Ekranı

```
ŞÖFÖR UYGULAMA ANA EKRANI (Gizli Buton):
┌──────────────────────────────────────────────┐
│  🟢 AKTİF                                     │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │  🚨 PANİK                                ││
│  │  (3 saniye basılı tut)                   ││
│  │  ┌─────┐                                 ││
│  │  │  ⚠️  │                                ││
│  │  └─────┘                                 ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Aciliyet:                                    │
│  ○ 1 - Şüpheli durum                         │
│  ○ 2 - Tehdit / soygun                       │
│  ● 3 - Hayati tehlike                        │
│                                              │
│  Tetiklenince:                                │
│  ✅ Polis bilgilendirilecek                   │
│  ✅ Konum paylaşılacak                        │
│  ✅ Ses kaydı başlayacak                      │
│                                              │
└──────────────────────────────────────────────┘
```

### 24.5 Veritabanı

```sql
CREATE TABLE taxi_panic_alerts (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    trip_id             UUID REFERENCES taxi_trips(id) NULL,
    
    alert_level         INTEGER NOT NULL,                     -- 1, 2, 3
    trigger_type        VARCHAR(30) NOT NULL,                 -- physical_button, app_button, auto, voice
    trigger_location    GEOGRAPHY(POINT) NOT NULL,
    
    status              VARCHAR(30) DEFAULT 'active',         -- active, responding, resolved, false_alarm
    resolved_at         TIMESTAMP,
    police_notified     BOOLEAN DEFAULT FALSE,
    police_arrival_time TIMESTAMP,
    
    audio_recording_url VARCHAR(500),
    camera_footage_url  VARCHAR(500),
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_panic_alerts_status ON taxi_panic_alerts(status);
CREATE INDEX idx_panic_alerts_driver ON taxi_panic_alerts(driver_id);
```

### 24.6 Sahte Alarm Yönetimi

```
SAHTE ALARM KORUMASI:
├── Yanlışlıkla tetikleme: Şöför 30 sn içinde iptal edebilir
├── 3+ sahte alarm / ay: -5 puan + uyarı
├── 5+ sahte alarm / ay: Hesap geçici dondurulur (24 saat)
└── Gerçek alarm: Hiçbir ceza uygulanmaz, aksine teşvik puanı +1
```

### 24.7 API

```
POST   /api/v1/taxi/driver/panic/trigger      # Panik butonu tetikle
POST   /api/v1/taxi/driver/panic/{alertId}/cancel    # İptal (yanlış alarm)
GET    /api/v1/taxi/driver/panic/{alertId}/status   # Durum sorgula
GET    /api/v1/taxi/admin/panic/active         # Aktif alarmlar (admin)
POST   /api/v1/taxi/admin/panic/{alertId}/resolve    # Alarm çözüldü
```

---

## 25. AKARYAKIT İNDİRİM VE İSTASYON AĞI

### 25.1 Felsefe

Taksicinin en büyük gider kalemi yakıttır (%30-40). Sistem, anlaşmalı akaryakıt istasyonlarında **özel taksi indirimi** sağlayarak hem şöförün cebini korur hem de platform sadakatini artırır.

### 25.2 Anlaşma Modelleri

```
ANLAŞMA TÜRLERİ:
├── 1️⃣ YÜZDE İNDİRİM
│   ├── Her litre başına sistem kullanıcısına %5-10 indirim
│   ├── İstasyon: Opet, Shell, BP, Aytemiz, Petrol Ofisi
│   └── Örnek: Motorin 44 TL/L → Sistem taksicisi: 40 TL/L
│
├── 2️⃣ LİTRE BAŞI KOMİSYON
│   ├── İstasyon sisteme litre başı 0.50 TL komisyon öder
│   ├── Sistem bunun 0.25 TL'sini şöföre ek indirim olarak yansıtır
│   └── Kalan 0.25 TL sistem geliri
│
├── 3️⃣ AYLIK SABİT KOTA
│   ├── Şöför aylık 500L+ alırsa ekstra %3 indirim
│   ├── 1000L+ alırsa +%5 ek indirim
│   └── Karta iade olarak yansır
│
└── 4️⃣ SADAKAT PUANI
    ├── Her TL harcamaya 1 puan
    ├── 1000 puan → 1 depo yıkama
    ├── 5000 puan → 1 lastik değişimi
    └── 10000 puan → 1 bakım
```

### 25.3 Şöför Ekranı

```
YAKIT İNDİRİM EKRANI:
┌──────────────────────────────────────────────┐
│  ⛽ YAKIT FIRSATLARI                          │
│                                              │
│  En Yakın İstasyonlar:                       │
│  ┌──────────────────────────────────────────┐│
│  │ ⛽ Opet - Kadıköy                        ││
│  │ ├─ Motorin: 40.50 TL/L (normal: 44 TL)  ││
│  │ ├─ 📍 500 m · ⭐ 4.5                     ││
│  │ └─ [ YOL TARİFİ ]  [ YAKIT ALDIM ]     ││
│  └──────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────┐│
│  │ ⛽ Shell - Bostancı                      ││
│  │ ├─ Motorin: 41.20 TL/L (normal: 44 TL)  ││
│  │ ├─ 📍 1.2 km · ⭐ 4.2                    ││
│  │ └─ [ YOL TARİFİ ]  [ YAKIT ALDIM ]     ││
│  └──────────────────────────────────────────┘│
│                                              │
│  📊 Aylık Yakıt Raporu:                     │
│  ├─ Toplam harcama: 8.450 TL                 │
│  ├─ Sistem indirimi: -845 TL (%10)           │
│  └─ Kazanç: 845 TL cebinde kaldı             │
│                                              │
└──────────────────────────────────────────────┘
```

### 25.4 Veritabanı

```sql
CREATE TABLE taxi_fuel_partners (
    id                  UUID PRIMARY KEY,
    brand               VARCHAR(100) NOT NULL,             -- Opet, Shell, BP
    station_name        VARCHAR(200),
    address             TEXT,
    latitude            DECIMAL(10,7),
    longitude           DECIMAL(11,7),
    city                VARCHAR(100),
    district            VARCHAR(100),
    
    discount_percent    DECIMAL(5,2),                      -- % indirim
    commission_per_liter DECIMAL(5,2),                     -- Litre başı komisyon
    fuel_types          JSONB,                              -- ["diesel", "gasoline", "lpg"]
    
    contract_start      DATE,
    contract_end        DATE,
    is_active           BOOLEAN DEFAULT TRUE,
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE taxi_driver_fuel_purchases (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    station_id          UUID REFERENCES taxi_fuel_partners(id),
    
    fuel_type           VARCHAR(20),                       -- diesel, gasoline, lpg
    liters              DECIMAL(8,2),
    total_amount        DECIMAL(10,2),
    discount_amount     DECIMAL(10,2),
    commission_amount   DECIMAL(10,2),
    
    purchase_date       TIMESTAMP DEFAULT NOW()
);
```

### 25.5 API

```
POST   /api/v1/taxi/fuel/partners/nearby      # Yakındaki anlaşmalı istasyonlar
POST   /api/v1/taxi/fuel/purchase/record       # Yakıt alımı kaydet
GET    /api/v1/taxi/fuel/driver/report         # Şöför yakıt raporu
GET    /api/v1/taxi/fuel/driver/savings        # Toplam indirim
```

---

## 26. ÇEKİCİ / YOL YARDIM VE TAMİR AĞI

### 26.1 Felsefe

Taksi arızalandığında şöför saatlerce yol yardımı bekler. Sistem, anlaşmalı çekici ve tamirci ağı ile **30 dk içinde müdahale** vaat eder.

### 26.2 Hizmet Türleri

```
HİZMET KATEGORİLERİ:
├── 🛞 YOL YARDIMI
│   ├── Lastik patlağı (stepne değişim)
│   ├── Akü takviyesi
│   ├── Yakıt bitmesi (5L ikram)
│   ├── Kilitli kapı / anahtar içerde
│   └── Çekici çağırma
│
├── 🔧 ACİL TAMİR
│   ├── Fren arızası
│   ├── Motor arızası
│   ├── Elektrik arızası
│   ├── Soğutma sistemi
│   └── Yerinde tamir (mümkünse)
│
├── 🚛 ÇEKİCİ
│   ├── Anlaşmalı çekici firmaları
│   ├── Sabit fiyat tarifesi (km başı)
│   ├── Sistem üzerinden çağırma
│   └── Ödeme sistem cüzdanından otomatik
│
└── 🔩 TAMİRHANE
    ├── Anlaşmalı oto tamirciler
    ├── Özel taksi fiyat tarifesi
    ├── İş takip sistemi (tamir ne zaman biter?)
    └── Garantili işçilik
```

### 26.3 Akış

```
ARIZA BİLDİRİM AKIŞI:
┌────────────────────────────────────────────────┐
│  ADIM 1: Şöför "Yol Yardım" butonuna basar     │
│  ├── Arıza türü seçer (lastik, akü, motor vb.) │
│  ├── Konum otomatik alınır                      │
│  └── Fotoğraf ekler (opsiyonel)                │
│                                                 │
│  ADIM 2: Sistem en yakın hizmeti bulur          │
│  ├── Çekici: 15 dk uzaklıkta                    │
│  ├── Tamirci: 2.5 km'de                         │
│  └── Süre tahmini: 20 dk                        │
│                                                 │
│  ADIM 3: Onay ve çağrı                         │
│  ├── Şöför teklifi görür (fiyat + süre)        │
│  ├── Kabul eder → Hizmet çağrılır              │
│  └── Canlı takip başlar                        │
│                                                 │
│  ADIM 4: Hizmet tamam                          │
│  ├── Ödeme otomatik (cüzdan)                   │
│  └── Puanlama (opsiyonel)                      │
└────────────────────────────────────────────────┘
```

### 26.4 Veritabanı

```sql
CREATE TABLE taxi_roadside_partners (
    id                  UUID PRIMARY KEY,
    partner_type        VARCHAR(30) NOT NULL,               -- tow_truck, mechanic, tire
    company_name        VARCHAR(200),
    service_area        VARCHAR(100),                        -- Hizmet bölgesi
    phone               VARCHAR(20),
    latitude            DECIMAL(10,7),
    longitude           DECIMAL(11,7),
    
    has_tow_truck       BOOLEAN DEFAULT FALSE,
    has_mobile_repair   BOOLEAN DEFAULT FALSE,
    service_hours       VARCHAR(50),                         -- 7/24, 08:00-22:00
    base_fee            DECIMAL(10,2),
    km_fee              DECIMAL(5,2),
    
    is_active           BOOLEAN DEFAULT TRUE,
    rating              DECIMAL(2,1) DEFAULT 5.0,
    
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE taxi_roadside_requests (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    partner_id          UUID REFERENCES taxi_roadside_partners(id),
    
    issue_type          VARCHAR(50) NOT NULL,               -- flat_tire, battery, engine, tow
    description         TEXT,
    location            GEOGRAPHY(POINT) NOT NULL,
    photos              JSONB DEFAULT '[]',
    
    request_time        TIMESTAMP DEFAULT NOW(),
    arrival_time        TIMESTAMP,
    completion_time     TIMESTAMP,
    total_cost          DECIMAL(10,2),
    
    status              VARCHAR(30) DEFAULT 'pending',      -- pending, accepted, en_route, in_progress, completed
    payment_status      VARCHAR(20) DEFAULT 'pending',
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 26.5 API

```
POST   /api/v1/taxi/roadside/request          # Yol yardım çağrısı
GET    /api/v1/taxi/roadside/{requestId}       # Durum sorgula
POST   /api/v1/taxi/roadside/{requestId}/cancel  # İptal
GET    /api/v1/taxi/roadside/nearby           # Yakındaki hizmetler
```

---

## 27. KAZA / HASAR BİLDİRİM SİSTEMİ

### 27.1 Felsefe

Kaza anında şöför ne yapacağını şaşırır. Sistem, adım adım yönlendirme ile **kaza tutanağı, sigorta bildirimi ve çekici çağırma** işlemlerini tek bir akışta toplar.

### 27.2 Kaza Bildirim Akışı

```
KAZA BİLDİRİM SİHİRBAZI:
┌────────────────────────────────────────────────┐
│  ADIM 1: Kaza Bildir                          │
│  ├── "Kaza Yaptım" butonuna bas               │
│  ├── Konum otomatik                            │
│  └── Araç durumu: çalışıyor / çalışmıyor      │
│                                                 │
│  ADIM 2: Can güvenliği kontrolü                │
│  ├── Yaralı var mı? → 112 çağrılsın mı?       │
│  └── Polis gerekli mi? → 155 çağrılsın mı?    │
│                                                 │
│  ADIM 3: Fotoğraf + Video                      │
│  ├── Aracın ön/arka/yandan fotoğrafları        │
│  ├── Karşı araç plakası                        │
│  ├── Kaza yeri genel görünüm                   │
│  └── Hasar bölgeleri yakın çekim              │
│                                                 │
│  ADIM 4: Karşı taraf bilgileri                 │
│  ├── Plaka, marka, model                       │
│  ├── Sigorta bilgisi (varsa)                   │
│  ├── İsim ve telefon                          │
│  └── Ehliyet fotoğrafı                         │
│                                                 │
│  ADIM 5: Tutanak oluştur                       │
│  ├── Kaza krokisi (basit çizim)                │
│  ├── Kaza açıklaması                           │
│  ├── Hasar tahmini (AI ile fotoğraftan)        │
│  └── PDF tutanak oluştur + imzala             │
│                                                 │
│  ADIM 6: Sigorta bildirimi                     │
│  ├── Otomatik sigorta şirketine bildirim       │
│  ├── Dosya numarası al                         │
│  └── Eksper yönlendirmesi                     │
│                                                 │
│  ADIM 7: Çekici (gerekirse)                    │
│  ├── En yakın çekici çağır                    │
│  └── Tamirhaneye yönlendir                    │
└────────────────────────────────────────────────┘
```

### 27.3 Veritabanı

```sql
CREATE TABLE taxi_accident_reports (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    trip_id             UUID REFERENCES taxi_trips(id) NULL,
    
    accident_time       TIMESTAMP NOT NULL,
    location            GEOGRAPHY(POINT) NOT NULL,
    has_injuries        BOOLEAN DEFAULT FALSE,
    police_notified     BOOLEAN DEFAULT FALSE,
    ambulance_called    BOOLEAN DEFAULT FALSE,
    
    photos              JSONB DEFAULT '[]',
    description         TEXT,
    sketch_data         JSONB,                               -- Kaza krokisi
    
    other_vehicle_plate VARCHAR(20),
    other_driver_name   VARCHAR(100),
    other_phone         VARCHAR(20),
    other_insurance     VARCHAR(200),
    
    damage_estimate     DECIMAL(10,2),
    report_pdf_url      VARCHAR(500),
    
    insurance_claim_id  VARCHAR(100),
    insurance_status    VARCHAR(30),
    
    status              VARCHAR(30) DEFAULT 'open',          -- open, processing, closed
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 27.4 API

```
POST   /api/v1/taxi/accident/report           # Kaza bildir
POST   /api/v1/taxi/accident/{reportId}/photos  # Fotoğraf ekle
POST   /api/v1/taxi/accident/{reportId}/sketch  # Kroki ekle
GET    /api/v1/taxi/accident/{reportId}         # Rapor detayı
POST   /api/v1/taxi/accident/{reportId}/submit-to-insurance # Sigortaya bildir
```

---

## 28. VARDİYA PAZARI (SHIFT MARKETPLACE)

### 28.1 Felsefe

Şöför hasta olunca, izin alınca veya vardiyasını devretmek isteyince **boş vardiyayı paylaşabileceği** bir pazar yeri. Diğer şöförler boş vardiyalara talip olabilir.

### 28.2 Vardiya İlan Tipleri

```
İLAN TÜRLERİ:
├── 1️⃣ DEVRETME (Satılık Vardiya)
│   ├── "Benim vardiyamı devralacak var mı?"
│   ├── Kira bedeli: 200 TL (veya pazarlık)
│   ├── Süre: 8 saat (06:00-14:00)
│   └── Araç: 34 TAK 1234 - Renault Megane
│
├── 2️⃣ TALİP (Aranan Vardiya)
│   ├── "Bugün ek iş yapmak istiyorum"
│   ├── Müsait olduğum saatler: 14:00-22:00
│   ├── Kullandığım araç: 34 TAK 5678
│   └── Hemen başlayabilirim
│
├── 3️⃣ YEDEK HAVUZU
│   ├── Sürekli yedek şöför aranıyor
│   ├── Haftada en az 2 gün
│   └── Düzenli ek gelir
│
└── 4️⃣ ACİL DEVİR
    ├── "Şu an hastayım, 1 saat sonraki vardiyam boşalıyor"
    ├── Aciliyet: Yüksek
    └── Ek teşvik: Kira 50 TL indirimli
```

### 28.3 Akış

```
VARDİYA DEVRETME AKIŞI:
┌────────────────────────────────────────────────┐
│  ADIM 1: Şöför "Vardiyamı Devret" seçer       │
│  ├── Vardiya saati: 06:00-14:00               │
│  ├── Araç: 34 TAK 1234                        │
│  ├── Kira: 200 TL (araç sahibine)             │
│  └── Ek not: "Düzgün kullanan aranıyor"       │
│                                                 │
│  ADIM 2: İlan sisteme düşer                     │
│  ├── Bildirim: "Kadıköy'de sabah vardiyası"    │
│  ├── Uygun şöförlere push notification         │
│  └── İlan panosunda yayınlanır                  │
│                                                 │
│  ADIM 3: Talip olan şöför başvurur              │
│  ├── Şöför profili + puanı görünür             │
│  ├── "Ben talibim" butonu                       │
│  └── Araç sahibine bildirim                     │
│                                                 │
│  ADIM 4: Araç sahibi onayı                      │
│  ├── Aday şöförün puanı: 4.7 ✅                │
│  ├── Belgeler tam mı? ✅                       │
│  ├── Onay → Vardiya atanır                     │
│  └── Kira: 200 TL otomatik kesilecek            │
│                                                 │
│  ADIM 5: Vardiya başlar                         │
│  ├── Yeni şöför vardiyaya başlar               │
│  ├── Devreden şöför kira yükünden kurtulur      │
│  └── Araç sahibi kirasını alır (değişen yok)   │
└────────────────────────────────────────────────┘
```

### 28.4 Veritabanı

```sql
CREATE TABLE taxi_shift_marketplace (
    id                  UUID PRIMARY KEY,
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    original_driver_id  UUID REFERENCES taxi_drivers(id),
    
    shift_date          DATE NOT NULL,
    shift_start         TIME NOT NULL,
    shift_end           TIME NOT NULL,
    rental_fee          DECIMAL(10,2),                       -- Kira bedeli
    
    listing_type        VARCHAR(30) NOT NULL,                -- transfer, request, backup, urgent
    description         TEXT,
    status              VARCHAR(30) DEFAULT 'open',          -- open, matched, completed, cancelled
    
    applicant_id        UUID REFERENCES taxi_drivers(id) NULL,
    matched_at          TIMESTAMP,
    approved_by_owner   BOOLEAN DEFAULT FALSE,
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 28.5 API

```
POST   /api/v1/taxi/shift-marketplace/list     # Vardiya ilanı ver
GET    /api/v1/taxi/shift-marketplace/search    # Boş vardiya ara
POST   /api/v1/taxi/shift-marketplace/{listingId}/apply  # Talip ol
POST   /api/v1/taxi/shift-marketplace/{listingId}/approve # Onayla
POST   /api/v1/taxi/shift-marketplace/{listingId}/cancel  # İptal
GET    /api/v1/taxi/shift-marketplace/my-listings  # Kendi ilanlarım
```

---

## 29. DİJİTAL BAHŞİŞ SİSTEMİ

### 29.1 Felsefe

Nakit çağı dışındayız. Yolcu, yolculuk sonu **tek tuşla bahşiş** verebilmeli. Bahşiş şöförün cüzdanına direkt ve komisyonsuz yansır.

### 29.2 Bahşiş Tipleri

```
BAHŞİŞ YÖNTEMLERİ:
├── 1️⃣ YOLCULUK SONU (Önerili)
│   ├── Yolculuk ücreti: 185 TL
│   ├── 💪 İyi hizmet: 18.50 TL (%10)
│   ├── 🌟 Çok iyi: 27.75 TL (%15)
│   ├── 👑 Mükemmel: 37.00 TL (%20)
│   └── Özel tutar: [________] TL
│
├── 2️⃣ ÖNCE BAHŞİŞ (Önceden belirleme)
│   ├── Yolculuk başlamadan bahşiş vaadi
│   ├── Şöför: "Bahşişli yolcu" olarak görür
│   └── Öncelikli eşleşme hakkı
│
├── 3️⃣ QR İLE BAHŞİŞ
│   ├── Araç içinde şöförün QR kodu
│   ├── Yolcu kendi uygulamasından okutur
│   └── Sonradan bahşiş (yolculuk bitti ama çıkarken)
│
└── 4️⃣ TOPLU BAHŞİŞ (Durak)
    ├── Bir durağa bağlı tüm şöfölere bahşiş
    ├── "Bu durak iyi çalışıyor" genel teşekkür
    └── Eşit paylaşım
```

### 29.3 Yolcu Ekranı

```
YOLCULUK SONU BAHŞİŞ:
┌──────────────────────────────────────────────┐
│  ✅ Yolculuk Tamamlandı                       │
│  💰 Ücret: 185 TL (ödendi)                   │
│                                              │
│  ─── BAHŞİŞ EKLE ───                       │
│                                              │
│  Sürüş nasıldı?                              │
│  ┌──────┐                                    │
│  │ 💪   │  🌟   │  👑   │                    │
│  │ %10  │ %15  │ %20  │                    │
│  │ 18 TL│ 28 TL│ 37 TL│                    │
│  └──────┴──────┴──────┘                    │
│                                              │
│  veya özel: [___________] TL                 │
│                                              │
│  💡 Bahşişin %100'ü şöföre gider,            │
│  sistem komisyon almaz.                      │
│                                              │
│  [ BAHŞİŞ EKLE ]  [ GEÇ ]                    │
└──────────────────────────────────────────────┘
```

### 29.4 Veritabanı

```sql
CREATE TABLE taxi_tips (
    id                  UUID PRIMARY KEY,
    trip_id             UUID REFERENCES taxi_trips(id),
    passenger_id        UUID REFERENCES users(id),
    driver_id           UUID REFERENCES taxi_drivers(id),
    
    tip_type            VARCHAR(30) NOT NULL,               -- post_trip, pre_trip, qr, group
    amount              DECIMAL(10,2) NOT NULL,
    tip_percent         DECIMAL(5,2),                        -- %10, %15, %20
    
    passenger_note      TEXT,
    
    created_at          TIMESTAMP DEFAULT NOW()
);

ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    total_tips_today    DECIMAL(10,2) DEFAULT 0;
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    total_tips_month    DECIMAL(10,2) DEFAULT 0;
```

### 29.5 API

```
POST   /api/v1/taxi/trip/{tripId}/tip          # Bahşiş ekle
GET    /api/v1/taxi/driver/tips/today           # Günlük bahşiş
GET    /api/v1/taxi/driver/tips/month           # Aylık bahşiş
POST   /api/v1/taxi/driver/tip-qr               # QR bahşiş kodu oluştur
```

---

## 30. GÜNLÜK GELİR/GİDER DEFTERİ (MUHASEBE)

### 30.1 Felsefe

Taksi şöförleri vergi beyannamesi için gelir-gider takibi yapmak zorunda. Sistem, **otomatik kazanç kaydı + manuel gider girişi** ile yıllık muhasebeyi kolaylaştırır.

### 30.2 Gider Kategorileri

```
GİDER KATEGORİLERİ:
├── ⛽ Akaryakıt (manuel veya istasyon entegrasyonu)
├── 🔧 Bakım / Tamir
├── 🛞 Lastik
├── 🚗 Kira (otomatik, sistemden çekilir)
├── 📟 Pos Cihazı / Abonelik
├── 🌐 İletişim / İnternet
├── 🅿️ Otopark
├── 🧼 Yıkama / Temizlik
├── 🍽️ Yemek / Mola
└── 📋 Diğer (sigorta, vergi, harç)
```

### 30.3 Şöför Ekranı

```
MUHASEBE EKRANI:
┌──────────────────────────────────────────────┐
│  📊 HAZİRAN 2026 - KAZANÇ RAPORU             │
├──────────────────────────────────────────────┤
│                                              │
│  GELİR:                                       │
│  ├── Toplam yolculuk: 18.450 TL              │
│  ├── Bahşiş: 1.240 TL                        │
│  ├── Bekleme ücreti: 320 TL                  │
│  └── Toplam gelir: 20.010 TL                 │
│                                              │
│  GİDER:                                       │
│  ├── ⛽ Akaryakıt: -5.200 TL                 │
│  ├── 🚗 Kira: -6.000 TL (30 gün)             │
│  ├── 🔧 Bakım: -750 TL                       │
│  ├── 📟 Pos kirası: -150 TL                  │
│  ├── 🧼 Yıkama: -200 TL                      │
│  └── Toplam gider: -12.300 TL                │
│                                              │
│  💰 NET: 7.710 TL                            │
│                                              │
│  📋 VERGİ BEYAN ÖZETİ:                      │
│  ├── Yıllık gelir: 120.000 TL                │
│  ├── Götürü gider (%70): -84.000 TL          │
│  └── Vergiye tabi: 36.000 TL                 │
│                                              │
│  📥 [ Excel İndir ]  [ PDF İndir ]           │
└──────────────────────────────────────────────┘
```

### 30.4 Veritabanı

```sql
CREATE TABLE taxi_driver_expenses (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    expense_type        VARCHAR(30) NOT NULL,                -- fuel, maintenance, tire, rent, etc.
    amount              DECIMAL(10,2) NOT NULL,
    receipt_photo       VARCHAR(500),
    notes               TEXT,
    is_auto_recorded    BOOLEAN DEFAULT FALSE,              -- Sistem otomatik mi kaydetti?
    
    expense_date        DATE NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE taxi_driver_monthly_reports (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    year                INTEGER NOT NULL,
    month               INTEGER NOT NULL,
    
    total_earnings      DECIMAL(12,2) DEFAULT 0,
    total_tips          DECIMAL(10,2) DEFAULT 0,
    total_expenses      DECIMAL(12,2) DEFAULT 0,
    net_earnings        DECIMAL(12,2) DEFAULT 0,
    
    trip_count          INTEGER DEFAULT 0,
    total_km            DECIMAL(10,2) DEFAULT 0,
    total_hours         DECIMAL(8,2) DEFAULT 0,
    
    generated_at        TIMESTAMP DEFAULT NOW(),
    UNIQUE(driver_id, year, month)
);
```

### 30.5 API

```
POST   /api/v1/taxi/driver/expense/add        # Gider ekle
GET    /api/v1/taxi/driver/expense/list        # Gider listesi
GET    /api/v1/taxi/driver/report/daily        # Günlük rapor
GET    /api/v1/taxi/driver/report/monthly      # Aylık rapor
GET    /api/v1/taxi/driver/report/yearly       # Yıllık rapor
POST   /api/v1/taxi/driver/report/export       # Excel/PDF dışa aktar
```

---

## 31. OTOPARK / PARK İNDİRİMLERİ

### 31.1 Felsefe

İstanbul ve büyük şehirlerde taksi park yeri bulmak büyük sorun. Sistem, anlaşmalı otoparklarda **taksilere özel park alanı ve indirim** sağlar.

### 31.2 Otopark Tipleri

```
OTOPARK TÜRLERİ:
├── 1️⃣ TAKSİ DURAĞI OTOPARKI
│   ├── Durağa bağlı araçlar için ücretsiz
│   ├── Gece parkı (vardiya sonu)
│   └── Sadece durak araçlarına
│
├── 2️⃣ ANA OTOPARK (Sistem anlaşmalı)
│   ├── Tüm sistem taksilerine %50 indirim
│   ├── 7/24 güvenlik + kamera
│   ├── Araç yıkama hizmeti dahil
│   └── Aylık abonelik: 500 TL (sınırsız)
│
├── 3️⃣ CADDE PARK (Belediye anlaşmalı)
│   ├── Taksi plakalarına ücretsiz park
│   ├── Sarı çizgi alanları
│   └── Belediye ile entegrasyon
│
└── 4️⃣ Geçici Park (Yolculuk arası)
    ├── 15 dk ücretsiz
    ├── 1 saat: 10 TL
    └── Otomatik ödeme
```

### 31.3 API

```
GET    /api/v1/taxi/parking/nearby             # Yakındaki taksi park alanları
GET    /api/v1/taxi/parking/{parkingId}        # Park detayı
POST   /api/v1/taxi/parking/{parkingId}/enter # Park giriş kaydı
POST   /api/v1/taxi/parking/{parkingId}/exit  # Park çıkış
```

---

## 32. ARAÇ YIKAMA VE BAKIM İNDİRİMLERİ

### 32.1 Felsefe

Araç temizliği puanı sistemi var ama temizlik masrafı şöföre ait. Anlaşmalı yıkamacılar ile **taksilere özel indirimli yıkama** sağlanır.

### 32.2 Hizmet Kategorileri

```
YIKAMA PAKETLERİ:
├── 🚿 DIŞ YIKAMA: 50 TL (normal: 100 TL)
├── 🧼 İÇ YIKAMA (süpürme + silme): 80 TL (normal: 150 TL)
├── ✨ FULL DETAY: 150 TL (normal: 300 TL)
├── 🧴 OZON/KOKU GİDERME: 30 TL
└── 🎀 PAKET (Dış + İç + Ozon): 200 TL (normal: 400 TL)
```

### 32.3 API

```
GET    /api/v1/taxi/car-wash/nearby           # Yakındaki anlaşmalı yıkama
POST   /api/v1/taxi/car-wash/book             # Randevu al
POST   /api/v1/taxi/car-wash/wash-record      # Yıkama kaydet
GET    /api/v1/taxi/car-wash/discounts        # İndirimler
```

---

## 33. KADIN YOLCU GÜVENLİK MODU

### 33.1 Felsefe

Kadın yolcuların taksi kullanırken kendini güvende hissetmesi için **ek güvenlik katmanı**. Bu mod aktifken canlı takip, acil durum paylaşımı ve kadın şöför tercihi önceliklidir.

### 33.2 Güvenlik Özellikleri

```
GÜVENLİK MODU ÖZELLİKLERİ:
├── 1️⃣ CANLI TAKİP PAYLAŞIMI
│   ├── Yolculuk başlayınca 3 güvendiği kişiye link gider
│   ├── Canlı konum haritası
│   ├── Tahmini varış süresi
│   └── Acil durumda tek tuşla uyarı
│
├── 2️⃣ KADIN ŞÖFÖR TERCİHİ
│   ├── Mümkünse kadın şöför eşleştirilir
│   ├── Kadın şöför yoksa en yüksek puanlı erkek
│   └── Şöför puanı 4.5+ olmalı
│
├── 3️⃣ SESLİ UYARI
│   ├── Yolculuk anormal rotadaysa uyarı
│   ├── Araç durduysa / yavaşladıysa kontrol
│   └── "Her şey yolunda mı?" bildirimi
│
├── 4️⃣ ACİL DURUM BUTONU
│   ├── Ana ekranda büyük kırmızı buton
│   ├── Polis + güvendiği kişilere anlık bildirim
│   └── Telefon otomatik kayıt başlatır
│
└── 5️⃣ YOLCULUK RAPORU
    ├── Yolculuk bittiğinde güvendiği kişilere özet
    ├── "Varıldı" bildirimi
    └── 24 saat sonra rapor silinir (gizlilik)
```

### 33.3 Veritabanı

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    safety_mode         BOOLEAN DEFAULT FALSE;               -- Güvenlik modu aktif mi?
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    safety_contacts     JSONB DEFAULT '[]';                  -- Güvendiği kişiler
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    prefer_female_driver BOOLEAN DEFAULT FALSE;              -- Kadın şöför tercihi
```

### 33.4 API

```
POST   /api/v1/taxi/passenger/safety-mode/toggle  # Güvenlik modu aç/kapa
PUT    /api/v1/taxi/passenger/safety-contacts     # Güvendiği kişiler
POST   /api/v1/taxi/trip/{tripId}/share-location  # Canlı konum paylaş
GET    /api/v1/taxi/trip/{tripId}/safety-status   # Güvenlik durumu
POST   /api/v1/taxi/trip/{tripId}/panic           # Acil durum
```

---

## 34. MOLA NOKTALARI / SOSYAL ALAN HARİTASI

### 34.1 Felsefe

Taksiciler 8-16 saat direksiyon başında. Çay içecek, yemek yiyecek, camiye gidecek, tuvalet bulacak noktaları **harita üzerinde görmeleri** gerekir.

### 34.2 Nokta Türleri

```
MOLA NOKTASI TÜRLERİ:
├── ☕ ÇAY OCAĞI / KAHVE
│   ├── "Falanca çaycı - taksicilere %20 indirim"
│   └── Şöför puanı: 4.5 ⭐
│
├── 🍽️ LOKANTA / KÖFTECİ
│   ├── "Taksi esnafı menüsü: 120 TL"
│   └── Hızlı servis (15 dk içinde)
│
├── 🕌 CAMİ
│   ├── Abdestlik + park yeri
│   └── 5 vakit namaz saatleri
│
├── 🚻 WC / TUVALET
│   ├── Temizlik puanı
│   └── Ücretli/ücretsiz
│
├── 🛌 UYUMA / DİNLENME
│   ├── Güvenli park + yataklı kabin
│   └── 2 saatlik: 100 TL
│
└── 💪 SPOR / EGZERSİZ
    ├── Şöför sağlığı için
    └── Anlaşmalı spor salonları
```

### 34.3 API

```
GET    /api/v1/taxi/rest-points/nearby         # Yakındaki mola noktaları
GET    /api/v1/taxi/rest-points/{pointId}      # Nokta detayı
POST   /api/v1/taxi/rest-points/review         # Nokta değerlendir
```

---

## 35. DİL ROZETLERİ

### 35.1 Felsefe

Turistik bölgelerde (Sultanahmet, Taksim, Antalya, Kapadokya) yabancı dil bilen şöförler daha çok tercih edilir. Dil rozetleri sayesinde **yolcu kendi dilinde hizmet alabilir**.

### 35.2 Dil Seviyeleri

```
DİL ROZET SEVİYELERİ:
├── 🟢 TEMEL (A1-A2)
│   ├── "Hello, where to go?"
│   └── Basit iletişim
│
├── 🟡 ORTA (B1-B2)
│   ├── "Which route do you prefer?"
│   └── Günlük konuşma
│
└── 🔴 İLERİ (C1-C2)
    ├── Akıcı konuşma
    └── Turist rehberliği
```

### 35.3 Veritabanı

```sql
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    languages           JSONB DEFAULT '[]';                  -- [{"lang":"en","level":"intermediate"}]
ALTER TABLE taxi_drivers ADD COLUMN IF NOT EXISTS
    language_tests      JSONB DEFAULT '[]';                  -- Sınav sonuçları
```

### 35.4 API

```
PUT    /api/v1/taxi/driver/languages          # Dil bilgisi güncelle
GET    /api/v1/taxi/search?lang=en            # Dil filtresi ile ara
POST   /api/v1/taxi/driver/language-test     # Dil sınavına gir
```

---

## 36. EVCİL HAYVAN / BEBEK KOLTUĞU / ENGELLİ FİLTRESİ

### 36.1 Felsefe

Bazı yolcular:
- Evcil hayvanıyla seyahat etmek ister
- Bebek koltuğu gerekir
- Tekerlekli sandalye ile binebilir
Bu ihtiyaçları önceden belirtip uygun araçla eşleşmelidir.

### 36.2 Filtreler ve Rozetler

```
ARAÇ ÖZELLİK ROZETLERİ:
├── 🐾 EVcil HAYVAN İZİN
│   ├── Şöför kabul ediyor
│   ├── Kafes/taşıma çantası şart (opsiyonel)
│   └── Ek temizlik ücreti: 20 TL
│
├── 👶 BEBEK KOLTUĞU
│   ├── Araçta bebek koltuğu mevcut
│   ├── 0-3 yaş / 3-6 yaş / 6-12 yaş
│   └── Ek ücret: 15 TL
│
├── ♿ ENGELLİ ERİŞİMİ
│   ├── Tekerlekli sandalye sığar mı?
│   ├── Alçak taban / rampa var mı?
│   └── Kapı genişliği uygun mu?
│
└── 🧳 BÜYÜK BAGAJ
    ├── Havalimanı yolcusu
    ├── 2+ büyük valiz
    └── Bagaj hacmi geniş araç
```

### 36.3 API

```
PUT    /api/v1/taxi/vehicle/features          # Araç özelliklerini güncelle
GET    /api/v1/taxi/search?pet=yes            # Evcil hayvan izinli ara
GET    /api/v1/taxi/search?baby_seat=yes      # Bebek koltuklu ara
GET    /api/v1/taxi/search?wheelchair=yes     # Engelli uyumlu ara
POST   /api/v1/taxi/trip/{tripId}/pet-fee     # Evcil hayvan ek ücreti
```

---

## 37. POS CİHAZI / KART OKUYUCU KİRALAMA

### 37.1 Felsefe

Sistem nakit ödemeyi kapatıyor. Ancak her şöförün pos cihazı yok. Sistem üzerinden **pos cihazı kiralama** veya **sanal pos** hizmeti sunulur.

### 37.2 Pos Çözümleri

```
POS ÇÖZÜMLERİ:
├── 1️⃣ FİZİKSEL POS (Kiralık)
│   ├── Aylık kira: 150 TL
│   ├── Depozito: 500 TL (iade edilebilir)
│   ├── Komisyon: %1.5 (standart pos)
│   ├── Temassız + Chip + Manyetik
│   └── 7/24 destek
│
├── 2️⃣ SANAL POS (Uygulama içi)
│   ├── Ek ücret YOK
│   ├── Yolcu kendi telefonundan öder
│   ├── Şöför uygulamasında QR gösterir
│   └── Yolcu okutur → ödeme tamam
│
├── 3️⃣ KAREKOD POS
│   ├── Araç içindeki QR'ı okut
│   ├── Her araçta sabit QR
│   └── Yolculuk bağlantısız ödeme
│
└── 4️⃣ TAKSİMETRE ENTEGRE POS
    ├── Taksimetreye entegre kart okuyucu
    ├── Yolculuk bitince kartı tak → ödeme
    └── En profesyonel çözüm
```

### 37.3 Veritabanı

```sql
CREATE TABLE taxi_pos_rentals (
    id                  UUID PRIMARY KEY,
    driver_id           UUID REFERENCES taxi_drivers(id),
    vehicle_id          UUID REFERENCES taxi_vehicles(id),
    
    pos_type            VARCHAR(30) NOT NULL,                -- physical, virtual, qr, meter_integrated
    device_id           VARCHAR(100),
    monthly_fee         DECIMAL(10,2),
    deposit             DECIMAL(10,2),
    commission_rate     DECIMAL(5,2),
    
    rental_start        DATE NOT NULL,
    rental_end          DATE,
    is_active           BOOLEAN DEFAULT TRUE,
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 37.4 API

```
POST   /api/v1/taxi/pos/rent                  # Pos kirala
GET    /api/v1/taxi/pos/my-rental              # Kiralık pos durumu
POST   /api/v1/taxi/pos/return                 # Pos iade
PUT    /api/v1/taxi/driver/virtual-pos/toggle  # Sanal pos aç/kapa
```

---

## 38. PLAKA / TAKSİ ALIM-SATIM PLATFORMU

### 38.1 Felsefe

İstanbul'da taksi plakası fiyatı 2-3 milyon TL. Plaka alım-satımı büyük bir gayriresmi pazar. Sistem, **güvenilir ve resmi plaka alım-satım platformu** sunar.

### 38.2 Platform Özellikleri

```
PLATFORM ÖZELLİKLERİ:
├── 1️⃣ PLAKA İLANLARI
│   ├── Satılık plaka ilanı ver
│   ├── Alıcı plaka ara
│   ├── Fiyat aralığı: 1.500.000 - 5.000.000 TL
│   └── İlçe bazlı fiyatlandırma
│
├── 2️⃣ DEĞERLEME
│   ├── AI destekli plaka değerleme
│   ├── Son satış verileri
│   ├── Bölgeye göre fiyat endeksi
│   └── "Plakan ne kadar eder?" sorgulama
│
├── 3️⃣ RESMİ DEVRİŞ
│   ├── Noter onaylı devir süreci
│   ├── Sistem üzerinden sözleşme
│   ├── Güvenli ödeme (escrow)
│   └── Plaka devir takibi
│
└── 4️⃣ PLAKA RAPORLAMA
    ├── Plaka sorgula (geçmiş, ceza, haciz)
    ├── Geçmiş satış fiyatları
    └── Plaka gelir hesabı (aylık kira getirisi)
```

### 38.3 Veritabanı

```sql
CREATE TABLE taxi_plate_listings (
    id                  UUID PRIMARY KEY,
    seller_id           UUID REFERENCES users(id),
    plate_number        VARCHAR(20) NOT NULL,
    city                VARCHAR(100),
    district            VARCHAR(100),
    
    asking_price        DECIMAL(12,2) NOT NULL,
    plate_type          VARCHAR(30) DEFAULT 'taxi',          -- taxi, commercial
    monthly_income      DECIMAL(10,2),                       -- Tahmini aylık kira geliri
    has_active_lease    BOOLEAN DEFAULT FALSE,
    
    description         TEXT,
    photos              JSONB DEFAULT '[]',
    status              VARCHAR(30) DEFAULT 'active',        -- active, pending, sold, cancelled
    
    buyer_id            UUID REFERENCES users(id) NULL,
    sold_price          DECIMAL(12,2),
    sold_at             TIMESTAMP,
    
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### 38.4 API

```
POST   /api/v1/taxi/plate/listings           # Plaka ilanı ver
GET    /api/v1/taxi/plate/listings/search     # Plaka ara
GET    /api/v1/taxi/plate/{plateId}           # Plaka detayı
GET    /api/v1/taxi/plate/valuation           # Plaka değerleme
POST   /api/v1/taxi/plate/{plateId}/buy       # Plaka satın al
POST   /api/v1/taxi/plate/{plateId}/offer     # Teklif ver
GET    /api/v1/taxi/plate/market-report       # Piyasa raporu
```

---

*Son güncelleme: 2026-06-06*
*Durum: Tasarım Aşaması*
*Toplam Yeni Tablo: 60* (21 → 60)
*Toplam Yeni API: 200+* (90 → 200+)
