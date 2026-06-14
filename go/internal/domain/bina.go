package domain

import "time"

type Site struct {
	ID             int       `json:"id"`
	Adi            string    `json:"adi"`
	Adres          string    `json:"adres"`
	Sekil          string    `json:"sekil"` // site, apartman
	Kurucu         string    `json:"kurucu"`
	KurucuTel      string    `json:"kurucu_tel"`
	Banka          string    `json:"banka"`
	KomisyonYuzde  float64   `json:"komisyon_yuzde"`
	KurulumTamam   bool      `json:"kurulum_tamam"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

type Blok struct {
	ID       int    `json:"id"`
	SiteID   int    `json:"site_id"`
	Adi      string `json:"adi"`
	KatAdet  int    `json:"kat_adet"`
	DaireKat int    `json:"daire_kat"` // daire sayisi per kat
}

type Daire struct {
	ID      int    `json:"id"`
	BlokID  int    `json:"blok_id"`
	No      string `json:"no"`
	Kat     int    `json:"kat"`
	KapiNo  int    `json:"kapi_no"`
	Alan    float64 `json:"alan,omitempty"`
	SakinID *int   `json:"sakin_id,omitempty"`
}

type Kisi struct {
	ID             int       `json:"id"`
	SiteID         int       `json:"site_id"`
	Ad             string    `json:"ad"`
	Tel            string    `json:"tel"`
	Email          string    `json:"email,omitempty"`
	Rol            string    `json:"rol"` // malik, kiracil, yonetici
	DaireID        *int      `json:"daire_id,omitempty"`
	BlokID         *int      `json:"blok_id,omitempty"`
	Yetki          string    `json:"yetki,omitempty"` // yonetici
	CreatedAt      time.Time `json:"created_at"`
}

type Duyuru struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Baslik    string    `json:"baslik"`
	Icerik    string    `json:"icerik"`
	Kategori  string    `json:"kategori"` // genel, karar, hatirlatma, aidat
	Yapan     string    `json:"yapan"`
	CreatedAt time.Time `json:"created_at"`
}

type Aidat struct {
	ID       int       `json:"id"`
	SiteID   int       `json:"site_id"`
	DaireID  int       `json:"daire_id"`
	BlokID   int       `json:"blok_id"`
	DaireNo  string    `json:"daire_no"`
	Ay       int       `json:"ay"`
	Yil      int       `json:"yil"`
	Tutar    float64   `json:"tutar"`
	Odendi   bool      `json:"odendi"`
	OdemeTarihi *time.Time `json:"odeme_tarihi,omitempty"`
	KapiNo   int       `json:"kapi_no"`
	CreatedAt time.Time `json:"created_at"`
}

type Gelir struct {
	ID          int       `json:"id"`
	SiteID      int       `json:"site_id"`
	Baslik      string    `json:"baslik"`
	Tutar       float64   `json:"tutar"`
	Kategori    string    `json:"kategori"`
	Aciklama    string    `json:"aciklama,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type Gider struct {
	ID          int       `json:"id"`
	SiteID      int       `json:"site_id"`
	Baslik      string    `json:"baslik"`
	Tutar       float64   `json:"tutar"`
	Kategori    string    `json:"kategori"`
	FirmaID     *int      `json:"firma_id,omitempty"`
	Aciklama    string    `json:"aciklama,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type Arac struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Plaka     string    `json:"plaka"`
	DaireID   *int      `json:"daire_id,omitempty"`
	BlokID    *int      `json:"blok_id,omitempty"`
	SakinAd   string    `json:"sakin_ad"`
	Tel       string    `json:"tel,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type Personel struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Ad        string    `json:"ad"`
	Tel       string    `json:"tel"`
	Gorev     string    `json:"gorev"`
	Maas      float64   `json:"maas"`
	IseBaslama *time.Time `json:"ise_baslama,omitempty"`
	IsActive  bool      `json:"is_active"`
	CreatedAt time.Time `json:"created_at"`
}

