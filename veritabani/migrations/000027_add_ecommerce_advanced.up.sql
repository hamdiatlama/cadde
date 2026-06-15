-- Migration 000027: E-Ticaret Gelişmiş Özellikler
-- Wishlist, Campaign, Escrow, Payout, Advertising, Comparison, Dispute

-- Wishlist
CREATE TABLE IF NOT EXISTS wishlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(255) DEFAULT 'Favorilerim',
    is_public BOOLEAN DEFAULT 0,
    share_code VARCHAR(32) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wishlist_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wishlist_id INTEGER NOT NULL REFERENCES wishlists(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(wishlist_id, product_id)
);

-- Campaign/Promosyon
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(30) NOT NULL,
    discount_type VARCHAR(20),
    discount_value FLOAT DEFAULT 0,
    min_order_amount FLOAT DEFAULT 0,
    max_discount_amount FLOAT,
    max_uses INTEGER,
    current_uses INTEGER DEFAULT 0,
    per_user_limit INTEGER DEFAULT 1,
    applicable_categories TEXT,
    applicable_products TEXT,
    applicable_sellers TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    banner_url VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaign_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_id INTEGER REFERENCES orders(id),
    discount_amount FLOAT DEFAULT 0,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS flash_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER REFERENCES campaigns(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    sale_price FLOAT NOT NULL,
    quantity_limit INTEGER DEFAULT 0,
    sold_count INTEGER DEFAULT 0,
    max_per_user INTEGER DEFAULT 1,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Escrow (Emanet Ödeme)
CREATE TABLE IF NOT EXISTS escrow_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    seller_id INTEGER NOT NULL REFERENCES sellers(id),
    amount FLOAT NOT NULL,
    platform_fee FLOAT DEFAULT 0,
    seller_amount FLOAT DEFAULT 0,
    status VARCHAR(30) DEFAULT 'held',
    release_trigger VARCHAR(50),
    release_at TIMESTAMP,
    released_at TIMESTAMP,
    released_by VARCHAR(50),
    dispute_id INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dispute / Uyuşmazlık
CREATE TABLE IF NOT EXISTS disputes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    raised_by INTEGER NOT NULL REFERENCES users(id),
    raised_against VARCHAR(20),
    reason VARCHAR(255) NOT NULL,
    description TEXT,
    evidence TEXT,
    status VARCHAR(30) DEFAULT 'open',
    resolution VARCHAR(255),
    resolved_by INTEGER REFERENCES users(id),
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payout (Satıcı Ödemeleri)
CREATE TABLE IF NOT EXISTS payout_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_no VARCHAR(50) UNIQUE NOT NULL,
    total_amount FLOAT DEFAULT 0,
    total_sellers INTEGER DEFAULT 0,
    status VARCHAR(30) DEFAULT 'pending',
    notes TEXT,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL REFERENCES sellers(id),
    batch_id INTEGER REFERENCES payout_batches(id),
    amount FLOAT NOT NULL,
    platform_fee FLOAT DEFAULT 0,
    net_amount FLOAT NOT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    payment_method VARCHAR(50),
    payment_ref VARCHAR(255),
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    paid_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Advertising / Reklam
CREATE TABLE IF NOT EXISTS ad_campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL REFERENCES sellers(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(30),
    daily_budget FLOAT DEFAULT 0,
    total_budget FLOAT DEFAULT 0,
    spent FLOAT DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ad_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL REFERENCES ad_campaigns(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    bid_amount FLOAT DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comparison (Karşılaştırma)
CREATE TABLE IF NOT EXISTS comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(255) DEFAULT 'Karşılaştırma',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comparison_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comparison_id INTEGER NOT NULL REFERENCES comparisons(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(comparison_id, product_id)
);
