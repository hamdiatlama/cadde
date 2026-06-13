-- ============================================================
-- OTO EKSPERTİZ RAPOR SİSTEMİ - PostgreSQL Veritabanı Şeması
-- ============================================================

-- Kullanıcı tanımlı enum tipleri
CREATE TYPE yakit_tipi AS ENUM ('Benzin', 'Dizel', 'LPG', 'Hibrit', 'Elektrik');
CREATE TYPE arac_tipi AS ENUM ('Binek', 'Ticari', 'Agir Ticari');
CREATE TYPE renk_tipi AS ENUM ('Opak', 'Metalik');
CREATE TYPE durum_kodu AS ENUM (
    'ORJINAL', 'BOYALI', 'LOKAL_BOYALI', 'DEGISMI', 'KAPLAMA',
    'CIZIK', 'GOCUK', 'CATLAK', 'SOK_TAK', 'ISLEM_GORMUS',
    'PLASTIK_PARCA', 'TAS_IZI', 'DEFORME', 'YIPRANMA', 'YIRPIK'
);
CREATE TYPE ic_durum AS ENUM ('NOR', 'YRT', 'LEK', 'YOK');
CREATE TYPE dis_durum AS ENUM ('ORJ', 'DGS', 'KRK', 'BOY', 'EZIK');
CREATE TYPE lastik_durum AS ENUM ('Normal', 'HasarlI', 'JantKirigi');
CREATE TYPE evet_hayir AS ENUM ('Evet', 'Hayir');
CREATE TYPE kontrol_sonuc AS ENUM ('Basarili', 'Basarisiz', 'Uyarili');

-- ============================================================
-- 1. FİRMA / BAYİ
-- ============================================================
CREATE TABLE firmalar (
    id              SERIAL PRIMARY KEY,
    firma_adi       VARCHAR(200) NOT NULL,
    tse_no          VARCHAR(50),
    telefon         VARCHAR(20),
    adres           TEXT,
    eposta          VARCHAR(100),
    vergi_daire     VARCHAR(100),
    vergi_no        VARCHAR(20),
    yetkili_adi     VARCHAR(100),
    aktif           BOOLEAN DEFAULT true,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 2. KULLANICILAR (EKSPERLER)
-- ============================================================
CREATE TABLE kullanicilar (
    id              SERIAL PRIMARY KEY,
    firma_id        INTEGER REFERENCES firmalar(id) ON DELETE CASCADE,
    ad_soyad        VARCHAR(150) NOT NULL,
    kullanici_adi   VARCHAR(50) UNIQUE NOT NULL,
    sifre_hash      VARCHAR(255) NOT NULL,
    rol             VARCHAR(20) DEFAULT 'eksper',
    imza_data       TEXT,  -- base64 imza görseli
    aktif           BOOLEAN DEFAULT true,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 3. ARAÇLAR
-- ============================================================
CREATE TABLE araclar (
    id              SERIAL PRIMARY KEY,
    plaka           VARCHAR(20) NOT NULL,
    sasi_no         VARCHAR(50) NOT NULL,
    motor_no        VARCHAR(50),
    marka           VARCHAR(100),
    model           VARCHAR(100),
    model_yili      INTEGER,
    renk            renk_tipi,
    yakit           yakit_tipi,
    arac_tipi       arac_tipi,
    km              INTEGER,  -- km veya saat
    muayene_tarihi  DATE,
    created_at      TIMESTAMP DEFAULT NOW(),

    UNIQUE (plaka, sasi_no)
);

-- ============================================================
-- 4. PAKETLER
-- ============================================================
CREATE TABLE paketler (
    id              SERIAL PRIMARY KEY,
    paket_adi       VARCHAR(100) NOT NULL,
    tutar           NUMERIC(10,2),
    aciklama        TEXT,
    aktif           BOOLEAN DEFAULT true
);

-- ============================================================
-- 5. RAPORLAR (ANA TABLO)
-- ============================================================
CREATE TABLE raporlar (
    id              SERIAL PRIMARY KEY,
    rapor_no        VARCHAR(50) UNIQUE NOT NULL,
    firma_id        INTEGER NOT NULL REFERENCES firmalar(id),
    eksper_id       INTEGER NOT NULL REFERENCES kullanicilar(id),
    arac_id         INTEGER NOT NULL REFERENCES araclar(id),
    paket_id        INTEGER REFERENCES paketler(id),
    tarih           TIMESTAMP NOT NULL DEFAULT NOW(),
    anahtar         evet_hayir DEFAULT 'Evet',
    ruhsat          evet_hayir DEFAULT 'Evet',
    ucret           NUMERIC(10,2),
    eksper_notu     TEXT,
    genel_sonuc     kontrol_sonuc,
    qr_kod          TEXT,
    gecerlilik_tarihi DATE,
    durum           VARCHAR(20) DEFAULT 'Taslak', -- Taslak, Onayli, Iptal
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 6. KAPORTA / BOYA TEST SONUÇLARI (Panel Bazlı)
-- ============================================================
CREATE TABLE panel_olcumleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    panel_adi       VARCHAR(100) NOT NULL,  -- Örn: Ön Tampon, Kaput, Tavan vb.
    durum_kodu      durum_kodu,
    boya_kalinligi  INTEGER,  -- mikron (µm)
    aciklama        TEXT,
    sira            INTEGER DEFAULT 0
);

-- ============================================================
-- 7. İÇ MEKAN KONTROLLERİ
-- ============================================================
CREATE TABLE ic_mekan_kontrolleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    kontrol_noktasi VARCHAR(100) NOT NULL,  -- Koltuk, Taban Halısı, Tavan, Paspas
    durum           ic_durum,
    aciklama        TEXT
);

-- ============================================================
-- 8. DIŞ KONTROLLER (Aydınlatma & Cam & Fitil & Ekipman)
-- ============================================================
CREATE TABLE dis_kontroller (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    parca           VARCHAR(100) NOT NULL,  -- Ön Cam, Far, Tampon, Kapı Fitili vb.
    durum           dis_durum,
    aciklama        TEXT
);

-- ============================================================
-- 9. ZORUNLU EKİPMANLAR
-- ============================================================
CREATE TABLE zorunlu_ekipmanlar (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    ekipman_adi     VARCHAR(100) NOT NULL,  -- İlk yardım çantası, reflektör, üçgen, çekici halatı
    var_mi          BOOLEAN DEFAULT false
);

-- ============================================================
-- 10. LASTİK & JANT KONTROLLERİ
-- ============================================================
CREATE TABLE lastik_jant_kontrolleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    pozisyon        VARCHAR(20) NOT NULL,  -- Sağ Ön, Sol Ön, Sağ Arka, Sol Arka, Stepne
    lastik_disi_mm  NUMERIC(4,1),          -- diş derinliği mm
    jant_durum      lastik_durum,
    lastik_marka    VARCHAR(50),
    lastik_ebat     VARCHAR(30),
    aciklama        TEXT
);

