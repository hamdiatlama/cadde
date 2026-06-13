# 🏗️ KAPSAMLI WEB PLATFORMU - ANA PLAN DÖKÜMANI

---

## 📋 İÇİNDEKİLER

1. [Genel Bakış](#1-genel-bakış)
2. [Hesap Türleri ve Hiyerarşi](#2-hesap-türleri-ve-hiyerarşi)
3. [Bireysel Hesap Özellikleri](#3-bireysel-hesap-özellikleri)
4. [Kurumsal Hesap Özellikleri](#4-kurumsal-hesap-özellikleri)
5. [Kamusal Hesap Özellikleri](#5-kamusal-hesap-özellikleri)
6. [E-Ticaret Sistemi](#6-e-ticaret-sistemi)
7. [Yetkilendirilmiş Satış Sistemi](#7-yetkilendirilmiş-satış-sistemi)
8. [İlan Sayfası Sistemi](#8-İlan-sayfası-sistemi)
9. [Ödeme ve Komisyon Sistemi](#9-ödeme-ve-komisyon-sistemi)
10. [Güvenlik ve Yetkilendirme](#10-güvenlik-ve-yetkilendirme)
11. [API Endpoint'leri](#11-api-endpointleri)
12. [Veritabanı Şeması](#12-veritabanı-şeması)
13. [Proje Klasör Yapısı](#13-proje-klasor-yapisi)
14. [Tasarım İlkeleri](#14-tasarim-ilkeleri)
15. [Puanlama Sistemi](#15-puanlama-sistemi)
16. [Taksi Sistemi](#16-taksi-sistemi)

---

## 1. GENEL BAKIŞ

### 1.1 Platformun Amacı
Bu platform, üç farklı hesap türü ile çalışan kapsamlı bir e-ticaret ve sosyal paylaşım platformudur. Kullanıcılar:
- Kendi ürünlerini satabilir (fiziksel, dijital, hizmet)
- Başkasının ürünlerini komisyonla satabilir
- İlan sayfaları oluşturabilir
- Video eğitimler satabilir
- Hizmetlerini pazarlayabilir

### 1.2 Temel İş Modeli
```
┌─────────────────────────────────────────────────────────────────┐
│                    İŞ MODELİ ÖZETİ                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🆓 ÜYE OLMAK ÜCRETSİZ                                        │
│                                                                 │
│  💰 SATIŞ İŞLEMLERİNDEN ÇOK DÜŞÜK MİKTARDA KOMİSYON           │
│                                                                 │
│  ✅ ONAYLI SATIŞ SİSTEMİ                                       │
│     - Başkasının ürününü satmak için izin iste                  │
│     - Ürün sahibi onay verir → "Onaylı Satış" rozeti           │
│     - Komisyon paylaşımı otomatik yapılır                       │
│                                                                 │
│  🏪 İLAN SAYFALARI                                             │
│     - Gayrimenkul uzmanları, emlakçılar vb.                   │
│     - Kendi ilan sayfalarını oluşturabilirler                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1.2 Platform Genel Kuralları

Aşağıdaki kurallar **platformdaki tüm servisler** (taksi, yemek, e-ticaret, vb.) için geçerlidir:

| Kural | Açıklama |
|-------|----------|
| **Adres ve Konum Zorunlu** | Her kullanıcı (bireysel/kurumsal) **adres ve konum bilgisi** girmek zorundadır. Adressiz/konumsuz hesap ile işlem yapılamaz, hizmet verilemez. Konum: harita koordinatı (enlem/boylam) + açık adres. |
| **1 işlem = 1 yorum hakkı** | Platform üzerinden ödeme yapan kullanıcı, her işlem için 1 adet yorum/puan hakkı kazanır. |
| **3 seçenekli oylama** | Beğendim 👍 (+1) / Pas ⏭️ (0) / Kötü 👎 (-1). Klasik 1-5 yıldız kullanılmaz. |
| **Yorum silinemez** | Sadece platform yetkilisi ihlal durumunda gizleyebilir. |
| **Anti-troll** | %90+ olumsuz oy → tüm oylar geçersiz. |
| **Puan = sıralama** | Reklamla sıralama satın alınamaz. |

> Detaylı uygulama için: [TAXI-SYSTEM-DESIGN.md → Bölüm 7.0](docs/architecture/TAXI-SYSTEM-DESIGN.md) ve [YEMEK-SISTEMI-DESIGN.md → Kural 1](docs/architecture/YEMEK-SISTEMI-DESIGN.md).

## 2. HESAP TÜRLERİ VE HİYERARŞİ

### 2.1 Hesap Türleri

```
┌─────────────────────────────────────────────────────────────────┐
│                    HESAP TÜRÜ HİYERARŞİSİ                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Level 1: BİREYSEL HESAP                                       │
│  ├── Herkes açabilir                                            │
│  ├── Temel profil bilgileri                                     │
│  ├── Kendi ürünlerini satabilir                                 │
│  ├── Başkasının ürünlerini satabilir (onaylı)                  │
│  ├── İlan sayfası oluşturabilir                                 │
│  └── Video eğitim satabilir                                     │
│                                                                 │
│  Level 2: KURUMSAL HESAP                                       │
│  ├── Bireysel hesap gerekli                                     │
│  ├── Şirket profili                                             │
│  ├── Mağaza açma                                                │
│  ├── Çalışan yönetimi                                           │
│  ├── Finansal raporlar                                          │
│  └── Tüm bireysel özellikler                                    │
│                                                                 │
│  Level 3: KAMUSAL HESAP                                        │
│  ├── Bireysel hesap gerekli                                     │
│  ├── Resmi kurum hesabı                                         │
│  ├── Duyuru yapma yetkisi                                       │
│  ├── Toplu bildirim gönderme                                    │
│  ├── Onaylı/resmi rozet                                         │
│  ├── Öncelikli arama sıralaması                                 │
│  └── Tüm kurumsal özellikler                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Hesap Türü Karşılaştırması

| Özellik | Bireysel | Kurumsal | Kamusal |
|---------|----------|----------|---------|
| Üye olma | ✅ Ücretsiz | ✅ Bireysel gerekli | ✅ Bireysel gerekli |
| Profil yönetimi | ✅ | ✅ | ✅ |
| Ürün ekleme | ✅ | ✅ | ✅ |
| Mağaza açma | ✅ | ✅ | ✅ |
| Başkasının ürününü satma | ✅ (onaylı) | ✅ (onaylı) | ✅ (onaylı) |
| İlan sayfası | ✅ | ✅ | ✅ |
| Video eğitim satışı | ✅ | ✅ | ✅ |
| Hizmet pazarlama | ✅ | ✅ | ✅ |
| Çalışan yönetimi | ❌ | ✅ | ✅ |
| Finansal rapor | ❌ | ✅ | ✅ |
| Duyuru yapma | ❌ | ❌ | ✅ |
| Toplu bildirim | ❌ | ❌ | ✅ |
| Resmi rozet | ❌ | ❌ | ✅ |
| Öncelikli sıralama | ❌ | ❌ | ✅ |

---

## 3. BİREYSEL HESAP ÖZELLİKLERİ

### 3.1 Üyelik Bilgileri
```yaml
Profil Bilgileri:
  - Ad, Soyad
  - E-posta, Telefon
  - Profil Fotoğrafı
  - Kapak Fotoğrafı
  - Biyografi / Hakkında Yazısı
  - Doğum Tarihi
  - Cinsiyet

İletişim Bilgileri:
  - Adres (il, ilçe, postcode)
  - Telefon numaraları
  - E-posta adresleri

Sosyal Medya:
  - Twitter, Instagram, LinkedIn
  - GitHub, YouTube, TikTok
  - Özel web sitesi
```

### 3.2 Eğitimlerim
```yaml
Eğitim Geçmişi:
  - Okul Adı
  - Bölüm
  - Derece (lise, önlisans, lisans, yüksek lisans, doktora)
  - Başlangıç-Bitiş Tarihi
  - Not Ortalaması
  - Diploma/Sertifika Yükleme

Online Sertifikalar:
  - Udemy, Coursera, Khan Academy
  - Sertifika URL'si
  - Platform bilgisi
```

### 3.3 Kariyerim
```yaml
İş Geçmişi:
  - Şirket Adı
  - Pozisyon
  - Başlangıç-Bitiş Tarihi
  - Hala Devam Ediyor mu?
  - Maaş Bilgisi (opsiyonel, görünürlük ayarlanabilir)
  - İş Tanımı

Referanslar:
  - Ad Soyad
  - Pozisyon
  - Şirket
  - Telefon, E-posta
  - İlişki türü

CV Yükleme:
  - PDF/Word formatında
  - Güncelleme tarihi
```

### 3.4 Projelerim
```yaml
Proje Bilgileri:
  - Proje Adı
  - Açıklama
  - Başlangıç-Bitiş Tarihi
  - Durum (devam ediyor, tamamlandı, iptal)
  - Kullanılan Teknolojiler

Medya:
  - Proje Görselleri
  - Video
  - Dış Linkler (GitHub, website vb.)
```

### 3.5 Verdiğim Eğitimler
```yaml
Eğitim Bilgileri:
  - Eğitim Başlığı
  - Açıklama
  - Tarih
  - Katılımcı Sayısı
  - Konum (online/yerinde)
```

### 3.6 Ürünlerim (Satış)
```yaml
Fiziksel Ürünler:
  - Ev, Daire, Arsa
  - Araç, Tekne
  - Elektronik
  - Giyim
  - Her türlü mal

Dijital Ürünler:
  - Video Eğitimler
  - E-book'lar
  - Online Kurslar
  - Webinerler

Hizmetler:
  - Matematik Dersi
  - Danışmanlık
  - Tasarım Hizmeti
  - Her türlü hizmet
```

### 3.7 Varlıklarım
```yaml
Gayrimenkul:
  - Ev, Daire, Villa
  - Arsa, Tarla
  - İşyeri, Dükkan

Taşınır Mallar:
  - Araç (otomobil, kamyon, motosiklet)
  - Tekne, Gemi
  - Makine, Ekipman

Finansal Varlıklar:
  - Hisse Senetleri
  - Fonlar
  - Kripto Paralar
  - Tahviller

Fikri Mülkiyet:
  - Patentler
  - Tescilli Markalar
  - Telif Hakları
```

### 3.8 Danışmanlarım
```yaml
Danışman Türleri:
  - Akademik Danışmanlar
  - İş Danışmanları / Mentörler
  - Hukuki Danışmanlar
  - Finansal Danışmanlar
  - Diğer

Bilgiler:
  - Ad Soyad
  - Uzmanlık
  - Şirket
  - İletişim
  - LinkedIn
```

### 3.9 Finansal Bilgiler
```yaml
Banka Bilgileri:
  - Banka Adı
  - IBAN
  - Hesap Sahibi
  - Hesap Türü (vadeli, vadesiz, iş)

Vergi Bilgileri:
  - Vergi Numarası
  - Vergi Dairesi
  - Vergi Türü (bireysel/kurumsal)

Tescilli Belgeler:
  - Patentler
  - Tescilli Markalar
  - Lisanslar
  - Sertifikalar
```

---

## 4. KURUMSAL HESAP ÖZELLİKLERİ

### 4.1 STANDART FİRMA PROFİLİ

```yaml
Firma Temel Bilgileri:
  Zorunlu Alanlar:
    - Firma Adı (resmi unvan)
    - Firma Logosu
    - Kapak Görseli
    - Sektör (çoklu seçim)
    - Firma Türü (limited, anonim, şahıs, kooperatif, dernek, vakıf)
    - Vergi Numarası
    - Ticaret Sicil Numarası
    - Kuruluş Yılı
    - İletişim Bilgileri (telefon, e-posta, web sitesi)
    - Adres (il, ilçe, sokak, posta kodu)
    - Çalışan Sayısı

  İsteğe Bağlı Alanlar:
    - Kısa açıklama (160 karakter)
    - Detaylı açıklama (zengin metin)
    - Çalışma Saatleri
    - Sosyal Medya Hesapları
    - Fotoğraf Galerisi
    - Video Tanıtım
    - Harita Konumu

### 4.1A FİRMA WEB SİTESİ OLUŞTURUCU

  Platform üzerinde firmalar kendi web sitelerini oluşturabilir:
  
  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMALAR KENDİ WEB SİTELERİNİ KULLANACAKLAR             │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÖRNEK:                                                     │
  │  ├── firmaadi.platform.com.tr (alt domain)                  │
  │  ├── platform.com.tr/firmaadi (path tabanlı)                │
  │  ├── www.firmaadi.com (kendi domain'i)                      │
  │  └── www.firmaadi.com.tr (kendi domain'i)                   │
  │                                                             │
  │  WEB SİTEESİ YAPISI:                                        │
  │  ├── Ana Sayfa (Hero Section)                               │
  │  ├── Hakkımızda Sayfası                                     │
  │  ├── Hizmetler Sayfası                                      │
  │  ├── Ürünler/Mağaza Sayfası                                 │
  │  ├── Galeri Sayfası                                          │
  │  ├── Blog/Haberler Sayfası                                   │
  │  ├── İletişim Sayfası                                        │
  │  ├── Referanslar Sayfası                                     │
  │  ├── Kariyer Sayfası                                         │
  │  └── SSS Sayfası                                             │
  │                                                             │
  │  ŞABLON SEÇENEKLERİ:                                        │
  │  ├── Kurumsal Şablon (profesyonel firmalar)                  │
  │  ├── Mağaza Şablonu (e-ticaret odaklı)                       │
  │  ├── Hizmet Şablonu (servis sağlayan firmalar)               │
  │  ├── Restoran Şablonu (yemek/servis)                        │
  │  ├── Eğitim Şablonu (okul/kurs)                              │
  │  ├── Portföy Şablonu (serbest çalışanlar)                   │
  │  ├── Blog Şablonu (içerik odaklı)                           │
  │  ├── Emlak Şablonu (emlakçılar)                             │
  │  ├── Oto Servis Şablonu (otomotiv)                          │
  │  ├── Güzellik Şablonu (kuaför/güzellik merkezi)            │
  │  ├── Sağlık Şablonu (klinik/hastane)                        │
  │  └── Özel Şablon (tam özelleştirme)                         │
  │                                                             │
  │  SÜRÜKLE BIRAK DÜZENLEYİCİ:                                 │
  │  ├── Sayfa düzeni özelleştirme                              │
  │  ├── Renk ve font seçimi                                    │
  │  ├── Logo ve görsel yükleme                                  │
  │  ├── Menü özelleştirme                                       │
  │  ├── Footer özelleştirme                                     │
  │  ├── Sosyal medya bağlantıları                              │
  │  ├── İletişim formu ekleme                                   │
  │  ├── Harita ekleme                                            │
  │  ├── Galeri/video ekleme                                     │
  │  ├── Blog yazısı ekleme                                     │
  │  ├── Ürün/hizmet ekleme                                      │
  │  └── SEO ayarları                                            │
  │                                                             │
  │  WEB SİTEESİ ÖZELLİKLERİ:                                   │
  │  ├── Responsive tasarım (mobil, tablet, masaüstü)           │
  │  ├── Hızlı yükleme (CDN, önbellekleme)                      │
  │  ├── SEO dostu (meta etiketleri, site haritası)             │
  │  ├── SSL sertifikası (HTTPS)                                 │
  │  ├── Analytics entegrasyonu                                  │
  │  ├── Form yönetimi                                            │
  │  ├── E-posta bildirimleri                                     │
  │  ├── Çok dilli destek                                         │
  │  └── Özel kod ekleme (gelişmiş kullanıcılar)                │
  │                                                             │
  │  YÖNETİM PANELİ:                                            │
  │  ├── Sayfa düzenleme                                        │
  │  ├── İçerik yönetimi                                        │
  │  ├── Görünüm istatistikleri                                  │
  │  ├── Ziyaretçi analizi                                       │
  │  ├── Form başvuruları                                        │
  │  ├── Domain yönetimi                                         │
  │  ├── SSL yönetimi                                            │
  │  ├── Yedekleme                                               │
  │  └── Performans raporları                                    │
  │                                                             │
  │  DOMAIN YÖNETİMİ:                                            │
  │  ├── Alt domain: firma.platform.com.tr (ücretsiz)           │
  │  ├── Özel domain: firma.com (kendi domain'i)                │
  │  ├── Domain yönlendirme                                      │
  │  ├── Otomatik SSL                                             │
  │  └── DNS yönetimi                                            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  Firma Web Sitesi Şablonu Örneği:
  ┌─────────────────────────────────────────────┐
  │  🏢 ABC İnşaat Ltd. Şti.                   │
  │  ─────────────────────────────────────────  │
  │  ☰ Menü                                    │
  ├─────────────────────────────────────────────┤
  │  🏠 Ana Sayfa                               │
  │  📋 Hakkımızda                              │
  │  🔧 Hizmetlerimiz                          │
  │  🛒 Ürünlerimiz                             │
  │  📸 Galeri                                  │
  │  📰 Blog                                    │
  │  📞 İletişim                                │
  ├─────────────────────────────────────────────┤
  │  ┌─────────────────────────────────────┐   │
  │  │      HİZMET KALİTEMİZ               │   │
  │  │                                     │   │
  │  │  🔨 İnşaat    🏗️ Tadilat           │   │
  │  │  🔌 Elektrik  🚿 Su Tesisatı       │   │
  │  │  🎨 Boya      🪟 Doğrama           │   │
  │  └─────────────────────────────────────┘   │
  │                                             │
  │  ┌─────────────────────────────────────┐   │
  │  │      ÜRÜNLERİMİZ                     │   │
  │  │  [Ürün 1] [Ürün 2] [Ürün 3]         │   │
  │  └─────────────────────────────────────┘   │
  │                                             │
  │  ┌─────────────────────────────────────┐   │
  │  │      REFERANSLARIMIZ                 │   │
  │  │  ⭐⭐⭐⭐⭐ ABC Holding              │   │
  │  │  ⭐⭐⭐⭐⭐ XYZ İnşaat              │   │
  │  └─────────────────────────────────────┘   │
  │                                             │
  ├─────────────────────────────────────────────┤
  │  📍 Adres  📞 Telefon  📧 E-posta          │
  │  🌐 www.abcinsaat.com.tr                   │
  │  © 2026 ABC İnşaat - Tüm hakları saklıdır │
  └─────────────────────────────────────────────┘
```

### 4.2 KURS VE SERTİFİKA YÖNETİMİ

```yaml
Firma için Zorunlu Belgeler:
  Ticari Belgeler:
    - Vergi Levhası
    - Ticaret Sicil Gazetesi
    - İmza Sirküleri
    - Oda Kayıt Belgesi

  Mesleki Belgeler:
    - Meslek Odası Kayıt Belgesi
    - Ustalık Belgesi (mesleğe göre)
    - Kalfalık Belgesi
    - Çıraklık Belgesi
    - Mesleki Yeterlilik Belgesi

  Kalite Belgeleri:
    - ISO 9001 (Kalite Yönetimi)
    - ISO 14001 (Çevre Yönetimi)
    - ISO 22000 (Gıda Güvenliği)
    - OHSAS 18001 (İş Güvenliği)
    - CE Belgesi
    - TSE Belgesi

Kurs/Sertifika Bilgileri:
  Firma Kursları:
    - Kurs Adı
    - Kurs Türü (online, yüz yüze, hibrit)
    - Süre (saat/gün/ay)
    - Fiyat
    - Başlangıç/Bitiş Tarihi
    - Eğitmen
    - Kapasite
    - Konum (online/adres)
    - Müfredat
    - Fotoğraf/Videolar
    - Başvuru Sayısı
    - Puan Ortalaması

  Sertifika Türleri:
    - Firma içi eğitim sertifikası
    - Mesleki yeterlilik sertifikası
    - Kalite yönetim sertifikası
    - İş güvenliği sertifikası
    - Dijital beceri sertifikası
    - Dil yeterlilik sertifikası
    - İlk yardım sertifikası

  Sertifika Doğrulama:
    - Benzersiz sertifika numarası
    - Veren kurum bilgisi
    - Geçerlilik tarihi
    - QR kod ile doğrulama
    - Online doğrulama sayfası
```

### 4.3 VERİLEN HİZMETLER

```yaml
Hizmet Kategorileri:
  Temel Hizmetler:
    - Danışmanlık
    - Eğitim
    - Tamirat
    - Bakım
    - Kurulum
    - Montaj
    - Taşıma
    - Temizlik

  Profesyonel Hizmetler:
    - Hukuki danışmanlık
    - Mali müşavirlik
    - Mimarlık/mühendislik
    - Yazılım geliştirme
    - Tasarım
    - Pazarlama
    - İnsan kaynakları

  Teknik Hizmetler:
    - Bilgisayar/onarım
    - Elektrik tesisatı
    - Su tesisatı
    - Klima bakım
    - kombi bakım
    - Asansör bakım
    - Güvenlik sistemleri

Hizmet Detayları:
  Zorunlu Bilgiler:
    - Hizmet Adı
    - Hizmet Açıklaması
    - Hizmet Türü (online/yerinde/hibrit)
    - Fiyat (sabit/saatlik/keşif)
    - Tahmini Süre
    - Garanti Süresi
    - Konum Bilgisi

  İsteğe Bağlı:
    - Fotoğraf/Galeri
    - Video
    - Müşteri Yorumları
    - Örnek Work
    - Referanslar
    - SSS

Hizmet Kalite Standartları:
  - Hizmet sonrası destek
  - Garanti kapsamında hizmet
  - Memnuniyet garantisi
  - Profesyonel ekip
  - Zamanında teslimat
  - Şeffaf fiyatlandırma
  - Güvenilir malzeme kullanımı
```

### 4.5 MÜŞTERİ/YÖNETİMİ - ÜRÜN ALICILARI

  Firmaların ürünlerini alacak kişiler için müşteri yönetimi:

  ┌─────────────────────────────────────────────────────────────┐
  │  MÜŞTERİ YÖNETİM SİSTEMİ                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  MÜŞTERİ TÜRLERİ:                                           │
  │  ├── Bireysel Müşteri (kişisel alışveriş yapan)             │
  │  ├── Kurumsal Müşteri (firma adına alışveriş yapan)         │
  │  ├── Toptancı (toplu alan)                                  │
  │  ├── Perakende (tekli alan)                                 │
  │  ├── Abone (düzenli alan)                                   │
  │  └── VIP Müşteri (özel indirimli)                           │
  │                                                             │
  │  MÜŞTERİ BİLGİLERİ:                                         │
  │  ├── Temel Bilgiler                                         │
  │  │   ├── Ad Soyad / Firma Adı                               │
  │  │   ├── E-posta                                             │
  │  │   ├── Telefon                                             │
  │  │   ├── Adres (fatura ve teslimat)                         │
  │  │   └── Vergi Numarası (kurumsal için)                     │
  │  │                                                          │
  │  ├── Alışveriş Geçmişi                                      │
  │  │   ├── Toplam Sipariş Sayısı                              │
  │  │   ├── Toplam Harcama Tutarı                              │
  │  │   ├── Ortalama Sipariş Tutarı                            │
  │  │   ├── Son Alışveriş Tarihi                               │
  │  │   └── En Çok Aldığı Ürünler                              │
  │  │                                                          │
  │  ├── Tercihler                                               │
  │  │   ├── İlgi Alanları                                       │
  │  │   ├── Tercih Ettiği Kategoriler                           │
  │  │   ├── Bütçe Aralığı                                      │
  │  │   ├── Ödeme Tercihi                                      │
  │  │   └── İletişim Tercihi                                   │
  │  │                                                          │
  │  └── Sadakat Bilgileri                                      │
  │      ├── Sadakat Puanı                                      │
  │      ├── Üyelik Seviyesi (Bronz/Gümüş/Altın/Platin)        │
  │      ├── Kupon Kullanımı                                    │
  │      └── Ödül Geçmişi                                        │
  │                                                             │
  │  MÜŞTERİ SEGMENTASYONU:                                     │
  │  ├── Yeni Müşteri (ilk alışverişini yapan)                  │
  │  ├── Sadık Müşteri (tekrarlı alışveriş)                     │
  │  ├── Yüksek Değerli (çok harcama yapan)                     │
  │  ├── Düşük Değerli (az harcama yapan)                       │
  │  ├── Kayıp Müşteri (uzun süredir gelmeyen)                  │
  │  ├── Potansiyel Müşteri (sepete ekleyen ama almayan)        │
  │  └── Referans Müşteri (başkalarını yönlendiren)             │
  │                                                             │
  │  MÜŞTERİ İLETİŞİMİ:                                         │
  │  ├── Mesajlaşma                                              │
  │  ├── E-posta bildirimleri                                    │
  │  ├── SMS bildirimleri                                        │
  │  ├── Telefon görüşmesi                                       │
  │  └── Toplantı/randevu                                        │
  │                                                             │
  │  MÜŞTERİ ANALİTİĞİ:                                         │
  │  ├── Satış grafikleri                                        │
  │  ├── Müşteri memnuniyeti                                     │
  │  ├── Alışveriş davranışları                                  │
  │  ├── Segment analizi                                         │
  │  ├── ROI hesaplama                                           │
  │  └── Tahmini satışlar                                        │
  │                                                             │
  │  ÖZEL MÜŞTERİ YÖNETİMİ:                                     │
  │  ├── Kişiselleştirilmiş teklifler                            │
  │  ├── Doğum günü/kutlama mesajları                           │
  │  ├── Özel indirimler                                         │
  │  ├── Erken erişim                                           │
  │  └── VIP hizmetler                                           │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  SİPARİŞ YÖNETİMİ:
  ┌─────────────────────────────────────────────────────────────┐
  │  SİPARİŞ DÖNGÜSÜ:                                           │
  │                                                             │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │ Sepete    │→│ Ödeme    │→│ Hazırlan- │→│ Kargoya  │  │
  │  │ Ekleme    │  │ Yapma    │  │ ma       │  │ Verilme  │  │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
  │       │             │             │             │          │
  │       ▼             ▼             ▼             ▼          │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │ Stok      │  │ Fatura   │  │ Paketle- │  │ Teslimat │  │
  │  │ Kontrolü  │  │ Kesme    │  │ me       │  │ Takibi   │  │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
  │                                                             │
  │  SİPARİŞ DURUMLARI:                                        │
  │  ├── 🛒 Sepette                                            │
  │  ├── 💳 Ödeme Bekleniyor                                   │
  │  ├── ✅ Ödeme Alındı                                       │
  │  ├── 📋 Hazırlanıyor                                       │
  │  ├── 📦 Paketlendi                                         │
  │  ├── 🚚 Kargoya Verildi                                   │
  │  ├── 📍 Yolda                                              │
  │  ├── ✅ Teslim Edildi                                      │
  │  ├── ❌ İptal Edildi                                       │
  │  └── 🔄 İade Edildi                                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  MÜŞTERİ MEMNUNİYETİ:
  ┌─────────────────────────────────────────────────────────────┐
  │  MEMNUNİYET ÖLÇÜMÜ:                                        │
  │  ├── Sipariş sonrası anket                                  │
  │  ├── Ürün yorumu/oylama                                      │
  │  ├── NPS (Net Promoter Score)                               │
  │  ├── Customer Satisfaction (CSAT)                           │
  │  ├── Customer Effort Score (CES)                            │
  │  └── Şikayet yönetimi                                       │
  │                                                             │
  │  GERİ BİLDİRİM DÖNGÜSÜ:                                    │
  │  ├── Olumlu geri bildirim → Teşekkür + Ödül                 │
  │  ├── Nötr geri bildirim → İyileştirme planı                 │
  │  └── Olumsuz geri bildirim → Çözüm + Takip                  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

### 4.4 ÇALIŞAN YÖNETİMİ

```yaml
Çalışan Bilgileri:
  Temel Bilgiler:
    - Ad Soyad
    - Profil Fotoğrafı
    - Pozisyon
    - Departman
    - E-posta
    - Telefon (opsiyonel)
    - Başlangıç Tarihi

  Mesleki Bilgiler:
    - Uzmanlık Alanı
    - Deneyim Yılı
    - Mesleki Belgeler
    - Eğitim Bilgisi
    - Yetenekler
    - Diller

  Performans Bilgileri:
    - Puan Ortalaması
    - Tamamlanan İş Sayısı
    - Müşteri Memnuniyeti
    - Yanıt Hızı
    - Devam Durumu

Pozisyon Tipleri:
  Yönetici Kadro:
    - Firma Sahibi (tüm yetkiler)
    - Genel Müdür (genel yönetim)
    - Müdür (departman yönetimi)
    - Şef (ekip yönetimi)

  Personel Kadro:
    - Uzman (kendi alanında)
    - Teknisyen (teknik işler)
    - Asistan (destek)
    - Stajyer (öğrenme)

Yetki Matrisi:
  | Yetki             | Sahip | Admin | Müdür | Şef | Personel |
  |-------------------|-------|-------|-------|-----|----------|
  | Firma Silme       | ✅    | ❌    | ❌    | ❌  | ❌       |
  | Firma Düzenleme   | ✅    | ✅    | ❌    | ❌  | ❌       |
  | Çalışan Ekleme    | ✅    | ✅    | ✅    | ❌  | ❌       |
  | Çalışan Çıkarma   | ✅    | ✅    | ✅    | ❌  | ❌       |
  | Ürün Ekleme       | ✅    | ✅    | ✅    | ✅  | ❌       |
  | Sipariş Yönetimi  | ✅    | ✅    | ✅    | ✅  | ✅       |
  | Mesajlaşma        | ✅    | ✅    | ✅    | ✅  | ✅       |
  | Rapor Görme       | ✅    | ✅    | ✅    | ⚠️  | ❌       |
  | Finansallar       | ✅    | ✅    | ❌    | ❌  | ❌       |

Çalışan Davet Sistemi:
  - E-posta ile davet
  - Link ile davet
  - Toplu davet
  - QR kod ile katılma
  - Onay mekanizması
```

### 4.4A ÇALIŞANLAR ARASI İLETİŞİM VE İŞBİRLİĞİ

  Çalışanlar firmanın kurumsal sayfasında birbirleriyle görüşecekler:

  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMA KURUMSAL SAYFASI - ÇALIŞAN PORTALI                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  🏢 ABC İnşaat Ltd. Şti.                           │   │
  │  │  ────────────────────────────────────────────────   │   │
  │  │  📋 Kurumsal Sayfa | 👥 Çalışanlar | 💬 Mesajlaşma │   │
  │  │  📅 Takvim | 📁 Dosyalar | 📊 Raporlar             │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  SAĞ ÜSTE ÇALIŞAN PANELI:                                   │
  │  ├── 👤 Profil (kendi profilin)                             │
  │  ├── 👥 Çalışanlar (tüm ekip)                               │
  │  ├── 💬 Mesajlar (dahili mesajlaşma)                       │
  │  ├── 📅 Randevu (toplantı planlama)                         │
  │  ├── 📁 Dosyalar (paylaşılan dosyalar)                      │
  │  └── 🔔 Bildirimler                                         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DİHAHİ MESAJLAŞMA SİSTEMİ                                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  MESAJ TÜRLERİ:                                             │
  │  ├── Genel Sohbet (tüm çalışanlar)                         │
  │  ├── Departman Sohbeti (sadece o departman)                 │
  │  ├── Proje Sohbeti (belirli proje ekibi)                   │
  │  ├── Özel Mesaj (tek kişi ile)                              │
  │  ├── Grup Mesajı (belirli grup)                             │
  │  └── Duyuru (sadece okunabilir)                             │
  │                                                             │
  │  MESAJ ÖZELLİKLERİ:                                         │
  │  ├── Metin mesajı                                           │
  │  ├── Dosya ekleme (PDF, Word, Excel, görsel)                │
  │  ├── Ses kaydı                                              │
  │  ├── Video kaydı                                            │
  │  ├── Konum paylaşımı                                       │
  │  ├── Anket/oylama                                           │
  │  ├── Görev atama                                            │
  │  ├── Takvim daveti                                          │
  │  ├── Emoji/tepkisi                                          │
  │  └── Mesajı sabitleme                                       │
  │                                                             │
  │  SOHBET ARAYÜZÜ:                                            │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  💬 Genel Sohbet - ABC İnşaat                       │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  👤 Ahmet (Mühendis)  10:30                        │   │
  │  │  "Proje için malzeme listesi hazır"                 │   │
  │  │  📎 malzeme_listesi.pdf                             │   │
  │  │                                                     │   │
  │  │  👤 Mehmet (Tekniker)  10:35                        │   │
  │  │  "Tamam, kontrol edeyim"                            │   │
  │  │  👍 3 kişi beğendi                                   │   │
  │  │                                                     │   │
  │  │  👤 Ayşe (Ofis)  10:40                              │   │
  │  │  "Müşteri ile toplantı saat 14:00'te"               │   │
  │  │  📅 Takvime Ekle                                    │   │
  │  │                                                     │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │  📎  📷  🎤  📍  📋  👤  ➕                       │   │
  │  │  ┌─────────────────────────────────────────────┐   │   │
  │  │  │ Mesajınızı yazın...                         │   │   │
  │  │  └─────────────────────────────────────────────┘   │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  GÖREV YÖNETİMİ                                             │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  GÖREV OLUŞTURMA:                                           │
  │  ├── Görev başlığı                                          │
  │  ├── Açıklama                                                │
  │  ├── Sorumlu kişi/kişiler                                   │
  │  ├── Öncelik (düşük/normal/yüksek/acil)                    │
  │  ├── Başlangıç tarihi                                       │
  │  ├── Bitiş tarihi                                            │
  │  ├── Etiketler                                               │
  │  ├── Dosyalar                                                │
  │  └── Alt görevler                                            │
  │                                                             │
  │  GÖREV DURUMLARI:                                           │
  │  ├── 📋 Yeni                                               │
  │  ├── 🔄 Devam Ediyor                                        │
  │  ├── ⏳ Beklemede                                           │
  │  ├── ✅ Tamamlandı                                          │
  │  └── ❌ İptal                                               │
  │                                                             │
  │  KANBAN TAHTASI:                                            │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
  │  │ 📋 Yeni  │→│🔄Devam   │→│⏳Bekleme │→│✅Tamam   │      │
  │  │          │ │ Ediyor   │ │          │ │          │      │
  │  │ • Görev1 │ │ • Görev3 │ │ • Görev5 │ │ • Görev7 │      │
  │  │ • Görev2 │ │ • Görev4 │ │          │ │ • Görev8 │      │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  TAKVİM VE TOPLANTILAR                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  TAKVİM TÜRLERİ:                                            │
  │  ├── Kişisel takvim                                         │
  │  ├── Departman takvimi                                       │
  │  ├── Firma takvimi (tüm çalışanlar)                         │
  │  └── Proje takvimi                                          │
  │                                                             │
  │  TOPLANTI ÖZELLİKLERİ:                                      │
  │  ├── Toplantı başlığı                                       │
  │  ├── Tarih ve saat                                           │
  │  ├── Konum (online/yüz yüze)                                │
  │  ├── Katılımcılar                                           │
  │  ├── Gündem                                                   │
  │  ├── Toplantı notları                                        │
  │  ├── Ses/video kaydı                                         │
  │  └── Aksiyon maddeleri                                       │
  │                                                             │
  │  ZOOM/MEETS ENTEGRASYONU:                                   │
  │  ├── Otomatik toplantı linki oluşturma                      │
  │  ├── Takvime ekleme                                          │
  │  ├── Hatırlatma                                              │
  │  └── Toplantı sonrası not paylaşımı                         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DOSYA PAYLAŞIMI                                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  DOSYA TÜRLERİ:                                             │
  │  ├── Belgeler (PDF, Word, Excel, PowerPoint)                │
  │  ├── Görseller (JPG, PNG, GIF)                              │
  │  ├── Videolar (MP4, AVI)                                    │
  │  ├── Ses dosyaları (MP3, WAV)                               │
  │  ├── Arşivler (ZIP, RAR)                                    │
  │  └── Diğer dosyalar                                         │
  │                                                             │
  │  KLASÖR YAPISI:                                             │
  │  ├── 📁 Genel (tüm çalışanlar görebilir)                   │
  │  │   ├── 📁 Duyurular                                       │
  │  │   ├── � prosedürler                                      │
  │  │   └── 📁 Şablonlar                                       │
  │  ├── 📁 Departmanlar                                        │
  │  │   ├── 📁 İnşaat                                          │
  │  │   ├── 📁 Muhasebe                                         │
  │  │   └── 📁 İnsan Kaynakları                                │
  │  ├── 📁 Projeler                                             │
  │  │   ├── 📁 Proje A                                          │
  │  │   └── 📁 Proje B                                          │
  │  └── 📁 Kişisel (sadece kendin görebilir)                  │
  │                                                             │
  │  PAYLAŞIM ÖZELLİKLERİ:                                      │
  │  ├── Dosya yükleme/silme                                     │
  │  ├── Dosya paylaşma (kişi/departman)                        │
  │  ├── Versiyon kontrolü                                      │
  │  ├── Yorum ekleme                                            │
  │  ├── İndirme geçmişi                                         │
  │  └── Arama                                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÇALIŞAN PROFİLLERİ VE İLETİŞİM                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÇALIŞAN KARTI:                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  👤 Ahmet Yılmaz                                     │   │
  │  │  🏗️ İnşaat Mühendisi                                │   │
  │  │  📧 ahmet@abcinsaat.com                              │   │
  │  │  📞 +90 532 xxx xx xx                               │   │
  │  │  📍 İnşaat Departmanı                               │   │
  │  │  📅 Başlangıç: 01.01.2020                           │   │
  │  │                                                     │   │
  │  │  💬 Mesaj Gönder  📞 Ara  📅 Randevu Al            │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  ÇALIŞAN LİSTESİ:                                           │
  │  ├── İsim ile arama                                         │
  │  ├── Departmana göre filtreleme                              │
  │  ├── Pozisyona göre filtreleme                               │
  │  ├── Duruma göre filtreleme (çalışıyor/izinli/ayrılan)      │
  │  └── Sıralama (isim/departman/başlangıç tarihi)            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  BİLDİRİMLER VE HATIRLATMALAR                               │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  BİLDİRİM TÜRLERİ:                                          │
  │  ├── Yeni mesaj geldi                                       │
  │  ├── Görev atandı                                           │
  │  ├── Görev tamamlandı                                       │
  │  ├── Toplantı hatırlatması                                  │
  │  ├── Dosya paylaşıldı                                       │
  │  ├── Yorum yapıldı                                          │
  │  ├── Duyuru yayınlandı                                       │
  │  └── Acil bildirim                                           │
  │                                                             │
  │  BİLDİRİM KANALLARI:                                        │
  │  ├── Uygulama içi bildirim                                  │
  │  ├── E-posta bildirimi                                       │
  │  ├── SMS bildirimi                                           │
  │  ├── Push bildirim (mobil)                                   │
  │  └── Masaüstü bildirimi                                      │
  │                                                             │
  │  HATIRLATMALAR:                                              │
  │  ├── Toplantı öncesi 15 dk                                  │
  │  ├── Görev bitiş tarihi öncesi 1 gün                        │
  │  ├── Doğum günü hatırlatması                                 │
  │  ├── İş yıldönümü                                           │
  │  └── Özel günler                                             │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

---

## 5. KAMUSAL HESAP ÖZELLİKLERİ

### 5.1 Duyuru Sistemi
```yaml
Duyuru Oluşturma:
  - Başlık
  - İçerik (zengin metin)
  - Öncelik (düşük, normal, yüksek, acil)
  - Hedef Kitle
  - Yayınlama Tarihi
  - Bitiş Tarihi

Duyuru Türleri:
  - Resmi Duyuru
  - Haber
  - Bilgilendirme
  - Acil Duyuru
```

### 5.2 Toplu Bildirim Sistemi
```yaml
Bildirim Kanalları:
  - Uygulama İçi
  - E-posta
  - SMS
  - Push Bildirim

Hedefleme:
  - Tüm Kullanıcılar
  - Hesap Türü Bazlı
  - Segment Bazlı
  - Özel Liste
```

### 5.3 Onaylı/Rozet Sistemi
```yaml
Rozet Türleri:
  - ✅ Resmi Kurum (Onaylı)
  - 🏢 Kurumsal Hesap
  - ⭐ Premium Üye
  - 🏆 Satıcı Rozeti

Öncelik:
  - Arama sonuçlarında üstte görünme
  - Önerilen içeriklerde öncelik
  - Güvenilir hesap işareti
```

---

## 6. E-TİCARET SİSTEMİ

### 6.1 Ürün Türleri
```yaml
Fiziksel Ürünler:
  - Ev, Daire, Villa
  - Araç, Tekne
  - Elektronik Cihazlar
  - Giyim ve Aksesuar
  - Ev Eşyaları
  - Her türlü mal

Dijital Ürünler:
  - Video Eğitimler
  - E-book'lar
  - Online Kurslar
  - Yazılımlar
  - Dijital Sanat

Hizmetler:
  - Eğitim (matematik dersi vb.)
  - Danışmanlık
  - Tasarım
  - Tamirat
  - Her türlü hizmet
```

### 6.2 Ürün Özellikleri
```yaml
Temel Bilgiler:
  - Ürün Adı
  - Açıklama
  - Kategori
  - Fiyat
  - Para Birimi
  - SKU (Stok Takip Kodu)

Görsel ve Medya:
  - Ürün Fotoğrafları (birden fazla)
  - Ürün Videosu
  - 360° Görünüm

Stok ve Lojistik:
  - Stok Miktarı
  - Kargo Bilgisi
  - Teslim Süresi

SEO:
  - URL Slug
  - Meta Başlık
  - Meta Açıklama
  - Etiketler
```

### 6.3 Video Eğitim Sistemi
```yaml
Eğitim İçeriği:
  - Eğitim Başlığı
  - Açıklama
  - Süre (dakika)
  - Bölüm Sayısı
  - Önizleme (ücretsiz)
  - Erişim Türü (ömür boyu, abonelik, süreli)

Bölümler:
  - Bölüm Başlığı
  - Video URL
  - Süre
  - Sıralama
  - Ücretsiz mi?

Erişim Kontrolü:
  - Satın alma sonrası erişim
  - Süre bazlı erişim
  - İndirme izni
```

---

## 7. YETKİLENDİRİLMİŞ SATIŞ SİSTEMİ

### 7.1 Sistem Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 YETKİLENDİRİLMİŞ SATIŞ AKIŞI                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Satıcı Ürünü Bulur                                    │
│  ├── Gayrimenkul uzmanı bir ev看到ir                             │
│  ├── Araç satıcısı bir araç看到ır                                │
│  └── Herhangi bir ürün olabilir                                 │
│                                                                 │
│  ADIM 2: Yetki İsteği Gönderir                                 │
│  ├── Ürün detayına gider                                        │
│  ├── "Bu Ürünü Satmak İstiyorum" butonuna basar                │
│  ├── Komisyon oranını teklif eder                               │
│  └── Mesaj yazar                                               │
│                                                                 │
│  ADIM 3: Ürün Sahibi İnceler                                   │
│  ├── Bildirim alır                                             │
│  ├── İsteği görüntüler                                         │
│  ├── Satıcı profiline bakar                                    │
│  ├── Komisyon oranını değerlendirir                            │
│  └── Onaylar veya Reddeder                                     │
│                                                                 │
│  ADIM 4: Onaylanırsa                                           │
│  ├── "Onaylı Satış" rozeti eklenir                             │
│  ├── Satıcı ürün artık satabilir                               │
│  ├── Komisyon oranı sabitlenir                                 │
│  └── Sözleşme/doküman oluşturulur                              │
│                                                                 │
│  ADIM 5: Satış Gerçekleşir                                     │
│  ├── Alıcı ürünü satın alır                                    │
│  ├── Ödeme alınır                                               │
│  ├── Komisyon otomatik hesaplanır                              │
│  ├── Para paylaşılır                                           │
│  └── Satış kaydı oluşturulur                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Komisyon Dağılımı

```
┌─────────────────────────────────────────────────────────────────┐
│                   KOMİSYON DAĞILIMI ÖRNEĞİ                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Satış Fiyatı: 1000₺                                           │
│                                                                 │
│  Platform Komisyonu: %1 → 10₺                                  │
│  Satıcı Komisyonu:   %5 → 50₺                                 │
│  Ürün Sahibine Kalan:     → 940₺                               │
│                                                                 │
│  ┌─────────────────────────────────────────────┐               │
│  │  Satış Fiyatı          1000₺               │               │
│  │  - Platform (%1)        -10₺               │               │
│  │  - Satıcı (%5)         -50₺               │               │
│  │  ─────────────────────────────             │               │
│  │  Ürün Sahibine          940₺               │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Komisyon Oranları

| Kategori | Min Komisyon | Varsayılan | Maks Komisyon |
|----------|-------------|------------|---------------|
| Gayrimenkul | %1 | %3 | %10 |
| Araç | %1 | %5 | %15 |
| Elektronik | %1 | %5 | %20 |
| Giyim | %1 | %10 | %30 |
| Dijital Ürün | %1 | %10 | %30 |
| Hizmet | %1 | %10 | %50 |
| Diğer | %1 | %5 | %50 |

---

## 8. İLAN SAYFASI SİSTEMİ

### 8.1 İlan Sayfası Oluşturma

```
┌─────────────────────────────────────────────────────────────────┐
│                    İLAN SAYFASI OLUŞTURMA                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Kimler İlan Sayfası Açabilir?                                 │
│  ├── Gayrimenkul Uzmanları (emlakçılar)                       │
│  ├── İkinci El Satıcıları                                      │
│  ├── Araç Galericileri                                         │
│  ├── Koleksiyoncular                                           │
│  └── Herhangi bir bireysel hesap                               │
│                                                                 │
│  İlan Sayfası İçeriği:                                         │
│  ├── Sayfa Adı ve Açıklaması                                   │
│  ├── Logo/Kapak Görseli                                        │
│  ├── Uzmanlık Alanı                                            │
│  ├── İlan Listesi (ürünler)                                    │
│  ├── İletişim Bilgileri                                        │
│  └── Puan/Yorumlar                                             │
│                                                                 │
│  İlan Ürünleri:                                                 │
│  ├── Kendi Ürünleri                                             │
│  │   └── Doğrudan eklenebilir                                  │
│  └── Başkasının Ürünleri                                       │
│      └── Yetki isteği → Onay → Eklenebilir                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Gayrimenkul Uzmanı Örneği

```
┌─────────────────────────────────────────────────────────────────┐
│              AHMET EMLAK - İLAN SAYFASI                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🏠 Ahmet Emlak                                                │
│  ├── Uzmanlık: Gayrimenkul                                     │
│  ├── Konum: İstanbul, Kadıköy                                  │
│  ├── Puan: ⭐ 4.8 (156 değerlendirme)                          │
│  └── Onaylı Satıcı ✅                                          │
│                                                                 │
│  📋 İLANLARIM (25 aktif ilan)                                  │
│  │                                                              │
│  ├── 🏠 Satılık Daire - Kadıköy (450.000₺)                   │
│  │   └── Onaylı Satış ✅ (Sahibi: Mehmet Bey)                  │
│  │                                                              │
│  ├── 🏠 Satılık Villa - Beykoz (2.500.000₺)                   │
│  │   └── Onaylı Satış ✅ (Sahibi: Ayşe Hanım)                 │
│  │                                                              │
│  ├── 🚗 2020 Model BMW - (850.000₺)                           │
│  │   └── Onaylı Satış ✅ (Sahibi: Ali Bey)                    │
│  │                                                              │
│  ├── 🏗️ Arsa - Şile (1.200.000₺)                             │
│  │   └── Kendi Ürünü                                           │
│  │                                                              │
│  └── ...                                                        │
│                                                                 │
│  💬 İLETİŞİM                                                   │
│  ├── Telefon: 0532 XXX XXXX                                    │
│  ├── E-posta: ahmet@emlak.com                                  │
│  └── WhatsApp: 0532 XXX XXXX                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. ÖDEME VE KOMİSYON SİSTEMİ

### 9.1 EMANET (ESCROW) SİSTEMİ

  Para platformda bekler, hizmet tamamlanınca hizmet verene geçer:

  ┌─────────────────────────────────────────────────────────────┐
  │  EMANET SİSTEMİ NASIL ÇALIŞIYOR?                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ADIM 1: SİPARİŞ/TALEP OLUŞTURMA                           │
  │  ├── Hizmet Alan: Hizmeti veya ürünü seçer                 │
  │  ├── Fiyat: Anlaşılır (sabit veya keşif sonrası)           │
  │  └── Ödeme: Hizmet Alan → Platform'a öder                  │
  │                                                             │
  │  ADIM 2: PARA PLATFORMDA BEKLİYOR (EMANET)                 │
  │  ├── Para ne hizmet verende ne hizmet alanda                │
  │  ├── Para platformun güvenli hesabında tutulur              │
  │  └── Her iki taraf da güvende                               │
  │                                                             │
  │  ADIM 3: HİZMET VERİR/ÜRÜN GÖNDERİLİR                      │
  │  ├── Hizmet Veren: Hizmeti tamamlar                         │
  │  ├── Satıcı: Ürünü kargoya verir                            │
  │  └── Hizmet Alan: Teslim alır veya kontrol eder            │
  │                                                             │
  │  ADIM 4: ONAY SİSTEMİ                                       │
  │  ├── Hizmet Alan: "Onaylıyorum" butonuna basar              │
  │  ├── veya Otomatik onay (7 gün sonra)                       │
  │  └── veya Ret (sorun varsa)                                 │
  │                                                             │
  │  ADIM 5: PARA HİZMET VERENE GEÇER                          │
  │  ├── Komisyon platformda kalır                              │
  │  ├── Kalan tutar hizmet verenin hesabına geçer              │
  │  └── Hizmet Veren parasını alır                             │
  │                                                             │
  │  ADIM 6: DEĞERLENDİRME                                      │
  │  ├── Hizmet Alan: Hizmet vereni puanlar                     │
  │  ├── Yorum yapar                                            │
  │  └── Sıralama etkilenir                                     │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  EMANET SİSTEMİ GÖRSELİ                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ┌──────────┐      ┌──────────┐      ┌──────────┐         │
  │  │          │      │          │      │          │         │
  │  │  HİZMET  │      │ PLATFOR  │      │ HİZMET   │         │
  │  │  ALAN    │      │   M      │      │ VEREN    │         │
  │  │          │      │          │      │          │         │
  │  └────┬─────┘      └────┬─────┘      └────┬─────┘         │
  │       │                  │                  │               │
  │       │  1. ÖDEME       │                  │               │
  │       │ ─────────────►  │                  │               │
  │       │                  │                  │               │
  │       │                  │  2. PARA         │               │
  │       │                  │  BEKLİYOR       │               │
  │       │                  │  💰💰💰         │               │
  │       │                  │                  │               │
  │       │                  │  3. HİZMET       │               │
  │       │                  │  YAPILIR        │               │
  │       │                  │  ─────────────► │               │
  │       │                  │                  │               │
  │       │  4. ONAY        │  5. PARA         │               │
  │       │  ✅              │  GEÇİŞİ         │               │
  │       │ ─────────────►  │  ─────────────► │               │
  │       │                  │  💰→💰         │               │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  EMANET SİSTEMİ ÖRNEKLERİ                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÖRNEK 1: TAMİRHANE                                        │
  │  ├── Müşteri: "Buzdolabım bozuldu, tamir istiyorum"        │
  │  ├── Teknisyen: Keşif → "2000 TL" der                      │
  │  ├── Müşteri: Onay verir                                    │
  │  ├── Ödeme: 2000 TL → Platform'da emanet olarak bekler     │
  │  ├── Teknisyen: Tamir eder                                  │
  │  ├── Müşteri: Kontrol eder, "Tamir olmuş" der              │
  │  ├── Onay: "Onaylıyorum" butonuna basar                     │
  │  └── Sonuç: 2000 TL - %10 komisyon = 1800 TL teknisyene    │
  │                                                             │
  │  ÖRNEK 2: DERS/EĞİTİM                                       │
  │  ├── Öğrenci: "10 saat matematik dersi alacağım"            │
  │  ├── Öğretmen: "Saatlik 200 TL, toplam 2000 TL"            │
  │  ├── Öğrenci: Onay verir                                    │
  │  ├── Ödeme: 2000 TL → Platform'da emanet                   │
  │  ├── Dersler verilir (10 ders)                              │
  │  ├── Her ders sonrası onay alınır                           │
  │  └── Sonuç: Her ders sonrası 200 TL öğretmene geçer        │
  │                                                             │
  │  ÖRNEK 3: ÇİFTÇİDEN ÜRÜN ALIŞVERİŞİ                        │
  │  ├── Çiftçi: "5 kg taze domates, 75 TL"                    │
  │  ├── Müşteri: Sipariş verir                                 │
  │  ├── Ödeme: 75 TL → Platform'da emanet                     │
  │  ├── Çiftçi: Ürünü paketler, kargoya verir                  │
  │  ├── Müşteri: Ürünü teslim alır, kontrol eder              │
  │  ├── Onay: "Ürünleri onaylıyorum"                           │
  │  └── Sonuç: 75 TL - %8 komisyon = 69 TL çiftçiye geçer    │
  │                                                             │
  │  ÖRNEK 4: İNŞAAT/TADİLAT                                    │
  │  ├── Müşteri: "Ev badanası yaptırmak istiyorum"             │
  │  ├── Firma: "15.000 TL, 3 taksit"                          │
  │  ├── Müşteri: Onay verir                                    │
  │  ├── 1. Taksit: 5.000 TL → Emanet                          │
  │  ├── Firma: İşe başlar, yarısını bitirir                   │
  │  ├── Onay 1: 5.000 TL → Firmaya geçer                      │
  │  ├── 2. Taksit: 5.000 TL → Emanet                          │
  │  ├── Firma: İşi bitirir                                     │
  │  ├── Onay 2: 5.000 TL → Firmaya geçer                      │
  │  ├── 3. Taksit: 5.000 TL → Emanet                          │
  │  ├── Onay 3: 5.000 TL → Firmaya geçer                      │
  │  └── Sonuç: Toplam 15.000 TL firmaya geçti                 │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  EMANET SİSTEMİ GÜVENLİK KURALLARI                         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  PARA NE ZAMAN GEÇER?                                       │
  │  ├── Hizmet Alan: "Onaylıyorum" derse                      │
  │  ├── 7 gün içinde onay gelmezse otomatik onaylanır         │
  │  ├── Ret durumunda: Sorun çözümü başlar                     │
  │  ├── Tartışma: Platform arabirimi devreye girer            │
  │  └── Anlaşmazlık: Platform karar verir                      │
  │                                                             │
  │  HANGİ DURUMLARDA PARA GERİ ALINIR?                         │
  │  ├── Hizmet verilmediyse (tamamen)                          │
  │  ├── Ürün gönderilmediyse                                    │
  │  ├── Ürün hasarlı geldiyse                                   │
  │  ├── Açıklamaya uymuyorsa                                   │
  │  └── Anlaşmazlık çözümünde                                  │
  │                                                             │
  │  KOMİSYON NE ZAMAN KESİLİR?                                 │
  │  ├── Para hizmet verene geçerken kesilir                    │
  │  ├── Komisyon oranı açıkça görünür                          │
  │  └── İade durumunda komisyon da iade edilir                 │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  KARŞILIKLI ANLAŞMA ÇERÇEVESİNDE ÖDEME                      │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ANLAŞMA NASIL OLUŞUR?                                      │
  │                                                             │
  │  ADIM 1: TALEP/İLAN                                         │
  │  ├── Hizmet Alan: "Bu hizmeti/ürünü istiyorum"              │
  │  ├── veya Hizmet Veren: "Bu hizmeti veriyorum" ilanı        │
  │  └── Fiyat ve koşullar belirtilir                           │
  │                                                             │
  │  ADIM 2: TEKLİF VE PAZARLIK                                 │
  │  ├── Hizmet Alan: Teklif sunar                              │
  │  ├── Hizmet Veren: Karşılık teklif sunar                    │
  │  ├── Mesajlaşma ile pazarlık yapılır                        │
  │  └── Anlaşmaya varılır                                      │
  │                                                             │
  │  ADIM 3: ANLAŞMA SÖZLEŞMESİ OLUŞTURULUR                     │
  │  ├── Hizmetin türü ve detayları                             │
  │  ├── Toplam tutar                                           │
  │  ├── Ödeme planı (taksitli ise)                             │
  │  ├── Teslim tarihi                                          │
  │  ├── Garanti koşulları                                       │
  │  ├── İade koşulları                                          │
  │  └── Her iki tarafın onayı                                  │
  │                                                             │
  │  ADIM 4: HER İKİ TARAF ONAY VERİR                          │
  │  ├── Hizmet Alan: "Anlaşmayı onaylıyorum" ✅               │
  │  ├── Hizmet Veren: "Anlaşmayı onaylıyorum" ✅              │
  │  └── Ancak ondan sonra para emanete alınır                  │
  │                                                             │
  │  ADIM 5: ÖDEME YAPILIR                                      │
  │  ├── Para platformda emanete alınır                         │
  │  ├── Anlaşma şartları sistemde kayıtlı                      │
  │  └── Her iki taraf da yükümlülüklerini yerine getirir       │
  │                                                             │
  │  ADIM 6: HİZMET/ÜRÜN TESLİMİ                                │
  │  ├── Hizmet Veren: Anlaşmaya uygun hizmeti/ürünü verir     │
  │  └── Hizmet Alan: Kontrol eder                              │
  │                                                             │
  │  ADIM 7: KARŞILIKLI ONAY                                    │
  │  ├── Hizmet Alan: "Anlaşmaya uygundur" ✅                  │
  │  ├── Hizmet Veren: "Hizmet tamamlandı" ✅                   │
  │  └── Her iki taraf da onaylarsa para geçer                  │
  │                                                             │
  │  ADIM 8: PARA TRANSFERİ                                     │
  │  ├── Komisyon kesilir                                       │
  │  ├── Kalan tutar hizmet verene geçer                        │
  │  └── Anlaşma tamamlanır                                     │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ANLAŞMA SÖZLEŞMESİ ÖRNEĞİ                                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  📋 ANLAŞMA SÖZLEŞMESİ #12345                       │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  TARAF 1: Ahmet Yılmaz (Hizmet Alan)               │   │
  │  │  TARAF 2: Mehmet Kaya (Hizmet Veren)               │   │
  │  │                                                     │   │
  │  │  HİZMET: Ev boyama hizmeti                          │   │
  │  │  Tutar: 15.000 TL                                   │   │
  │  │  Ödeme Planı: 3 taksit (5.000 TL x 3)             │   │
  │  │  Başlangıç: 10.06.2026                              │   │
  │  │  Bitiş: 25.06.2026                                  │   │
  │  │  Garanti: 1 yıl                                      │   │
  │  │                                                     │   │
  │  │  KOŞULLAR:                                           │   │
  │  │  ├── Boya markası: Marshall veya同等 kalite          │   │
  │  │  ├── Kat sayısı: Minimum 2 kat                      │   │
  │  │  ├── Temizlik: İş sonrası temizlik dahil           │   │
  │  │  └── Malzeme: Firma tarafından karşılanacak         │   │
  │  │                                                     │   │
  │  │  ✅ Ahmet Yılmaz: Onayladı (01.06.2026)             │   │
  │  │  ✅ Mehmet Kaya: Onayladı (01.06.2026)              │   │
  │  │                                                     │   │
  │  │  💰 Ödeme Durumu: 5.000 TL emanette                 │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ANLAŞMA DURUMLARI                                          │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  📝 Teklif Aşaması                                          │
  │  ├── Bir taraf teklif sundu                                 │
  │  └── Diğer tarafın yanıtı bekleniyor                        │
  │                                                             │
  │  💬 Pazarlık Aşaması                                        │
  │  ├── Koşullar müzakere ediliyor                             │
  │  └── Fiyat üzerinde anlaşılıyor                             │
  │                                                             │
  │  ✅ Anlaşma Sağlandı                                         │
  │  ├── Her iki taraf onayladı                                 │
  │  └── Ödeme bekleniyor                                       │
  │                                                             │
  │  💰 Ödeme Alındı                                            │
  │  ├── Para emanete alındı                                    │
  │  └── Hizmet/ürün bekleniyor                                 │
  │                                                             │
  │  🔄 Hizmet Devam Ediyor                                     │
  │  ├── Hizmet veren işe başladı                               │
  │  └── Süreç takip ediliyor                                   │
  │                                                             │
  │  ✅ Tamamlandı                                               │
  │  ├── Hizmet/ürün teslim edildi                              │
  │  ├── Karşılıklı onay verildi                                │
  │  └── Para transfer edildi                                   │
  │                                                             │
  │  ❌ İptal/Anlaşmazlık                                       │
  │  ├── Bir taraf iptal etti                                   │
  │  ├── Anlaşmazlık var                                       │
  │  └── Platform müdahalesi                                    │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ANLAŞMAZLIK ÇÖZÜMÜ                                        │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ANLAŞMAZLIK DURUMUNDA:                                     │
  │                                                             │
  │  1. TARAFLAR ARASINDA ÇÖZÜM                                 │
  │  ├── Mesajlaşma ile iletişim kurulur                        │
  │  ├── Karşılıklı anlayış aranır                              │
  │  └── Uzlaşma sağlanmaya çalışılır                           │
  │                                                             │
  │  2. PLATFORM ARABİLİĞİ                                      │
  │  ├── Taraflar anlaşamazsa                                   │
  │  ├── Platform devreye girer                                 │
  │  ├── Kanıtlar incelenir (fotoğraf, mesaj, sözleşme)        │
  │  └── Adil karar verilir                                     │
  │                                                             │
  │  3. KARAR MEKANİZMASI                                       │
  │  ├── Haklı olan taraf belirlenir                            │
  │  ├── Para iadesi veya tam ödeme yapılır                     │
  │  ├── Tarafların puanları etkilenir                          │
  │  └── Gerekirse yasal yollara başvurulur                     │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  İŞ TALEBİ / ÇAĞRI SİSTEMİ                                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  KİŞİ İŞ YAPTIRMAK İSTEDİĞİNDE:                            │
  │                                                             │
  │  1. İŞ İLANI AÇAR                                           │
  │  ├── "Bu işi yaptırmak istiyorum" ilanı verir               │
  │  ├── İşin detaylarını yazar                                  │
  │  ├── Fiyat belirler veya "piyasa fiyatına" yazar            │
  │  ├── Konum belirler                                         │
  │  ├── Tarih belirler                                         │
  │  └── Fotoğraf/video ekler (varsa)                           │
  │                                                             │
  │  2. HİZMET VERENLER BAŞVURUR                                │
  │  ├── İlanı görür                                             │
  │  ├── "Bu işi yapabilirim" der                                │
  │  ├── Teklif sunar (fiyat + açıklama)                        │
  │  ├── Profilini/puanını gösterir                              │
  │  └── Referanslarını ekler                                    │
  │                                                             │
  │  3. KİŞİ TEKLİFLERİ İNCELER                                │
  │  ├── Gelen teklifleri karşılaştırır                          │
  │  ├── Hizmet verenlerin profiline bakar                       │
  │  ├── Yorumları okur                                         │
  │  └── En uygun olanı seçer                                    │
  │                                                             │
  │  4. ANLAŞMA YAPILIR                                          │
  │  ├── Seçilen hizmet vereni ile anlaşma yapar                 │
  │  ├── Fiyat ve koşullar belirlenir                            │
  │  ├── Anlaşma sözleşmesi oluşturulur                          │
  │  └── Her iki taraf onay verir                                │
  │                                                             │
  │  5. ÖDEME YAPILIR                                            │
  │  ├── Para emanete alınır                                     │
  │  ├── Hizmet verilir                                          │
  │  ├── Onay alınır                                             │
  │  └── Para hizmet verene geçer                                │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  İŞ İLANI FORMU                                              │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  📋 YENİ İŞ İLANI AÇ                                 │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  İŞİN TÜRÜ:                                         │   │
  │  │  ○ Tamirat/Bakım                                    │   │
  │  │  ○ İnşaat/Tadilat                                   │   │
  │  │  ○ Temizlik                                         │   │
  │  │  ○ Eğitim/Ders                                      │   │
  │  │  ○ Nakliyat/Taşıma                                  │   │
  │  │  ○ Danışmanlık                                      │   │
  │  │  ○ Tasarım/Yazılım                                  │   │
  │  │  ○ Diğer: ___________                               │   │
  │  │                                                     │   │
  │  │  BAŞLIK:                                            │   │
  │  │  ┌─────────────────────────────────────────────┐   │   │
  │  │  │ Evimin badanasını yaptırmak istiyorum       │   │   │
  │  │  └─────────────────────────────────────────────┘   │   │
  │  │                                                     │   │
  │  │  AÇIKLAMA:                                          │   │
  │  │  ┌─────────────────────────────────────────────┐   │   │
  │  │  │ 3+1 evimin tüm içi badana yapılacak.        │   │   │
  │  │  │ duvarlar beyaz, tavanlar açık gri olacak.  │   │   │
  │  │  │ Malzeme tarafımdan karşılanacak.            │   │   │
  │  │  └─────────────────────────────────────────────┘   │   │
  │  │                                                     │   │
  │  │  FİYAT:                                             │   │
  │  │  ○ Sabit fiyat: _______ TL                          │   │
  │  ○ Piyasa fiyatına (tekliflere göre)               │   │
  │  ○ Görüşmeye açım                                   │   │
  │  │                                                     │   │
  │  │  KONUM:                                             │   │
  │  │  📍 İstanbul, Kadıköy                               │   │
  │  │                                                     │   │
  │  │  TARİH:                                             │   │
  │  │  📅 Başlangıç: __/__/__                            │   │
  │  │  📅 Bitiş: __/__/__                                 │   │
  │  │                                                     │   │
  │  │  FOTOĞRAF/EK:                                       │   │
  │  │  📷 [Fotoğraf Ekle]                                 │   │
  │  │                                                     │   │
  │  │  [İLANI YAYINLA]                                    │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  HİZMET VEREN BAKIŞ AÇISI                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  İŞ İLANLARI SAYFASI:                                       │
  │  ├── Yakın çevremdeki işler                                 │
  │  ├── Kategori bazlı filtreleme                               │
  │  ├── Fiyat aralığına göre filtreleme                         │
  │  ├── Tarihe göre filtreleme                                  │
  │  └── Duruma göre filtreleme (yeni/devam eden/tamamlanan)    │
  │                                                             │
  │  İŞ İLANI DETAYI:                                           │
  │  ├── İşin açıklaması                                        │
  │  ├── Fotoğraflar                                            │
  │  ├── Fiyat bilgisi                                          │
  │  ├── Konum                                                  │
  │  ├── Tarih                                                  │
  │  ├── İlan sahibinin profili                                 │
  │  └── Başvuru butonu                                         │
  │                                                             │
  │  BAŞVURU YAPMA:                                             │
  │  ├── "Bu işi yapabilirim" butonuna basar                    │
  │  ├── Kendi fiyatını teklif eder                             │
  │  ├── Ne kadar sürede yapacağını yazar                        │
  │  ├── Neden kendisi olduğunu anlatır                         │
  │  └── Profilini/referanslarını gösterir                      │
  │                                                             │
  │  TEKLİF FORMU:                                              │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  💰 TEKLİF SUN                                      │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  Teklif Fiyatım: _______ TL                        │   │
  │  │  Süre: _______ gün                                 │   │
  │  │  Açıklama:                                         │   │
  │  │  ┌─────────────────────────────────────────────┐   │   │
  │  │  │ Bu işi 10 yıllık deneyimimle yapabilirim.  │   │   │
  │  │  │ Marshall boyalar kullanıyorum.             │   │   │
  │  │  │ Referanslarımı profilemden görebilirsiniz. │   │   │
  │  │  └─────────────────────────────────────────────┘   │   │
  │  │                                                     │   │
  │  │  [TEKLİFİ GÖNDER]                                  │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  İŞ ÇAĞRI SİSTEMİ ÖRNEKLERİ                                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÖRNEK 1: TAMİRAT                                          │
  │  İlan: "Buzdolabım çalışmıyor, tamirci arıyorum"           │
  │  Teklifler: 3 tane geldi                                     │
  │  Seçim: En uygun olanı seçildi                              │
  │  Sonuç: Tamir edildi, 2000 TL ödendi                       │
  │                                                             │
  │  ÖRNEK 2: EĞİTİM                                           │
  │  İlan: "Lise öğrencisine matematik dersi vermek istiyorum"  │
  │  Teklifler: 5 tane geldi                                     │
  │  Seçim: En yakın ve puanlı öğretmen seçildi                │
  │  Sonuç: 10 ders verildi, 2000 TL ödendi                     │
  │                                                             │
  │  ÖRNEK 3: NAKLİYAT                                         │
  │  İlan: "Evden eve nakliyat lazım, 2+1"                      │
  │  Teklifler: 4 tane geldi                                     │
  │  Seçim: Fiyat ve güvenilirlik baz alındı                   │
  │  Sonuç: Taşınma tamamlandı, 8000 TL ödendi                  │
  │                                                             │
  │  ÖRNEK 4: TEMİZLİK                                         │
  │  İlan: "Ofis temizliği yaptıracağım, haftalık"              │
  │  Teklifler: 6 tane geldi                                     │
  │  Seçim: Haftalık anlaşma yapıldı                            │
  │  Sonuç: Her hafta 500 TL ödeniyor                           │
  │                                                             │
  │  ÖRNEK 5: ÇİFTÇİ ÜRÜN İHTİYACI                              │
  │  İlan: "1 ton buğday arıyorum, toptan"                      │
  │  Teklifler: 8 çiftçiden geldi                               │
  │  Seçim: En yakın ve uygun fiyatlı çiftçi                   │
  │  Sonuç: 1 ton buğday alındı, 10.000 TL ödendi              │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
  │  5. Satıcıya Bildirim Gider                                 │
  │  6. Ürün Hazırlanır/Kargoya Verilir                         │
  │  7. Alıcı Ürünü Teslim Alır                                 │
  │  8. Onay Verir (para satıcıya geçer)                        │
  │  9. Puan/Yorum Hakkı Doğar                                  │
  │                                                             │
  │  PARA AKIŞI:                                                │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │ Alıcı    │→│ Platform │→│ Komisyon │→│ Satıcı   │  │
  │  │ Ödeme    │  │ Hesabı   │  │ Kesilir  │  │ Hesabı   │  │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
  │                                                             │
  │  ORNEK:                                                     │
  │  Alıcı 100 TL öder → Platform 10 TL komisyon               │
  │  → Satıcıya 90 TL geçer                                    │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  HİZMET ÖDEME SİSTEMİ                                       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  HİZMET ALAN → HİZMET VERENE ÖDEME YAPAR                   │
  │                                                             │
  │  ÖDEME DURUMLARI:                                           │
  │  ├── Hizmet Öncesi                                          │
  │  │   ├── Tam Ödeme (hizmetten önce)                         │
  │  │   ├── Kapora/Depozito (kısmi ön ödeme)                   │
  │  │   └── Ücretsiz keşif, ödeme sonra                        │
  │  │                                                          │
  │  ├── Hizmet Sırasında                                       │
  │  ├── Hizmet Sonrası (onay sonrası)                          │
  │  ├── Taksitli Ödeme                                         │
  │  └── Garanti Kapsamında                                     │
  │                                                             │
  │  HİZMET ÖDEME DÖNGÜSÜ:                                      │
  │                                                             │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │ Hizmet   │→│ Keşif/   │→│ Hizmet   │→│ Onay/    │  │
  │  │ Talebi   │  │ Teklif   │  │ Yapılır  │  │ Ödeme    │  │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
  │       │             │             │             │          │
  │       ▼             ▼             ▼             ▼          │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │ Sepete   │  │ Fiyat    │  │ Tamamla- │  │ Para     │  │
  │  │ Ekleme   │  │ Onayı    │  │ nma      │  │ Geçişi   │  │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  HİZMET ÖDEME ÖRNEKLERİ                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÖRNEK 1: Tamirat Hizmeti                                  │
  │  ├── Müşteri: "Buzdolabım bozuldu"                         │
  │  ├── Teknisyen: Keşif gelir, "2000 TL" der                 │
  │  ├── Müşteri: Onay verir                                    │
  │  ├── Teknisyen: Tamir eder                                  │
  │  ├── Müşteri: Kontrol eder, onay verir                      │
  │  └── Ödeme: 2000 TL → Teknisyene geçer                      │
  │                                                             │
  │  ÖRNEK 2: İnşaat Hizmeti                                   │
  │  ├── Müşteri: "Evimin badanasını yaptırmak istiyorum"       │
  │  ├── Firma: Keşif gelir, "15.000 TL" der                   │
  │  ├── Müşteri: Onay verir, 5.000 TL kapora öder             │
  │  ├── Firma: İşe başlar                                      │
  │  ├── Ara ödeme: İşin yarısında 5.000 TL daha               │
  │  ├── Firma: İşi bitirir                                     │
  │  ├── Müşteri: Kontrol eder, onay verir                      │
  │  └── Ödeme: Kalan 5.000 TL → Firmaya geçer                  │
  │                                                             │
  │  ÖRNEK 3: Ders Hizmeti                                      │
  │  ├── Öğrenci: "Matematik özel dersi almak istiyorum"        │
  │  ├── Öğretmen: "Ders başı 200 TL" der                      │
  │  ├── Öğrenci: 10 ders için 2000 TL öder                     │
  │  ├── Öğretmen: Her ders sonrası onay alır                   │
  │  └── Para: Her ders sonrası 200 TL geçer                    │
  │                                                             │
  │  ÖRNEK 4: Taksi Hizmeti                                     │
  │  ├── Yolcu: "Havalimanına gideceğim"                        │
  │  ├── Şoför: "500 TL" der                                   │
  │  ├── Yolcu: Onay verir                                      │
  │  ├── Şoför: Yolculuğu tamamlar                              │
  │  ├── Yolcu: Otomatik ödeme onayı                            │
  │  └── Ödeme: 500 TL → Şoföre geçer                           │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

### 9.2 Ödeme Yöntemleri

```yaml
Online Ödeme:
  - Kredi Kartı (Visa, Mastercard, Troy)
  - Banka Kartı
  - Havale/EFT
  - Mobil Ödeme (Apple Pay, Google Pay)

Kripto Ödeme (opsiyonel):
  - Bitcoin
  - Ethereum
  - USDT

Diğer:
  - Kapıda Ödeme (nakit/kart)
  - Taksit Seçenekleri
  - Kupon/İndirim Kodu
```

### 9.3 Fatura Sistemi

```yaml
Fatura Bilgileri:
  - Fatura Numarası
  - Fatura Tarihi
  - Satıcı Bilgileri
  - Alıcı Bilgileri
  - Ürün/Hizmet Detayları
  - Tutarlar (brüt, komisyon, net)
  - KDV Bilgisi
  - Ödeme Durumu

Fatura Türleri:
  - Satış Faturası
  - Hizmet Faturası
  - Proforma Fatura
  - İade Faturası
```

### 9.4 KOMİSYON ORANLARI

  ┌─────────────────────────────────────────────────────────────┐
  │  KOMİSYON YAPISI                                           │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ALIŞVERİŞ KOMİSYONU:                                       │
  │  ├── Fiziksel Ürün: %5-10 (sektöre göre)                   │
  │  ├── Dijital Ürün: %10-15                                  │
  │  ├── Hizmet: %8-12                                         │
  │  └── İkinci El: %3-5                                       │
  │                                                             │
  │  HİZMET KOMİSYONU:                                          │
  │  ├── Tamirat: %8-10                                        │
  │  ├── Eğitim/Ders: %10-12                                   │
  │  ├── Danışmanlık: %10-15                                   │
  │  ├── Nakliyat: %5-8                                        │
  │  ├── Temizlik: %8-10                                       │
  │  └── Diğer: %8-12                                          │
  │                                                             │
  │  KOMİSYON DAĞILIMI:                                         │
  │  ├── Platform Komisyonu: %5-8                               │
  │  ├── Satıcı/Hizmet Veren: Kalan %92-95                     │
  │  └── Özel Durumlar: Anlaşmaya bağlı                        │
  │                                                             │
  │  ÖRNEK:                                                     │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │ Hizmet Tutarı: 1000 TL                             │   │
  │  │ Platform Komisyonu: %10 = 100 TL                    │   │
  │  │ Hizmet Verene Kalan: 900 TL                         │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

---

## 10. GÜVENLİK VE YETKİLENDİRME

### 10.1 ZORUNLU KİMLİK DOĞRULAMA VE SAHTE HESAP ÖNLEME

  Platformda sahte hesap olmayacak, herkes doğrulanmış olacak:

  ┌─────────────────────────────────────────────────────────────┐
  │  SAHTE HESAP ÖNLEME SİSTEMİ                                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  SAHTE HESAP OLMAYACAK:                                     │
  │  ├── Her hesap zorunlu olarak doğrulanacak                  │
  │  ├── Doğrulanmamış hesaplar aktif olamaz                   │
  │  ├── Sahte bilgi girenler tespit edilecek                   │
  │  ├── Tek kişilik sahte hesaplar engellenecek               │
  │  └── Platformdan atılacak                                    │
  │                                                             │
  │  NEDEN ZORUNLU?                                             │
  │  ├── Güvenli alışveriş için                                 │
  │  ├── Hizmet kalitesi için                                   │
  │  ├── Anlaşmazlık çözümü için                                │
  │  ├── Yasal zorunluluk (5651 sayılı kanun)                  │
  │  └── Kullanıcı güveni için                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ZORUNLU DOĞRULAMA BİLGİLERİ                                │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  BİREYSEL HESAP İÇİN ZORUNLU:                               │
  │                                                             │
  │  1. TELEFON DOĞRULAMASI                                     │
  │  ├── SMS ile kod gönderimi                                  │
  │  ├── Telefon numarası tekilleştirme                          │
  │  ├── Aynı numara ile birden fazla hesap açılamaz            │
  │  └── Her numara sadece bir hesapta kullanılabilir           │
  │                                                             │
  │  2. E-POSTA DOĞRULAMASI                                     │
  │  ├── E-posta adresine doğrulama linki gönderilir            │
  │  ├── Doğrulanmamış hesaplar kısıtlıdır                     │
  │  └── Her e-posta tekilleştirme                               │
  │                                                             │
  │  3. KİMLİK DOĞRULAMASI (ZORUNLU)                            │
  │  ├── T.C. Kimlik Numarası                                   │
  │  ├── Ad Soyad (kimlikteki ile aynı)                         │
  │  ├── Doğum Tarihi                                            │
  │  ├── Kimlik fotokopisi (ön ve arka)                         │
  │  ├── Selfie (kimlik ile birlikte)                           │
  │  │                                                          │
  │  │  DOĞRULAMA SÜRECİ:                                      │
  │  │  ├── Kullanıcı kimlik bilgilerini girer                  │
  │  │  ├── Kimlik fotokopisini yükler                          │
  │  │  │   ├── Ön yüz: Fotoğraf, ad, soyad, T.C. no           │
  │  │  │   └── Arka yüz: Seri no, imza                         │
  │  │  ├── Selfie çeker (kimlik ile birlikte)                  │
  │  │  ├── Yapay zeka ile otomatik kontrol                     │
  │  │  ├── Gerekirse manuel kontrol                             │
  │  │  └── Onaylanırsa hesap aktif olur                        │
  │  │                                                          │
  │  │  DOĞRULAMA KRİTERLERİ:                                   │
  │  │  ├── Kimlik fotokopisi okunabilir olmalı                 │
  │  │  ├── Selfie ile kimlik fotoğrafı uyuşmalı                │
  │  │  ├── Bilgiler tutarlı olmalı                             │
  │  │  ├── Kimlik geçerli tarihli olmalı                       │
  │  │  └── Sahte/fotoğraf manipülasyonu olmamalı               │
  │  │                                                          │
  │  └── Doğrulanmamış hesap:                                   │
  │      ├── Ürün ekleyemez                                     │
  │      ├── Satış yapamaz                                      │
  │      ├── Hizmet veremez                                     │
  │      ├── Para çekemez                                       │
  │      └── Sadece alışveriş yapabilir (sınırlı)              │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  KURUMSAL HESAP İÇİN ZORUNLU                                │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  1. TÜM BİREYSEL DOĞRULAMALARI YAPILMIŞ OLMALI             │
  │  │                                                          │
  │  2. ŞİRKET DOĞRULAMASI                                      │
  │  ├── Vergi Levhası                                          │
  │  ├── Ticaret Sicil Gazetesi                                 │
  │  ├── İmza Sirküleri                                         │
  │  ├── Oda Kayıt Belgesi                                      │
  │  └── Yetkili kişinin kimlik doğrulaması                     │
  │                                                             │
  │  3. YETKİLİ KİŞİ DOĞRULAMASI                               │
  │  ├── Şirket yetkilisinin kimlik doğrulaması                │
  │  ├── İmza yetkisi belgesi                                   │
  │  └── Vergi numarası doğrulaması                             │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DOĞRULAMA DURUMLARI                                        │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ⏳ Beklemede (Doğrulama bekleniyor)                        │
  │  ├── Hesap oluşturuldu                                      │
  │  ├── Bilgiler girildi                                       │
  │  ├── Doğrulama bekleniyor                                   │
  │  └── Sınırlı erişim                                         │
  │                                                             │
  │  🔄 İnceleniyor (Manuel kontrol)                            │
  │  ├── Otomatik kontrol tamamlandı                             │
  │  ├── Manuel inceleme gerekiyor                              │
  │  └── 24-48 saat içinde sonuçlanır                           │
  │                                                             │
  │  ✅ Doğrulandı (Aktif)                                       │
  │  ├── Tüm bilgiler onaylandı                                 │
  │  ├── Hesap tam aktif                                        │
  │  └── Tüm özellikler kullanılabilir                          │
  │                                                             │
  │  ❌ Reddedildi (Doğrulanamadı)                               │
  │  ├── Bilgiler yetersiz/hatalı                               │
  │  ├── Sahte bilgi tespit edildi                              │
  │  ├── Tekrar deneme hakkı var (2 kez)                        │
  │  └── 2. ret sonrası hesap kapatılır                        │
  │                                                             │
  │  🚫 Askıya Alındı (Şüpheli aktivite)                       │
  │  ├── Sahte hesap şüphesi                                    │
  │  ├── Dolandırıcılık şüphesi                                 │
  │  ├── İnceleme altına alındı                                 │
  │  └── Geçici olarak askıya alındı                            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SAHTE HESAP TESPİT SİSTEMİ                                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  OTOMATİK TESPİT YÖNTEMLERİ:                               │
  │                                                             │
  │  1. KİMLİK DOĞRULAMA                                        │
  │  ├── Kimlik fotokopisi analizi (Yapay Zeka)                 │
  │  │   ├── Fotoğraf kalitesi kontrolü                        │
  │  │   ├── Bilgi okunabilirliği                               │
  │  │   ├── Manipülasyon tespiti (photoshop vb.)               │
  │  │   └── Kimlik doğrulama servisi entegrasyonu              │
  │  │                                                          │
  │  ├── Selfie kontrolü                                        │
  │  │   ├── Yüz tanıma (kimlikteki yüz ile karşılaştırma)     │
  │  │   ├── Canlılık kontrolü (fotoğraf mı gerçek mi)         │
  │  │   └── Kimlik ile birlikte selfie zorunlu                 │
  │  │                                                          │
  │  └── Bilgi çapraz doğrulama                                 │
  │  │   ├── Nüfus müdürlüğü verisi ile karşılaştırma          │
  │  │   ├── Vergi dairesi doğrulaması                          │
  │  │   └── Banka hesap doğrulaması                            │
  │  │                                                          │
  │  2. DAVRANIŞ ANALİZİ                                        │
  │  ├── Aynı IP'den birden fazla hesap                         │
  │  ├── Aynı cihazdan birden fazla hesap                       │
  │  ├── Şüpheli giriş denemeleri                               │
  │  ├── Anormal aktivite paternleri                             │
  │  └── Hızlı hesap oluşturma/silme                            │
  │                                                             │
  │  3. İÇERİK ANALİZİ                                          │
  │  ├── Sahte ürün fotoğrafları (tersine görsel arama)        │
  │  ├── Kopyalanmış açıklamalar                                │
  │  ├── Şüpheli fiyatlandırma                                  │
  │  └── Dolandırıcılık kalıpları                               │
  │                                                             │
  │  4. TOPLULUK BİLDİRİMİ                                      │
  │  ├── Kullanıcıların sahte hesap bildirimi                   │
  │  ├── Şikayet sistemi                                        │
  │  └── Değerlendirme sistemi                                  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SAHTE HESAP CEZALARI                                       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  SAHTE BİLGİ GİRENLER:                                     │
  │  ├── Uyarı (ilk sefer)                                      │
  │  ├── Hesap askıya alma (tekrar)                             │
  │  ├── Hesap kalıcı olarak kapatma (3. sefer)                │
  │  └── Yasal işlem (dolandırıcılık durumunda)                │
  │                                                             │
  │  SAHTE HESAP AÇANLAR:                                       │
  │  ├── Hesap anında kapatılır                                 │
  │  ├── IP adresi engellenir                                   │
  │  ├── Cihaz bilgisi kaydedilir                               │
  │  ├── Yeni hesap açılması engellenir                          │
  │  └── Gerekirse yasal işlem başlatılır                       │
  │                                                             │
  │  DOLANDIRICILIK YAPANLAR:                                   │
  │  ├── Hesap kapatılır                                        │
  │  ├── Para dondurulur                                        │
  │  ├── Mağdurlara iade yapılır                                │
  │  ├── Yasal makamlara bildirilir                             │
  │  └── Kara listeye alınır                                    │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  KULLANICI DOĞRULAMA ADIMLARI                               │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ADIM 1: KAYIT                                              │
  │  ├── E-posta/telefon ile kayıt                              │
  │  └── Şifre belirleme                                        │
  │                                                             │
  │  ADIM 2: TELEFON DOĞRULAMASI                                │
  │  ├── SMS kodu gönderilir                                    │
  │  ├── Kod girilir                                            │
  │  └── Telefon doğrulanır                                     │
  │                                                             │
  │  ADIM 3: E-POSTA DOĞRULAMASI                                │
  │  ├── Doğrulama linki gönderilir                             │
  │  ├── Link tıklanır                                          │
  │  └── E-posta doğrulanır                                     │
  │                                                             │
  │  ADIM 4: KİMLİK DOĞRULAMASI                                 │
  │  ├── T.C. Kimlik Numarası girilir                           │
  │  ├── Ad Soyad, Doğum Tarihi girilir                         │
  │  ├── Kimlik fotokopisi yüklenir                             │
  │  ├── Selfie çekilir                                         │
  │  ├── Otomatik kontrol yapılır                               │
  │  └── Onaylanırsa hesap tam aktif olur                       │
  │                                                             │
  │  ADIM 5: PROFİL DOLDurma                                    │
  │  ├── Profil fotoğrafı                                       │
  │  ├── Kısa açıklama                                         │
  │  ├── Meslek/bilgi                                           │
  │  └── İsteğe bağlı diğer bilgiler                            │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  📱 DOĞRULAMA DURUMU                                 │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  ✅ E-posta doğrulandı                              │   │
  │  │  ✅ Telefon doğrulandı                              │   │
  │  │  ⏳ Kimlik doğrulanıyor...                          │   │
  │  │  ❌ Profil fotoğrafı eklenmedi                      │   │
  │  │                                                     │   │
  │  │  📊 Tamamlanma: %60                                │   │
  │  │  ████████████░░░░░░░░                              │   │
  │  │                                                     │   │
  │  │  ⚠️ Kimlik doğrulaması yapılmadan:                │   │
  │  │  ├── Ürün ekleyemezsiniz                           │   │
  │  │  ├── Satış yapamazsınız                           │   │
  │  │  └── Hizmet veremezsiniz                           │   │
  │  │                                                     │   │
  │  │  [KİMLİK DOĞRULAMAYA BAŞLA]                        │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

### 10.2 Rol-Tabanlı Erişim Kontrolü (RBAC)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROL VE YETKİ MATRİSİ                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ROL                │ YETKİLER                                  │
│  ───────────────────┼──────────────────────────────────────────  │
│  Super Admin        │ Tüm yetkiler                              │
│  Admin              │ Kullanıcı, içerik, ayar yönetimi          │
│  Corp Manager       │ Mağaza, ürün, çalışan, rapor yönetimi    │
│  Corp Staff         │ Ürün ekleme, sipariş görme               │
│  Seller             │ Kendi satışı, yetkili ürünler            │
│  User               │ Profil, alışveriş, yorum                 │
│  Viewer             │ Sadece okuma                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.3 Hesap Türü Bazlı Erişim

```yaml
Bireysel Hesap:
  - ✅ Kendi profilini düzenleme
  - ✅ Kendi ürünlerini ekleme/silme
  - ✅ İlan sayfası oluşturma
  - ✅ Video eğitim ekleme
  - ✅ Hizmet ekleme
  - ✅ Başkasının ürünlerini satma (onaylı)
  - ❌ Çalışan yönetimi
  - ❌ Finansal rapor

Kurumsal Hesap:
  - ✅ Tüm bireysel yetkiler
  - ✅ Mağaza yönetimi
  - ✅ Çalışan ekleme/çıkarma
  - ✅ Çalışan yetkilendirme
  - ✅ Finansal raporlar
  - ❌ Duyuru yapma
  - ❌ Toplu bildirim

Kamusal Hesap:
  - ✅ Tüm kurumsal yetkiler
  - ✅ Duyuru oluşturma
  - ✅ Toplu bildirim gönderme
  - ✅ Resmi onay
  - ✅ Öncelikli sıralama
```

### 10.4 Güvenlik Önlemleri

```yaml
Veri Güvenliği:
  - Şifre Hashleme (bcrypt, argon2)
  - Hassas verilerin şifrelenmesi (AES-256)
  - SQL Injection koruması
  - XSS koruması
  - CSRF token

API Güvenliği:
  - Rate Limiting
  - CORS ayarları
  - API Key yönetimi
  - IP whitelist (opsiyonel)

Oturum Yönetimi:
  - Concurrent session limit
  - Session timeout
  - Cihaz yönetimi
  - Konum bazlı oturum açma
```

### 10.5 GİZLİLİK VE KİŞİSEL VERİ KORUMA

  Kişisel bilgiler (ev adresi, telefon vb.) gizli tutulur:

  ┌─────────────────────────────────────────────────────────────┐
  │  KİŞİSEL BİLGİ GİZLİLİĞİ                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  GİZLİ TUTULAN BİLGİLER:                                   │
  │  ├── Ev adresi (sadece gerekli kişilere gösterilir)         │
  │  ├── Telefon numarası (gizlenebilir)                        │
  │  ├── E-posta adresi (gizlenebilir)                          │
  │  ├── Kimlik bilgileri (asla gösterilmez)                    │
  │  │                                                          │
  │  │  KİMLİK BİLGİLERİ HİÇ KİMSEYE GÖSTERİLMEZ:             │
  │  │  ├── T.C. Kimlik Numarası                               │
  │  │  ├── Pasaport Numarası                                   │
  │  │  ├── Ehliyet Numarası                                    │
  │  │  ├── Vergi Numarası (gerekli olmadıkça)                 │
  │  │  └── Banka Hesap Numarası (sadece ödeme sırasında)      │
  │  │                                                          │
  │  ├── Doğum tarihi (yaş olarak gösterilebilir)              │
  │  │                                                          │
  │  └── Fotoğraf (opsiyonel)                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  GİZLİLİK AYARLARI                                         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  KULLANICI KENDİ BİLGİLERİNİ KONTROL EDER:                 │
  │                                                             │
  │  📱 Telefon Numarası:                                       │
  │  ├── Herkese açık ❌                                       │
  │  ├── Sadece mesajlaşma arkadaşlarıma ✅                    │
  │  ├── Sadece işletme hesaplarına ✅                          │
  │  ├── Sadece ben onay verirsem ✅                            │
  │  └── Hiç kimseye ❌                                        │
  │                                                             │
  │  🏠 Ev Adresi:                                              │
  │  ├── Herkese açık ❌                                       │
  │  ├── Sadece kargo firmasına ✅                              │
  │  ├── Sadece hizmet verene (hizmet sırasında) ✅             │
  │  ├── Sadece ben onay verirsem ✅                            │
  │  ├── Sadece harita üzerinde genel bölge ❌                  │
  │  └── Hiç kimseye ❌ (sadece kargo firması bilir)           │
  │                                                             │
  │  📧 E-posta:                                                │
  │  ├── Herkese açık ❌                                       │
  │  ├── Sadece mesajlaşma arkadaşlarıma ✅                    │
  │  └── Hiç kimseye ❌                                        │
  │                                                             │
  │  📸 Fotoğraf:                                               │
  │  ├── Herkese açık ✅                                       │
  │  ├── Sadece arkadaşlarıma ✅                                │
  │  ├── Sadece ben onay verirsem ✅                            │
  │  └── Hiç kimseye ❌                                        │
  │                                                             │
  │  🎂 Doğum Tarihi:                                           │
  │  ├── Tam tarih herkese açık ❌                             │
  │  ├── Sadece yaş (30) ✅                                     │
  │  ├── Sadece arkadaşlarıma ✅                                │
  │  └── Hiç kimseye ❌                                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ADRES GİZLEMESİ - NASIL ÇALIŞIR?                          │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  DURUM 1: ÜRÜN SATIŞI                                       │
  │  ├── Satıcı: Adresini girer (kargo için)                   │
  │  ├── Alıcı: Sadece "İstanbul, Kadıköy" görür              │
  │  ├── Kargo Firması: Tam adresi görür                        │
  │  └── Sistem: Otomatik olarak gizler                         │
  │                                                             │
  │  DURUM 2: HİZMET ALIMI                                      │
  │  ├── Hizmet Alan: Adresini girer (hizmet için)             │
  │  ├── Hizmet Veren: Anlaşma sonrası tam adresi görür        │
  │  ├── Anlaşma Öncesi: Sadece ilçe/sem                       │
  │  └── Anlaşma Sonrası: Tam adres (izin ile)                 │
  │                                                             │
  │  DURUM 3: İŞ İLANI                                          │
  │  ├── İlan Sahibi: Konum belirler                            │
  │  ├── Başvuranlar: Sadece genel bölge görür                 │
  │  ├── Seçilen: Anlaşma sonrası tam adres                     │
  │  └── Reddedilenler: Adresi hiç görmez                       │
  │                                                             │
  │  DURUM 4: TAKSİ/HİZMET                                      │
  │  ├── Yolcu: Alınma adresini girer                           │
  │  ├── Şoför: Harita üzerinde noktayı görür                   │
  │  ├── Tam adres: Sadece biniş anında görünür                │
  │  └── Varmış adresi: Sadece varış anında görünür            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  MAHREMİYET KATMANLARI                                      │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  SEVİYE 1: HERKESE AÇIK (Profil)                           │
  │  ├── İsim, soyisim                                          │
  │  ├── Fotoğraf                                               │
  │  ├── Meslek                                                 │
  │  ├── Konum (il/seviye)                                      │
  │  └── Puan/değerlendirme                                     │
  │                                                             │
  │  SEVİYE 2: KISITLI (Arkadaşlar/İş)                         │
  │  ├── Telefon numarası (izin ile)                            │
  │  ├── E-posta (izin ile)                                     │
  │  ├── Doğum tarihi (opsiyonel)                               │
  │  └── Detaylı konum (ilçe/semt)                              │
  │                                                             │
  │  SEVİYE 3: GİZLİ (Sadece Gerekli)                          │
  │  ├── Tam adres (kargo/hizmet için)                          │
  │  ├── Kimlik bilgileri (platform tarafından saklanır)       │
  │  │                                                          │
  │  │  KİMLİK BİLGİLERİ PLATFORMDA SAKLANIR:                 │
  │  │  ├── T.C. Kimlik No: Şifreli (AES-256)                 │
  │  │  ├── Vergi No: Şifreli                                  │
  │  │  ├── Banka Hesabı: Şifreli                              │
  │  │  └── Hiçbir kullanıcıya gösterilmez                     │
  │  │                                                          │
  │  └── Banka bilgileri (sadece ödeme sırasında)              │
  │                                                             │
  │  SEVİYE 4: MUTLAK GİZLİ (Sadece Platform)                  │
  │  ├── Kimlik fotokopisi                                      │
  │  ├── Banka hesap detayları                                  │
  │  ├── IP adresi                                              │
  │  ├── Cihaz bilgisi                                          │
  │  └── Yasal zorunluluk olmadıkça kimseye gösterilmez         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  EV ADRESİ GİZLİ TUTMA SİSTEMİ                             │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  KULLANICI EV ADRESİNİ GİRDİĞİNDE:                         │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  🏠 Ev Adresi Ayarları                              │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  Adres: Atatürk Mah. 123. Sok. No:5/3              │   │
  │  │        Kadıköy / İstanbul                           │   │
  │  │                                                     │   │
  │  │  🔒 GİZLİLİK AYARI:                               │   │
  │  │                                                     │   │
  │  │  Bu adresi kimler görebilir?                        │   │
  │  │  ○ Herkese açık                                    │   │
  │  │  ● Sadece kargo firması (önerilen)                 │   │
  │  │  ○ Sadece hizmet verenler (hizmet sırasında)       │   │
  │  │  ○ Sadece ben onay verirsem                        │   │
  │  │  ○ Hiç kimseye (kargo firması hariç)              │   │
  │  │                                                     │   │
  │  │  📍 HARİTA ÜZERİNDE:                               │   │
  │  │  ○ Tam adres gösterilsin                           │   │
  │  │  ● Sadece genel bölge (Kadıköy)                    │   │
  │  │  ● Harita üzerinde nokta (yaklaşık konum)         │   │
  │  │                                                     │   │
  │  │  [KAYDET]                                          │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Alıcı: Sadece "Kadıköy, İstanbul" görür               │
  │  ├── Hizmet Veren: Anlaşma sonrası tam adresi görür        │
  │  ├── Kargo: Tam adresi görür                                │
  │  └── Diğerleri: Adresi hiç görmez                           │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

---

## 11. API ENDPOINT'LERİ

### 11.1 Kimlik Doğrulama

```
POST   /api/v1/auth/register              # Kayıt ol
POST   /api/v1/auth/login                 # Giriş yap
POST   /api/v1/auth/logout                # Çıkış yap
POST   /api/v1/auth/refresh               # Token yenile
POST   /api/v1/auth/forgot-password       # Şifre sıfırla
POST   /api/v1/auth/reset-password        # Şifre değiştir
POST   /api/v1/auth/verify-email          # E-posta doğrula
POST   /api/v1/auth/verify-phone          # Telefon doğrula
POST   /api/v1/auth/change-password       # Şifre değiştir
```

### 11.2 Kullanıcı Profili

```
GET    /api/v1/users/me                   # Mevcut kullanıcı bilgisi
GET    /api/v1/users/:id                  # Kullanıcı profili
PUT    /api/v1/users/me                   # Profili güncelle
DELETE /api/v1/users/me                   # Hesabı sil
PATCH  /api/v1/users/me/avatar            # Profil fotoğrafı güncelle
PATCH  /api/v1/users/me/cover             # Kapak fotoğrafı güncelle
```

### 11.3 Bireysel Hesap Modülleri

```
# Eğitimler
GET    /api/v1/users/:id/educations       # Eğitim listesi
POST   /api/v1/users/me/educations        # Eğitim ekle
PUT    /api/v1/users/me/educations/:id    # Güncelle
DELETE /api/v1/users/me/educations/:id    # Sil

# Kariyer
GET    /api/v1/users/:id/careers          # Kariyer listesi
POST   /api/v1/users/me/careers           # Kariyer ekle
PUT    /api/v1/users/me/careers/:id       # Güncelle
DELETE /api/v1/users/me/careers/:id       # Sil
POST   /api/v1/users/me/careers/:id/cv    # CV yükle

# İletişim
GET    /api/v1/users/me/contact           # İletişim bilgileri
PUT    /api/v1/users/me/contact           # Güncelle

# Projeler
GET    /api/v1/users/:id/projects         # Proje listesi
POST   /api/v1/users/me/projects          # Proje ekle
PUT    /api/v1/users/me/projects/:id      # Güncelle
DELETE /api/v1/users/me/projects/:id      # Sil
POST   /api/v1/users/me/projects/:id/media # Medya ekle

# Eğitimlerim
GET    /api/v1/users/:id/trainings        # Eğitim listesi
POST   /api/v1/users/me/trainings         # Eğitim ekle
PUT    /api/v1/users/me/trainings/:id     # Güncelle
DELETE /api/v1/users/me/trainings/:id     # Sil

# Sosyal Medya
GET    /api/v1/users/:id/social-accounts  # Hesap listesi
POST   /api/v1/users/me/social-accounts   # Hesap ekle
PUT    /api/v1/users/me/social-accounts/:id  # Güncelle
DELETE /api/v1/users/me/social-accounts/:id  # Sil

# Sosyal Çevre
GET    /api/v1/users/me/connections       # Bağlantılar
POST   /api/v1/users/me/connections       # İstek gönder
PUT    /api/v1/users/me/connections/:id   # İsteği kabul/reddet
DELETE /api/v1/users/me/connections/:id    # Bağlantıyı kaldır

# Varlıklarım
GET    /api/v1/users/:id/assets           # Varlık listesi
POST   /api/v1/users/me/assets            # Varlık ekle
PUT    /api/v1/users/me/assets/:id        # Güncelle
DELETE /api/v1/users/me/assets/:id        # Sil

# Danışmanlarım
GET    /api/v1/users/:id/advisors         # Danışman listesi
POST   /api/v1/users/me/advisors          # Danışman ekle
PUT    /api/v1/users/me/advisors/:id      # Güncelle
DELETE /api/v1/users/me/advisors/:id      # Sil

# İlgi Alanlarım
GET    /api/v1/users/:id/interests        # İlgi alanları
POST   /api/v1/users/me/interests         # Ekle
PUT    /api/v1/users/me/interests/:id     # Güncelle
DELETE /api/v1/users/me/interests/:id     # Sil

# Banka Bilgilerim
GET    /api/v1/users/me/banking           # Banka bilgileri
POST   /api/v1/users/me/banking           # Ekle
PUT    /api/v1/users/me/banking/:id       # Güncelle
DELETE /api/v1/users/me/banking/:id       # Sil

# Vergi Bilgilerim
GET    /api/v1/users/me/tax               # Vergi bilgileri
POST   /api/v1/users/me/tax               # Ekle
PUT    /api/v1/users/me/tax/:id           # Güncelle
DELETE /api/v1/users/me/tax/:id           # Sil

# Tescilli Belgelerim
GET    /api/v1/users/me/certified-docs    # Belgeler
POST   /api/v1/users/me/certified-docs    # Belge ekle
PUT    /api/v1/users/me/certified-docs/:id  # Güncelle
DELETE /api/v1/users/me/certified-docs/:id  # Sil
```

### 11.4 E-Ticaret Sistemi

```
# Ürünler
GET    /api/v1/products                   # Ürünleri listele
POST   /api/v1/products                   # Ürün oluştur
GET    /api/v1/products/:id               # Ürün detayı
PUT    /api/v1/products/:id               # Güncelle
DELETE /api/v1/products/:id               # Sil
POST   /api/v1/products/:id/media         # Medya ekle
DELETE /api/v1/products/:id/media/:mediaId  # Medya sil

# Kategoriler
GET    /api/v1/categories                 # Kategorileri listele
POST   /api/v1/categories                 # Kategori oluştur
GET    /api/v1/categories/:id             # Kategori detayı
PUT    /api/v1/categories/:id             # Güncelle
DELETE /api/v1/categories/:id             # Sil

# Dijital Ürünler
POST   /api/v1/products/:id/digital       # Dijital ürün ekle
PUT    /api/v1/products/:id/digital       # Güncelle
GET    /api/v1/products/:id/chapters      # Bölümleri listele
POST   /api/v1/products/:id/chapters      # Bölüm ekle
PUT    /api/v1/products/:id/chapters/:chapterId  # Bölümü güncelle
DELETE /api/v1/products/:id/chapters/:chapterId  # Bölümü sil

# Hizmetler
GET    /api/v1/services                   # Hizmetleri listele
POST   /api/v1/services                   # Hizmet oluştur
GET    /api/v1/services/:id               # Hizmet detayı
PUT    /api/v1/services/:id               # Güncelle
DELETE /api/v1/services/:id               # Sil
POST   /api/v1/services/:id/media         # Medya ekle
DELETE /api/v1/services/:id/media/:mediaId  # Medya sil

# Mağazalar
GET    /api/v1/stores                     # Mağazaları listele
POST   /api/v1/stores                     # Mağaza oluştur
GET    /api/v1/stores/:id                 # Mağaza detayı
PUT    /api/v1/stores/:id                 # Güncelle
DELETE /api/v1/stores/:id                 # Sil
GET    /api/v1/stores/:id/products        # Mağaza ürünleri
GET    /api/v1/stores/:id/services        # Mağaza hizmetleri
```

### 11.5 İlan Sayfası Sistemi

```
# İlan Sayfaları
GET    /api/v1/listings                   # İlan sayfalarını listele
POST   /api/v1/listings                   # İlan sayfası oluştur
GET    /api/v1/listings/:id               # İlan sayfası detayı
PUT    /api/v1/listings/:id               # Güncelle
DELETE /api/v1/listings/:id               # Sil
GET    /api/v1/listings/:id/products      # İlan ürünleri

# İlan Ürünleri
POST   /api/v1/listings/:id/products      # İlandan ürün ekle
DELETE /api/v1/listings/:id/products/:productId  # Ürünü kaldır
```

### 11.6 Yetkilendirilmiş Satış Sistemi

```
# Yetki İstekleri
POST   /api/v1/auth-requests              # Yetki isteği gönder
GET    /api/v1/auth-requests              # İstekleri listele
GET    /api/v1/auth-requests/:id          # İstek detayı
PUT    /api/v1/auth-requests/:id/approve  # İsteği onayla
PUT    /api/v1/auth-requests/:id/reject   # İsteği reddet

# Yetkilendirilmiş Satışlar
GET    /api/v1/authorized-sales           # Onaylı satışları listele
GET    /api/v1/authorized-sales/:id       # Satış detayı
GET    /api/v1/users/:id/seller-profile   # Satıcı profili
PUT    /api/v1/users/me/seller-profile    # Satıcı profilini güncelle
```

### 11.7 Sipariş ve Ödeme

```
# Siparişler
GET    /api/v1/orders                     # Siparişleri listele
POST   /api/v1/orders                     # Sipariş oluştur
GET    /api/v1/orders/:id                 # Sipariş detayı
PUT    /api/v1/orders/:id/cancel          # Siparişi iptal et
GET    /api/v1/orders/:id/tracking        # Kargo takibi

# Ödemeler
POST   /api/v1/payments                   # Ödeme yap
GET    /api/v1/payments/:id               # Ödeme detayı
GET    /api/v1/users/me/payments          # Ödeme geçmişi

# Faturalar
GET    /api/v1/invoices                   # Faturaları listele
GET    /api/v1/invoices/:id               # Fatura detayı
POST   /api/v1/invoices/:id/download      # Fatura indir
```

### 11.8 Kamusal Hesap

```
# Duyurular
POST   /api/v1/announcements              # Duyuru oluştur
GET    /api/v1/announcements              # Duyuruları listele
GET    /api/v1/announcements/:id          # Duyuru detayı
PUT    /api/v1/announcements/:id          # Güncelle
DELETE /api/v1/announcements/:id          # Sil

# Toplu Bildirimler
POST   /api/v1/bulk-notifications         # Bildirim oluştur
GET    /api/v1/bulk-notifications         # Bildirimleri listele
GET    /api/v1/bulk-notifications/:id     # Bildirim detayı
POST   /api/v1/bulk-notifications/:id/send  # Bildirimi gönder
```

### 11.9 Sosyal Özellikler

```
# Takip
POST   /api/v1/users/:id/follow           # Takip et
DELETE /api/v1/users/:id/follow           # Takipten çık
GET    /api/v1/users/:id/followers        # Takipçiler
GET    /api/v1/users/:id/following        # Takip edilenler

# Beğeni
POST   /api/v1/contents/:id/like          # Beğen
DELETE /api/v1/contents/:id/like          # Beğeniyi kaldır

# Yorumlar
GET    /api/v1/contents/:id/comments      # Yorumları listele
POST   /api/v1/contents/:id/comments      # Yorum ekle
PUT    /api/v1/comments/:id              # Yorumu güncelle
DELETE /api/v1/comments/:id              # Yorumu sil

# Mesajlaşma
GET    /api/v1/conversations              # Konuşmaları listele
POST   /api/v1/conversations              # Konuşma başlat
GET    /api/v1/conversations/:id          # Konuşma detayı
POST   /api/v1/conversations/:id/messages # Mesaj gönder
GET    /api/v1/conversations/:id/messages # Mesajları listele
```

### 11.10 Bildirimler

```
GET    /api/v1/notifications              # Bildirimleri listele
PATCH  /api/v1/notifications/:id/read     # Bildirimi okundu işaretle
PATCH  /api/v1/notifications/read-all     # Tümünü okundu işaretle
DELETE /api/v1/notifications/:id          # Bildirimi sil
```

### 11.11 Dosya Yükleme

```
POST   /api/v1/upload                     # Dosya yükle
POST   /api/v1/upload/multiple            # Çoklu dosya yükle
DELETE /api/v1/upload/:id                 # Dosyayı sil
GET    /api/v1/upload/presigned-url       # Presigned URL al
```

### 11.12 Admin

```
GET    /api/v1/admin/dashboard            # Dashboard verileri
GET    /api/v1/admin/users                # Tüm kullanıcılar
PATCH  /api/v1/admin/users/:id            # Kullanıcı yönetimi
GET    /api/v1/admin/accounts             # Tüm hesaplar
PATCH  /api/v1/admin/accounts/:id         # Hesap yönetimi
GET    /api/v1/admin/auth-requests        # Yetki istekleri
PATCH  /api/v1/admin/auth-requests/:id    # İstek yönetimi
GET    /api/v1/admin/audit-logs           # Denetim kayıtları
GET    /api/v1/admin/reports              # Raporlar
```

---

## 12. VERİTABANI ŞEMASI

Veritabanı şeması için detaylı bilgi → [DATABASE.md](./DATABASE.md)

---

## 13. PROJE KLASÖR YAPISI

```
web-platform/
├── docs/
│   ├── architecture/
│   │   ├── MASTER-PLAN.md           # Bu dosya
│   │   ├── DATABASE.md              # Veritabanı şeması
│   │   ├── API.md                   # API dokümantasyonu
│   │   └── SECURITY.md              # Güvenlik dokümanı
│   └── guides/
│       ├── deployment.md            # Deployment rehberi
│       └── development.md           # Geliştirme rehberi
│
├── src/
│   ├── core/                        # Çekirdek modüller
│   │   ├── auth/                    # Kimlik doğrulama
│   │   ├── database/                # Veritabanı
│   │   ├── storage/                 # Dosya depolama
│   │   ├── notification/            # Bildirim sistemi
│   │   ├── email/                   # E-posta sistemi
│   │   ├── cache/                   # Önbellek
│   │   └── search/                  # Arama motoru
│   │
│   ├── modules/                     # İş modülleri
│   │   ├── user/                    # Kullanıcı yönetimi
│   │   ├── account/                 # Hesap yönetimi
│   │   │   ├── individual/          # Bireysel hesap
│   │   │   ├── corporate/           # Kurumsal hesap
│   │   │   ├── public/              # Kamusal hesap
│   │   │   └── upgrade/             # Hesap yükseltme
│   │   ├── ecommerce/               # E-ticaret
│   │   │   ├── product/             # Ürün yönetimi
│   │   │   ├── order/               # Sipariş yönetimi
│   │   │   ├── payment/             # Ödeme yönetimi
│   │   │   └── shipping/            # Kargo yönetimi
│   │   ├── content/                 # İçerik yönetimi
│   │   │   ├── video/               # Video eğitim
│   │   │   ├── training/            # Eğitim yönetimi
│   │   │   ├── service/             # Hizmet yönetimi
│   │   │   └── post/                # Gönderi yönetimi
│   │   ├── store/                   # Mağaza yönetimi
│   │   ├── employee/                # Çalışan yönetimi
│   │   ├── announcement/            # Duyuru yönetimi
│   │   ├── messaging/               # Mesajlaşma
│   │   ├── review/                  # Değerlendirme
│   │   ├── asset/                   # Varlık yönetimi
│   │   ├── advisory/                # Danışmanlık
│   │   ├── finance/                 # Finans yönetimi
│   │   ├── certification/           # Belge yönetimi
│   │   └── listing/                 # İlan yönetimi
│   │
│   ├── api/                         # API katmanı
│   │   └── routes/                  # API rotaları
│   │
│   ├── middleware/                   # Middleware'ler
│   ├── utils/                       # Yardımcı fonksiyonlar
│   └── templates/                   # Şablonlar
│
├── frontend/                        # Frontend uygulaması
│   ├── src/
│   │   ├── components/              # Bileşenler
│   │   ├── pages/                   # Sayfalar
│   │   ├── hooks/                   # Hook'lar
│   │   ├── store/                   # State yönetimi
│   │   └── styles/                  # Stiller
│   └── public/                      # Statik dosyalar
│
├── admin/                           # Admin paneli
│   └── src/
│
├── tests/                           # Testler
│   ├── unit/                        # Birim testleri
│   ├── integration/                 # Entegrasyon testleri
│   └── e2e/                         # Uçtan uca testler
│
├── scripts/                         # Scriptler
├── docker/                          # Docker yapılandırma
├── .env.example                     # Çevre değişkenleri
├── package.json                     # Bağımlılıklar
├── tsconfig.json                    # TypeScript ayarları
└── README.md                        # Proje tanımı
```

---

## 14. TASARIM İLKELERİ

### 14.1 Sade ve Minimal Tasarım
```yaml
Tasarım İlkeleri:
  - Sadelik: Gereksiz element yok, sadece gerekli bilgiler
  - Beyaz Alan: Bol boşluk, göz yorgunluğu yok
  - Tipografi: Açık ve okunabilir fontlar
  - Renk: Sınırlı renk paleti (maksimum 3-4 renk)
  - İkonlar: Basit, anlaşılır ikonlar
  - Animasyon: Minimum, işlevsel animasyonlar

Sayfa Yapıları:
  - Ana Sayfa: Arama + Kategoriler + Öne Çıkanlar
  - Profil Sayfası: Bilgi + Hizmetler + Değerlendirmeler
  - Hizmet Detay: Basit, net bilgi
  - Sipariş: Adım adım, sadece gerekli alanlar
  - Mesajlaşma: WhatsApp benzeri sade sohbet
```

### 14.2 Mobil Uyumlu Tasarım
```yaml
Mobil Öncelikli:
  - İlk olarak mobilde çalışır
  - Masaüstü için genişletilir
  - Dokunmatik dostu butonlar
  - Parmağa uygun tıklama alanları
  - Hızlı yükleme
```

---

## 15. PUANLAMA SİSTEMİ

### 15.1 Puanlama Kuralı
```yaml
TEMEL KURAL: Sadece HİZMET ALAN kişi puanlama yapar!

Kim Puanlar?
  ✅ Hizmet Alan (alıcı/müşteri) → Hizmet Vereni puanlar
  ❌ Hizmet Veren (satıcı/sağlayıcı) → Puanlama YAPAMAZ

Neden?
  - Hizmet veren kendi kendini puanlayamaz
  - Hizmet alan gerçek deneyimini paylaşır
  - Daha güvenilir ve objektif değerlendirmeler

⚠️ PUANLAMA ZORUNLUDUR!
  - Hizmet tamamlandıktan sonra hizmet alan kişi puanlama YAPMAK ZORUNDADIR
  - Puanlama yapılmadan yeni hizmet alamaz
  - Puanlama yapılmadan hesap kısıtlamalara uğrar
  - Bu sayede her hizmet değerlendirmiş olur

🎯 PUANLAMA FİRMALAR İÇİN KRİTER OLUR!
  - Düşük puan alan firma/hizmet veren → İş kaybeder
  - Yüksek puan alan firma → Daha fazla müşteri çeker
  - Puan ortalaması arama sonuçlarında üst sıralara çıkar
  - Firmalar puanları için rekabet eder
  - Müşteriler puanlamaya göre karar verir

📊 FİRMALAR İÇİN KRİTER SİSTEMİ:
  
  ⭐ 4.5 - 5.0 Puan:
    ├── "Mükemmel" rozeti
    ├── Arama sonuçlarında EN ÜSTTE
    ├── Önerilen firmalar listesinde
    ├── Yeni müşteriler için otomatik önerilme
    └── Platform indirimlerinden faydalanma
  
  ⭐ 4.0 - 4.4 Puan:
    ├── "Güvenilir" rozeti
    ├── Arama sonuçlarında ÜST SIRADA
    ├── İyi konumda görünme
    └── Normal müşteri akışı
  
  ⭐ 3.5 - 3.9 Puan:
    ├── "Orta" rozeti
    ├── Arama sonuçlarında ORTA SIRADA
    └── Dikkatli müşteri seçimi gerekli
  
  ⭐ 3.0 - 3.4 Puan:
    ├── "Dikkat" rozeti
    ├── Arama sonuçlarında ALT SIRADA
    ├── Müşteri kaybı başlar
    └── Uyarı sistemi aktif
  
  ⭐ 1.0 - 2.9 Puan:
    ├── "Risk" rozeti
    ├── Arama sonuçlarında EN ALTTA
    ├── Yeni müşteri bulması ZOR
    ├── Platform kısıtlamaları
    └── Hesap askıya alma riski
  
  ⭐ 0 - 1.0 Puan:
    ├── Hesap KAPATILIR
    └── Platformdan atılır

📈 FİRMALAR İÇİN İŞ MODELİ:

  Yüksek Puanın Getirileri:
    ├── Daha fazla müşteri → Daha fazla gelir
    ├── Platformda üst sıralarda çıkma → Görünürlük artışı
    ├── Müşteri sadakati → Tekrar eden işler
    ├── Referans sistemi → Yeni müşteriler
    ├── Premium özellikler → Ek gelir kapıları
    └── Rekabet avantajı → Pazar payı artışı

  Düşük Puanın Sonuçları:
    ├── Müşteri kaybı → Gelir düşüşü
    ├── Alt sıralarda görünme → Görünürlük azalması
    ├── Referans alamama → Yeni müşteri bulamama
    ├── Platform kısıtlamaları → İş yapamama
    ├── Hesap askıya alma → Tamamen işsizlik
    └── Hesap kapatma → Platformdan atılma

  Firmalar İçin Strateji:
    ├── Her işi titizlikle yap → Yüksek puan al
    ├── Müşteri memnuniyeti öncelik → Puanını koru
    ├── Zamanında teslim → Güvenilirlik kazan
    ├── İyi iletişim → İletişim puanını yüksek tut
    ├── Uygun fiyat → Fiyat/performans puanını yüksek tut
    └── Sürekli geliş → Puanını artır

🏆 ÖRNEK SENARYO:

  Ahmet Usta (Alçı Ustası):
    ├── Puan: 4.8 ⭐ (156 değerlendirme)
    ├── Durum: "Mükemmel" rozetli
    ├── Ayda ortalama: 25 iş
    ├── Kazanç: Yüksek
    └── Sebep: Her işini titizlikle yapıyor, zamanında bitiriyor

  Mehmet Usta (Alçı Ustası):
    ├── Puan: 2.3 ⭐ (12 değerlendirme)
    ├── Durum: "Risk" rozetli
    ├── Ayda ortalama: 2 iş
    ├── Kazanç: Çok düşük
    └── Sebep: Geç kalıyor, iletişim sorunlu, işi yarım bırakıyor

  SONUÇ:
    Ahmet Usta her ay 25 iş yaparak yüksek kazanç elde ediyor.
    Mehmet Usta neredeyse hiç iş bulamıyor ve platformdan ayrılıyor.

  BU SİSTEM SADECE PUANLAMA DEĞİL,
  İŞ YAPMA KAPASİTESİNİ DOĞRUDAN ETKİLİYOR!

🔧 SANAYİ ÖRNEĞİ: YEDEK PARÇA SATICISI

  Arama: "Fren Balatası" yazıyorsun

  SONUÇLAR (puana göre sıralanmış):

  1. ⭐ 4.9 (250 değerlendirme) → Ali Yedek Parça
     ├── "Mükemmel" rozeti
     ├── EN ÜSTTE GÖRÜNÜR
     ├── Tıklanma oranı: Yüksek
     └── Satış: Çok yüksek

  2. ⭐ 4.7 (180 değerlendirme) → Mehmet Oto Yedek
     ├── "Güvenilir" rozeti
     ├── ÜST SIRADA
     ├── Tıklanma oranı: İyi
     └── Satış: İyi

  3. ⭐ 4.2 (95 değerlendirme) → Veli Oto Parça
     ├── "İyi" rozeti
     ├── ORTA SIRADA
     ├── Tıklanma oranı: Orta
     └── Satış: Orta

  4. ⭐ 3.1 (45 değerlendirme) → Hasan Ticaret
     ├── "Dikkat" rozeti
     ├── ALT SIRADA
     ├── Tıklanma oranı: Düşük
     └── Satış: Düşük

  5. ⭐ 1.8 (8 değerlendirme) → Şüpheli Parça
     ├── "Risk" rozeti
     ├── EN ALTTA
     ├── Tıklanma oranı: Çok düşük
     └── Satış: Neredeyse yok

  SONUÇ:
  Ali Yedek Parça her ay binlerce satış yapıyor
  çünkü en yüksek puanla EN ÜSTTE Görünüyor.

  Şüpheli Parça ise neredeyse hiç satış yapamıyor
  çünkü EN ALTTA ve kimsenin güveni yok.

📊 ARAMA ALGORİTMASI NASIL ÇALIŞIYOR:

  Arama Yapıldığında:
    1. Önce ilgili sektör/meslek filtresi
    2. Sonra konum filtresi (yakınlık)
    3. EN SON SIRA ALGORİTMASI ile sıralar

  ══════════════════════════════════════════════════════════════
  SIRA ALGORİTMASI: Tüm etmenler birleşir = Sıralama
  ══════════════════════════════════════════════════════════════

  KRİTERLER VE AĞIRLIKLARI:

  ┌─────────────────────────────────────────────────────────────┐
  │  KRİTER                        │ AĞIRLIK  │ ETKİ           │
  ├─────────────────────────────────┼──────────┼────────────────┤
  │  1. Puan Ortalaması (yıldız)   │   %30    │ Çok Yüksek     │
  │  2. Değerlendirme Sayısı       │   %15    │ Yüksek         │
  │  3. Toplam Hizmet İş Sayısı    │   %20    │ Çok Yüksek     │
  │  4. Beğeni Sayısı              │   %10    │ Yüksek         │
  │  5. Son 30 Gün Aktifliği       │   %10    │ Yüksek         │
  │  6. Yanıt Hızı                 │   %5     │ Orta           │
  │  7. İçerik Kalitesi            │   %5     │ Orta           │
  │  8. Hesap Yaşı                 │   %5     │ Düşük          │
  └─────────────────────────────────┴──────────┴────────────────┘

  DETAYLI AÇIKLAMA:

  1. PUAN ORTALAMASI (%30):
     ├── 5.0 yıldız → 100 puan
     ├── 4.5 yıldız → 90 puan
     ├── 4.0 yıldız → 80 puan
     ├── 3.5 yıldız → 70 puan
     ├── 3.0 yıldız → 60 puan
     ├── 2.5 yıldız → 50 puan
     ├── 2.0 yıldız → 30 puan
     └── 1.0 yıldız → 10 puan

  2. DEĞERLENDİRME SAYISI (%15):
     ├── 500+ değerlendirme → 100 puan
     ├── 250-499 → 85 puan
     ├── 100-249 → 70 puan
     ├── 50-99 → 55 puan
     ├── 20-49 → 40 puan
     ├── 10-19 → 25 puan
     └── 0-9 → 10 puan

  3. TOPLAM HİZMET İŞ SAYISI (%20):
     ├── 1000+ iş → 100 puan
     ├── 500-999 → 85 puan
     ├── 200-499 → 70 puan
     ├── 100-199 → 55 puan
     ├── 50-99 → 40 puan
     ├── 20-49 → 25 puan
     └── 0-19 → 10 puan

  4. BEĞENİ SAYISI (%10):
     ├── 2000+ beğeni → 100 puan
     ├── 1000-1999 → 85 puan
     ├── 500-999 → 70 puan
     ├── 200-499 → 55 puan
     ├── 100-199 → 40 puan
     ├── 50-99 → 25 puan
     └── 0-49 → 10 puan

  5. SON 30 GÜN AKTİVLİĞİ (%10):
     ├── 30+ iş → 100 puan
     ├── 20-29 → 85 puan
     ├── 15-19 → 70 puan
     ├── 10-14 → 55 puan
     ├── 5-9 → 40 puan
     ├── 1-4 → 25 puan
     └── 0 → 0 puan

  6. YANIT HIZI (%5):
     ├── 5 dakika altında → 100 puan
     ├── 5-15 dakika → 80 puan
     ├── 15-30 dakika → 60 puan
     ├── 30-60 dakika → 40 puan
     ├── 1-24 saat → 20 puan
     └── 24+ saat → 0 puan

  7. İÇERİK KALİTESİ (%5):
     ├── Profil fotoğrafı var → +10
     ├── Kapak fotoğrafı var → +10
     ├── Detaylı açıklama var → +10
     ├── Fotoğraf galerisi var → +10
     ├── Video var → +10
     └── Düzgünbiosu var → +10

  8. HESAP YAŞI (%5):
     ├── 5+ yıl → 100 puan
     ├── 3-5 yıl → 80 puan
     ├── 1-3 yıl → 60 puan
     ├── 6 ay-1 yıl → 40 puan
     └── 6 ay altı → 20 puan

  ══════════════════════════════════════════════════════════════

  ÖRNEK HESABLAMA:

  Ali (Alçı Ustası):
    ├── Puan: 4.9 × 30 = 147
    ├── Değerlendirme: 250 × 15 = 127.5
    ├── İş Sayısı: 800 × 20 = 160
    ├── Beğeni: 1500 × 10 = 150
    ├── Aktiflik: 25 × 10 = 83
    ├── Yanıt Hızı: 8 dk × 5 = 40
    ├── İçerik: 50 × 5 = 25
    └── Hesap Yaşı: 3 yıl × 5 = 15
    TOPLAM: 747.5 puan → 1. SIRA

  Mehmet (Alçı Ustası):
    ├── Puan: 4.2 × 30 = 126
    ├── Değerlendirme: 85 × 15 = 63.75
    ├── İş Sayısı: 200 × 20 = 40
    ├── Beğeni: 300 × 10 = 30
    ├── Aktiflik: 8 × 10 = 26
    ├── Yanıt Hızı: 45 dk × 5 = 15
    ├── İçerik: 20 × 5 = 10
    └── Hesap Yaşı: 1 yıl × 5 = 5
    TOPLAM: 315.75 puan → 5. SIRA

  Hasan (Alçı Ustası):
    ├── Puan: 2.8 × 30 = 84
    ├── Değerlendirme: 20 × 15 = 15
    ├── İş Sayısı: 30 × 20 = 6
    ├── Beğeni: 50 × 10 = 5
    ├── Aktiflik: 2 × 10 = 6.6
    ├── Yanıt Hızı: 3 saat × 5 = 5
    ├── İçerik: 5 × 5 = 2.5
    └── Hesap Yaşı: 6 ay × 5 = 2.5
    TOPLAM: 126.6 puan → 18. SIRA

  ══════════════════════════════════════════════════════════════

  SONUÇ FORMÜLÜ:

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  ÇOK İŞ YAP + YÜKSEK PUAN AL + BEĞENİ TOPLA              │
  │  + İÇERİK PAYLAŞ + HIZLI YANIT VER + AKTİF OL             │
  │  ═══════════════════════════════════════════════           │
  │  = EN ÜST SIRALARDA GÖRÜNÜR = ÇOK İŞ YAPARSIN            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  BU YÜZDEN HER İŞ ÇOK ÖNEMLİ!
  HER DEĞERLENDİRME HAYATI ÖNEM TAŞIYOR!
  HER BEĞENİ SIKIYLAŞTIRIYOR!
  HER İÇERİK GÖRÜNÜRLÜĞÜ ARTIRIYOR!

🚗 YOL YARDIMI ÖRNEĞİ:

  Senaryo: Araban yolda kaldı, yol yardımı arıyorsun

  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMA A: Güven Yol Yardımı (İyi Hizmet)                  │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 4.8 (320 değerlendirme)                          │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "20 dakikada geldi, çok yardımcı oldu" ⭐⭐⭐⭐⭐      │
  │  ├── "Uygun fiyat, dürüst çalıştı" ⭐⭐⭐⭐⭐              │
  │  ├── "Arızamı hemen buldu, çözüme ulaştırdı" ⭐⭐⭐⭐⭐    │
  │  └── "Kesinlikle tavsiye ederim" ⭐⭐⭐⭐⭐                │
  │                                                             │
  │  Ücret: Piyasa fiyatının altında                             │
  │  Süre: ortalama 25 dakikada ulaşım                           │
  │  Garanti: Yaptığı işe garanti veriyor                        │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 1. SIRADA ÇIKAR                               │
  │  ├── Her gün 8-10 müşteri alıyor                            │
  │  └── Kazanç: ÇOK YÜKSEK                                    │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMA B: Hızır Oto (Kötü Hizmet + Fahiş Fiyat)           │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 1.6 (35 değerlendirme)                           │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "2 saat bekletti, gelmedi" ⭐                          │
  │  ├── "Piyasanın 3 katı fiyat istedi" ⭐                    │
  │  ├── "Arızayı bulamadı, boş yere para aldı" ⭐             │
  │  ├── "Telefonumu açmıyor, geri dönüş yapmıyor" ⭐          │
  │  └── "KESİNLİKLE UZAK DURUN!" ⭐                          │
  │                                                             │
  │  Ücret: Piyasa fiyatının 2-3 katı                           │
  │  Süre: ortalama 1.5 saat geç geliyor                        │
  │  Garanti: Garanti vermiyor                                  │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 20. SIRADA ÇIKAR                               │
  │  ├── Haftada 1-2 müşteri zor buluyor                        │
  │  ├── Müşteriler iade istiyor                                │
  │  ├── Şikayet yağıyor                                        │
  │  └── Kazanç: ÇOK DÜŞÜK + Platformdan atılma riski         │
  └─────────────────────────────────────────────────────────────┘

  ══════════════════════════════════════════════════════════════
  KÖTÜ HİZMET ARTIK GİZLİ KALMIYOR!

  Eskiden:
  ├── Kötü hizmet verirsin → Müşteri sessizce gider
  ├── Kimse bilmez → Aynı şeyi başkasına yaparsın
  └── Döngü devam eder

 Şimdi (Bu Platformda):
  ├── Kötü hizmet verirsin → Müşteri hemen puanlar ⭐
  ├── HERKES görür → Yorumlar herkese açık
  ├── Aramada EN ALTTA ÇIKARSIN → Kimse seni bulamaz
  ├── İş kaybedersin → Kazancın düşer
  └── Platformdan atılırsın → Tamamen biter

  MÜŞTERİ MEMNUNİYETİ ARTIK ZORUNLU!
  ─────────────────────────────────────
  İyi hizmet ver → Yüksek puan al → Çok iş yap → Çok kazan
  Kötü hizmet ver → Düşük puan al → İş bulamaz → Kazançsız kal
  ══════════════════════════════════════════════════════════════

🚕 TAKSİ ŞOFÖRÜ ÖRNEĞİ:

  ┌─────────────────────────────────────────────────────────────┐
  │  ŞOFÖR A: Mehmet Abi (Müşteri Odaklı)                      │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 4.9 (450 değerlendirme)                          │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Çok temiz araç, güzel sohbet" ⭐⭐⭐⭐⭐             │
  │  ├── "Trafik durumunu haber verdi, alternatif yol gösterdi"│
  │  ├── "Ücret konusunda dürüst, fazla almadı" ⭐⭐⭐⭐⭐    │
  │  ├── "Bagajlara yardımcı oldu" ⭐⭐⭐⭐⭐                  │
  │  ├── "Çocuklar için oto koltuğu vardı" ⭐⭐⭐⭐⭐         │
  │  └── "Her seferinde onu arıyorum, başka taksi kullanmıyorum"│
  │                                                             │
  │  Özellikler:                                                │
  │  ├── Aracı her zaman temiz ve kokulu                        │
  │  ├── Müşteriyle iyi iletişim kurar                          │
  │  ├── Dürüst ücret alır (taksimetreye sadık)                │
  │  ├── Yolculuk sırasında yardımcı olur                       │
  │  └── Her zaman güleryüzlü                                   │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 1. SIRADA ÇIKAR                               │
  │  ├── Günde 20+ yolcu taşıyor                                │
  │  ├── Sabit müşterileri var                                  │
  │  ├── Kazanç: ÇOK YÜKSEK                                    │
  │  └── "En İyi Taksi" rozeti var                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ŞOFÖR B: Ali Abi (Müşteri Memnuniyetsizliği)              │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 1.2 (60 değerlendirme)                           │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Aracı çok pisti, kokuyordu" ⭐                       │
  │  ├── "Taksimetreyi açmadı, keyfi fiyat söyledi" ⭐        │
  │  ├── "Telefonla konuştu durdu, dikkatli değildi" ⭐       │
  │  ├── "Yolcu indirmek istedim, daha uzağa götürdü" ⭐     │
  │  ├── "Kaba davranış, sesli müzik dinletti" ⭐             │
  │  ├── "Bagajı kendi kaldırdım, yardımcı olmadı" ⭐        │
  │  └── "Bir daha asla binmem, herkes uzak dursun!" ⭐      │
  │                                                             │
  │  Özellikler:                                                │
  │  ├── Aracı kirli ve bakımsız                               │
  │  ├── Müşteriyle uğraşır, kaba davranır                     │
  │  ├── Taksimetreyi açmaz, fazla fiyat ister                 │
  │  ├── Gereksiz yere uzun yol gider                          │
  │  ├── Müşteriyi indirmek istemez                            │
  │  └── Telefonla sürekli konuşur                              │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 30. SIRADA ÇIKAR                              │
  │  ├── Günde 2-3 yolcu zor buluyor                           │
  │  ├── Hiçbir sabit müşterisi yok                            │
  │  ├── Müşteriler iade istiyor                               │
  │  ├── Şikayet yağıyor                                       │
  │  ├── Kazanç: ÇOK DÜŞÜK                                    │
  │  └── Platformdan atılma riski ÇOK YÜKSEK                   │
  └─────────────────────────────────────────────────────────────┘

  ══════════════════════════════════════════════════════════════
  TAKSİCİLİKTE FARK YARATAN ŞEYLER:

  ┌─────────────────────────────────────────────────────────────┐
  │  İYİ TAKSİCİ               │  KÖTÜ TAKSİCİ                │
  ├─────────────────────────────┼──────────────────────────────┤
  │  ✅ Temiz araç              │  ❌ Kirli araç                │
  │  ✅ Dürüst ücret            │  ❌ Fazla ücret               │
  │  ✅ İyi iletişim            │  ❌ Kaba davranış             │
  │  ✅ Zamanında gelir         │  ❌ Geç gelir                 │
  │  │  Yardımcı olur           │  ❌ Yardım etmez             │
  │  ✅ Güleryüzlü              │  ❌ Suratsız                  │
  │  ✅ Alternatif yol gösterir │  ❌ Gereksiz yere uzatır      │
  │  ✅ Bagajlara yardım eder   │  ❌ İlgilenmez                │
  ├─────────────────────────────┼──────────────────────────────┤
  │  SONUÇ:                    │  SONUÇ:                      │
  │  Yüksek puan → Çok müşteri │  Düşük puan → Az müşteri     │
  │  Yüksek kazanç             │  Düşük kazanç                 │
  │  Platformda kalır          │  Platformdan atılır           │
  └─────────────────────────────┴──────────────────────────────┘

  BU SİSTEMDE:
  ─────────────
  Taksi şoförü artık sadece "yolcu taşımıyor"
  → MÜŞTERİ MEMNUNİYETİ SATIYOR!

  Her yolculuk bir DEĞERLENDİRME fırsatı
  Her puan bir KRİTER
  Her yorum bir REHBER

  MÜŞTERİLER ARTIK SEÇİCİ:
  ├── Yüksek puanlı şoförleri tercih ediyor
  ├── Düşük puanlı şoförlerden kaçınıyor
  └── Yorumları okuyarak karar veriyor

  ══════════════════════════════════════════════════════════════

🚌 OTOBÜS FİRMASI ÖRNEĞİ:

  "istanbul ankara otobüs" araması yapıldığında:

  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMA A: Güven Tur (Müşteri Memnuniyeti Odaklı)           │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 4.8 (1200 değerlendirme)                         │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Koltuklar çok rahat, wifi mükemmel" ⭐⭐⭐⭐⭐      │
  │  ├── "Klima mükemmeldi, üşümedik" ⭐⭐⭐⭐⭐             │
  │  ├── "İkramlar bol ve lezzetli" ⭐⭐⭐⭐⭐                │
  │  ├── "Şoför çok profesyonel, güvende hissettik" ⭐⭐⭐⭐⭐ │
  │  ├── "Tam zamanında kalktı, tam zamanında vardı" ⭐⭐⭐⭐⭐│
  │  ├── "Tuvalet çok temizdi" ⭐⭐⭐⭐⭐                     │
  │  └── "Her seferinde bu firmayı tercih ediyorum" ⭐⭐⭐⭐⭐ │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 1. SIRADA ÇIKAR                               │
  │  ├── Seferleri HEMEN TÜKENİR                               │
  │  ├── Sabit müşteri kitlesi var                              │
  │  └── Kazanç: ÇOK YÜKSEK                                    │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  FİRMA B: ucuz Tur (Kalitesiz Hizmet)                      │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 1.8 (850 değerlendirme)                          │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Koltuklar çok rahatsız, belim ağrıdı" ⭐            │
  │  ├── "Klima bozuk, sıcakta kaldık" ⭐                     │
  │  ├── "Hiçbir ikram yok, su bile vermediler" ⭐            │
  │  ├── "Şoför telefonla konuştu, dikkatsiz sürdü" ⭐        │
  │  ├── "2 saat rötar yaptı, uçağı kaçırdım" ⭐              │
  │  ├── "Tuvalet çok pisti, kullanılamıyordu" ⭐             │
  │  ├── "Bir daha asla bu firmaya binmem!" ⭐               │
  │  └── "Arkadaşlarıma da tavsiye etmiyorum" ⭐             │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 15. SIRADA ÇIKAR                              │
  │  ├── Seferleri DOLMAZ                                     │
  │  ├── Sürekli müşteri kaybediyor                             │
  │  ├── Şikayet yağıyor                                       │
  │  └── Kazanç: ÇOK DÜŞÜK                                    │
  └─────────────────────────────────────────────────────────────┘

  ══════════════════════════════════════════════════════════════

  ✈️ HAVA YOLU ŞİRKETİ ÖRNEĞİ:

  "istanbal london uçak bileti" araması yapıldığında:

  ┌─────────────────────────────────────────────────────────────┐
  │  ŞİRKET A: Türk Hava Yolları (Yüksek Kalite)              │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 4.7 (5000+ değerlendirme)                        │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Koltuklar çok rahat, 12 saatlik uçuş bile rahat"    │
  │  ├── "Yemekler çok lezzetli ve bol"                        │
  │  ├── "Hostesler çok ilgili ve_profesyonel"                 │
  │  ├── "Bagaj hakkı yeterli, kayıp bagaj yok"               │
  │  ├── "Uçaklar yeni ve temiz"                               │
  │  ├── "Gecikme neredeyse hiç olmuyor"                       │
  │  └── "Her seferinde THY tercih ediyorum"                   │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 1. SIRADA ÇIKAR                               │
  │  ├── Biletleri HEMEN TÜKENİR                               │
  │  ├── Sadakat programı çok güçlü                            │
  │  └── Kazanç: DÜNYA LİDERİ                                 │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ŞİRKET B: ucuzAir (Düşük Kalite)                         │
  ├─────────────────────────────────────────────────────────────┤
  │  Puan: ⭐ 2.1 (2000+ değerlendirme)                        │
  │                                                             │
  │  Yorumlar:                                                  │
  │  ├── "Koltuklar çok dar, bacaklarım uyuştu" ⭐           │
  │  ├── "Yemekler çok kötü ve az" ⭐                        │
  │  ├── "Hostesler ilgisiz, sorularıma cevap vermedi" ⭐     │
  │  ├── "Bagajım kayboldu, 3 gün sonra geldi" ⭐            │
  │  ├── "Uçak eski ve pisti" ⭐                              │
  │  ├── "3 saat rötar yaptı, hiçbir açıklama yapmadılar" ⭐ │
  │  ├── "Ekstra bagaj için fahiş fiyat istedi" ⭐           │
  │  └── "Bir daha bu havayoluyla uçmam!" ⭐                │
  │                                                             │
  │  SONUÇ:                                                     │
  │  ├── Aramada 12. SIRADA ÇIKAR                              │
  │  ├── Biletleri ZOR TÜKENİR                                │
  │  ├── Sürekli müşteri kaybediyor                             │
  │  ├── Sosyal medyada linç yiyor                             │
  │  └── Kazanç: ÇOK DÜŞÜK + Zarar ediyor                     │
  └─────────────────────────────────────────────────────────────┘

  ══════════════════════════════════════════════════════════════

  TÜM SEKTÖRLERDE AYNI KURAL GEÇERLİ:
  ────────────────────────────────────

  SEKTÖR          │ İYİ HİZMET              │ KÖTÜ HİZMET
  ────────────────┼─────────────────────────┼──────────────────
  Taksi           │ Üst sırada, çok iş      │ Alt sırada, az iş
  Otobüs          │ Hemen biter, sadakat    │ Dolmaz, kayıp
  Hava Yolu       │ Liderlik, karlılık      │ Gerileme, zarar
  Otomobil Tamiri │ Güven, tekrar gelir     │ Kayıp, şikayet
  Restoran        │ Popüler, sürekli gelir  │ Boş, kapanma
  Emlakçı         │ Çok satış, referans     │ Az satış, iflas
  Elektronik      │ Çok satış, güven        │ Az satış, iade
  ├───────────────┼─────────────────────────┼──────────────────
  TÜMÜNDE ORTAK:  │ MÜŞTERİ MEMNUNİYETİ    │ MÜŞTERİ KAYBI
                  │ = BAŞARI               │ = BAŞARISIZLIK

  ══════════════════════════════════════════════════════════════

🏛️ KAMUSAL KURUMLAR, ODALAR VE DERNEKLER:

  ┌─────────────────────────────────────────────────────────────┐
  │  KAMUSAL HESAP TÜRLERİ                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  1. BELEDİYELER                                             │
  │     ├── İlçe Belediyeleri                                   │
  │     ├── Büyükşehir Belediyeleri                             │
  │     ├── Köy/Kasaba Belediyeleri                             │
  │     └── Özel İdareler                                      │
  │                                                             │
  │  2. ODALAR                                                  │
  │     ├── Ticaret ve Sanayi Odası (TSO)                       │
  │     ├── Sanayi Odası                                        │
  │     ├── Ticaret Borsası                                     │
  │     ├── Esnaf ve Sanatkarlar Odası                         │
  │     ├── Ziraat Odası                                        │
  │     ├── Mimarlar Odası                                     │
  │     ├── Mühendisler Odası                                  │
  │     ├── Baro (Avukatlar Odası)                             │
  │     ├── Hekimler Odası (Tabip Odası)                       │
  │     ├── Eczacılar Odası                                    │
  │     ├── Muhasebeciler Odası                                │
  │     └── Diğer Meslek Odaları                               │
  │                                                             │
  │  3. DERNEKLER                                               │
  │     ├── Meslek Dernekleri                                   │
  │     ├── Spor Kulüpleri                                      │
  │     ├── Kültür Dernekleri                                   │
  │     ├── Eğitim Dernekleri                                   │
  │     ├── Hayır Kuruluşları                                   │
  │     ├── Çevre Dernekleri                                   │
  │     └── Diğer Dernekler                                    │
  │                                                             │
  │  4. DİĞER KAMUSAL KURUMLAR                                 │
  │     ├── Üniversiteler                                       │
  │     ├── Hastaneler                                          │
  │     ├── Kütüphaneler                                        │
  │     ├── Müzeler                                             │
  │     └── Kültür Merkezleri                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

📋 ÜYE LİSTESİ SİSTEMİ:

  ┌─────────────────────────────────────────────────────────────┐
  │  AKTİF ÜYE LİSTESİ                                         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Her kamusal kurumun üye listesi GÖRÜNÜR olacak:           │
  │                                                             │
  │  Örnek: İstanbul Ticaret ve Sanayi Odası                   │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  📋 ÜYE LİSTESİ (Aktif: 1250 üye)                  │   │
  │  ├─────────────────────────────────────────────────────┤   │
  │  │                                                     │   │
  │  │  🔍 Üye Ara: [________________]                     │   │
  │  │                                                     │   │
  │  │  SEKTÖRE GÖRE FİLTRE:                              │   │
  │  │  [Tümü] [Tarım] [İmalat] [Hizmet] [Teknoloji]     │   │
  │  │                                                     │   │
  │  │  ┌──────────────────────────────────────────────┐  │   │
  │  │  │ #  │ Firma Adı          │ Sektör    │ Puan   │  │   │
  │  │  ├────┼───────────────────┼──────────┼────────┤  │   │
  │  │  │ 1  │ Ahmet Tarım       │ Tarım    │ 4.8 ⭐ │  │   │
  │  │  │ 2  │ Mehmet İnşaat     │ İnşaat   │ 4.7 ⭐ │  │   │
  │  │  │ 3  │ Ali Teknoloji     │ Teknoloji│ 4.6 ⭐ │  │   │
  │  │  │ 4  │ Veli Gıda         │ Gıda     │ 4.5 ⭐ │  │   │
  │  │  │ 5  │ Hasan Oto         │ Otomotiv │ 4.3 ⭐ │  │   │
  │  │  │ ...│ ...                │ ...      │ ...    │  │   │
  │  │  │1250│ Zeynep Emlak      │ Emlak    │ 4.9 ⭐ │  │   │
  │  │  └──────────────────────────────────────────────┘  │   │
  │  │                                                     │   │
  │  │  [← Önceki]  Sayfa 1/125  [Sonraki →]             │   │
  │  │                                                     │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  Her üye için GÖRÜNEN BİLGİLER:                            │
  │  ├── Firma/Kişi Adı                                        │
  │  ├── Sektör/Meslek                                         │
  │  ├── Puan (yıldız)                                         │
  │  ├── Değerlendirme Sayısı                                  │
  │  ├── Konum (il/ilçe)                                       │
  │  ├── Üyelik Tarihi                                         │
  │  ├── Aktif/Pasif Durumu                                    │
  │  └── İletişim Bilgileri (opsiyonel)                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

🔗 ÜYE KAYDI AKIŞI:

  Bir kişinin odaya/derneğe/kamusal kuruma üye olması:

  ADIM 1: Üyelik Başvurusu
  ├── Kişi platforma giriş yapar
  ├── İlgili oda/derneğin sayfasına gider
  └── "Üye Ol" butonuna basar

  ADIM 2: Başvuru Formu
  ├── Kişisel bilgiler
  ├── Firma bilgileri (varsa)
  ├── Sektör/Meslek seçimi
  ├── Vergi numarası
  └── İstenen belgeler

  ADIM 3: Onay Süreci
  ├── Oda/Dernek yönetimi başvuruyu inceler
  ├── Belgeler kontrol edilir
  ├── Üyelik aidatı varsa ödeme yapılır
  └── Onay veya red yanıtı gönderilir

  ADIM 4: Üyelik Aktifleşir
  ├── "Üye" rozeti eklenir
  ├── Üye listesinde görünmeye başlar
  ├── Tüm kamusal özellikler aktif olur
  └── Duyuru ve bildirimleri almaya başlar

📊 ODALAR İÇİN ÖZEL ÖZELLİKLER:

  Ticaret ve Sanayi Odası (TSO):
  ├── Üye listesi (tüm firmalar)
  ├── Sektörel raporlar
  ├── Fuar ve etkinlik duyuruları
  ├── Üyelere özel eğitimler
  ├── Networking etkinlikleri
  └── Ticari fırsatlar

  Esnaf ve Sanatkarlar Odası:
  ├── Esnaf üye listesi
  ├── Meslek kolları
  ├── Çırak/kalfalık ilanları
  ├── Staj imkanları
  ├── Mesleki eğitimler
  └── Esnaf destekleri

  Ziraat Odası:
  ├── Çiftçi üye listesi
  ├── Tarımsal destekler
  ├── Zirai ilaç/bilgi
  ├── Pazar fiyatları
  ├── Hasat planları
  └── Tarımsal danışmanlık

  Mimarlar/Mühendisler Odası:
  ├── Üye listesi (meslek erbapları)
  ├── Proje onayları
  ├── Mesleki gelişim
  ├── İhale bilgilendirmeleri
  ├── Staj ve iş imkanları
  └── Mesleki standartlar

🏛️ BELEDİYELER İÇİN ÖZEL ÖZELLİKLER:

  ├── Halk duyuruları
  ├── Etkinlik takvimi
  ├── İhale ilanları
  ├── Ruhsat/başvuru işlemleri
  ├── Vatandaş şikayet/öneri sistemi
  ├── Toplantı ve meclis kararları
  ├── Kamuoyu yoklamaları
  └── Acil durum uyarıları

📝 ODALAR VE DERNEKLER ÜYE YÖNETİMİ:

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE EKLEME YÖNTEMLERİ                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  1. TOPLU ÜYE EKLEME (Excel/CSV)                           │
  │     ├── Oda/Dernek yöneticisi Excel dosyası hazırlar       │
  │     ├── Dosyayı sisteme yükler                              │
  │     ├── Sistem otomatik olarak parse eder                   │
  │     ├── Üyeler otomatik oluşturulur                         │
  │     └── Üyelere Hoş Geldin e-postası/gönderilir            │
  │                                                             │
  │     Excel Formatı:                                          │
  │     ├── Ad Soyad                                            │
  │     ├── E-posta                                             │
  │     ├── Telefon                                             │
  │     ├── Firma Adı (varsa)                                  │
  │     ├── Sektör/Meslek                                       │
  │     ├── Vergi Numarası                                      │
  │     ├── Üyelik Tarihi                                       │
  │     └── Üyelik Durumu (aktif/pasif)                        │
  │                                                             │
  │  2. TEK TEK ÜYE EKLEME                                     │
  │     ├── "Yeni Üye Ekle" butonuna basılır                   │
  │     ├── Üye bilgileri formu doldurulur                      │
  │     ├── Gerekli belgeler yüklenir                           │
  │     ├── Kaydedilir                                          │
  │     └── Üyeye bildirim gönderilir                           │
  │                                                             │
  │  3. BAŞVURU İLE ÜYELİK                                     │
  │     ├── Kişi "Üye Ol" butonuna basar                        │
  │     ├── Başvuru formunu doldurur                            │
  │     ├── Belgelerini yükler                                  │
  │     ├── Oda/Dernek yönetimi onaylar                         │
  │     └── Üye otomatik olarak listeye eklenir                 │
  │                                                             │
  │  4. SİSTEME ENTEGRASYON                                    │
  │     ├── Mevcut veritabanından üye aktarımı                 │
  │     ├── Diğer sistemlerle entegrasyon                       │
  │     └── API ile otomatik güncelleme                         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE YÖNETİMİ PANELİ                                       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  📋 ÜYE LİSTESİ (Aktif: 250, Pasif: 15)                    │
  │                                                             │
  │  [+ Yeni Üye Ekle] [📥 Toplu Üye Yükle] [📤 Dışa Aktar]   │
  │                                                             │
  │  🔍 Üye Ara: [________________]                             │
  │                                                             │
  │  FİLTRE:                                                    │
  │  [Tümü] [Aktif] [Pasif] [Bekleyen] [Sektöre Göre ▼]       │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │ #  │ Ad Soyad      │ Firma        │ Durum  │ İşlemler│  │
  │  ├────┼──────────────┼──────────────┼────────┼────────┤  │
  │  │ 1  │ Ahmet Yılmaz │ Ahmet Tarım  │ ✅ Aktif│ ✏️ 🗑️ │  │
  │  │ 2  │ Mehmet Kaya  │ Mehmet İnşaat│ ✅ Aktif│ ✏️ 🗑️ │  │
  │  │ 3  │ Ali Demir    │ Ali Teknoloji│ ⏸️ Pasif│ ✏️ 🗑️ │  │
  │  │ 4  │ Veli Çelik   │ Beklemede    │ ⏳ Bekliyor│ ✅ ❌│  │
  │  │ ...│ ...          │ ...          │ ...    │ ...    │  │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  İŞLEMLER:                                                  │
  │  ├── ✏️ Düzenle: Üye bilgilerini güncelle                   │
  │  ├── 🗑️ Sil: Üyeyi listeden çıkar                          │
  │  ├── ✅ Onayla: Bekleyen başvuruyu onayla                   │
  │  ├── ❌ Reddet: Bekleyen başvuruyu reddet                   │
  │  ├── 📧 E-posta Gönder: Toplu veya tekli e-posta           │
  │  ├── 📱 SMS Gönder: Toplu veya tekli SMS                    │
  │  └── 📄 Belge İste: Eksik belge talep et                    │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE BİLGİLERİ (Detay Görünümü)                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  👤 Ahmet Yılmaz                                           │
  │  ──────────────────────────────                             │
  │  Firma: Ahmet Tarım Ltd. Şti.                              │
  │  Sektör: Tarım ve Hayvancılık                               │
  │  Üyelik No: 2024-00156                                      │
  │  Üyelik Tarihi: 15.03.2024                                 │
  │  Durum: ✅ Aktif                                            │
  │                                                             │
  │  İLETİŞİM:                                                  │
  │  ├── E-posta: ahmet@tarim.com                               │
  │  ├── Telefon: 0532 XXX XXXX                                │
  │  └── Adres: İstanbul, Kadıköy                              │
  │                                                             │
  │  SİSTEMDEKİ AKTİVİTE:                                       │
  │  ├── Son Giriş: 2 saat önce                                 │
  │  ├── Toplam İş Sayısı: 45                                  │
  │  ├── Puan Ortalaması: 4.7 ⭐                               │
  │  └── Değerlendirme Sayısı: 38                              │
  │                                                             │
  │  [✏️ Düzenle] [📧 E-posta Gönder] [📄 Belgeler]            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

🏢 TİCARET ODALARI İÇİN ÜYE YÖNETİMİ:

  ┌─────────────────────────────────────────────────────────────┐
  │  TİCARET ODASI ÜYE YÖNETİM SİSTEMİ                        │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Ticaret Odaları şunları yapabilir:                        │
  │                                                             │
  │  1. ÜYE LİSTESİ OLUŞTURMA                                  │
  │     ├── Tüm üyelerini sisteme ekler                         │
  │     ├── Firma bilgilerini girer                             │
  │     ├── Sektör dağılımını yapar                             │
  │     └── Üye listesini yayınlar (görünür hale getirir)      │
  │                                                             │
  │  2. ÜYELERİ GÜNCELLEME                                     │
  │     ├── Firma bilgilerini günceller                         │
  │     ├── Sektör değişikliğini yapar                          │
  │     ├── İletişim bilgilerini günceller                       │
  │     └── Üyelik durumunu değiştirir (aktif/pasif)           │
  │                                                             │
  │  3. YENİ ÜYE KABULÜ                                        │
  │     ├── Başvuruları inceler                                 │
  │     ├── Belgeleri kontrol eder                              │
  │     ├── Onay/Red verir                                      │
  │     └── Üyeyi listeye ekler                                 │
  │                                                             │
  │  4. ÜYE ÇIKARMA                                             │
  │     ├── Aidatını ödemeyen üyeleri pasif yapar               │
  │     ├── Kurallara uymayanları çıkarır                       │
  │     └── Listeyi günceller                                   │
  │                                                             │
  │  5. ÜYE BİLGİLERİNİ PAYLAŞMA                               │
  │     ├── Üye listesini herkese açık yapar                   │
  │     ├── Sektörel bazda filtreleme sağlar                    │
  │     ├── Arama yapılabilir hale getirir                      │
  │     └── Üyeler arasındaki iletişimi sağlar                  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  TİCARET ODASI ÖRNEĞİ: İstanbul Ticaret Odası (İTO)       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  📋 ÜYE LİSTESİ (Aktif: 15.000 üye)                        │
  │                                                             │
  │  [+ Yeni Üye Ekle] [📥 Toplu Üye Yükle] [📤 Dışa Aktar]   │
  │                                                             │
  │  SEKTÖRE GÖRE DAĞILIM:                                     │
  │  ├── Ticaret: 5.000 üye                                    │
  │  ├── Hizmet: 3.500 üye                                     │
  │  ├── İmalat: 3.000 üye                                     │
  │  ├── İnşaat: 2.000 üye                                     │
  │  ├── Teknoloji: 1.000 üye                                  │
  │  └── Diğer: 500 üye                                        │
  │                                                             │
  │  ARAMA SONUÇLARI:                                           │
  │  "inşaat şirketi" araması yapıldığında:                     │
  │                                                             │
  │  SIRA │ Firma               │ İlçe     │ Puan  │ Üye No    │
  │  ─────┼────────────────────┼──────────┼───────┼──────────│
  │   1.  │ Mehmet İnşaat       │ Kadıköy  │ 4.8 ⭐│ İTO-1234  │
  │   2.  │ Ali Yapı             │ Beşiktaş │ 4.7 ⭐│ İTO-2345  │
  │   3.  │ Veli İnşaat         │ Şişli    │ 4.5 ⭐│ İTO-3456  │
  │   ...│ ...                  │ ...      │ ...   │ ...       │
  │                                                             │
  │  HER ÜYE İÇİN GÖRÜNEN BİLGİLER:                           │
  │  ├── 🏷️ "İTO Üyesi" rozeti                                │
  │  ├── Firma adı ve logosu                                    │
  │  ├── Sektör                                                 │
  │  ├── Konum (ilçe)                                          │
  │  ├── Puan (yıldız)                                         │
  │  ├── Değerlendirme sayısı                                  │
  │  ├── Üyelik numarası                                       │
  │  └── İletişim (opsiyonel)                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DİĞER ODA ÖRNEKLERİ                                       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Esnaf ve Sanatkarlar Odası:                               │
  │  ├── 2.500 aktif üye                                       │
  │  ├── Berberler, kuaförler, tamirciler vb.                  │
  │  ├── Meslek kollarına göre dağılım                         │
  │  └── Her üye "ESO Üyesi" rozeti                             │
  │                                                             │
  │  Ziraat Odası:                                              │
  │  ├── 8.000 aktif çiftçi üye                                │
  │  ├── Ürün çeşitlerine göre dağılım                          │
  │  ├── Konum bazlı filtreleme                                 │
  │  └── Her üye "ZO Üyesi" rozeti                              │
  │                                                             │
  │  Mimarlar Odası:                                            │
  │  ├── 1.200 aktif üye                                       │
  │  ├── Uzmanlık alanlarına göre                               │
  │  ├── Proje portföyleri                                      │
  │  └── Her üye "MO Üyesi" rozeti                              │
  │                                                             │
  │  Mühendisler Odası:                                         │
  │  ├── 3.000 aktif üye                                       │
  │  ├── Mühendislik dallarına göre                             │
  │  ├── Lisans bilgileri                                       │
  │  └── Her üye "MDO Üyesi" rozeti                             │
  │                                                             │
  │  Baro (Avukatlar Odası):                                    │
  │  ├── 1.500 aktif avukat                                    │
  │  ├── Uzmanlık alanlarına göre                               │
  │  ├── Dava geçmişi (opsiyonel)                               │
  │  └── Her üye "Baro Üyesi" rozeti                            │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

🎓 OKULLAR VE ÜNİVERSİTELER - MEZUN LİSTESİ:

  ┌─────────────────────────────────────────────────────────────┐
  │  MEZUN YÖNETİM SİSTEMİ                                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Okullar ve üniversiteler şunları yapabilir:                │
  │                                                             │
  │  1. MEZUN LİSTESİ OLUŞTURMA                                 │
  │     ├── Tüm mezunlarını sisteme ekler                        │
  │     ├── Mezuniyet yıllarına göre gruplar                    │
  │     ├── Bölüm/fakülte bazında dağılım                       │
  │     └── Mezun listesini yayınlar                            │
  │                                                             │
  │  2. MEZUN PROFİLLERİ                                       │
  │     ├── Her mezunun güncel bilgileri görünür                │
  │     ├── Hangi sektörde çalıştığı                             │
  │     ├── Hangi firmada çalıştığı                              │
  │     ├── Mesleki başarısı (puan)                             │
  │     └── İletişim bilgileri (opsiyonel)                      │
  │                                                             │
  │  3. MEZUN AĞI (ALUMNI NETWORK)                             │
  │     ├── Mezunlar birbirini bulabilir                        │
  │     ├── Meslektaş mezunlar eşleşir                          │
  │     ├── Networking etkinlikleri düzenlenir                   │
  │     └── Mentörlük sistemi kurulur                           │
  │                                                             │
  │  4. MEZUNLARA ÖZEL İMKANLAR                                 │
  │     ├── Mezunlara indirimli hizmetler                       │
  │     ├── Mezunlar arası ticaret                              │
  │     ├── Ortak projeler                                       │
  │     └── Kariyer fırsatları                                  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜNİVERSİTE ÖRNEĞİ: İstanbul Üniversitesi                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  📋 MEZUN LİSTESİ (Toplam: 50.000 mezun)                   │
  │                                                             │
  │  [+ Mezun Ekle] [📥 Toplu Mezun Yükle] [📤 Dışa Aktar]     │
  │                                                             │
  │  BÖLÜME GÖRE DAĞILIM:                                      │
  │  ├── Hukuk Fakültesi: 8.000 mezun                          │
  │  ├── Tıp Fakültesi: 5.000 mezun                            │
  │  ├── Mühendislik Fakültesi: 7.000 mezun                    │
  │  ├── İktisat Fakültesi: 6.000 mezun                        │
  │  ├── İşletme Fakültesi: 6.500 mezun                        │
  │  ├── Fen Edebiyat Fakültesi: 4.000 mezun                   │
  │  └── Diğer: 13.500 mezun                                   │
  │                                                             │
  │  ARAMA SONUÇLARI:                                           │
  │  "hukuk mezunu" araması yapıldığında:                       │
  │                                                             │
  │  SIRA │ Ad Soyad       │ Mezun Yılı │ Şehir  │ Puan        │
  │  ─────┼───────────────┼───────────┼────────┼─────────────│
  │   1.  │ Ahmet Yılmaz  │ 2015      │ İstanbul│ 4.9 ⭐      │
  │   2.  │ Ayşe Demir    │ 2018      │ Ankara  │ 4.8 ⭐      │
  │   3.  │ Mehmet Kaya   │ 2012      │ İzmir   │ 4.7 ⭐      │
  │   ...│ ...            │ ...       │ ...     │ ...          │
  │                                                             │
  │  HER MEZUN İÇİN GÖRÜNEN BİLGİLER:                         │
  │  ├── 🎓 "İÜ Mezunu" rozeti                                 │
  │  ├── Ad Soyad                                               │
  │  ├── Bölüm ve Mezuniyet Yılı                                │
  │  ├── Güncel Çalıştığı Yer (opsiyonel)                       │
  │  ├── Meslek                                                 │
  │  ├── Şehir                                                 │
  │  ├── Puan (yıldız)                                         │
  │  └── İletişim (opsiyonel)                                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DİĞER KURULUŞ ÖRNEKLERİ                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  Lise ve Ortaokullar:                                       │
  │  ├── Mezun listesi                                          │
  │  ├── Yıllara göre dağılım                                   │
  │  ├── Etkinlik duyuruları                                    │
  │  └── Mezunlar arası iletişim                                │
  │                                                             │
  │  Meslek Okulları:                                           │
  │  ├── Mezun listesi                                          │
  │  ├── Mesleki dağılım                                        │
  │  ├── Staj ve iş imkanları                                   │
  │  └── Sertifika programları                                  │
  │                                                             │
  │  Sertifika/ Eğitim Kurumları:                               │
  │  ├── Kursiyer listesi                                       │
  │  ├── Aldıkları sertifikalar                                 │
  │  ├── Uzmanlık alanları                                      │
  │  └── Devam eden eğitimler                                   │
  │                                                             │
  │  Spor Kulüpleri:                                            │
  │  ├── Eski sporcular                                         │
  │  ├── Aktif sporcular                                        │
  │  ├── Antrenörler                                            │
  │  └── Altyapı oyuncuları                                     │
  │                                                             │
  │  Kültür/Sanat Dernekleri:                                   │
  │  ├── Üyeler                                                 │
  │  ├── Sanatçılar                                             │
  │  ├── Eser sahipleri                                         │
  │  └── Koleksiyoncular                                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════

---

## 📌 ÖNEMLİ NOTLAR

### SİSTEMİN TEMEL DİNAMİKLERİ

  1. HERKES HEM ALICI HEM SATICI
     ├── Taksi şoförü → Taksicilik yapar + Yemek sipariş eder
     ├── Dürümcü → Dürüm satar + Tamirci çağırır
     ├── Yedek parça satıcısı → Parça satar + Kargo gönderir
     ├── Çiftçi → Ürün satar + Gübre sipariş eder
     └── Telefoncu → Telefon satar + Berbere gider

  2. PUANLAMA ZORUNLU
     ├── Hizmet alan kişi → Hizmet vereni puanlamak ZORUNDA
     ├── Puanlama yapılmadan → Yeni hizmet alınamaz
     ├── Her puan → Firma kariyerini etkiler
     └── Düşük puan → İş kaybı demek

  3. PUAN KRİTER OLUŞTURUYOR
     ├── Yüksek puan → ÜST SIRALARDA GÖRÜNÜR
     ├── Düşük puan → ALT SIRALARDA KAYBOLUR
     ├── Firma rekabeti → Puan için mücadele
     └── Müşteri kararını puana göre verir

  4. TÜM SEKTÖRLER KAPSANIYOR
     ├── Sanayi: Yedek parça, hırdavat, makine
     ├── Gıda: Dürümcü, restoran, market
     ├── Hizmet: Usta, tamirci, kurye
     ├── Tarım: Çiftçi, hayvan yetiştiricisi
     ├── Teknoloji: Telefoncu, bilgisayarcı
     ├── Ulaşım: Taksi, kargo, nakliyat
     └── Daha fazlası...

### BAŞARI FORMÜLÜ

  ┌─────────────────────────────────────────────┐
  │  İyi İş Yap + Zamanında Teslim Et          │
  │  + İyi İletişim Kur + Uygun Fiyat Ver      │
  │  = Yüksek Puan                             │
  │  = Çok İş Yapma Fırsatı                    │
  │  = Yüksek Kazanç                           │
  │  = Platformda Kalıcı Olma                  │
  └─────────────────────────────────────────────┘

### BAŞARISIZLIK FORMÜLÜ

  ┌─────────────────────────────────────────────┐
  │  Kötü İş Yap + Geç Kal                     │
  │  + Kötü İletişim + Pahalı Fiyat            │
  │  = Düşük Puan                              │
  │  = Az İş Yapma Fırsatı                     │
  │  = Düşük Kazanç                            │
  │  = Platformdan Atılma                      │
  └─────────────────────────────────────────────┘

---

*Son güncelleme: 2026-06-04*
*Durum: Planlama Aşaması - Tamamlandı*
*Toplam Tablo Sayısı: 50+*
*Toplam Modül Sayısı: 15+*

### 15.2 Puanlama Türleri
```yaml
Hizmet Veren Puanlama (Hizmet Alan → Hizmet Veren):
  - Genel Puan: 1-5 yıldız
  - Kategori Bazlı:
    ├── Kalite: 1-5
    ├── Zamanında Gelme: 1-5
    ├── İletişim: 1-5
    └── Fiyat/Performans: 1-5
  - Yorum: Metin
  - Fotoğraf: İş görseli (opsiyonel)

Ürün Puanlama (Alıcı → Satıcı):
  - Genel Puan: 1-5 yıldız
  - Ürün Kalitesi: 1-5
  - Kargo Hızı: 1-5
  - Paketleme: 1-5
  - Yorum: Metin
  - Fotoğraf: Ürün görseli (opsiyonel)
```

### 15.3 Puanlama Akışı
```
Hizmet Tamamlanır
       ↓
Hizmet Alan Kişi Bildirim Alır
       ↓
Puanlama Sayfası Açılır
       ↓
1-5 Yıldız Seçilir
       ↓
Kategori Puanları Girilir
       ↓
Yorum Yazılır (opsiyonel)
       ↓
Fotoğraf Eklenir (opsiyonel)
       ↓
Gönder
       ↓
Hizmet Verenin Puan Ortalaması Güncellenir
```

### 15.4 Değerlendirme Tablosu
```sql
CREATE TABLE reviews (
    id              UUID PRIMARY KEY,
    reviewer_id     UUID REFERENCES users(id),       -- Hizmet alan (PUANLAYAN)
    reviewee_id     UUID REFERENCES users(id),       -- Hizmet veren (PUANLANAN)
    
    -- İlişki Türü
    review_type     VARCHAR(30),                     -- service, product, food_delivery, taxi
    
    -- İlişki
    order_id        UUID,                            -- İlgili sipariş/çalışma ID'si
    
    -- Puanlar
    rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
    quality_rating  INTEGER CHECK(quality_rating BETWEEN 1 AND 5),
    punctuality_rating INTEGER CHECK(punctuality_rating BETWEEN 1 AND 5),
    communication_rating INTEGER CHECK(communication_rating BETWEEN 1 AND 5),
    value_rating    INTEGER CHECK(value_rating BETWEEN 1 AND 5),
    
    -- Yorum
    title           VARCHAR(255),
    comment         TEXT,
    
    -- Fotoğraflar
    photos          JSONB DEFAULT '[]',
    
    -- Yanıt (Hizmet Veren yanıt verebilir)
    response        TEXT,
    response_date   TIMESTAMP,
    
    -- Görünürlük
    is_visible      BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,           -- Doğrulanmış değerlendirme
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 16. TAKSİ SİSTEMİ

### 16.1 Genel Bakış

Taksi sistemi, platformun ulaşım hizmetleri modülüdür. Bireysel hesap sahiplerinin taksi şoförü olarak kaydolmasına, ticari plaka (araç) yönetimine, çoklu vardiya sistemine ve yolcuların taksi çağırmasına olanak tanır.

**Ön Koşul:** Her taksi şoförü öncelikle **Bireysel Hesap** açmak ve kimlik doğrulamasını tamamlamak zorundadır.

### 16.2 Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Şoför Kaydı** | 9 zorunlu belge (ehliyet, psikoteknik, SRC, sabıka vb.) ile AI+manuel doğrulama |
| **Araç Yönetimi** | Ticari plaka kaydı, sigorta/muayene/taksimetre takibi, OBD/GPS entegrasyonu |
| **Çoklu Şoför** | Bir araca 2+ şoför atanabilir (sabah/akşam/gece/haftasonu vardiyaları) |
| **Araç Kiralama** | Günlük/vardiyalı/haftalık/aylık kira modelleri, otomatik tahsilat |
| **Araç Ortaklığı** | Hisseli plaka desteği (%50-%50, %70-%30, karma modeller) |
| **Anlık Eşleşme** | "Sürücü koltuğunda kim varsa çağrı o kişiye gider" prensibi |
| **Çift Yönlü Puanlama** | Şoför (%60) + Araç (%40) = Kombine puan, detaylı kriterler |
| **Çağrı Reddetme Cezası** | Kısa mesafe reddine -1 puan, günlük/aylık limit aşımında geçici men |
| **Eşleştirme Algoritması** | Mesafe (%50) + Kombine Puan (%50) ile optimize sıralama |
| **Zorunlu Sistem Ödemesi** | Nakit yasak, cüzdan veya tanımlı kart zorunlu, bloke+otomatik çekim |
| **Fiyat Tahmini** | Açılış + km + dakika + dinamik faktörler (gece, yoğun saat, özel gün) |
| **Erken İnme / Taahhüt** | Ayda 1 hak, yılda 3 ay ihlalde Onurlu Müşteri kaybı, taahhüt ücreti ödeme zorunluluğu |
| **Paylaşımlı Yolculuk** | ≥3 kişi binişte paylaşımlı statü, taksici rota sonuna kadar yolcu alabilir, her yolcu kendi mesafesini öder |
| **Hediye Yolculuk** | Başkası için taksi çağırma, rotayı belirleme, ödemeyi yapma; yolcu üye olmadan SMS ile biner |
| **Konfor Tercih & Bahşiş** | Puan=konfor, müşteri konfor seviyesi seçebilir, eşleşme yoksa bahşiş (+50/100 TL) teklif ederek taksi çağırabilir |
| **Müşteri Puanlama (Çift Yön)** | Şöför yolcuyu davranış/güvenilirlik/düzen bazında puanlar; düşük puan uzun bekleme, yüksek puan öncelik |
| **Çağrı İptal / Binmeme Cezası** | Müşteri binmezse taksi geliş mesafesini öder; tekrarda bekleme süresi artar, öncelik düşer |
| **Transfer Taksi (Uzun Mesafe)** | İller arası yolculukta müşteri ya tek taksi ile gider ya da bölge sınırlarında taksi değiştirerek transfer yapar; her şöför kendi bölgesinde kalır |
| **Aktif/Pasif + Konum Zorunlu** | Taksici aktif/pasif seçer; aktifse GPS açık olmak zorunda, konum kapanırsa otomatik pasif |
| **Araç QR Kod Sistemi** | Her araç için eşsiz QR kod (sağ/sol kapı + iç); müşteri binmeden önce okutarak doğrular |
| **Anlık QR Hızlı Biniş** | Müşteri çağrı yapmadan QR okutup biner; şöför aktifse onay; taksimetre açılışı zorunlu (1 m bile olsa) |
| **Müşteri Taksi Terminali** | Taksi sistemi ana platform içinde bağımsız terminal; izole state/crash/resource; ayrı API gateway |
| **Planlanmış Rotalar** | Çok bacaklı ön rezervasyon (12s-30gün); %30 premium; iptal cezaları; özel servis statüsü |
| **Dinamik Konfor Fiyatlandırması** | Eğrisel (non-linear) talep primi +%5 → +%100; VIP Concierge sadece en yüksek puanlı şöför+araç; kalite teşvik döngüsü |
| **Araç İçi Güvenlik Kamerası** | Tüm taksilerde ZORUNLU; kamerasız araçlar işaretlenir ve uyarı gösterilir; 30 gün men |
| **Araç Marka/Model/Yakıt Filtresi** | Müşteri marka, model, yakıt tipine (benzinli/dizel/LPG/elektrikli/hibrit) göre araç arayabilir |
| **Şöför Cinsiyet Tercihi** | Müşteri kadın/erkek şöför tercihinde bulunabilir; her şöförün cinsiyeti listelenir |
| **Trafik Muayene OCR + Otomatik Süre Takibi** | Muayene belgesi OCR ile okunur; tarih geçince araç otomatik güvenlik dışı işaretlenir ve devre dışı kalır; gece cron job ile tarama |
| **Taksi Durakları (Durak Sistemi)** | Sistem lokasyonlu duraklar; araç/şöför durağa bağlanır; müşteri durak filtreleyebilir; sıra sistemi |
| **Taksi Bekleme Lokasyonu** | Taksiciler "Ben Buradayım" bekleme noktası oluşturur; müşteri haritada görür; GPS hareketiyle otomatik sorgu |
| **Durak Sıra Sistemi (Kuyruk)** | Durak yöneticisi araç sırası yönetir; FIFO çağrı yönlendirme; reddeden sıra sonu; tüm işlem loglu |
| **Yolculuk Sonrası Otomatik Görevlendirme** | Yolculuk bitince şöför aktifse yeni çağrıya yönlendirilir (otomatik/öneri/durağa dönüş); kesintisiz döngü |
| **Geliş Öncesi Karşılama Rezervasyonu** | Müşteri başka şehirden varış noktasına taksi çağırır; bekleme ücreti saatlik kazanca göre (×0.80); ilk 15dk ücretsiz; rötar bildirimi |
| **Şöför Beklememe Hakkı + Dinamik Ceza** | Şöför beklemeyi reddedebilir; gündüz -5, gece/zor durumda -100 puana kadar ceza; müşteri bekleme ücreti ödemez; sistem alternatif yönlendirir |
| **Karşılıklı Taahhüt Sistemi** | Çağrı öncesi müşteriye bekleme ücreti, şöföre beklememe cezası + müşterinin alternatif bulma olasılığı gösterilir; ilk 5dk ücretsiz bekleme |

### 16.3 Yeni Veritabanı Tabloları

Detaylı şema için → [TAXI-SYSTEM-DESIGN.md](./TAXI-SYSTEM-DESIGN.md#11-veritabanı-şeması-yeni-tablolar)

| Tablo | Açıklama |
|-------|----------|
| `taxi_driver_documents` | Şoför belgeleri (ehliyet, psikoteknik, SRC, sabıka, ikamet, vergi) |
| `taxi_vehicles` | Ticari plaka/araç bilgileri |
| `taxi_vehicle_owners` | Araç sahipleri ve hisse oranları |
| `taxi_driver_assignments` | Vardiya atamaları |
| `taxi_rental_agreements` | Kira sözleşmeleri |
| `taxi_driver_status` | Şoför anlık durumu (online/müsait/yolculukta) |
| `taxi_ride_requests` | Çağrı logları |
| `taxi_trips` | Yolculuk kayıtları |
| `taxi_ratings` | Çift yönlü puanlama |
| `user_wallets` | Kullanıcı cüzdanı |
| `wallet_transactions` | Cüzdan hareketleri |
| `call_rejection_log` | Çağrı red logları (ceza puanı) |

### 16.4 API Endpoint'leri

Detaylı liste için → [TAXI-SYSTEM-DESIGN.md](./TAXI-SYSTEM-DESIGN.md#12-api-endpointleri)

| Grup | Sayı |
|------|------|
| Şoför Yönetimi | 8 endpoint |
| Araç Yönetimi | 10 endpoint |
| Vardiya ve Atama | 10 endpoint |
| Kiralama | 7 endpoint |
| Taksi Çağırma ve Yolculuk | 12 endpoint |
| Ödeme | 7 endpoint |
| Admin | 10 endpoint |

**Toplam: 50+ yeni endpoint**

### 16.5 Detaylı Tasarım

Taksi sistemi için kapsamlı tasarım dokümanına buradan ulaşabilirsiniz:
➡️ [TAXI-SYSTEM-DESIGN.md](./TAXI-SYSTEM-DESIGN.md)

Doküman içeriği:
- Şoför kaydı ve belge doğrulama süreci
- Araç sahipliği türleri (tek/hisseli/kurumsal/karma)
- Çoklu vardiya sistemi ve izin yönetimi
- Araç kiralama ve otomatik tahsilat
- Sürücü-araç anlık eşleşme (durum makinesi)
- Çift yönlü puanlama algoritması
- Taksi çağırma ve eşleştirme algoritması
- Fiyat tahmin ve rota gösterim sistemi
- Zorunlu cüzdan/payment sistemi
- 12 yeni veritabanı tablosu (SQL DDL)
- 50+ API endpoint'i
- Akış diyagramları

---

## 29. ÜYE NUMARASI SİSTEMİ

  Her kişiye sistem tarafından benzersiz bir numara verilir (T.C. Kimlik No gibi):

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE NUMARASI SİSTEMİ                                       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  HER KİŞİYE BENZERSİZ BİR NUMARA VERİLİR:                  │
  │                                                             │
  │  FORMAT: XXXX-XXXX-XXXX                                    │
  │  ÖRNEK: 1001-2345-6789                                     │
  │                                                             │
  │  NUMARA YAPISI:                                             │
  │  ├── İlk 4 hane: Kayıt yılı (2026)                         │
  │  ├── Orta 4 hane: Sıra numarası (0001'den başlar)           │
  │  └── Son 4 hane: Doğrulama kodu                             │
  │                                                             │
  │  ÖRNEKLER:                                                  │
  │  ├── 2026-0001-3847 → İlk kaydolan kişi                    │
  │  ├── 2026-0002-9156 → İkinci kaydolan kişi                  │
  │  ├── 2026-0100-2738 → 100. kaydolan kişi                    │
  │  └── 2026-1000-8462 → 1000. kaydolan kişi                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE NUMARASI NEREDE KULLANILIR?                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  PROFİL SAYFASINDA:                                         │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  👤 Ahmet Yılmaz                                    │   │
  │  │  🔢 Üye No: 2026-0001-3847                         │   │
  │  │  ⭐ Puan: 4.8 (150 değerlendirme)                   │   │
  │  │  📅 Üye: 01.01.2026 (6 aydır üye)                  │   │
  │  │  🏆 Rozet: Onaylı Satıcı                           │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  ARAMA SONUÇLARINDA:                                        │
  │  ├── Kişi adının yanında üye numarası görünür              │
  │  ├── Güvenilirlik göstergesi olarak kullanılır              │
  │  └── Sahte hesap tespitinde kolaylık sağlar                 │
  │                                                             │
  │  İŞLEM YAPARKEN:                                            │
  │  ├── Anlaşma sözleşmesinde üye numarası yer alır           │
  │  ├── Faturada üye numarası yer alır                        │
  │  ├── Kargo bilgisinde üye numarası yer alır                 │
  │  └── Anlaşmazlık durumunda kimlik doğrulama sağlar         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE NUMARASI ÖZELLİKLERİ                                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ✅ BENZERSİZ:                                               │
  │  ├── Her kişiye sadece bir numara verilir                   │
  │  ├── Aynı numara iki kişiye verilmez                        │
  │  ├── Silinen hesap numarası tekrar kullanılmaz              │
  │  └── Ömür boyu geçerli                                      │
  │                                                             │
  │  ✅ SİSTEM TARAFINDAN VERİLİR:                              │
  │  ├── Kullanıcı numarayı seçemez                             │
  │  ├── Otomatik olarak atanır                                 │
  │  ├── Kayıt sırasında otomatik oluşturulur                   │
  │  └── Değiştirilemez                                          │
  │                                                             │
  │  ✅ GÜVENLİ:                                                 │
  │  ├── Sahte hesap tespitini kolaylaştırır                   │
  │  ├── Kimlik doğrulamada kullanılır                          │
  │  ├── Anlaşmazlık çözümünde kanıt olur                       │
  │  └── Dolandırıcılığı önler                                  │
  │                                                             │
  │  ✅ KOLAY:                                                   │
  │  ├── Kişiyi numara ile bulabilirsin                         │
  │  ├── Ticaret yaparken güven sağlar                          │
  │  ├── Profesyonel görünüm verir                              │
  │  └── Platform içi kimlik doğrulama sağlar                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  ÜYE NUMARASI KULLANIM ÖRNEKLERİ                            │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  ÖRNEK 1: ÜRÜN SATIŞI                                       │
  │  ├── Satıcı: "Ben 2026-0001-3847 numaralı üyeyim"          │
  │  ├── Alıcı: Numarayı arar, profili görür                    │
  │  ├── Güven: Puanı, yorumları, satış sayısını görür         │
  │  └── Sonuç: Güvenle alışveriş yapar                         │
  │                                                             │
  │  ÖRNEK 2: HİZMET ALIMI                                      │
  │  ├── Müşteri: "Bu tamirciyi nereden buldun?"               │
  │  ├── Arkadaş: "Üye numarası: 2026-0050-1234"               │
  │  ├── Müşteri: Numarayı arar, profili görür                  │
  │  └── Sonuç: Güvenle hizmet alır                             │
  │                                                             │
  │  ÖRNEK 3: ANLAŞMAZLIK                                       │
  │  ├── Sorun: Ürün hasarlı geldi                              │
  │  ├── Çözüm: "Satıcının üye numarası: 2026-0001-3847"       │
  │  ├── Platform: Numara ile satıcıyı bulur, inceler          │
  │  └── Sonuç: Adil karar verilir                              │
  │                                                             │
  │  ÖRNEK 4: TİCARİ İLİŞKİ                                    │
  │  ├── Firma: "Bize üye numaranızı verir misiniz?"           │
  │  ├── Kullanıcı: "2026-0001-3847"                           │
  │  ├── Firma: Numarayı sistemde arar                          │
  │  ├── Firma: Kullanıcının güvenilirliğini görür              │
  │  └── Sonuç: Güvenle ticaret yaparlar                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

---

## 📌 ÖNEMLİ NOTLAR

1. **Teknoloji Seçimi**: Henüz teknoloji stack'ine karar verilmedi. Seçim sonrası bu plan güncellenecektir.

2. **Ölçeklenebilirlik**: Mimari modular yapıdadır, yeni modüller kolayca eklenebilir.

3. **Güvenlik**: Tüm hassas veriler şifrelenecek, JWT token ile yetkilendirme kullanılacaktır.

4. **Performans**: Önbellekleme, CDN, veritabanı indeksleme ile yüksek performans hedeflenmektedir.

5. **Mobil Uyumlu**: Responsive tasarım ile tüm cihazlarda çalışacaktır.

---

*Son güncelleme: 2026-06-04*
*Durum: Planlama Aşaması*
