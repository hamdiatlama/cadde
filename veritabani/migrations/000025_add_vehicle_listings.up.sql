-- ============================================================
-- MIGRATION 000025: Araç İlan Sistemi (Oto Galeri)
-- ============================================================
-- Mevcut araç kataloğu üzerine ilan/pazarlama katmanı.
-- Ödeme, doküman, şirket yönetimi tabloları ortak (domain='vehicle')

-- 1. Araç İlanları (ana tablo)
CREATE TABLE IF NOT EXISTS vehicle_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER REFERENCES sellers(id),
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    -- Araç bilgileri
    brand_id INTEGER REFERENCES vehicle_brands(id),
    model_id INTEGER REFERENCES vehicle_models(id),
    year INTEGER NOT NULL,
    body_type_id INTEGER REFERENCES body_types(id),
    segment_code VARCHAR(10),
    mileage INTEGER,
    mileage_unit VARCHAR(10) DEFAULT 'km',
    fuel_type VARCHAR(30),
    transmission VARCHAR(30),
    engine_displacement_cc INTEGER,
    engine_power_hp INTEGER,
    color VARCHAR(50),
    interior_color VARCHAR(50),
    condition VARCHAR(20) DEFAULT 'ikinci_el',
    warranty_months INTEGER,
    -- Konum
    city VARCHAR(100),
    district VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    -- Fiyat
    price FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'TRY',
    is_negotiable BOOLEAN DEFAULT TRUE,
    -- Durum
    status VARCHAR(20) DEFAULT 'draft',
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    view_count INTEGER DEFAULT 0,
    -- Zaman
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sold_at TIMESTAMP
);

-- 2. Araç Fotoğrafları
CREATE TABLE IF NOT EXISTS vehicle_listing_photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER REFERENCES vehicle_listings(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    sort_order INTEGER DEFAULT 0,
    is_cover BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Oto Galeri Şirket Profili
CREATE TABLE IF NOT EXISTS vehicle_gallery_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    tax_id VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(255),
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    description TEXT,
    logo_url VARCHAR(500),
    cover_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_status VARCHAR(20) DEFAULT 'pending',
    certificate_no VARCHAR(100),
    certificate_expiry DATE,
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Favori İlanlar
CREATE TABLE IF NOT EXISTS vehicle_favorite_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    listing_id INTEGER REFERENCES vehicle_listings(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, listing_id)
);

-- 5. Araç İlan Sorgulamaları
CREATE TABLE IF NOT EXISTS vehicle_inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER REFERENCES vehicle_listings(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_vehicle_listings_status ON vehicle_listings(status);
CREATE INDEX IF NOT EXISTS idx_vehicle_listings_brand ON vehicle_listings(brand_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_listings_city ON vehicle_listings(city);
CREATE INDEX IF NOT EXISTS idx_vehicle_listings_price ON vehicle_listings(price);
CREATE INDEX IF NOT EXISTS idx_vehicle_listings_user ON vehicle_listings(user_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_listing_photos_listing ON vehicle_listing_photos(listing_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_gallery_slug ON vehicle_gallery_companies(slug);
CREATE INDEX IF NOT EXISTS idx_vehicle_favorites_user ON vehicle_favorite_listings(user_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_inquiries_listing ON vehicle_inquiries(listing_id);