-- ============================================================
-- 11. MEKANİK & MOTOR KONTROLLERİ
-- ============================================================
CREATE TABLE mekanik_kontroller (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    test_adi        VARCHAR(100) NOT NULL,  -- Motor, Şanzıman, Fren, Süspansiyon vb.
    sonuc_deger     TEXT,
    birim           VARCHAR(30),
    referans_deger  TEXT,
    basarili_mi     BOOLEAN,
    aciklama        TEXT
);

-- ============================================================
-- 12. ELEKTRONİK SİSTEM KONTROLLERİ (OBD)
-- ============================================================
CREATE TABLE elektronik_kontroller (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    sistem_adi      VARCHAR(100) NOT NULL,  -- Motor, ABS, Airbag, Klima, Sensörler, Akü
    kontrol         TEXT,
    hata_kodu       VARCHAR(20),
    basarili_mi     BOOLEAN,
    aciklama        TEXT
);

-- ============================================================
-- 13. DYNO TESTİ
-- ============================================================
CREATE TABLE dyno_testleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    olcum_adi       VARCHAR(100) NOT NULL,  -- Motor Gücü, Tork, Şanzıman Aralık, Tekerlek Gücü
    olcum_degeri    NUMERIC(10,2),
    birim           VARCHAR(20),
    fabrika_degeri  NUMERIC(10,2),
    fark_yuzde      NUMERIC(5,2),
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 14. TRAMER SORGUSU
-- ============================================================
CREATE TABLE tramer_kayitlari (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    kaza_var_mi     BOOLEAN DEFAULT false,
    hasar_detayi    TEXT,
    agir_hasar_mi   BOOLEAN DEFAULT false,
    degisen_parcalar TEXT,
    sorgu_tarihi    TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 15. ŞASİ / VİN ORİJİNALLİK KONTROLÜ
-- ============================================================
CREATE TABLE sasi_kontrolleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    sasi_orijinal_mi BOOLEAN DEFAULT true,
    etiketler_mvcut_mu BOOLEAN DEFAULT true,
    vin_tablasi_durum VARCHAR(100),
    aciklama        TEXT
);

-- ============================================================
-- 16. EKSTRA DONANIMLAR
-- ============================================================
CREATE TABLE ekstra_donanimlar (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    donanim_adi     VARCHAR(100) NOT NULL,  -- Sunroof, Navigasyon, Kamera, Park sensörü vb.
    var_mi          BOOLEAN DEFAULT true
);

-- ============================================================
-- 17. FOTOĞRAFLAR
-- ============================================================
CREATE TABLE fotograflar (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    dosya_yolu      TEXT NOT NULL,
    kategorisi      VARCHAR(50),  -- Ruhsat, Genel, Hasar, TestEkrani
    aciklama        TEXT,
    sira            INTEGER DEFAULT 0
);

