-- ============================================================
-- MIGRATION 000026: Kargo / Lojistik Sistemi
-- ============================================================
-- Firmalar kendi kendini kaydeder, API ile entegre olur.
-- E-ticaret, yemek ve diğer modüller gönderi oluşturabilir.

-- 1. Kargo Firması Profili
CREATE TABLE IF NOT EXISTS cargo_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    tax_id VARCHAR(50),
    tax_office VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(500),
    description TEXT,
    logo_url VARCHAR(500),
    cover_url VARCHAR(500),
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    -- Yetkilendirme / API
    api_key VARCHAR(64),
    api_webhook_url VARCHAR(500),
    api_allowed_ips TEXT,
    -- Profil durumu
    is_verified BOOLEAN DEFAULT FALSE,
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_doc_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    shipment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Kargo Şubeleri
CREATE TABLE IF NOT EXISTS cargo_branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    branch_name VARCHAR(255) NOT NULL,
    branch_code VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    address TEXT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    is_main_branch BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    working_hours TEXT,
    manager_name VARCHAR(255),
    capacity_daily INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Kuryeler
CREATE TABLE IF NOT EXISTS cargo_couriers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    branch_id INTEGER REFERENCES cargo_branches(id),
    user_id INTEGER REFERENCES users(id),
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    tc_kimlik VARCHAR(11),
    vehicle_type VARCHAR(50),
    vehicle_plate VARCHAR(20),
    license_no VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_available BOOLEAN DEFAULT TRUE,
    current_latitude FLOAT,
    current_longitude FLOAT,
    last_location_update TIMESTAMP,
    rating FLOAT DEFAULT 0,
    total_deliveries INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Kargo Gönderileri
CREATE TABLE IF NOT EXISTS cargo_shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    branch_id INTEGER REFERENCES cargo_branches(id),
    courier_id INTEGER REFERENCES cargo_couriers(id),
    -- Gönderici
    sender_name VARCHAR(255) NOT NULL,
    sender_phone VARCHAR(20),
    sender_email VARCHAR(255),
    sender_city VARCHAR(100),
    sender_district VARCHAR(100),
    sender_address TEXT,
    sender_latitude FLOAT,
    sender_longitude FLOAT,
    -- Alıcı
    recipient_name VARCHAR(255) NOT NULL,
    recipient_phone VARCHAR(20),
    recipient_email VARCHAR(255),
    recipient_city VARCHAR(100) NOT NULL,
    recipient_district VARCHAR(100),
    recipient_address TEXT NOT NULL,
    recipient_latitude FLOAT,
    recipient_longitude FLOAT,
    -- Kargo bilgileri
    tracking_no VARCHAR(50) UNIQUE NOT NULL,
    reference_no VARCHAR(100),
    barcode VARCHAR(100),
    weight_kg FLOAT,
    volume_dm3 FLOAT,
    piece_count INTEGER DEFAULT 1,
    package_type VARCHAR(50),
    description TEXT,
    -- Durum
    status VARCHAR(30) DEFAULT 'hazirlaniyor',
    is_express BOOLEAN DEFAULT FALSE,
    is_international BOOLEAN DEFAULT FALSE,
    -- Ücret
    total_price FLOAT,
    currency VARCHAR(10) DEFAULT 'TRY',
    is_paid BOOLEAN DEFAULT FALSE,
    payment_method VARCHAR(30),
    -- Entegrasyon (hangi modülden geldi)
    source_module VARCHAR(50),
    source_order_id INTEGER,
    -- QR Teslimat Kodu (alıcıya özel, kurye okutur)
    delivery_code VARCHAR(10),
    delivery_confirmed_by_recipient BOOLEAN DEFAULT FALSE,
    delivery_confirmed_at TIMESTAMP,
    delivery_note TEXT,
    delivery_photo_url VARCHAR(500),
    -- Ürün hassasiyeti
    is_fragile BOOLEAN DEFAULT FALSE,
    sensitivity_note VARCHAR(255),
    requires_signature BOOLEAN DEFAULT FALSE,
    -- Teslim Alma (kurye ürünü alırken onayı)
    pickup_confirmed_by_courier BOOLEAN DEFAULT FALSE,
    pickup_confirmed_at TIMESTAMP,
    pickup_photo_url VARCHAR(500),
    pickup_note TEXT,
    -- Teslimat başarısız / şubede bekleme
    delivery_attempt_count INTEGER DEFAULT 0,
    last_delivery_attempt_at TIMESTAMP,
    undelivered_reason VARCHAR(255),
    branch_wait_until TIMESTAMP,
    customer_extended_pickup BOOLEAN DEFAULT FALSE,
    customer_pickup_deadline TIMESTAMP,
    -- İade / Para iadesi
    refund_amount FLOAT,
    refund_delivery_cost FLOAT,
    refund_return_cost FLOAT,
    refund_net_amount FLOAT,
    refund_processed BOOLEAN DEFAULT FALSE,
    refund_processed_at TIMESTAMP,
    -- Zaman
    estimated_delivery_date TIMESTAMP,
    actual_delivery_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Kargo Takip Adımları
CREATE TABLE IF NOT EXISTS cargo_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER REFERENCES cargo_shipments(id) NOT NULL,
    status VARCHAR(30) NOT NULL,
    location_name VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    notes TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Fiyatlandırma Kademeleri
