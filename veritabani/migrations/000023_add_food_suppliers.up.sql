-- ============================================================
-- MIGRATION 000023: Yemek Tedarikçi/Ürün İzlenebilirlik Sistemi
-- ============================================================
-- Restoranların kullandıkları ürünlerin tedarikçilerini
-- sisteme ekleyerek şeffaflık puanı kazanmalarını sağlar.

-- 1. Tedarikçiler (Üreticiler)
CREATE TABLE IF NOT EXISTS food_suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    seller_id INTEGER REFERENCES sellers(id),
    company_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    cover_url VARCHAR(500),
    supplier_type VARCHAR(20) NOT NULL DEFAULT 'producer',
    city VARCHAR(100),
    district VARCHAR(100),
    address TEXT,
    latitude REAL,
    longitude REAL,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(255),
    website_url VARCHAR(500),
    is_organic_certified INTEGER DEFAULT 0,
    is_halal_certified INTEGER DEFAULT 0,
    certifications TEXT,
    product_categories TEXT,
    kitchen_photos TEXT,
    rating REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    verification_status VARCHAR(20) DEFAULT 'pending',
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 2. Tedarikçi Ürünleri
CREATE TABLE IF NOT EXISTS food_supplier_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL REFERENCES food_suppliers(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    unit VARCHAR(50) NOT NULL DEFAULT 'kg',
    price_per_unit REAL,
    is_organic INTEGER DEFAULT 0,
    is_local INTEGER DEFAULT 0,
    season_start_month INTEGER,
    season_end_month INTEGER,
    image_url VARCHAR(500),
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_supplier_products_supplier ON food_supplier_products(supplier_id);
CREATE INDEX IF NOT EXISTS idx_supplier_products_category ON food_supplier_products(category);

-- 3. Restoran-Tedarikçi İlişkisi
CREATE TABLE IF NOT EXISTS food_restaurant_suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    supplier_id INTEGER NOT NULL REFERENCES food_suppliers(id),
    is_preferred INTEGER DEFAULT 0,
    contract_start TEXT,
    contract_end TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(restaurant_id, supplier_id)
);
CREATE INDEX IF NOT EXISTS idx_rest_suppliers_rest ON food_restaurant_suppliers(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_rest_suppliers_supp ON food_restaurant_suppliers(supplier_id);

-- 4. Menü Öğesi - İçerik Bağlantısı (İzlenebilirlik)
CREATE TABLE IF NOT EXISTS food_menu_item_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_item_id INTEGER NOT NULL REFERENCES food_menu_items(id),
    supplier_product_id INTEGER NOT NULL REFERENCES food_supplier_products(id),
    quantity REAL,
    unit VARCHAR(50),
    notes TEXT,
    is_visible_to_customer INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(menu_item_id, supplier_product_id)
);
CREATE INDEX IF NOT EXISTS idx_menu_ingredients_item ON food_menu_item_ingredients(menu_item_id);
CREATE INDEX IF NOT EXISTS idx_menu_ingredients_product ON food_menu_item_ingredients(supplier_product_id);

-- 5. Şeffaflık Puanları
CREATE TABLE IF NOT EXISTS food_transparency_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL UNIQUE REFERENCES restaurants(id),
    total_menu_items INTEGER DEFAULT 0,
    items_with_ingredients INTEGER DEFAULT 0,
    total_suppliers_linked INTEGER DEFAULT 0,
    transparency_percentage REAL DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    last_calculated_at TEXT DEFAULT (datetime('now')),
    created_at TEXT DEFAULT (datetime('now'))
);
