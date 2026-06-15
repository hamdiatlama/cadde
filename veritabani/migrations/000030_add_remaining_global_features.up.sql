-- Migration 000030: Remaining global marketplace features

-- 1. Marketplace Core
CREATE TABLE IF NOT EXISTS multi_vendor_carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total_amount DOUBLE PRECISION DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS multi_vendor_cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES multi_vendor_carts(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS seller_applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    company_name VARCHAR(200),
    tax_number VARCHAR(50),
    phone VARCHAR(20),
    business_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS pre_orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    expected_stock_date TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'pending',
    order_id INTEGER REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS guest_checkouts (
    id SERIAL PRIMARY KEY,
    email VARCHAR(200) NOT NULL,
    session_id VARCHAR(100),
    order_id INTEGER NOT NULL REFERENCES orders(id),
    converted_to_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Review Media
CREATE TABLE IF NOT EXISTS review_media (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id),
    media_type VARCHAR(10),
    url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Social Commerce
CREATE TABLE IF NOT EXISTS social_channels (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    platform VARCHAR(50) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,
    page_id VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS social_product_syncs (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER NOT NULL REFERENCES social_channels(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    platform_product_id VARCHAR(200),
    status VARCHAR(20) DEFAULT 'pending',
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS social_orders (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    platform_order_id VARCHAR(200),
    order_id INTEGER REFERENCES orders(id),
    buyer_name VARCHAR(200),
    buyer_platform_id VARCHAR(200),
    total DOUBLE PRECISION,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS shopping_feeds (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    feed_type VARCHAR(50),
    feed_url VARCHAR(500),
    product_count INTEGER DEFAULT 0,
    last_generated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS affiliate_networks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    api_key VARCHAR(500),
    api_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE
);

-- 4. Developer (API Keys, Webhooks)
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    key_hash VARCHAR(200) UNIQUE NOT NULL,
    key_prefix VARCHAR(10),
    name VARCHAR(100),
    permissions VARCHAR(500),
    rate_limit INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS webhooks (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    url VARCHAR(500) NOT NULL,
    secret VARCHAR(200),
    events VARCHAR(1000),
    is_active BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS webhook_events (
    id SERIAL PRIMARY KEY,
    webhook_id INTEGER NOT NULL REFERENCES webhooks(id),
    event_type VARCHAR(100) NOT NULL,
    payload TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    response_code INTEGER,
    response_body TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Fraud Detection
CREATE TABLE IF NOT EXISTS fraud_rules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    rule_type VARCHAR(50),
    threshold_value DOUBLE PRECISION,
    score INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS fraud_checks (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    total_score INTEGER DEFAULT 0,
    risk_level VARCHAR(20),
    flags TEXT,
    is_blocked BOOLEAN DEFAULT FALSE,
    checked_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS fraud_transaction_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    ip_address VARCHAR(50),
    device_fingerprint VARCHAR(200),
    amount DOUBLE PRECISION,
    success BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Product Enhanced (Q&A, Bundle, Registry, Barcode, Expiry)
CREATE TABLE IF NOT EXISTS product_questions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    question TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES product_questions(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    answer TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_bundles (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200),
    total_price DOUBLE PRECISION,
    discount_rate DOUBLE PRECISION DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS bundle_items (
    id SERIAL PRIMARY KEY,
    bundle_id INTEGER NOT NULL REFERENCES product_bundles(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS gift_registries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    type VARCHAR(20),
    title VARCHAR(200),
    event_date TIMESTAMPTZ,
    is_public BOOLEAN DEFAULT TRUE,
    share_code VARCHAR(20) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS gift_registry_items (
    id SERIAL PRIMARY KEY,
    registry_id INTEGER NOT NULL REFERENCES gift_registries(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    purchased_quantity INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS product_barcodes (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    barcode VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_expiry_batches (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    batch_no VARCHAR(100),
    lot_no VARCHAR(100),
    quantity INTEGER DEFAULT 0,
    expiry_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Tax Extended
CREATE TABLE IF NOT EXISTS tax_rate_addresses (
    id SERIAL PRIMARY KEY,
    country VARCHAR(2) NOT NULL,
    state VARCHAR(100),
    city VARCHAR(100),
    rate DOUBLE PRECISION NOT NULL,
    tax_type VARCHAR(20) DEFAULT 'vat',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS gib_invoices (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    gib_id VARCHAR(100),
    invoice_no VARCHAR(50) UNIQUE,
    status VARCHAR(20) DEFAULT 'draft',
    xml_content TEXT,
    qr_code VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS international_documents (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    doc_type VARCHAR(50),
    doc_number VARCHAR(100),
    file_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Logistics Advanced
CREATE TABLE IF NOT EXISTS carriers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_url VARCHAR(500),
    api_key VARCHAR(500),
    services VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS carrier_rates (
    id SERIAL PRIMARY KEY,
    carrier_id INTEGER NOT NULL REFERENCES carriers(id),
    service_name VARCHAR(100),
    weight_min DOUBLE PRECISION DEFAULT 0,
    weight_max DOUBLE PRECISION,
    price DOUBLE PRECISION NOT NULL,
    estimated_days_min INTEGER,
    estimated_days_max INTEGER
);
CREATE TABLE IF NOT EXISTS shipments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    carrier_id INTEGER REFERENCES carriers(id),
    service_name VARCHAR(100),
    tracking_no VARCHAR(100),
    label_url VARCHAR(500),
    cost DOUBLE PRECISION,
    weight DOUBLE PRECISION,
    status VARCHAR(20) DEFAULT 'pending',
    shipped_at TIMESTAMPTZ,
    estimated_delivery TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS carbon_footprints (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    shipment_id INTEGER REFERENCES shipments(id),
    co2_grams DOUBLE PRECISION,
    offset_cost DOUBLE PRECISION,
    offset_paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS gift_wraps (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100),
    price DOUBLE PRECISION DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- 9. Compliance
CREATE TABLE IF NOT EXISTS map_policies (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    min_advertised_price DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS map_violations (
    id SERIAL PRIMARY KEY,
    policy_id INTEGER NOT NULL REFERENCES map_policies(id),
    reported_price DOUBLE PRECISION NOT NULL,
    reported_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS counterfeit_reports (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    reported_by INTEGER NOT NULL REFERENCES users(id),
    description TEXT,
    evidence_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending',
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_compliance (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    cert_type VARCHAR(100),
    cert_number VARCHAR(100),
    cert_file_url VARCHAR(500),
    issued_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_recalls (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    reason TEXT NOT NULL,
    risk_level VARCHAR(20),
    affected_batch VARCHAR(100),
    action_taken VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS policy_violations (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    violation_type VARCHAR(100),
    description TEXT,
    evidence VARCHAR(500),
    penalty VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Seller Tools
CREATE TABLE IF NOT EXISTS listing_scores (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) UNIQUE,
    score INTEGER DEFAULT 0,
    title_score INTEGER DEFAULT 0,
    description_score INTEGER DEFAULT 0,
    image_score INTEGER DEFAULT 0,
    price_score INTEGER DEFAULT 0,
    category_score INTEGER DEFAULT 0,
    suggestions TEXT,
    calculated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS seller_academy_courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content_url VARCHAR(500),
    category VARCHAR(50),
    duration_minutes INTEGER,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS seller_academy_progress (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES seller_academy_courses(id),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Customer Service
CREATE TABLE IF NOT EXISTS help_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    content TEXT,
    category VARCHAR(50),
    is_published BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS forum_topics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    view_count INTEGER DEFAULT 0,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS forum_posts (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER NOT NULL REFERENCES forum_topics(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS kyc_documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    doc_type VARCHAR(50),
    doc_number VARCHAR(100),
    file_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending',
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS co_browsing_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    agent_id INTEGER REFERENCES users(id),
    session_token VARCHAR(200),
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);

-- 12. Storefront / PWA / GDPR
CREATE TABLE IF NOT EXISTS pwa_manifests (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    name VARCHAR(200),
    short_name VARCHAR(50),
    icon_url VARCHAR(500),
    theme_color VARCHAR(7),
    background_color VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS cookie_consents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(100),
    consent_type VARCHAR(50),
    ip_address VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS gdpr_data_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    request_type VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_multivendor_cart_user ON multi_vendor_carts(user_id);
CREATE INDEX IF NOT EXISTS idx_multivendor_cart_items ON multi_vendor_cart_items(cart_id);
CREATE INDEX IF NOT EXISTS idx_seller_applications_status ON seller_applications(status);
CREATE INDEX IF NOT EXISTS idx_preorder_user ON pre_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_guest_checkout_session ON guest_checkouts(session_id);
CREATE INDEX IF NOT EXISTS idx_social_channel_seller ON social_channels(seller_id);
CREATE INDEX IF NOT EXISTS idx_social_orders_platform ON social_orders(platform_order_id);
CREATE INDEX IF NOT EXISTS idx_api_key_seller ON api_keys(seller_id);
CREATE INDEX IF NOT EXISTS idx_api_key_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_webhook_seller ON webhooks(seller_id);
CREATE INDEX IF NOT EXISTS idx_webhook_events_status ON webhook_events(status);
CREATE INDEX IF NOT EXISTS idx_fraud_check_order ON fraud_checks(order_id);
CREATE INDEX IF NOT EXISTS idx_product_qna ON product_questions(product_id);
CREATE INDEX IF NOT EXISTS idx_barcode_lookup ON product_barcodes(barcode);
CREATE INDEX IF NOT EXISTS idx_tax_rate_country ON tax_rate_addresses(country, state);
CREATE INDEX IF NOT EXISTS idx_carrier_rates_weight ON carrier_rates(carrier_id, weight_min, weight_max);
CREATE INDEX IF NOT EXISTS idx_shipment_tracking ON shipments(tracking_no);
CREATE INDEX IF NOT EXISTS idx_listing_score_product ON listing_scores(product_id);
CREATE INDEX IF NOT EXISTS idx_help_article_slug ON help_articles(slug);
CREATE INDEX IF NOT EXISTS idx_forum_topic ON forum_topics(created_at);
CREATE INDEX IF NOT EXISTS idx_kyc_user ON kyc_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_cookie_session ON cookie_consents(session_id);
CREATE INDEX IF NOT EXISTS idx_gdpr_user ON gdpr_data_requests(user_id);