type Firma struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Ad        string    `json:"ad"`
	Yetkili   string    `json:"yetkili"`
	Tel       string    `json:"tel"`
	Adres     string    `json:"adres,omitempty"`
	Sektor    string    `json:"sektor"`
	CreatedAt time.Time `json:"created_at"`
}

type IsTalebi struct {
	ID           int       `json:"id"`
	SiteID       int       `json:"site_id"`
	Baslik       string    `json:"baslik"`
	Aciklama     string    `json:"aciklama,omitempty"`
	Sektor       string    `json:"sektor"`
	Durum        string    `json:"durum"` // bekliyor, atandi, tamamlandi
	TalepEdenAd  string    `json:"talep_eden_ad"`
	AtananFirmaID *int     `json:"atanan_firma_id,omitempty"`
	Teklifler    string    `json:"teklifler,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    *time.Time `json:"updated_at,omitempty"`
}

type Sayac struct {
	ID          int       `json:"id"`
	SiteID      int       `json:"site_id"`
	DaireID     int       `json:"daire_id"`
	BlokID      int       `json:"blok_id"`
	DaireNo     string    `json:"daire_no"`
	Tur         string    `json:"tur"` // su, elektrik, dogalgaz
	SonEndeks   float64   `json:"son_endeks"`
	OncekiEndeks float64  `json:"onceki_endeks"`
	BirimFiyat  float64   `json:"birim_fiyat"`
	Tarih       time.Time `json:"tarih"`
	CreatedAt   time.Time `json:"created_at"`
}

type Kargo struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	TakipNo   string    `json:"takip_no"`
	DaireID   *int      `json:"daire_id,omitempty"`
	BlokID    *int      `json:"blok_id,omitempty"`
	SakinAd   string    `json:"sakin_ad"`
	Tel       string    `json:"tel,omitempty"`
	Durum     string    `json:"durum"` // teslimEdildi, bekliyor
	CreatedAt time.Time `json:"created_at"`
}

type Ziyaretci struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Ad        string    `json:"ad"`
	DaireID   *int      `json:"daire_id,omitempty"`
	BlokID    *int      `json:"blok_id,omitempty"`
	Giris     time.Time `json:"giris"`
	Cikis     *time.Time `json:"cikis,omitempty"`
	Plaka     string    `json:"plaka,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type Anket struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Baslik    string    `json:"baslik"`
	Aciklama  string    `json:"aciklama,omitempty"`
	Baslangic time.Time `json:"baslangic"`
	Bitis     *time.Time `json:"bitis,omitempty"`
	Aktif     bool      `json:"aktif"`
	CreatedAt time.Time `json:"created_at"`
}

type AnketSecenek struct {
	ID        int    `json:"id"`
	AnketID   int    `json:"anket_id"`
	Metin     string `json:"metin"`
	OySayisi  int    `json:"oy_sayisi"`
}

type AnketOy struct {
	ID        int       `json:"id"`
	AnketID   int       `json:"anket_id"`
	SecenekID int       `json:"secenek_id"`
	KisiID    *int      `json:"kisi_id,omitempty"`
	DaireID   *int      `json:"daire_id,omitempty"`
	Oy        time.Time `json:"oy"`
}