-- ============================================================
-- 18. TEST SÜRÜŞÜ DEĞERLENDİRMESİ
-- ============================================================
CREATE TABLE test_surusu (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    direksiyon      TEXT,
    viraj           TEXT,
    titresim        TEXT,
    ses             TEXT,
    kaciklik        TEXT,
    genel_not       TEXT
);

-- ============================================================
-- 19. EGZOZ EMİSYON ÖLÇÜMÜ
-- ============================================================
CREATE TABLE egzoz_emisyon (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    co              NUMERIC(6,2),
    hc              NUMERIC(6,2),
    co2             NUMERIC(6,2),
    lambda          NUMERIC(4,2),
    dpf_doluluk     NUMERIC(5,2),
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 20. FREN HİDROLİĞİ & ANTİFRİZ TESTİ
-- ============================================================
CREATE TABLE sivi_testleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    test_turu       VARCHAR(50) NOT NULL,  -- Fren Hidroliği, Antifriz
    su_orani        NUMERIC(5,2),
    donma_noktasi   NUMERIC(5,2),
    kaynama_noktasi NUMERIC(5,2),
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 21. EL FRENİ PERFORMANS TESTİ
-- ============================================================
CREATE TABLE el_freni_testleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    cekme_mesafesi  NUMERIC(5,1),
    kuvvet          NUMERIC(6,2),
    etkinlik_oran   NUMERIC(5,2),
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 22. DÖRT ÇEKER / DİFERANSİYEL KONTROLÜ
-- ============================================================
CREATE TABLE dort_ceker_kontrolleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    transfer_kutusu TEXT,
    on_diferansiyel TEXT,
    arka_diferansiyel TEXT,
    tork_dagilimi   TEXT,
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 23. KAYIŞ & GERGİ SİSTEMİ
-- ============================================================
CREATE TABLE kayis_kontrolleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    kayis_turu      VARCHAR(50) NOT NULL,  -- Triger, Alternatör, Klima
    asinma_durumu   VARCHAR(50),
    gerginlik_durumu VARCHAR(50),
    basarili_mi     BOOLEAN
);

-- ============================================================
-- 24. KABUL KRİTERLERİ (Rapor bazında referans)
-- ============================================================
CREATE TABLE kabul_kriterleri (
    id              SERIAL PRIMARY KEY,
    rapor_id        INTEGER NOT NULL REFERENCES raporlar(id) ON DELETE CASCADE,
    fren_dengesi_sapma_max NUMERIC(5,2) DEFAULT 15.00,
    suspansiyon_verim_min   NUMERIC(5,2) DEFAULT 40.00,
    el_freni_etkinlik_min   NUMERIC(5,2) DEFAULT 16.00
);

-- ============================================================
-- INDEXLER
-- ============================================================
CREATE INDEX idx_raporlar_firma ON raporlar(firma_id);
CREATE INDEX idx_raporlar_eksper ON raporlar(eksper_id);
CREATE INDEX idx_raporlar_arac ON raporlar(arac_id);
CREATE INDEX idx_raporlar_tarih ON raporlar(tarih);
CREATE INDEX idx_raporlar_plaka ON raporlar(rapor_no);
CREATE INDEX idx_araclar_plaka ON araclar(plaka);
CREATE INDEX idx_araclar_sasi ON araclar(sasi_no);
CREATE INDEX idx_panel_olcumleri_rapor ON panel_olcumleri(rapor_id);
CREATE INDEX idx_mekanik_rapor ON mekanik_kontroller(rapor_id);
CREATE INDEX idx_elektronik_rapor ON elektronik_kontroller(rapor_id);

-- ============================================================
-- ÖRNEK VERİ
-- ============================================================
INSERT INTO firmalar (firma_adi, tse_no, telefon) VALUES
    ('Ornek Ekspertiz Merkezi', 'TS-13805-001', '0212 XXX XX XX');

INSERT INTO kullanicilar (firma_id, ad_soyad, kullanici_adi, sifre_hash, rol) VALUES
    (1, 'Ahmet Yilmaz', 'ahmet', 'hash_placeholder', 'eksper');

INSERT INTO paketler (paket_adi, tutar, aciklama) VALUES
    ('Temel Paket', 500.00, 'Kaporta, boya, mekanik ve OBD testi'),
    ('Premium Paket', 950.00, 'Temel paket + Dyno testi + Tramer sorgusu'),
    ('VIP Paket', 1500.00, 'Tüm testler + test sürüşü + detayli rapor');

-- ============================================================
-- RAPOR GÖRÜNTÜLEME İÇİN ÖRNEK SORGU
-- ============================================================
-- SELECT
--     r.rapor_no,
--     r.tarih,
--     a.plaka,
--     a.marka || ' ' || a.model AS arac,
--     k.ad_soyad AS eksper,
--     p.paket_adi,
--     r.genel_sonuc
-- FROM raporlar r
-- JOIN araclar a ON a.id = r.arac_id
-- JOIN kullanicilar k ON k.id = r.eksper_id
-- LEFT JOIN paketler p ON p.id = r.paket_id
-- ORDER BY r.tarih DESC;
