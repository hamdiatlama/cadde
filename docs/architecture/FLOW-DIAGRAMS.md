# 🔄 AKIŞ DİYAGRAMLARI

---

## 1. GENEL Kullanıcı Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANA SAYFA                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  GİRİŞ YAP  │  │  KAYIT OL   │  │  ARA        │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              KULLANICI TİPİ SEÇİMİ                  │       │
│  │                                                      │       │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │       │
│  │  │ BİREYSEL │  │ KURUMSAL │  │ KAMUSAL  │          │       │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │       │
│  │       │              │              │                  │       │
│  └───────┼──────────────┼──────────────┼──────────────┘       │
│          │              │              │                        │
│          ▼              ▼              ▼                        │
│  ┌─────────────────────────────────────────────────────┐       │
│  │                 PROFİL OLUŞTURMA                     │       │
│  │  ├── Ad, Soyad                                       │       │
│  │  ├── E-posta, Telefon                                │       │
│  │  ├── Profil Fotoğrafı                                │       │
│  │  └── Biyografi                                       │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. HESAP TÜRÜNE GÖRE AKIŞ

### 2.1 Bireysel Hesap Kayıt Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 BİREYSEL HESAP KAYIT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Kayıt Formu                                           │
│  ├── Ad, Soyad                                                 │
│  ├── E-posta                                                   │
│  ├── Telefon                                                   │
│  ├── Şifre                                                     │
│  └── [Kayıt Ol] butonu                                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Doğrulama                                             │
│  ├── E-posta doğrulama kodu gönder                              │
│  ├── Telefon doğrulama kodu gönder                              │
│  └── Kod girilir → Doğrulanır                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Profil Tamamlama                                      │
│  ├── Profil fotoğrafı yükle                                    │
│  ├── Biyografi yaz                                             │
│  ├── İletişim bilgileri                                        │
│  └── [Devam Et] butonu                                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Hesap Hazır                                           │
│  ├── Dashboard'a yönlendirilir                                 │
│  ├── İlk adım rehberi gösterilir                               │
│  └── Hizmet verebilir veya hizmet alabilir                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Kurumsal Hesap Kayıt Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 KURUMSAL HESAP KAYIT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ÖN KOŞUL: Bireysel hesap gerekli!                             │
│                                                                 │
│  ADIM 1: Kurumsal Hesap Talebi                                 │
│  ├── Bireysel hesaba giriş yap                                  │
│  ├── "Kurumsal Hesap Aç" butonuna bas                          │
│  └── Talep formu doldurulur                                    │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Şirket Bilgileri                                      │
│  ├── Şirket Adı                                                │
│  ├── Logo                                                      │
│  ├── Sektör                                                    │
│  ├── Şirket Türü (limited, anonim vb.)                        │
│  ├── Vergi Numarası                                            │
│  ├── Ticaret Sicil No                                          │
│  ├── Adres                                                     │
│  └── [Devam Et] butonu                                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Belgeler                                               │
│  ├── Vergi levhası yükle                                       │
│  ├── Ticaret sicil gazetesi yükle                               │
│  ├── İmza sirküleri yükle                                      │
│  └── [Belgeleri Gönder] butonu                                │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Onay Beklemesi                                        │
│  ├── "Talebiniz inceleniyor" mesajı                            │
│  ├── E-posta ile bilgilendirme                                  │
│  └── Onay süresi: 1-3 iş günü                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Onaylanırsa                                           │
│  ├── "Kurumsal Hesap" rozeti eklenir                           │
│  ├── Mağaza açma yetkisi                                       │
│  ├── Çalışan ekleme yetkisi                                    │
│  └── Tüm kurumsal özellikler aktif                             │
│                                                                 │
│  ADIM 6: Reddedilirse                                          │
│  ├── Red nedeni bildirilir                                     │
│  ├── Eksikler tamamlanabilir                                    │
│  └── Tekrar başvuru yapılabilir                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Kamusal Hesap Kayıt Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 KAMUSAL HESAP KAYIT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ÖN KOŞUL: Bireysel hesap gerekli!                             │
│                                                                 │
│  ADIM 1: Kamusal Hesap Talebi                                  │
│  ├── Bireysel hesaba giriş yap                                  │
│  ├── "Kamusal Hesap Aç" butonuna bas                           │
│  └── Talep formu doldurulur                                    │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Kurum Bilgileri                                       │
│  ├── Kurum Adı                                                 │
│  ├── Kurum Türü (belediye, bakanlık, dernek vb.)             │
│  ├── Logo                                                      │
│  ├── Adres                                                     │
│  ├── Telefon, E-posta                                          │
│  ├── Web Sitesi                                                │
│  └── [Devam Et] butonu                                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Belgeler                                               │
│  ├── Resmi evrak yükle                                         │
│  ├── Kurum sicil belgesi                                       │
│  ├── Yetki belgesi                                             │
│  └── [Belgeleri Gönder] butonu                                │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Onay Beklemesi                                        │
│  ├── "Talebiniz inceleniyor" mesajı                            │
│  ├── E-posta ile bilgilendirme                                  │
│  └── Onay süresi: 3-7 iş günü                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Onaylanırsa                                           │
│  ├── "Resmi Kurum" rozeti eklenir                              │
│  ├── Duyuru yapma yetkisi                                      │
│  ├── Toplu bildirim yetkisi                                    │
│  ├── Öncelikli sıralama                                        │
│  └── Tüm kamusal özellikler aktif                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. HİZMET ALMA/VERME AKIŞI