type Icra struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	DaireID   int       `json:"daire_id"`
	BlokID    int       `json:"blok_id"`
	DaireNo   string    `json:"daire_no,omitempty"`
	KapiNo    *int      `json:"kapi_no,omitempty"`
	Baslik    string    `json:"baslik"`
	Aciklama  string    `json:"aciklama,omitempty"`
	BorcTuru  string    `json:"borc_turu"`
	Tutar     float64   `json:"tutar"`
	Tarih     *time.Time `json:"tarih,omitempty"`
	Durum     string    `json:"durum"`
	Avukat    string    `json:"avukat,omitempty"`
	Masraf    float64   `json:"masraf"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt *time.Time `json:"updated_at,omitempty"`
}

type Otopark struct {
	ID         int       `json:"id"`
	SiteID     int       `json:"site_id"`
	BlokID     *int      `json:"blok_id,omitempty"`
	No         string    `json:"no"`
	Kat        string    `json:"kat,omitempty"`
	Tip        string    `json:"tip"`
	DaireID    *int      `json:"daire_id,omitempty"`
	KisiID     *int      `json:"kisi_id,omitempty"`
	AracPlaka  string    `json:"arac_plaka,omitempty"`
	KiraBedeli float64   `json:"kira_bedeli"`
	CreatedAt  time.Time `json:"created_at"`
}

type Rezervasyon struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Alan      string    `json:"alan"`
	KisiID    *int      `json:"kisi_id,omitempty"`
	DaireID   *int      `json:"daire_id,omitempty"`
	Baslangic time.Time `json:"baslangic"`
	Bitis     time.Time `json:"bitis"`
	Notlar    string    `json:"notlar,omitempty"`
	Durum     string    `json:"durum"`
	Ucret     float64   `json:"ucret"`
	CreatedAt time.Time `json:"created_at"`
}

type Toplanti struct {
	ID         int       `json:"id"`
	SiteID     int       `json:"site_id"`
	Baslik     string    `json:"baslik"`
	Tarih      time.Time `json:"tarih"`
	Yer        string    `json:"yer,omitempty"`
	Katilanlar string    `json:"katilanlar,omitempty"`
	Gundem     string    `json:"gundem,omitempty"`
	Kararlar   string    `json:"kararlar,omitempty"`
	TutanakURL string    `json:"tutanak_url,omitempty"`
	CreatedAt  time.Time `json:"created_at"`
}

type BankaHesap struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	BankaAdi  string    `json:"banka_adi"`
	Sube      string    `json:"sube,omitempty"`
	HesapAdi  string    `json:"hesap_adi,omitempty"`
	Iban      string    `json:"iban"`
	HesapNo   string    `json:"hesap_no,omitempty"`
	Tur       string    `json:"tur"`
	Bakiye    float64   `json:"bakiye"`
	CreatedAt time.Time `json:"created_at"`
}

type Isitma struct {
	ID           int       `json:"id"`
	SiteID       int       `json:"site_id"`
	Tur          string    `json:"tur"`
	DaireID      *int      `json:"daire_id,omitempty"`
	BlokID       *int      `json:"blok_id,omitempty"`
	YakilanM3    float64   `json:"yakilan_m3"`
	BirimFiyat   float64   `json:"birim_fiyat"`
	Tutar        float64   `json:"tutar"`
	Ay           int       `json:"ay"`
	Yil          int       `json:"yil"`
	Odendi       bool      `json:"odendi"`
	OdemeTarihi  *time.Time `json:"odeme_tarihi,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}

type Butce struct {
	ID           int       `json:"id"`
	SiteID       int       `json:"site_id"`
	Yil          int       `json:"yil"`
	Baslik       string    `json:"baslik"`
	Kategori     string    `json:"kategori"`
	Tur          string    `json:"tur"`
	Planlanan    float64   `json:"planlanan"`
	Gerceklesen  float64   `json:"gerceklesen"`
	Aciklama     string    `json:"aciklama,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    *time.Time `json:"updated_at,omitempty"`
}

type Dosya struct {
	ID        int       `json:"id"`
	SiteID    int       `json:"site_id"`
	Baslik    string    `json:"baslik"`
	DosyaTuru string    `json:"dosya_turu,omitempty"`
	DosyaURL  string    `json:"dosya_url,omitempty"`
	Boyut     int64     `json:"boyut"`
	Aciklama  string    `json:"aciklama,omitempty"`
	Yukleyen  string    `json:"yukleyen,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type Bildirim struct {
	ID         int       `json:"id"`
	SiteID     int       `json:"site_id"`
	Baslik     string    `json:"baslik"`
	Icerik     string    `json:"icerik,omitempty"`
	Tur        string    `json:"tur"`
	Hedef      string    `json:"hedef"`
	HedefID    *int      `json:"hedef_id,omitempty"`
	Gonderildi bool      `json:"gonderildi"`
	CreatedAt  time.Time `json:"created_at"`
}
