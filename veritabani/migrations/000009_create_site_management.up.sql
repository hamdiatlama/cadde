-- ============================================================
-- DOMAIN: BINA / SITE YONETIMI
-- ============================================================

-- Site/Bina tanimi
CREATE TABLE siteler (
    id              SERIAL PRIMARY KEY,
    adi             VARCHAR(200) NOT NULL,
    adres           TEXT,
    sekil           VARCHAR(20) DEFAULT 'site', -- site, apartman
    kurucu          VARCHAR(100),
    kurucu_tel      VARCHAR(20),
    banka           VARCHAR(100),
    komisyon_yuzde  NUMERIC(4,2) DEFAULT 2,
    kurulum_tamam   BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Bloklar
CREATE TABLE bloklar (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    adi             VARCHAR(100) NOT NULL,
    kat_adet        INT DEFAULT 4,
    daire_kat       INT DEFAULT 2
);

CREATE INDEX idx_bloklar_site ON bloklar(site_id);

-- Daireler
CREATE TABLE daireler (
    id              SERIAL PRIMARY KEY,
    blok_id         INT NOT NULL REFERENCES bloklar(id) ON DELETE CASCADE,
    no              VARCHAR(20) NOT NULL,
    kat             INT NOT NULL,
    kapi_no         INT NOT NULL,
    alan            NUMERIC(8,2),
    sakin_id        INT REFERENCES site_kisiler(id) ON DELETE SET NULL
);

CREATE INDEX idx_daireler_blok ON daireler(blok_id);

-- Kisi / Sakin
CREATE TABLE site_kisiler (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    ad              VARCHAR(100) NOT NULL,
    tel             VARCHAR(20),
    email           VARCHAR(200),
    rol             VARCHAR(20) DEFAULT 'malik', -- malik, kiracil, yonetici, diger
    daire_id        INT REFERENCES daireler(id) ON DELETE SET NULL,
    blok_id         INT REFERENCES bloklar(id) ON DELETE SET NULL,
    yetki           VARCHAR(50), -- yonetici, yardimci
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_kisiler_site ON site_kisiler(site_id);

-- Duyuru
CREATE TABLE site_duyurulari (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik          VARCHAR(300) NOT NULL,
    icerik          TEXT,
    kategori        VARCHAR(50) DEFAULT 'genel', -- genel, karar, hatirlatma, aidat, duyuru
    yapan           VARCHAR(100),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_duyuru_site ON site_duyurulari(site_id);

-- Aidat
CREATE TABLE aidat (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    daire_id        INT NOT NULL REFERENCES daireler(id) ON DELETE CASCADE,
    blok_id         INT NOT NULL REFERENCES bloklar(id) ON DELETE CASCADE,
    daire_no        VARCHAR(20),
    ay              INT NOT NULL,
    yil             INT NOT NULL,
    tutar           NUMERIC(10,2) NOT NULL,
    odendi          BOOLEAN DEFAULT false,
    odeme_tarihi    TIMESTAMPTZ,
    kapi_no         INT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_aidat_site ON aidat(site_id);
CREATE INDEX idx_aidat_daire ON aidat(daire_id);
CREATE INDEX idx_aidat_donem ON aidat(yil, ay);
CREATE INDEX idx_aidat_odendi ON aidat(odendi) WHERE odendi = false;

-- Gelir
CREATE TABLE site_gelir (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik          VARCHAR(300) NOT NULL,
    tutar           NUMERIC(10,2) NOT NULL,
    kategori        VARCHAR(50) DEFAULT 'aidat',
    aciklama        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_gelir_site ON site_gelir(site_id);

-- Gider
CREATE TABLE site_gider (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik          VARCHAR(300) NOT NULL,
    tutar           NUMERIC(10,2) NOT NULL,
    kategori        VARCHAR(50) DEFAULT 'genel',
    firma_id        INT REFERENCES site_firma(id) ON DELETE SET NULL,
    aciklama        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_gider_site ON site_gider(site_id);

-- Arac / Park
CREATE TABLE site_arac (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    plaka           VARCHAR(20) NOT NULL,
    daire_id        INT REFERENCES daireler(id) ON DELETE SET NULL,
    blok_id         INT REFERENCES bloklar(id) ON DELETE SET NULL,
    sakin_ad        VARCHAR(100),
    tel             VARCHAR(20),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_arac_site ON site_arac(site_id);
CREATE INDEX idx_arac_plaka ON site_arac(plaka);

-- Personel
CREATE TABLE site_personel (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    ad              VARCHAR(100) NOT NULL,
    tel             VARCHAR(20),
    gorev           VARCHAR(100),
    maas            NUMERIC(10,2) DEFAULT 0,
    ise_baslama     DATE,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_personel_site ON site_personel(site_id);

-- Firma / Tedarikci
CREATE TABLE site_firma (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    ad              VARCHAR(200) NOT NULL,
    yetkili         VARCHAR(100),
    tel             VARCHAR(20),
    adres           TEXT,
    sektor          VARCHAR(100),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_firma_site ON site_firma(site_id);

-- Is Talebi
CREATE TABLE site_is_talepleri (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik          VARCHAR(300) NOT NULL,
    aciklama        TEXT,
    sektor          VARCHAR(100),
    durum           VARCHAR(20) DEFAULT 'bekliyor', -- bekliyor, atandi, tamamlandi, iptal
    talep_eden_ad   VARCHAR(100),
    atanan_firma_id INT REFERENCES site_firma(id) ON DELETE SET NULL,
    teklifler       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ
);

CREATE INDEX idx_istalepleri_site ON site_is_talepleri(site_id);

-- Sayac (su, elektrik, dogalgaz)
CREATE TABLE site_sayac (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    daire_id        INT NOT NULL REFERENCES daireler(id) ON DELETE CASCADE,
    blok_id         INT NOT NULL REFERENCES bloklar(id) ON DELETE CASCADE,
    daire_no        VARCHAR(20),
    tur             VARCHAR(20) NOT NULL, -- su, elektrik, dogalgaz
    son_endeks      NUMERIC(10,2) NOT NULL,
    onceki_endeks   NUMERIC(10,2) DEFAULT 0,
    birim_fiyat     NUMERIC(8,4) NOT NULL,
    tarih           TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sayac_site ON site_sayac(site_id);
CREATE INDEX idx_sayac_daire ON site_sayac(daire_id);

-- Kargo
CREATE TABLE site_kargo (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    takip_no        VARCHAR(100) NOT NULL,
    daire_id        INT REFERENCES daireler(id) ON DELETE SET NULL,
    blok_id         INT REFERENCES bloklar(id) ON DELETE SET NULL,
    sakin_ad        VARCHAR(100),
    tel             VARCHAR(20),
    durum           VARCHAR(20) DEFAULT 'bekliyor', -- bekliyor, teslimEdildi
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_kargo_site ON site_kargo(site_id);

-- Ziyaretci
CREATE TABLE site_ziyaretci (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    ad              VARCHAR(100) NOT NULL,
    daire_id        INT REFERENCES daireler(id) ON DELETE SET NULL,
    blok_id         INT REFERENCES bloklar(id) ON DELETE SET NULL,
    giris           TIMESTAMPTZ NOT NULL,
    cikis           TIMESTAMPTZ,
    plaka           VARCHAR(20),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ziyaretci_site ON site_ziyaretci(site_id);
