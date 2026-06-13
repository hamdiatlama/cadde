-- ============================================================
-- DOMAIN: ARAÇ KATALOĞU (Vehicle Catalog)
-- ============================================================
-- Vasıta modülündeki 23 araç kategorisini kapsar

-- Araç ana kategorileri
CREATE TABLE vehicle_categories (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    parent_id       SMALLINT REFERENCES vehicle_categories(id),
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Segment kodları (A, B, C, D, E, F, J, S, M, P, V)
CREATE TABLE vehicle_segments (
    code            CHAR(1) PRIMARY KEY,
    name            VARCHAR(50) NOT NULL,
    description     VARCHAR(200),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Kasa tipleri
CREATE TABLE body_types (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Markalar
CREATE TABLE vehicle_brands (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    country         VARCHAR(100),
    logo_url        TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_vbrands_name ON vehicle_brands(name);

-- Modeller
CREATE TABLE vehicle_models (
    id              SERIAL PRIMARY KEY,
    brand_id        INT NOT NULL REFERENCES vehicle_brands(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    segment_code    CHAR(1) REFERENCES vehicle_segments(code),
    production_start SMALLINT,
    production_end  SMALLINT,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_vmodels_brand ON vehicle_models(brand_id);
CREATE INDEX idx_vmodels_name ON vehicle_models(name);
CREATE INDEX idx_vmodels_segment ON vehicle_models(segment_code);

-- Model-kasa tipi ilişkisi
CREATE TABLE vehicle_model_body_types (
    model_id        INT NOT NULL REFERENCES vehicle_models(id) ON DELETE CASCADE,
    body_type_id    SMALLINT NOT NULL REFERENCES body_types(id) ON DELETE CASCADE,
    PRIMARY KEY (model_id, body_type_id)
);

-- Araç kategori-model ilişkisi (bir model birden çok kategoride olabilir)
CREATE TABLE vehicle_category_models (
    category_id     SMALLINT NOT NULL REFERENCES vehicle_categories(id) ON DELETE CASCADE,
    model_id        INT NOT NULL REFERENCES vehicle_models(id) ON DELETE CASCADE,
    PRIMARY KEY (category_id, model_id)
);

-- Yıl bazlı model varyantları
CREATE TABLE vehicle_model_years (
    id              SERIAL PRIMARY KEY,
    model_id        INT NOT NULL REFERENCES vehicle_models(id) ON DELETE CASCADE,
    year            SMALLINT NOT NULL,
    trim_name       VARCHAR(200),
    engine_volume   NUMERIC(4,1),
    horsepower      SMALLINT,
    fuel_type       VARCHAR(50),
    transmission    VARCHAR(50),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (model_id, year, trim_name)
);

CREATE INDEX idx_vmodelyears_model ON vehicle_model_years(model_id);
CREATE INDEX idx_vmodelyears_year ON vehicle_model_years(year);

-- Özellik grupları (örn: Güvenlik, Konfor, Multimedya)
CREATE TABLE feature_groups (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Özellikler/Donanımlar
CREATE TABLE features (
    id              SERIAL PRIMARY KEY,
    group_id        SMALLINT NOT NULL REFERENCES feature_groups(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Model-özellik ilişkisi
CREATE TABLE vehicle_model_features (
    model_id        INT NOT NULL REFERENCES vehicle_models(id) ON DELETE CASCADE,
    feature_id      INT NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    is_standard     BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (model_id, feature_id)
);