CREATE TABLE IF NOT EXISTS cargo_pricing_tiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    tier_name VARCHAR(100) NOT NULL,
    -- Ağırlık aralığı
    min_weight_kg FLOAT DEFAULT 0,
    max_weight_kg FLOAT,
    -- Boyut aralığı (desi)
    min_volume_dm3 FLOAT DEFAULT 0,
    max_volume_dm3 FLOAT,
    -- Bölge tipi (şehir içi, şehirler arası, bölgesel)
    zone_type VARCHAR(30),
    -- Fiyat
    base_price FLOAT NOT NULL,
    price_per_kg FLOAT DEFAULT 0,
    price_per_dm3 FLOAT DEFAULT 0,
    fuel_surcharge_percent FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Hizmet Bölgeleri
CREATE TABLE IF NOT EXISTS cargo_service_areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    branch_id INTEGER REFERENCES cargo_branches(id),
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    delivery_time_hours INTEGER,
    pickup_available BOOLEAN DEFAULT TRUE,
    daily_capacity INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Satıcı-Kargo Anlaşmaları (satıcı hangi firmayla çalışıyor)
CREATE TABLE IF NOT EXISTS cargo_seller_agreements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER REFERENCES sellers(id) NOT NULL,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    is_preferred BOOLEAN DEFAULT FALSE,
    contract_start VARCHAR,
    contract_end VARCHAR,
    negotiated_price_factor FLOAT DEFAULT 1.0,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(seller_id, company_id)
);

-- 9. Ürün-Kargo Ayarları (satıcı her ürün için hangi kargo firması, teslimat süresi vs.)
CREATE TABLE IF NOT EXISTS cargo_product_shipping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER REFERENCES sellers(id) NOT NULL,
    product_id INTEGER,
    company_id INTEGER REFERENCES cargo_companies(id) NOT NULL,
    -- Teslimat bilgileri
    estimated_delivery_hours INTEGER,
    max_delivery_days INTEGER,
    available_days VARCHAR(100),
    max_distance_km FLOAT,
    -- Ürün hassasiyeti
    sensitivity_level VARCHAR(20) DEFAULT 'normal',
    is_fragile BOOLEAN DEFAULT FALSE,
    requires_special_packaging BOOLEAN DEFAULT FALSE,
    packaging_instructions TEXT,
    -- Fiyat
    shipping_price FLOAT,
    free_shipping_min_amount FLOAT,
    is_free_shipping BOOLEAN DEFAULT FALSE,
    -- Durum
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(seller_id, product_id, company_id)
);

-- 10. Teslimat Memnuniyet Anketi
CREATE TABLE IF NOT EXISTS cargo_delivery_surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER REFERENCES cargo_shipments(id) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    -- Zamanında teslim
    delivered_on_time BOOLEAN,
    -- Ürün durumu
    package_condition VARCHAR(30),
    is_package_damaged BOOLEAN,
    is_package_opened BOOLEAN,
    -- Memnuniyet
    satisfaction_score INTEGER,
    courier_rating INTEGER,
    comment TEXT,
    -- Fotoğraf kanıtı
    photo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(shipment_id, user_id)
);

-- 11. Teslimat Sonrası İtiraz / İade (30 dk test süresi)
CREATE TABLE IF NOT EXISTS cargo_return_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER REFERENCES cargo_shipments(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    reason VARCHAR(255) NOT NULL,
    description TEXT,
    evidence_photos TEXT,
    evidence_videos TEXT,
    status VARCHAR(30) DEFAULT 'beklemede',
    is_within_window BOOLEAN,
    -- Kusur / Sorumluluk
    liability_party VARCHAR(20),
    liable_amount FLOAT,
    replacement_required BOOLEAN DEFAULT FALSE,
    replacement_shipped BOOLEAN DEFAULT FALSE,
    reviewed_by INTEGER REFERENCES users(id),
    review_notes TEXT,
    resolution VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Satıcı Askıya Alma Cezaları
CREATE TABLE IF NOT EXISTS cargo_seller_suspensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER REFERENCES sellers(id) NOT NULL,
    offense_count INTEGER NOT NULL,
    suspension_days INTEGER NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NOT NULL,
    reason TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cargo_companies_slug ON cargo_companies(slug);
CREATE INDEX IF NOT EXISTS idx_cargo_companies_user ON cargo_companies(user_id);
CREATE INDEX IF NOT EXISTS idx_cargo_companies_city ON cargo_companies(city);
CREATE INDEX IF NOT EXISTS idx_cargo_branches_company ON cargo_branches(company_id);
CREATE INDEX IF NOT EXISTS idx_cargo_branches_city ON cargo_branches(city);
CREATE INDEX IF NOT EXISTS idx_cargo_couriers_company ON cargo_couriers(company_id);
CREATE INDEX IF NOT EXISTS idx_cargo_couriers_branch ON cargo_couriers(branch_id);
CREATE INDEX IF NOT EXISTS idx_cargo_shipments_company ON cargo_shipments(company_id);
CREATE INDEX IF NOT EXISTS idx_cargo_shipments_tracking ON cargo_shipments(tracking_no);
CREATE INDEX IF NOT EXISTS idx_cargo_shipments_status ON cargo_shipments(status);
CREATE INDEX IF NOT EXISTS idx_cargo_shipments_recipient ON cargo_shipments(recipient_city);
CREATE INDEX IF NOT EXISTS idx_cargo_tracking_shipment ON cargo_tracking(shipment_id);
CREATE INDEX IF NOT EXISTS idx_cargo_tracking_status ON cargo_tracking(status);
CREATE INDEX IF NOT EXISTS idx_cargo_pricing_company ON cargo_pricing_tiers(company_id);
CREATE INDEX IF NOT EXISTS idx_cargo_service_areas_company ON cargo_service_areas(company_id);
CREATE INDEX IF NOT EXISTS idx_cargo_service_areas_city ON cargo_service_areas(city);