### 3.1 Hizmet Veren Kayıt Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 HİZMET VEREN KAYIT                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Hizmet Veren Profili                                  │
│  ├── Mevcut hesaba giriş yap                                    │
│  ├── "Hizmet Veren Ol" butonuna bas                            │
│  └── Meslek/Sektör seçimi                                     │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Meslek Bilgileri                                      │
│  ├── Meslek seç (alçı ustası, tesisatçı vb.)                 │
│  ├── Sektör seç (inşaat, hizmet vb.)                          │
│  ├── Deneyim yılı                                              │
│  ├── Uzmanlık alanı                                            │
│  ├── Hizmet verdiği bölgeler                                   │
│  └── [Devam Et] butonu                                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Hizmet Detayları                                      │
│  ├── Hizmet türü (sabit fiyat, saatlik, günlük)               │
│  ├── Fiyat bilgisi                                             │
│  ├── Çalışma saatleri                                          │
│  ├── Konum (adrese gelebilir, kendi yerinde vb.)              │
│  ├── Fotoğraf yükle                                            │
│  └── [Hizmeti Oluştur] butonu                                 │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Doğrulama (Opsiyonel)                                 │
│  ├── Lisans yükle                                              │
│  ├── Sertifika yükle                                           │
│  ├── Referans ekle                                             │
│  └── [Belgeleri Gönder] butonu                                │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Hizmet Veren Profili Hazır                            │
│  ├── Profil sayfası oluşturulur                                │
│  ├── Hizmet ilanı yayınlanır                                   │
│  ├── Arama sonuçlarında görünmeye başlar                        │
│  └── Müşteri beklemeye başlar                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Hizmet Arama ve Bulma Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 HİZMET ARAMA                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Arama Yapma                                           │
│  ├── Ana sayfada arama kutusuna yaz                             │
│  │   Örnek: "alçı ustası" veya "dürümcü"                      │
│  ├── Kategori filtresi kullan                                   │
│  └── Konum filtresi kullan (ilçe, semt)                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Sonuçları Görüntüleme                                 │
│  ├── Puanına göre sıralanmış liste                             │
│  ├── Her ilanda:                                               │
│  │   ├── Fotoğraf                                             │
│  │   ├── Ad/Soyad veya İşyeri Adı                            │
│  │   ├── Puan (yıldız)                                        │
│  │   ├── Değerlendirme sayısı                                 │
│  │   ├── Konum                                                │
│  │   ├── Fiyat                                                │
│  │   └── Açık/Kapalı durumu                                   │
│  └── harita görünümü (opsiyonel)                               │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Detay Görüntüleme                                     │
│  ├── Profil sayfasına tıkla                                    │
│  ├── Hizmet detaylarını gör                                    │
│  ├── Yorumları oku                                             │
│  ├── Fotoğrafları incele                                       │
│  └── İletişim bilgilerini gör                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Hizmet Verenle İletişim                               │
│  ├── "Mesaj Gönder" butonu                                    │
│  ├── "Ara" butonu                                              │
│  ├── "WhatsApp" butonu                                         │
│  └── "Randevu Al" butonu                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Hizmet Satın Alma Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                 HİZMET SATIN ALMA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Hizmet Seçimi                                         │
│  ├── Hizmet verenin profil sayfasına git                        │
│  ├── İstenen hizmeti seç                                       │
│  └── "Bu Hizmeti Al" butonuna bas                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Talep Oluşturma                                       │
│  ├── Hizmet açıklaması yaz                                     │
│  ├── Tarih ve saat seç                                         │
│  ├── Konum gir (adres)                                         │
│  ├── Fotoğraf ekle (opsiyonel)                                 │
│  ├── Bütçe belirle (opsiyonel)                                 │
│  └── [Talebi Gönder] butonu                                   │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Hizmet Veren Yanıtı                                   │
│  ├── Hizmet veren bildirim alır                                │
│  ├── İsteği görüntüler                                         │
│  ├── Kabul eder veya reddeder                                  │
│  └── Fiyat teklifi gönderir (opsiyonel)                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Anlaşma Sağlanırsa                                    │
│  ├── Fiyat ve tarih onaylanır                                  │
│  ├── Randevu oluşturulur                                       │
│  ├── Takvimlere eklenir                                        │
│  └── Hatırlatma gönderilir                                     │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Hizmet Gerçekleşir                                    │
│  ├── Hizmet veren belirlenen zamanda gelir                     │
│  ├── Hizmeti yapar                                             │
│  ├── İş tamamlanır                                             │
│  └── Ödeme yapılır                                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 6: ZORUNLU DEĞERLENDİRME ⭐                              │
│  ├── Hizmet alan kişiye bildirim gider                         │
│  ├── "Hizmeti değerlendirmeniz gerekiyor"                      │
│  ├── 1-5 yıldız puan ver                                       │
│  ├── Kategori puanları gir                                     │
│  ├── Yorum yaz (opsiyonel)                                     │
│  ├── Fotoğraf ekle (opsiyonel)                                 │
│  └── [Gönder] butonu → PUANLAMA ZORUNLU                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. E-TİCARET AKIŞI

