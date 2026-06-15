-- Migration 000031: Final enterprise features (POS, Messaging, Vault, Pricing, Analytics, Integration, Payout, Automation)

-- 1. POS System
CREATE TABLE IF NOT EXISTS pos_terminals (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100),
    serial_no VARCHAR(100) UNIQUE,
    location VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS pos_orders (
    id SERIAL PRIMARY KEY,
    terminal_id INTEGER NOT NULL REFERENCES pos_terminals(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    customer_id INTEGER REFERENCES users(id),
    order_id INTEGER REFERENCES orders(id),
    total DOUBLE PRECISION NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS pos_order_items (
    id SERIAL PRIMARY KEY,
    pos_order_id INTEGER NOT NULL REFERENCES pos_orders(id),
    product_id INTEGER REFERENCES products(id),
    barcode VARCHAR(100),
    name VARCHAR(200),
    quantity INTEGER DEFAULT 1,
    unit_price DOUBLE PRECISION NOT NULL,
    total DOUBLE PRECISION NOT NULL
);

-- 2. Messaging (Email + SMS + Push)
CREATE TABLE IF NOT EXISTS email_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    subject VARCHAR(200),
    body_html TEXT,
    event_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,
    to_email VARCHAR(200) NOT NULL,
    subject VARCHAR(200),
    template VARCHAR(100),
    reference_type VARCHAR(50),
    reference_id INTEGER,
    status VARCHAR(20) DEFAULT 'sent',
    error TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS sms_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    body TEXT,
    event_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS sms_logs (
    id SERIAL PRIMARY KEY,
    to_phone VARCHAR(20) NOT NULL,
    body TEXT,
    reference_type VARCHAR(50),
    reference_id INTEGER,
    status VARCHAR(20) DEFAULT 'sent',
    error TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    platform VARCHAR(20),
    token TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS push_notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200),
    body TEXT,
    data TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Payment Vault
CREATE TABLE IF NOT EXISTS saved_payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    token VARCHAR(500) NOT NULL,
    last_four VARCHAR(4),
    card_holder VARCHAR(100),
    card_brand VARCHAR(50),
    expiry_month INTEGER,
    expiry_year INTEGER,
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Dynamic Pricing
CREATE TABLE IF NOT EXISTS pricing_rules (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    rule_type VARCHAR(50),
    min_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    target_margin DOUBLE PRECISION,
    adjustment_rate DOUBLE PRECISION DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    old_price DOUBLE PRECISION,
    new_price DOUBLE PRECISION,
    reason VARCHAR(100),
    changed_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS inventory_forecasts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    forecast_date TIMESTAMPTZ,
    predicted_demand INTEGER DEFAULT 0,
    confidence DOUBLE PRECISION DEFAULT 0.8,
    reorder_point INTEGER DEFAULT 0,
    suggested_order_qty INTEGER DEFAULT 0,
    calculated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Analytics
CREATE TABLE IF NOT EXISTS analytics_reports (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200),
    report_type VARCHAR(50),
    date_from TIMESTAMPTZ,
    date_to TIMESTAMPTZ,
    config TEXT,
    last_generated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS saved_dashboards (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200),
    widgets TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS rfm_segments (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100),
    r_score INTEGER,
    f_score INTEGER,
    m_score INTEGER,
    customer_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Integration (ERP / Muhasebe)
CREATE TABLE IF NOT EXISTS erp_connections (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    erp_type VARCHAR(50),
    api_url VARCHAR(500),
    api_key TEXT,
    api_secret TEXT,
    company_id VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS erp_sync_logs (
    id SERIAL PRIMARY KEY,
    connection_id INTEGER NOT NULL REFERENCES erp_connections(id),
    sync_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    records_synced INTEGER DEFAULT 0,
    error TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 7. Payout Extended
CREATE TABLE IF NOT EXISTS payout_schedules (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,
    frequency VARCHAR(20),
    day_of_week INTEGER,
    day_of_month INTEGER,
    min_amount DOUBLE PRECISION DEFAULT 50,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS multi_currency_balances (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    currency VARCHAR(10) NOT NULL,
    balance DOUBLE PRECISION DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Marketing Automation
CREATE TABLE IF NOT EXISTS automation_workflows (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(200),
    trigger_event VARCHAR(50),
    conditions TEXT,
    actions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS workflow_logs (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES automation_workflows(id),
    triggered_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    result TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pos_terminal_seller ON pos_terminals(seller_id);
CREATE INDEX IF NOT EXISTS idx_pos_order_terminal ON pos_orders(terminal_id);
CREATE INDEX IF NOT EXISTS idx_email_log_sent ON email_logs(sent_at);
CREATE INDEX IF NOT EXISTS idx_push_user ON push_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_push_notif_user ON push_notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_payment_vault_user ON saved_payment_methods(user_id);
CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_forecast ON inventory_forecasts(product_id, forecast_date);
CREATE INDEX IF NOT EXISTS idx_analytics_seller ON analytics_reports(seller_id);
CREATE INDEX IF NOT EXISTS idx_rfm_seller ON rfm_segments(seller_id);
CREATE INDEX IF NOT EXISTS idx_erp_seller ON erp_connections(seller_id);
CREATE INDEX IF NOT EXISTS idx_payout_schedule ON payout_schedules(seller_id);
CREATE INDEX IF NOT EXISTS idx_multi_currency ON multi_currency_balances(seller_id, currency);
CREATE INDEX IF NOT EXISTS idx_workflow_seller ON automation_workflows(seller_id);
