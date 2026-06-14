-- ============================================================
-- DOMAIN: BINA — EK OZELLIKLER (Anket, Icra, Otopark, Rezervasyon, Toplanti, Banka, Isitma, Butce, Dosya, Bildirim)
-- ============================================================

-- Anket
CREATE TABLE site_anket (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik      VARCHAR(300) NOT NULL,
    aciklama    TEXT,
    baslangic   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    bitis       TIMESTAMPTZ,
    aktif       BOOLEAN DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_anket_site ON site_anket(site_id);

CREATE TABLE site_anket_secenek (
    id          SERIAL PRIMARY KEY,
    anket_id    INT NOT NULL REFERENCES site_anket(id) ON DELETE CASCADE,
    metin       VARCHAR(500) NOT NULL,
    oy_sayisi   INT DEFAULT 0
);
CREATE INDEX idx_anket_secenek ON site_anket_secenek(anket_id);

CREATE TABLE site_anket_oy (
    id          SERIAL PRIMARY KEY,
    anket_id    INT NOT NULL REFERENCES site_anket(id) ON DELETE CASCADE,
    secenek_id  INT NOT NULL REFERENCES site_anket_secenek(id) ON DELETE CASCADE,
    kisi_id     INT REFERENCES site_kisiler(id) ON DELETE SET NULL,
    daire_id    INT REFERENCES daireler(id) ON DELETE SET NULL,
    oy          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Icra / Haciz / Yasal Takip
CREATE TABLE site_icra (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    daire_id        INT NOT NULL REFERENCES daireler(id) ON DELETE CASCADE,
    blok_id         INT NOT NULL REFERENCES bloklar(id) ON DELETE CASCADE,
    daire_no        VARCHAR(20),
    kapi_no         INT,
    baslik          VARCHAR(300) NOT NULL,
    aciklama        TEXT,
    borc_turu       VARCHAR(50) DEFAULT 'aidat',
    tutar           NUMERIC(12,2) NOT NULL DEFAULT 0,
    tarih           DATE,
    durum           VARCHAR(30) DEFAULT 'basiyor',
    avukat          VARCHAR(100),
    masraf          NUMERIC(12,2) DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ
);
CREATE INDEX idx_icra_site ON site_icra(site_id);
CREATE INDEX idx_icra_daire ON site_icra(daire_id);

-- Otopark / Park Yeri
CREATE TABLE site_otopark (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    blok_id     INT REFERENCES bloklar(id) ON DELETE SET NULL,
    no          VARCHAR(20) NOT NULL,
    kat         VARCHAR(20),
    tip         VARCHAR(30) DEFAULT 'arac', -- arac, bisiklet, motosiklet
    daire_id    INT REFERENCES daireler(id) ON DELETE SET NULL,
    kisi_id     INT REFERENCES site_kisiler(id) ON DELETE SET NULL,
    arac_plaka  VARCHAR(20),
    kira_bedeli NUMERIC(10,2) DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_otopark_site ON site_otopark(site_id);

-- Rezervasyon (Saha, Havuz, Spor Salonu)
CREATE TABLE site_rezervasyon (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    alan        VARCHAR(100) NOT NULL, -- saha, havuz, spor_salonu, dugun_salonu
    kisi_id     INT REFERENCES site_kisiler(id) ON DELETE SET NULL,
    daire_id    INT REFERENCES daireler(id) ON DELETE SET NULL,
    baslangic   TIMESTAMPTZ NOT NULL,
    bitis       TIMESTAMPTZ NOT NULL,
    notlar      TEXT,
    durum       VARCHAR(20) DEFAULT 'onaylandi', -- onaylandi, iptal, bekliyor
    ucret       NUMERIC(10,2) DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_rezervasyon_site ON site_rezervasyon(site_id);

-- Toplanti / Yonetim Kurulu Kararlari
CREATE TABLE site_toplanti (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik      VARCHAR(300) NOT NULL,
    tarih       TIMESTAMPTZ NOT NULL,
    yer         VARCHAR(200),
    katilanlar  TEXT,
    gundem      TEXT,
    kararlar    TEXT,
    tutanak_url TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_toplanti_site ON site_toplanti(site_id);

-- Banka Hesaplari
CREATE TABLE site_banka (
    id              SERIAL PRIMARY KEY,
    site_id         INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    banka_adi       VARCHAR(100) NOT NULL,
    sube            VARCHAR(100),
    hesap_adi       VARCHAR(200),
    iban            VARCHAR(50) NOT NULL,
    hesap_no        VARCHAR(30),
    tur             VARCHAR(20) DEFAULT 'vadesiz', -- vadesiz, vadeli, pos
    bakiye          NUMERIC(12,2) DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_banka_site ON site_banka(site_id);

-- Isitma / Kalorifer / Merkezi Sistem
CREATE TABLE site_isitma (
    id            SERIAL PRIMARY KEY,
    site_id       INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    tur           VARCHAR(30) DEFAULT 'dogalgaz', -- dogalgaz, kalorifer, merkezi, kombi
    daire_id      INT REFERENCES daireler(id) ON DELETE SET NULL,
    blok_id       INT REFERENCES bloklar(id) ON DELETE SET NULL,
    yakilan_m3    NUMERIC(10,2) DEFAULT 0,
    birim_fiyat   NUMERIC(8,4) DEFAULT 0,
    tutar         NUMERIC(10,2) DEFAULT 0,
    ay            INT NOT NULL,
    yil           INT NOT NULL,
    odendi        BOOLEAN DEFAULT false,
    odeme_tarihi  TIMESTAMPTZ,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_isitma_site ON site_isitma(site_id);

-- Butce / Yillik Plan
CREATE TABLE site_butce (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    yil         INT NOT NULL,
    baslik      VARCHAR(300) NOT NULL,
    kategori    VARCHAR(50) DEFAULT 'gelir', -- gelir, gider
    tur         VARCHAR(50) DEFAULT 'aidat', -- aidat, elektrik, su, dogalgaz, bakim, temizlik, guvenlik, diger
    planlanan   NUMERIC(12,2) DEFAULT 0,
    gerceklesen NUMERIC(12,2) DEFAULT 0,
    aciklama    TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ
);
CREATE INDEX idx_butce_site ON site_butce(site_id);

-- Dosya / Evrak Yonetimi
CREATE TABLE site_dosya (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik      VARCHAR(300) NOT NULL,
    dosya_turu  VARCHAR(50), -- sozlesme, fatura, tutanak, karar, yonetmelik, diger
    dosya_url   TEXT,
    boyut       BIGINT DEFAULT 0,
    aciklama    TEXT,
    yukleyen    VARCHAR(100),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_dosya_site ON site_dosya(site_id);

-- Bildirim / Mobil Push + Email
CREATE TABLE site_bildirim (
    id          SERIAL PRIMARY KEY,
    site_id     INT NOT NULL REFERENCES siteler(id) ON DELETE CASCADE,
    baslik      VARCHAR(300) NOT NULL,
    icerik      TEXT,
    tur         VARCHAR(30) DEFAULT 'duyuru', -- duyuru, aidat_hatirlatma, odeme, etkinlik, uyari
    hedef       VARCHAR(30) DEFAULT 'herkes', -- herkes, blok, daire, kisi
    hedef_id    INT,
    gonderildi  BOOLEAN DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_bildirim_site ON site_bildirim(site_id);