### 4.1 Ürün Ekleme Akışı (Kendi Ürününü Satma)

```
┌─────────────────────────────────────────────────────────────────┐
│                 ÜRÜN EKLEME                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Ürün Türü Seçimi                                     │
│  ├── Fiziksel Ürün (ev, araba, telefon vb.)                    │
│  ├── Dijital Ürün (video eğitim, e-book vb.)                   │
│  └── Hizmet (daniuşmanlık, ders vb.)                           │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Ürün Bilgileri                                        │
│  ├── Ürün Adı                                                  │
│  ├── Açıklama                                                  │
│  ├── Kategori seçimi                                           │
│  ├── Fiyat                                                     │
│  ├── Para birimi                                               │
│  └── Stok (varsa)                                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Ürün Görselleri                                       │
│  ├── Kapak fotoğrafı yükle                                     │
│  ├── Detaylı fotoğraflar yükle                                 │
│  ├── Video ekle (opsiyonel)                                    │
│  └── Görselleri sırala                                         │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Ek Bilgiler                                           │
│  ├── Konum                                                     │
│  ├── Kargo bilgisi                                             │
│  ├── Garanti bilgisi                                           │
│  └── Özel notlar                                               │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Ürün Yayında                                          │
│  ├── [Yayınla] butonu                                          │
│  ├── Ürün satışa sunulur                                       │
│  ├── Arama sonuçlarında görünmeye başlar                        │
│  └── Sipariş beklenmeye başlanır                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Başkasının Ürününü Satma Akışı (Yetkilendirilmiş Satış)

```
┌─────────────────────────────────────────────────────────────────┐
│            BAŞKASININ ÜRÜNÜNÜ SATMA                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Ürün Bul                                              │
│  ├── Platformda ürün ara                                        │
│  ├── İlgili ürünü bul                                           │
│  └── Ürün detayına git                                          │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Yetki İsteği                                          │
│  ├── "Bu Ürünü Satmak İstiyorum" butonuna bas                  │
│  ├── Komisyon oranını teklif et                                 │
│  ├── Mesaj yaz (neden satabileceğin)                           │
│  └── [İsteği Gönder] butonu                                   │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Ürün Sahibi İnceler                                   │
│  ├── Ürün sahibine bildirim gider                              │
│  ├── İsteği görüntüler                                         │
│  ├── Satıcı profiline bakar                                    │
│  ├── Komisyon oranını değerlendirir                            │
│  └── Onaylar veya Reddeder                                     │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Onaylanırsa                                           │
│  ├── "Onaylı Satış" rozeti eklenir                             │
│  ├── Satıcı artık bu ürünü satabilir                           │
│  ├── Komisyon oranı sabitlenir                                 │
│  └── Sözleşme/doküman oluşturulur                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Satış Gerçekleşir                                     │
│  ├── Alıcı ürünü satın alır                                    │
│  ├── Ödeme alınır                                               │
│  ├── Komisyon otomatik hesaplanır                              │
│  ├── Para paylaşılır                                           │
│  └── Satış kaydı oluşturulur                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. TAKSİ SİSTEMİ AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                 TAKSİ ÇAĞIRMA                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Taksi Çağırma                                         │
│  ├── Ana sayfada "Taksi" butonuna bas                          │
│  ├── Konum otomatik algılanır veya girilir                      │
│  ├── Varış noktası girilir                                      │
│  └── [Taksi Çağır] butonu                                      │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Yakın Taksi Bulma                                     │
│  ├── Sistem yakındaki müsait taksileri bulur                   │
│  ├── Puanlarına göre sıralar                                    │
│  ├── Mesafe ve tahmini ücret gösterir                          │
│  └── Taksi seçimi yapılır                                       │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Taksi Şoförü Kabul Eder                               │
│  ├── Şoföre bildirim gider                                     │
│  ├── İsteği görüntüler                                         │
│  └── Kabul eder veya reddeder                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Yolculuk Başlar                                       │
│  ├── Taksi konumu haritada görünür                              │
│  ├── Tahmini varış süresi gösterilir                            │
│  ├── Şoför yolcuğa başlar                                       │
│  └── Gerçek zamanlı takip                                      │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Yolculuk Biter                                        │
│  ├── Varış noktasına ulaşılır                                   │
│  ├── Ücret hesaplanır (taksimetre)                             │
│  ├── Ödeme yapılır                                              │
│  └── [Yolculuğu Değerlendir] butonu                           │
│         │                                                      │
│         ▼                                                      │
│  ADIM 6: ZORUNLU DEĞERLENDİRME ⭐                              │
│  ├── 1-5 yıldız puan ver                                       │
│  ├── Sürüş kalitesi puanla                                     │
│  ├── Yorum yaz (opsiyonel)                                     │
│  └── [Gönder] butonu → PUANLAMA ZORUNLU                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. RESTORAN SİSTEMİ AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                 YEMEK SİPARİŞİ                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Restoran Seçimi                                       │
│  ├── Ana sayfada "Yemek" butonuna bas                          │
│  ├── Yakın restoranları gör                                     │
│  ├── Puanlarına göre sıralanmış                                 │
│  ├── Restoran seçimi                                           │
│  └── Menüye git                                                 │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Menüden Seçim                                         │
│  ├── Kategoriye göre ürünleri gör                               │
│  ├── Ürünü seç ( dürüm, porsiyon vb.)                          │
│  ├── Ek seçenekleri seç (peynir, acı sos vb.)                  │
│  ├── Adet belirle                                               │
│  └── [Sepete Ekle] butonu                                      │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Sepet ve Sipariş                                      │
│  ├── Sepeti görüntüler                                         │
│  ├── Toplam tutarı gör                                         │
│  ├── Teslimat türü seç:                                        │
│  │   ├── Paket Servis (adrese teslimat)                        │
│  │   ├── Gel Al (kendin al)                                    │
│  │   └── Yerinde Ye                                            │
│  └── [Siparişi Onayla] butonu                                 │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Teslimat Bilgisi                                      │
│  ├── Adres gir (paket servis için)                             │
│  ├── Telefon numarası                                          │
│  ├── Ödeme yöntemi seç                                         │
│  └── [Siparişi Ver] butonu                                    │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Sipariş Hazırlanıyor                                  │
│  ├── Restoran siparişi alır                                    │
│  ├── [Kabul Et] butonuna basar                                 │
│  ├── Sipariş hazırlanmaya başlanır                              │
│  ├── Müşteriye bildirim gider: "Siparişiniz hazırlanıyor"     │
│  └── Tahmini süre gösterilir                                    │
│         │                                                      │
│         ▼                                                      │
│  ADIM 6: Teslimat                                              │
│  ├── Kuryeye verilir veya hazır olur                            │
│  ├── Kurye yola çıkar (paket servis)                           │
│  ├── Müşteriye bildirim: "Siparişiniz yolda"                  │
│  └── Teslim edilir                                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 7: ZORUNLU DEĞERLENDİRME ⭐                              │
│  ├── 1-5 yıldız puan ver                                       │
│  ├── Lezzet puanla                                              │
│  ├── Hız puanla                                                │
│  ├── Paketleme puanla                                           │
│  ├── Yorum yaz (opsiyonel)                                     │
│  └── [Gönder] butonu → PUANLAMA ZORUNLU                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. ÇİFT YÖNLÜ HİZMET AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│            AYNI ANDA HİZMET VEREN VE ALAN                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ÖRNEK: ALÇI USTASI (Ali)                                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ALI'NIN GÜNÜ                                            │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                          │   │
│  │  08:00 - Kahvaltı                                       │   │
│  │         └── Marketten ekmek/çay alır (ÜRÜN ALIR)        │   │
│  │                                                          │   │
│  │  09:00 - İş Başlar                                      │   │
│  │         └── Müşterinin evine gider                       │   │
│  │         └── Alçı işi yapar (HİZMET VERİR)              │   │
│  │                                                          │   │
│  │  12:00 - Öğle Yemeği                                    │   │
│  │         └── Dürümcüden dürüm sipariş eder (HİZMET ALIR)│   │
│  │         └── Dürümcü dürümü hazırlar (HİZMET VERİR)     │   │
│  │                                                          │   │
│  │  13:00 - İş Devam                                       │   │
│  │         └── Malzeme lazım olur                           │   │
│  │         └── Yakındaki hırdavatçıdan boya alır (ÜRÜN ALIR)│  │
│  │         └── Hırdavatçı boya satar (ÜRÜN SATAR)          │   │
│  │                                                          │   │
│  │  15:00 - İş Biter                                       │   │
│  │         └── Müşteri Ali'yi puanlar ⭐ (ZORUNLU)         │   │
│  │                                                          │   │
│  │  16:00 - Taksi ile eve döner                             │   │
│  │         └── Taksi çağırır (HİZMET ALIR)                 │   │
│  │         └── Taksi şoförü hizmet verir (HİZMET VERİR)    │   │
│  │                                                          │   │
│  │  17:00 - Eve Varış                                     │   │
│  │         └── Taksi şoförünü puanlar ⭐ (ZORUNLU)         │   │
│  │                                                          │   │
│  │  18:00 - Akşam Yemeği                                   │   │
│  │         └── Restorandan yemek sipariş eder (HİZMET ALIR)│   │
│  │         └── Restoran yemek hazırlar (HİZMET VERİR)      │   │
│  │                                                          │   │
│  │  19:00 - Akşam                                         │   │
│  │         └── Restoranı puanlar ⭐ (ZORUNLU)              │   │
│  │         └── Telefon tamircisini arar (HİZMET ALIR)      │   │
│  │         └── Telefon tamircisi tamir eder (HİZMET VERİR) │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ALI'NIN GÜNÜ ÖZETİ:                                          │
│  ├── HİZMET VERDİ: Alçı işi (1 iş)                            │
│  ├── HİZMET ALDI: Taksi, yemek, tamir (3 hizmet)              │
│  ├── ÜRÜN ALDI: Ekmek, çay, boya (3 ürün)                     │
│  └── PUANLAMA YAPTI: Taksi şoförü, restoran, tamirci (3 kez) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. PUANLAMA AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                 PUANLAMA AKIŞI                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Hizmet/Satış Tamamlanır                               │
│  ├── Alıcı ve satıcı arasında işlem biter                       │
│  ├── Otomatik bildirim gönderilir                               │
│  └── "Lütfen hizmeti değerlendirin" mesajı                     │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Puanlama Sayfası Açılır                               │
│  ├── Hizmet alan kişi puanlama sayfasına yönlendirilir          │
│  ├── Sayfa sade ve nettir                                       │
│  └── Hızlıca doldurulabilir                                     │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Yıldız Puanlama                                       │
│  ├── 1-5 yıldız seçilir (zorunlu)                              │
│  ├── Mouse/touch ile tıklama                                    │
│  └── Anında görsel geri bildirim                                │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Kategori Puanları                                     │
│  ├── Kalite: 1-5 yıldız (zorunlu)                              │
│  ├── Zamanında Gelme: 1-5 yıldız (zorunlu)                     │
│  ├── İletişim: 1-5 yıldız (zorunlu)                            │
│  └── Fiyat/Performans: 1-5 yıldız (zorunlu)                    │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Yorum Yazma                                           │
│  ├── Yorum alanı (opsiyonel ama önerilir)                       │
│  ├── En az 10 karakter                                          │
│  └── Maksimum 500 karakter                                      │
│         │                                                      │
│         ▼                                                      │
│  ADIM 6: Fotoğraf Ekleme                                       │
│  ├── İşin görselini ekle (opsiyonel)                            │
│  ├── En fazla 5 fotoğraf                                        │
│  └── Her biri maks 5MB                                         │
│         │                                                      │
│         ▼                                                      │
│  ADIM 7: Gönder                                                 │
│  ├── [Değerlendirmeyi Gönder] butonu                           │
│  ├── Onay ekranı çıkar: "Emin misiniz?"                        │
│  ├── [Evet, Gönder] butonu                                     │
│  └── Başarılı mesajı: "Teşekkürler!"                           │
│         │                                                      │
│         ▼                                                      │
│  ADIM 8: Sonuç                                                 │
│  ├── Hizmet verenin puan ortalaması güncellenir                 │
│  ├── Hizmet veren bildirim alır                                 │
│  ├── Değerlendirme sayfasında görünür                           │
│  └── Arama sıralamasını etkiler                                 │
│                                                                 │
│  ⚠️ NOT: PUANLAMA YAPILMADAN YENİ HİZMET ALINAMAZ!           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. ÖDEME AKIŞI

