CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- DOMAIN: KULLANICILAR & ADRESLER & KONUM (İl/İlçe/Semt)
-- ============================================================

-- Bölgeler lookup tablosu
CREATE TABLE regions (
    id          SMALLSERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- İller
CREATE TABLE provinces (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    plate_code      CHAR(2) NOT NULL,
    phone_code      VARCHAR(5) NOT NULL,
    region_id       SMALLINT REFERENCES regions(id),
    location        GEOGRAPHY(POINT, 4326),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_provinces_region ON provinces(region_id);
CREATE INDEX idx_provinces_plate ON provinces(plate_code);
CREATE INDEX idx_provinces_location ON provinces USING GIST(location);

-- İlçeler
CREATE TABLE districts (
    id              SERIAL PRIMARY KEY,
    province_id     SMALLINT NOT NULL REFERENCES provinces(id),
    name            VARCHAR(100) NOT NULL,
    location        GEOGRAPHY(POINT, 4326),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_districts_province ON districts(province_id);
CREATE INDEX idx_districts_location ON districts USING GIST(location);

-- Semtler/Mahalleler
CREATE TABLE neighborhoods (
    id              SERIAL PRIMARY KEY,
    district_id     INT NOT NULL REFERENCES districts(id),
    name            VARCHAR(100) NOT NULL,
    zip_code        VARCHAR(10),
    location        GEOGRAPHY(POINT, 4326),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_neighborhoods_district ON neighborhoods(district_id);
CREATE INDEX idx_neighborhoods_location ON neighborhoods USING GIST(location);

-- Kullanıcı roller
CREATE TYPE user_role AS ENUM ('customer', 'seller', 'courier', 'driver', 'expert', 'admin');

-- Kullanıcılar
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    phone           VARCHAR(20),
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(200) NOT NULL,
    role            user_role NOT NULL DEFAULT 'customer',
    is_active       BOOLEAN NOT NULL DEFAULT true,
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    avatar_url      TEXT,
    device_token    TEXT,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created ON users(created_at);

-- Kullanıcı adresleri
CREATE TABLE user_addresses (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(100) NOT NULL,
    full_address    TEXT NOT NULL,
    province_id     SMALLINT NOT NULL REFERENCES provinces(id),
    district_id     INT NOT NULL REFERENCES districts(id),
    neighborhood_id INT REFERENCES neighborhoods(id),
    postal_code     VARCHAR(10),
    latitude        NUMERIC(10,7),
    longitude       NUMERIC(10,7),
    location        GEOGRAPHY(POINT, 4326),
    is_default      BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_addresses_user ON user_addresses(user_id);
CREATE INDEX idx_addresses_location ON user_addresses USING GIST(location);

-- Kullanıcı oturum logları (partitionsız, ileride partition eklenebilir)
CREATE TABLE user_sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token   VARCHAR(500) NOT NULL,
    ip_address      INET,
    user_agent      TEXT,
    device_info     JSONB,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);
