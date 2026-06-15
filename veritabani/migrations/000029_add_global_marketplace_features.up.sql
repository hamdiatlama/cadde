-- Migration 000029: Global marketplace features (multi-seller, auction, payment, marketing, fulfillment, etc.)

-- 1. Multi-Seller + Buy Box
CREATE TABLE IF NOT EXISTS seller_offers (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    price DOUBLE PRECISION NOT NULL,
    stock INTEGER DEFAULT 0,
    is_winning BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Auction
CREATE TABLE IF NOT EXISTS auctions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    start_price DOUBLE PRECISION NOT NULL,
    current_bid DOUBLE PRECISION,
    bidder_id INTEGER REFERENCES users(id),
    start_time TIMESTAMPTZ DEFAULT NOW(),
    end_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    winner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auction_bids (
    id SERIAL PRIMARY KEY,
    auction_id INTEGER NOT NULL REFERENCES auctions(id),
    bidder_id INTEGER NOT NULL REFERENCES users(id),
    amount DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Gift Card
CREATE TABLE IF NOT EXISTS gift_cards (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    balance DOUBLE PRECISION NOT NULL,
    currency VARCHAR(10) DEFAULT 'TRY',
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    recipient_email VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gift_card_transactions (
    id SERIAL PRIMARY KEY,
    gift_card_id INTEGER NOT NULL REFERENCES gift_cards(id),
    amount DOUBLE PRECISION NOT NULL,
    order_id INTEGER REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Payment Extended (COD, BNPL, Crypto, Wallet)
DO $$ BEGIN
    CREATE TYPE payment_method_type AS ENUM ('card', 'cod', 'bnpl', 'crypto', 'installment', 'wallet');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS cod_orders (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    status VARCHAR(20) DEFAULT 'pending',
    collected_amount DOUBLE PRECISION,
    collected_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bnpl_installments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    total_amount DOUBLE PRECISION NOT NULL,
    installment_count INTEGER NOT NULL,
    installment_amount DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    next_payment_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crypto_payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    currency VARCHAR(10) NOT NULL,
    wallet_address VARCHAR(200),
    amount DOUBLE PRECISION NOT NULL,
    tx_hash VARCHAR(200),
    status VARCHAR(20) DEFAULT 'pending',
    confirmations INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    balance DOUBLE PRECISION DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wallet_transactions (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER NOT NULL REFERENCES wallets(id),
    amount DOUBLE PRECISION NOT NULL,
    type VARCHAR(20) NOT NULL,
    reference_id INTEGER,
    reference_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Commission
CREATE TABLE IF NOT EXISTS commission_rules (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES product_categories(id),
    seller_id INTEGER REFERENCES users(id),
    rate DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS commission_transactions (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    amount DOUBLE PRECISION NOT NULL,
    rate DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Loyalty
CREATE TABLE IF NOT EXISTS loyalty_tiers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    min_spend DOUBLE PRECISION DEFAULT 0,
    discount_rate DOUBLE PRECISION DEFAULT 0,
    free_shipping BOOLEAN DEFAULT FALSE,
    badge_color VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS user_loyalty (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    points INTEGER DEFAULT 0,
    total_spend DOUBLE PRECISION DEFAULT 0,
    tier_id INTEGER REFERENCES loyalty_tiers(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS loyalty_point_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    points INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    reference_type VARCHAR(50),
    reference_id INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Marketing (Email, SMS, Affiliate, Blog, Segment)
CREATE TABLE IF NOT EXISTS email_campaigns (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200),
    subject VARCHAR(200),
    body TEXT,
    audience_segment VARCHAR(100),
    sent_count INTEGER DEFAULT 0,
    open_count INTEGER DEFAULT 0,
    click_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',
    scheduled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sms_campaigns (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    message TEXT NOT NULL,
    audience_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    referral_code VARCHAR(50) UNIQUE NOT NULL,
    commission_rate DOUBLE PRECISION DEFAULT 5.0,
    total_earnings DOUBLE PRECISION DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id SERIAL PRIMARY KEY,
    affiliate_id INTEGER NOT NULL REFERENCES affiliates(id),
    clicked_by INTEGER REFERENCES users(id),
    ip_address VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_sales (
    id SERIAL PRIMARY KEY,
    affiliate_id INTEGER NOT NULL REFERENCES affiliates(id),
    order_id INTEGER NOT NULL REFERENCES orders(id),
    commission DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES users(id),
    author_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    content TEXT,
    excerpt VARCHAR(500),
    image_url VARCHAR(500),
    tags VARCHAR(500),
    is_published BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customer_segments (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    criteria TEXT,
    member_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Fulfillment
CREATE TABLE IF NOT EXISTS fulfillment_centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(500),
    city VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fulfillment_requests (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    center_id INTEGER REFERENCES fulfillment_centers(id),
    status VARCHAR(20) DEFAULT 'pending',
    tracking_no VARCHAR(100),
    shipped_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Delivery Extended (Slots, Express, Pickup, International)
CREATE TABLE IF NOT EXISTS delivery_slots (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    date VARCHAR(10) NOT NULL,
    start_time VARCHAR(5) NOT NULL,
    end_time VARCHAR(5) NOT NULL,
    max_orders INTEGER DEFAULT 10,
    current_orders INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS express_deliveries (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    courier_id INTEGER REFERENCES users(id),
    estimated_minutes INTEGER,
    fee DOUBLE PRECISION,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pickup_points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    address VARCHAR(500),
    city VARCHAR(100),
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS international_shipments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    origin_country VARCHAR(2) NOT NULL,
    destination_country VARCHAR(2) NOT NULL,
    customs_value DOUBLE PRECISION,
    customs_tax DOUBLE PRECISION,
    shipping_cost DOUBLE PRECISION,
    tracking_no VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Subscribe & Save
CREATE TABLE IF NOT EXISTS subscription_save_plans (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    interval_days INTEGER NOT NULL,
    discount_rate DOUBLE PRECISION DEFAULT 5,
    max_orders INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscription_save_orders (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER NOT NULL REFERENCES subscription_save_plans(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    next_order_date TIMESTAMPTZ,
    total_orders INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Recommendation / Tracking
CREATE TABLE IF NOT EXISTS product_views (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    session_id VARCHAR(100),
    viewed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query VARCHAR(200) NOT NULL,
    session_id VARCHAR(100),
    searched_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. Live Shopping
CREATE TABLE IF NOT EXISTS live_streams (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200),
    stream_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'scheduled',
    viewer_count INTEGER DEFAULT 0,
    scheduled_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS live_stream_products (
    id SERIAL PRIMARY KEY,
    stream_id INTEGER NOT NULL REFERENCES live_streams(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    discount_rate DOUBLE PRECISION DEFAULT 0,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS live_stream_orders (
    id SERIAL PRIMARY KEY,
    stream_id INTEGER NOT NULL REFERENCES live_streams(id),
    order_id INTEGER NOT NULL REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. Return Management
CREATE TABLE IF NOT EXISTS return_requests (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    reason VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending',
    refund_amount DOUBLE PRECISION,
    refund_method VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- 14. Trade-In / Refurbished
CREATE TABLE IF NOT EXISTS trade_in_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_to_trade VARCHAR(200),
    estimated_value DOUBLE PRECISION,
    condition VARCHAR(50),
    target_product_id INTEGER REFERENCES products(id),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS refurbished_products (
    id SERIAL PRIMARY KEY,
    original_product_id INTEGER REFERENCES products(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    condition_grade VARCHAR(20),
    price DOUBLE PRECISION NOT NULL,
    stock INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 15. Handmade / Custom Orders
CREATE TABLE IF NOT EXISTS custom_orders (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    description VARCHAR(1000),
    requirements VARCHAR(2000),
    status VARCHAR(20) DEFAULT 'pending',
    price DOUBLE PRECISION,
    estimated_days INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 16. Brand Registry
CREATE TABLE IF NOT EXISTS brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    trademark_no VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    logo_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 17. Dropshipping
CREATE TABLE IF NOT EXISTS dropshipping_suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    api_url VARCHAR(500),
    api_key VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dropshipping_products (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES dropshipping_suppliers(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    supplier_sku VARCHAR(100),
    cost_price DOUBLE PRECISION,
    is_active BOOLEAN DEFAULT TRUE
);

-- 18. Product Verification
CREATE TABLE IF NOT EXISTS product_verifications (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    verifier_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    verified_at TIMESTAMPTZ,
    notes VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 19. Chatbot
CREATE TABLE IF NOT EXISTS chatbot_intents (
    id SERIAL PRIMARY KEY,
    intent VARCHAR(100) NOT NULL,
    keywords VARCHAR(500),
    response TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chatbot_conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_seller_offers_product ON seller_offers(product_id, is_active);
CREATE INDEX IF NOT EXISTS idx_seller_offers_price ON seller_offers(product_id, price);
CREATE INDEX IF NOT EXISTS idx_auction_status ON auctions(status);
CREATE INDEX IF NOT EXISTS idx_auction_bids ON auction_bids(auction_id, amount);
CREATE INDEX IF NOT EXISTS idx_gift_card_code ON gift_cards(code);
CREATE INDEX IF NOT EXISTS idx_wallet_user ON wallets(user_id);
CREATE INDEX IF NOT EXISTS idx_commission_order ON commission_transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_loyalty_user ON user_loyalty(user_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_code ON affiliates(referral_code);
CREATE INDEX IF NOT EXISTS idx_blog_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_live_stream_status ON live_streams(status);
CREATE INDEX IF NOT EXISTS idx_return_user ON return_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_brand_name ON brands(name);
CREATE INDEX IF NOT EXISTS idx_product_views_user ON product_views(user_id, product_id);
CREATE INDEX IF NOT EXISTS idx_search_history_user ON search_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chatbot_intent ON chatbot_intents(intent);
