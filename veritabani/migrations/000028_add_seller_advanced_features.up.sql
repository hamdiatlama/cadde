-- Migration 000028: Satıcı gelişmiş özellikleri (varyasyon, sohbet, B2B, vergi, depo, terk edilmiş sepet, performans)

-- 1. Varyasyon/SKU Yönetimi
CREATE TABLE IF NOT EXISTS product_variant_groups (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    name VARCHAR(100) NOT NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS product_variant_options (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES product_variant_groups(id),
    value VARCHAR(100) NOT NULL,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS product_variant_skus (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    sku VARCHAR(100) UNIQUE NOT NULL,
    barcode VARCHAR(100),
    price_override DOUBLE PRECISION,
    compare_price_override DOUBLE PRECISION,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS product_variant_mappings (
    id SERIAL PRIMARY KEY,
    sku_id INTEGER NOT NULL REFERENCES product_variant_skus(id),
    option_id INTEGER NOT NULL REFERENCES product_variant_options(id)
);

-- 2. Sohbet / Mesajlaşma
DO $$ BEGIN
    CREATE TYPE chat_status AS ENUM ('open', 'closed');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(50) PRIMARY KEY,
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    order_id INTEGER,
    status chat_status DEFAULT 'open',
    last_message_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(50) NOT NULL REFERENCES conversations(id),
    sender_id INTEGER NOT NULL REFERENCES users(id),
    receiver_id INTEGER NOT NULL REFERENCES users(id),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. B2B / Toptan Satış
CREATE TABLE IF NOT EXISTS b2b_price_tiers (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    min_qty INTEGER NOT NULL,
    max_qty INTEGER,
    unit_price DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS b2b_customers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    company_name VARCHAR(200),
    tax_office VARCHAR(100),
    tax_number VARCHAR(50),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS b2b_quotes (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES b2b_customers(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DOUBLE PRECISION,
    notes VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS b2b_quote_items (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER NOT NULL REFERENCES b2b_quotes(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DOUBLE PRECISION NOT NULL
);

-- 4. Vergi / e-Fatura
DO $$ BEGIN
    CREATE TYPE tax_type AS ENUM ('kdv', 'stopaj', 'gelir_vergisi');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS tax_rates (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES product_categories(id),
    tax_type tax_type DEFAULT 'kdv',
    rate DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    invoice_no VARCHAR(50) UNIQUE NOT NULL,
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    subtotal DOUBLE PRECISION NOT NULL,
    tax_total DOUBLE PRECISION NOT NULL,
    grand_total DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    pdf_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Depo / Envanter
CREATE TABLE IF NOT EXISTS warehouses (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    address VARCHAR(500),
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Türkiye',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS warehouse_stock (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    sku_id INTEGER REFERENCES product_variant_skus(id),
    quantity INTEGER DEFAULT 0,
    min_threshold INTEGER DEFAULT 5,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS warehouse_transfers (
    id SERIAL PRIMARY KEY,
    from_warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    to_warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 6. Terk Edilmiş Sepet
CREATE TABLE IF NOT EXISTS abandoned_carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    cart_data TEXT,
    total INTEGER DEFAULT 0,
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_count INTEGER DEFAULT 0,
    recovered BOOLEAN DEFAULT FALSE,
    recovered_order_id INTEGER REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_reminder_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS cart_reminder_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    subject VARCHAR(200),
    body TEXT,
    delay_hours INTEGER DEFAULT 24,
    is_active BOOLEAN DEFAULT TRUE
);

-- 7. Satıcı Performans Puanı + Rozetler
CREATE TABLE IF NOT EXISTS seller_ratings (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    order_id INTEGER NOT NULL REFERENCES orders(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS seller_badges (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    badge_type VARCHAR(50) NOT NULL,
    awarded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS seller_performance_metrics (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    period VARCHAR(10) NOT NULL,
    total_orders INTEGER DEFAULT 0,
    completed_orders INTEGER DEFAULT 0,
    cancelled_orders INTEGER DEFAULT 0,
    late_shipments INTEGER DEFAULT 0,
    avg_rating DOUBLE PRECISION DEFAULT 0,
    return_rate DOUBLE PRECISION DEFAULT 0,
    on_time_rate DOUBLE PRECISION DEFAULT 100,
    calculated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_variant_sku_product ON product_variant_skus(product_id);
CREATE INDEX IF NOT EXISTS idx_variant_mapping_sku ON product_variant_mappings(sku_id);
CREATE INDEX IF NOT EXISTS idx_variant_mapping_option ON product_variant_mappings(option_id);
CREATE INDEX IF NOT EXISTS idx_chat_conversation_participants ON conversations(buyer_id, seller_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_conv ON chat_messages(conversation_id, created_at);
CREATE INDEX IF NOT EXISTS idx_chat_unread ON chat_messages(receiver_id, is_read);
CREATE INDEX IF NOT EXISTS idx_b2b_tier_product ON b2b_price_tiers(product_id, min_qty);
CREATE INDEX IF NOT EXISTS idx_warehouse_stock_lookup ON warehouse_stock(warehouse_id, product_id, sku_id);
CREATE INDEX IF NOT EXISTS idx_abandoned_user ON abandoned_carts(user_id, recovered);
CREATE INDEX IF NOT EXISTS idx_seller_rating ON seller_ratings(seller_id, rating);
CREATE INDEX IF NOT EXISTS idx_seller_badge ON seller_badges(seller_id, badge_type);
CREATE INDEX IF NOT EXISTS idx_seller_metrics ON seller_performance_metrics(seller_id, period);
