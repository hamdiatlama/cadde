-- ============================================================
-- MIGRATION 000024: Çiçek Sistemi
-- ============================================================
-- Çiçekçi perakende + üretici + toptancı + malzeme tedarikçisi
-- Dört kademeli tedarik zinciri, özel gün takvimi, tazelik zinciri

-- 1. Çiçekçi (Perakende) Profili
CREATE TABLE IF NOT EXISTS florist_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER REFERENCES sellers(id),
    user_id INTEGER REFERENCES users(id),
    shop_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    cover_url VARCHAR(500),
    phone VARCHAR(20),
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    is_open BOOLEAN DEFAULT TRUE,
    preparation_time_min INTEGER DEFAULT 30,
    delivery_radius_km FLOAT DEFAULT 5.0,
    min_order_amount FLOAT DEFAULT 0,
    delivery_fee FLOAT DEFAULT 0,
    free_delivery_min_amount FLOAT,
    working_hours_json TEXT,
    holiday_dates TEXT,
    verification_status VARCHAR(20) DEFAULT 'pending',
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Çiçek Üreticisi (Çiftçi) Profili
CREATE TABLE IF NOT EXISTS flower_producer_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    company_name VARCHAR(255),
    production_type VARCHAR(50),
    capacity_per_month INTEGER,
    area_size FLOAT,
    area_unit VARCHAR(10) DEFAULT 'donum',
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    organic_certificate BOOLEAN DEFAULT FALSE,
    global_gap BOOLEAN DEFAULT FALSE,
    good_agriculture BOOLEAN DEFAULT FALSE,
    harvest_calendar_json TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    rating FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Toptancı Profili
CREATE TABLE IF NOT EXISTS flower_wholesaler_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    tax_id VARCHAR(50),
    warehouse_address TEXT,
    city VARCHAR(100),
    district VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    has_cold_storage BOOLEAN DEFAULT FALSE,
    min_order_amount FLOAT DEFAULT 0,
    shipping_type VARCHAR(50),
    working_region VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    rating FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Malzeme Tedarikçisi
CREATE TABLE IF NOT EXISTS material_supplier_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    supplier_type VARCHAR(50),
    product_list_json TEXT,
    min_order_amount FLOAT DEFAULT 0,
    shipping_conditions TEXT,
    city VARCHAR(100),
    district VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Çiçek Ürünleri
CREATE TABLE IF NOT EXISTS flower_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_type VARCHAR(20) NOT NULL,
    seller_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    description TEXT,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    occasion VARCHAR(50),
    price FLOAT NOT NULL,
    compare_price FLOAT,
    stock INTEGER DEFAULT 0,
    unit VARCHAR(20) DEFAULT 'adet',
    size VARCHAR(50),
    weight_kg FLOAT,
    color VARCHAR(50),
    colors_json TEXT,
    flowers_json TEXT,
    meaning TEXT,
    season VARCHAR(50),
    lifespan_days INTEGER,
    care_level VARCHAR(20),
    has_vase BOOLEAN DEFAULT FALSE,
    vase_type VARCHAR(50),
    is_express_eligible BOOLEAN DEFAULT FALSE,
    is_customizable BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    images_json TEXT,
    origin VARCHAR(100),
    fragrance VARCHAR(50),
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Özel Sipariş Tasarımı
CREATE TABLE IF NOT EXISTS custom_order_designs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER REFERENCES users(id),
    florist_id INTEGER REFERENCES florist_profiles(id),
    theme VARCHAR(50),
    size VARCHAR(20),
    flowers_json TEXT,
    extras_json TEXT,
    vase_type VARCHAR(50),
    card_message TEXT NOT NULL,
    card_design VARCHAR(50),
    card_type VARCHAR(20) DEFAULT 'dijital',
    total_price FLOAT,
    status VARCHAR(20) DEFAULT 'tasarim',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Özel Gün Hatırlatıcı
CREATE TABLE IF NOT EXISTS special_day_reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    reminder_date DATE NOT NULL,
    occasion_type VARCHAR(50),
    is_yearly BOOLEAN DEFAULT TRUE,
    previous_order_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Çiçekçi Zorunlu Görselleri
CREATE TABLE IF NOT EXISTS florist_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    florist_id INTEGER REFERENCES florist_profiles(id),
    category VARCHAR(30) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    resolution VARCHAR(20),
    taken_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    score_contribution INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Canlı Kamera
CREATE TABLE IF NOT EXISTS florist_cameras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    florist_id INTEGER REFERENCES florist_profiles(id),
    camera_name VARCHAR(255),
    resolution VARCHAR(20),
    stream_url VARCHAR(500),
    is_active BOOLEAN DEFAULT FALSE,
    last_interruption_at TIMESTAMP,
    working_hours_compliant BOOLEAN DEFAULT TRUE,
    score_contribution INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Tazelik Zinciri
CREATE TABLE IF NOT EXISTS freshness_chain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    stage VARCHAR(30) NOT NULL,
    happened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    photo_url VARCHAR(500),
    is_confirmed BOOLEAN DEFAULT FALSE
);

-- 11. Evrak Puanı
CREATE TABLE IF NOT EXISTS florist_document_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    florist_id INTEGER REFERENCES florist_profiles(id),
    document_type VARCHAR(50) NOT NULL,
    score INTEGER DEFAULT 0,
    file_path VARCHAR(500),
    valid_until DATE,
    is_confirmed BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Çiçek Puanlama (3 yönlü)
CREATE TABLE IF NOT EXISTS flower_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    rater_id INTEGER REFERENCES users(id),
    rater_type VARCHAR(20) NOT NULL,
    rated_id INTEGER NOT NULL,
    rated_type VARCHAR(20) NOT NULL,
    score FLOAT NOT NULL DEFAULT 5.0,
    criteria_json TEXT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Teslimat Süre Logu
CREATE TABLE IF NOT EXISTS delivery_time_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    estimated_minutes INTEGER,
    actual_minutes INTEGER,
    weather_condition VARCHAR(50),
    traffic_condition VARCHAR(50),
    deviation_percent FLOAT,
    improvement_suggestion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_florist_profiles_slug ON florist_profiles(slug);
CREATE INDEX IF NOT EXISTS idx_florist_profiles_city ON florist_profiles(city);
CREATE INDEX IF NOT EXISTS idx_florist_profiles_is_active ON florist_profiles(is_active);
CREATE INDEX IF NOT EXISTS idx_flower_products_category ON flower_products(category);
CREATE INDEX IF NOT EXISTS idx_flower_products_occasion ON flower_products(occasion);
CREATE INDEX IF NOT EXISTS idx_flower_products_seller ON flower_products(seller_type, seller_id);
CREATE INDEX IF NOT EXISTS idx_freshness_chain_order ON freshness_chain(order_id);
CREATE INDEX IF NOT EXISTS idx_special_day_reminders_user ON special_day_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_flower_ratings_order ON flower_ratings(order_id);
