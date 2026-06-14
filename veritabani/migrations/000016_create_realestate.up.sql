-- ============================================================
-- DOMAIN: EMLAK / GAYRİMENKUL (Real Estate)
-- ============================================================
-- İlan, yetkilendirme, ekspertiz, müteahhit, değerlendirme

-- İlan kategorileri (satilik, kiralik, gunluk_kiralik, devren)
CREATE TABLE property_categories (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(50) NOT NULL,
    slug            VARCHAR(50) UNIQUE NOT NULL,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- İlan tipleri (daire, villa, mustakil_ev, arsa, tarla, ofis, dukkan, depo, bina, devremulk)
CREATE TABLE property_types (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    icon            VARCHAR(50),
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Müteahhit / İnşaat Firmaları
CREATE TABLE contractor_companies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    tax_no          VARCHAR(20),
    tax_office      VARCHAR(100),
    phone           VARCHAR(20),
    email           VARCHAR(100),
    address         TEXT,
    website         VARCHAR(200),
    logo_url        TEXT,
    description     TEXT,
    rating          NUMERIC(2,1) DEFAULT 0,
    review_count    INT NOT NULL DEFAULT 0,
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    location        GEOGRAPHY(POINT, 4326),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contractor_name ON contractor_companies(name);
CREATE INDEX idx_contractor_rating ON contractor_companies(rating DESC);

-- Müteahhit firma değerlendirmeleri
CREATE TABLE contractor_reviews (
    id              BIGSERIAL PRIMARY KEY,
    company_id      INT NOT NULL REFERENCES contractor_companies(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating          SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (company_id, user_id)
);

CREATE INDEX idx_contractor_review_company ON contractor_reviews(company_id);

-- İlanlar (ana tablo)
CREATE TABLE property_listings (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id     SMALLINT NOT NULL REFERENCES property_categories(id),
    type_id         SMALLINT NOT NULL REFERENCES property_types(id),
    contractor_id   INT REFERENCES contractor_companies(id),
    title           VARCHAR(300) NOT NULL,
    description     TEXT,
    price           NUMERIC(14,2) NOT NULL,
    currency        VARCHAR(5) NOT NULL DEFAULT 'TRY',
    is_for_sale     BOOLEAN NOT NULL DEFAULT false,
    is_for_rent     BOOLEAN NOT NULL DEFAULT false,
    rent_deposit    NUMERIC(10,2),
    dues            NUMERIC(8,2), -- aidat

    -- Konum
    location        GEOGRAPHY(POINT, 4326),
    country         VARCHAR(100) DEFAULT 'Türkiye',
    city            VARCHAR(100) NOT NULL,
    district        VARCHAR(100) NOT NULL,
    neighborhood    VARCHAR(100),
    address         TEXT,
    map_address     VARCHAR(500),

    -- Bina bilgileri
    building_name   VARCHAR(200),
    block           VARCHAR(50),
    floor           VARCHAR(50),
    door_number     VARCHAR(20),
    construction_year SMALLINT,
    building_age    SMALLINT,
    floor_count     SMALLINT,
    total_apartments SMALLINT,
    contractor_name_history VARCHAR(200),

    -- Arsa bilgileri
    land_area       NUMERIC(10,2), -- m2
    building_area   NUMERIC(10,2), -- m2
    zoning_status   VARCHAR(50), -- imarli, imarsiz, iskanli
    land_use_type   VARCHAR(100), -- konut, ticari, konut+ticari, sanayi, tarim
    density_value   VARCHAR(50), -- E:0.20, KAKS gibi
    parcel_no       VARCHAR(50),
    island_no       VARCHAR(50),

    -- Daire özellikleri
    room_count      VARCHAR(20), -- 2+1, 3+1, 4+1
    bathroom_count  SMALLINT,
    net_area        NUMERIC(8,2), -- m2
    gross_area      NUMERIC(8,2), -- m2
    heating_type    VARCHAR(50), -- dogalgaz, merkezi, soba, klimali, yerden_isitma
    furnishing      VARCHAR(50), -- esyali, esyasiz, yari_esyali
    facade         VARCHAR(50), -- on_cephe, arka_cephe, kose_daire, ara_kat, cati_kat
    balcony_count   SMALLINT DEFAULT 0,

    -- Durum
    status          VARCHAR(20) NOT NULL DEFAULT 'active', -- active, pending, sold, rented, inactive, deleted
    view_count      INT NOT NULL DEFAULT 0,
    is_highlighted  BOOLEAN NOT NULL DEFAULT false,
    valid_from     DATE,
    valid_until    DATE,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_listings_user ON property_listings(user_id);
CREATE INDEX idx_listings_category ON property_listings(category_id);
CREATE INDEX idx_listings_type ON property_listings(type_id);
CREATE INDEX idx_listings_status ON property_listings(status);
CREATE INDEX idx_listings_city ON property_listings(city);
CREATE INDEX idx_listings_district ON property_listings(district);
CREATE INDEX idx_listings_price ON property_listings(price);
CREATE INDEX idx_listings_location ON property_listings USING GIST(location);
CREATE INDEX idx_listings_created ON property_listings(created_at DESC);

-- İlan fotoğrafları (kategorili)
CREATE TABLE property_photos (
    id              BIGSERIAL PRIMARY KEY,
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    file_path       TEXT NOT NULL,
    category        VARCHAR(50) NOT NULL DEFAULT 'genel',
    description     TEXT,
    is_cover        BOOLEAN NOT NULL DEFAULT false,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_property_photo_listing ON property_photos(listing_id);

-- İlan özellik etiketleri
CREATE TABLE property_features (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    icon            VARCHAR(50),
    category        VARCHAR(50), -- bina, konum, oda, tesisat, manzara, guvenlik
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- İlan-özellik ilişkisi
CREATE TABLE property_listing_features (
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    feature_id      INT NOT NULL REFERENCES property_features(id) ON DELETE CASCADE,
    value           VARCHAR(200), -- opsiyonel değer (örn: havuz tipi)
    PRIMARY KEY (listing_id, feature_id)
);

-- Yetkilendirme (mülk sahibi -> emlak ofisi)
CREATE TABLE authorization_requests (
    id              BIGSERIAL PRIMARY KEY,
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    owner_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id      INT NOT NULL REFERENCES contractor_companies(id) ON DELETE CASCADE,
    auth_type       VARCHAR(20) NOT NULL DEFAULT 'sell', -- sell, rent, manage, all
    commission_rate NUMERIC(5,2), -- yüzde
    commission_fixed NUMERIC(10,2), -- sabit ücret
    valid_from      DATE NOT NULL,
    valid_until     DATE,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, approved, rejected, expired, cancelled
    owner_note      TEXT,
    company_note    TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_auth_listing ON authorization_requests(listing_id);
CREATE INDEX idx_auth_owner ON authorization_requests(owner_id);
CREATE INDEX idx_auth_company ON authorization_requests(company_id);

-- Gayrimenkul ekspertiz / değerleme talebi
CREATE TABLE property_appraisal_requests (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    listing_id      BIGINT REFERENCES property_listings(id) ON DELETE SET NULL,
    company_id      INT REFERENCES contractor_companies(id),
    expert_id       INT REFERENCES experts(id),

    -- Adres bilgisi (listing yoksa girilir)
    city            VARCHAR(100),
    district        VARCHAR(100),
    neighborhood    VARCHAR(100),
    address         TEXT,
    location        GEOGRAPHY(POINT, 4326),

    -- Mülk bilgisi
    property_type_id SMALLINT REFERENCES property_types(id),
    land_area       NUMERIC(10,2),
    building_area   NUMERIC(10,2),
    room_count      VARCHAR(20),
    construction_year SMALLINT,

    -- Talep durumu
    status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, assigned, in_progress, completed, cancelled
    notes           TEXT,
    report_data     JSONB, -- ekspertiz raporu verisi
    report_file_url TEXT,
    requested_date  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_date  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_appraisal_user ON property_appraisal_requests(user_id);
CREATE INDEX idx_appraisal_listing ON property_appraisal_requests(listing_id);
CREATE INDEX idx_appraisal_status ON property_appraisal_requests(status);

-- Favori ilanlar
CREATE TABLE favorite_listings (
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, listing_id)
);

CREATE INDEX idx_fav_listing ON favorite_listings(listing_id);

-- İlan mesaj/soru
CREATE TABLE property_inquiries (
    id              BIGSERIAL PRIMARY KEY,
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    from_user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    to_user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message         TEXT NOT NULL,
    parent_id       BIGINT REFERENCES property_inquiries(id),
    is_read         BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_inquiry_listing ON property_inquiries(listing_id);
CREATE INDEX idx_inquiry_from ON property_inquiries(from_user_id);
CREATE INDEX idx_inquiry_to ON property_inquiries(to_user_id);