```
┌─────────────────────────────────────────────────────────────────┐
│                 ÖDEME AKIŞI                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADIM 1: Ödeme Sayfası                                         │
│  ├── Sepet/sipariş özeti                                        │
│  ├── Toplam tutar                                               │
│  └── [Öde] butonu                                               │
│         │                                                      │
│         ▼                                                      │
│  ADIM 2: Ödeme Yöntemi Seçimi                                  │
│  ├── Kredi Kartı                                                │
│  │   ├── Kart numarası                                         │
│  │   ├── Son kullanma tarihi                                   │
│  │   ├── CVV                                                    │
│  │   └── Kart sahibi adı                                       │
│  ├── Banka Kartı                                                │
│  ├── Havale/EFT                                                 │
│  ├── Mobil Ödeme (Apple Pay, Google Pay)                        │
│  └── Kapıda Ödeme (belirli ürünler için)                        │
│         │                                                      │
│         ▼                                                      │
│  ADIM 3: Ödeme İşlemi                                          │
│  ├── 3D Secure doğrulaması (gerekirse)                          │
│  ├── Banka onayı                                                │
│  ├── Ödeme tamamlanır                                           │
│  └── Makbuz/fatura oluşturulur                                  │
│         │                                                      │
│         ▼                                                      │
│  ADIM 4: Sipariş Onaylanır                                     │
│  ├── Satıcıya bildirim gider                                    │
│  ├── "Yeni siparişiniz var" mesajı                              │
│  ├── Sipariş detayları gösterilir                               │
│  └── Satıcı işi hazırlamaya başlar                              │
│         │                                                      │
│         ▼                                                      │
│  ADIM 5: Komisyon Hesaplama                                    │
│  ├── Satış tutarı: 100₺                                        │
│  ├── Platform komisyonu: %1 → 1₺                               │
│  ├── Satıcı komisyonu (varsa): %5 → 5₺                        │
│  └── Ürün sahibine kalan: 94₺                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. KARAR DİYAGRAMI: HANGİ HESAP TÜRÜ?

```
┌─────────────────────────────────────────────────────────────────┐
│              HANGİ HESAP TÜRÜNÜ SEÇMELİM?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Soru: Ne yapmak istiyorsun?                                   │
│                                                                 │
│  ├── "Kendi işimi yapmak istiyorum"                             │
│  │   └── BİREYSEL HESAP                                        │
│  │       ├── Ürün sat (ev, araba, telefon)                     │
│  │       ├── Hizmet ver (usta, danışman)                       │
│  │       ├── Video eğitim sat                                  │
│  │       └── İlan sayfası aç                                   │
│  │                                                              │
│  ├── "Şirket kurmak istiyorum"                                  │
│  │   └── KURUMSAL HESAP                                        │
│  │       ├── Mağaza aç                                         │
│  │       ├── Çalışan yönetimi                                  │
│  │       ├── Finansal raporlar                                 │
│  │       └── Toplu satış yap                                   │
│  │                                                              │
│  ├── "Resmi kurum olarak duyuru yapmak istiyorum"               │
│  │   └── KAMUSAL HESAP                                         │
│  │       ├── Duyuru yap                                        │
│  │       ├── Toplu bildirim gönder                              │
│  │       └── Resmi rozet al                                    │
│  │                                                              │
│  └── "Hem iş yapıp hem hizmet almak istiyorum"                 │
│      └── BİREYSEL HESAP + ÇİFT YÖNLÜ MOD                      │
│          ├── Hizmet ver (usta olarak)                           │
│          ├── Hizmet al (taksi, yemek vb.)                      │
│          ├── Ürün sat (kendi ürettiğin)                         │
│          └── Ürün al (ihtiyacın olan)                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Bu diyagramlar kullanıcı deneyimini ve sistem akışlarını göstermektedir.*
*Tüm akışlar minimal tasarım ilkesiyle tasarlanmıştır.*
