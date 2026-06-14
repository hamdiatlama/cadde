-- ============================================================
-- DOMAIN: YEMEK + DESTEK + ABONELIK + PIDYON + ODEME
-- ============================================================

-- ---------- RESTORAN ----------

CREATE TABLE restaurants (
    id                  SERIAL PRIMARY KEY,
    seller_id           INT UNIQUE NOT NULL REFERENCES sellers(id) ON DELETE CASCADE,
    name                VARCHAR(200) NOT NULL,
    slug                VARCHAR(200),
    cuisine_type        VARCHAR(100),
    cuisine_subtypes    TEXT,
    phone               VARCHAR(20),
    description         TEXT,
    logo_url            TEXT,
    cover_image_url     TEXT,
    is_active           BOOLEAN NOT NULL DEFAULT true,
    is_open             BOOLEAN NOT NULL DEFAULT true,
    accepts_orders      BOOLEAN NOT NULL DEFAULT true,
    opening_time        VARCHAR(10) DEFAULT '09:00',
    closing_time        VARCHAR(10) DEFAULT '22:00',
    closed_days         TEXT,
    min_order_amount    NUMERIC(10,2) DEFAULT 0,
    delivery_fee        NUMERIC(10,2) DEFAULT 19.90,
    free_delivery_min_amount NUMERIC(10,2) DEFAULT 100,
    max_delivery_radius_km  NUMERIC(5,2) DEFAULT 5.0,
    preparation_time_min    INT DEFAULT 20,
    has_thermal_bags    BOOLEAN DEFAULT false,
    hygiene_rating      VARCHAR(20) DEFAULT 'pending',
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_docs   TEXT,
    commission_rate     NUMERIC(4,2) DEFAULT 0.15,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_verified ON restaurants(verification_status);

-- Restoran subeleri
CREATE TABLE restaurant_branches (
    id              SERIAL PRIMARY KEY,
    restaurant_id   INT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name            VARCHAR(200),
    address         TEXT,
    latitude        NUMERIC(10,7),
    longitude       NUMERIC(10,7),
    phone           VARCHAR(20),
    opening_time    VARCHAR(10),
    closing_time    VARCHAR(10),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_branches_restaurant ON restaurant_branches(restaurant_id);

-- Teslimat bolgeleri (restoran bazli)
CREATE TABLE delivery_zones (
    id              SERIAL PRIMARY KEY,
    restaurant_id   INT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    min_latitude    NUMERIC(10,7) NOT NULL,
    max_latitude    NUMERIC(10,7) NOT NULL,
    min_longitude   NUMERIC(10,7) NOT NULL,
    max_longitude   NUMERIC(10,7) NOT NULL,
    delivery_fee    NUMERIC(10,2) DEFAULT 0,
    min_order       NUMERIC(10,2) DEFAULT 0,
    estimated_delivery_min INT DEFAULT 30,
    is_active       BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX idx_deliveryzones_restaurant ON delivery_zones(restaurant_id);

-- ---------- MENU ----------

CREATE TABLE food_menu_items (
    id                  SERIAL PRIMARY KEY,
    restaurant_id       INT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    branch_id           INT REFERENCES restaurant_branches(id) ON DELETE SET NULL,
    name                VARCHAR(200) NOT NULL,
    description         TEXT,
    category            VARCHAR(100),
    subcategory         VARCHAR(100),
    price               NUMERIC(10,2) NOT NULL,
    compare_price       NUMERIC(10,2),
    calories_kcal       INT,
    protein_g           NUMERIC(6,2),
    carbs_g             NUMERIC(6,2),
    fat_g               NUMERIC(6,2),
    fiber_g             NUMERIC(6,2),
    serving_size        VARCHAR(50),
    is_vegetarian       BOOLEAN DEFAULT false,
    is_vegan            BOOLEAN DEFAULT false,
    is_gluten_free      BOOLEAN DEFAULT false,
    is_halal            BOOLEAN DEFAULT false,
    is_spicy            BOOLEAN DEFAULT false,
    dietary_tags        TEXT,
    allergens           TEXT,
    image_url           TEXT,
    image_urls          TEXT,
    is_available        BOOLEAN NOT NULL DEFAULT true,
    preparation_time_min INT DEFAULT 10,
    sort_order          INT DEFAULT 0,
    total_orders        INT DEFAULT 0,
    rating              NUMERIC(3,2) DEFAULT 0,
    review_count        INT DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_menu_restaurant ON food_menu_items(restaurant_id);
CREATE INDEX idx_menu_category ON food_menu_items(category);
CREATE INDEX idx_menu_available ON food_menu_items(is_available) WHERE is_available = true;

-- Menu modifierlari (extra malzeme, boyut vs)
CREATE TABLE menu_item_modifiers (
    id              SERIAL PRIMARY KEY,
    menu_item_id    INT NOT NULL REFERENCES food_menu_items(id) ON DELETE CASCADE,
    group_name      VARCHAR(100) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    price_modifier  NUMERIC(10,2) DEFAULT 0,
    max_select      INT DEFAULT 1,
    sort_order      INT DEFAULT 0,
    is_default      BOOLEAN DEFAULT false,
    is_active       BOOLEAN DEFAULT true
);

CREATE INDEX idx_modifiers_item ON menu_item_modifiers(menu_item_id);

-- ---------- SICAKLIK / HIYEN / SURUCU RAPOR ----------

CREATE TABLE temperature_checks (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    courier_id      INT NOT NULL REFERENCES couriers(id),
    temperature_celsius NUMERIC(5,2) NOT NULL,
    check_type      VARCHAR(20) DEFAULT 'pickup',
    photo_url       TEXT,
    notes           TEXT,
    is_acceptable   BOOLEAN,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE hygiene_reports (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    reporter_id     INT NOT NULL REFERENCES users(id),
    report_type     VARCHAR(20) DEFAULT 'customer',
    issue_type      VARCHAR(100) NOT NULL,
    description     TEXT,
    photo_urls      TEXT,
    status          VARCHAR(20) DEFAULT 'pending',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE driver_reports (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    reporter_id     INT NOT NULL REFERENCES users(id),
    courier_id      INT NOT NULL REFERENCES couriers(id),
    rating          INT DEFAULT 5,
    issue_type      VARCHAR(100),
    description     TEXT,
    is_anonymous    BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------- SIPARIS MESAJLARI (YEMEK) ----------

CREATE TABLE chat_messages (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sender_id       INT NOT NULL REFERENCES users(id),
    receiver_role   VARCHAR(20) NOT NULL,
    message         TEXT NOT NULL,
    is_read         BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_order ON chat_messages(order_id);

-- ---------- DESTEK / TICKET ----------

CREATE TABLE support_tickets (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id        INT REFERENCES orders(id) ON DELETE SET NULL,
    subject         VARCHAR(300) NOT NULL,
    category        VARCHAR(50) DEFAULT 'other',
    status          VARCHAR(20) DEFAULT 'open',
    priority        VARCHAR(20) DEFAULT 'normal',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ,
    resolved_at     TIMESTAMPTZ
);

CREATE INDEX idx_tickets_user ON support_tickets(user_id);
CREATE INDEX idx_tickets_status ON support_tickets(status);

CREATE TABLE ticket_messages (
    id              SERIAL PRIMARY KEY,
    ticket_id       INT NOT NULL REFERENCES support_tickets(id) ON DELETE CASCADE,
    sender_id       INT NOT NULL REFERENCES users(id),
    message         TEXT NOT NULL,
    is_staff        BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ticketmsgs_ticket ON ticket_messages(ticket_id);

-- ---------- ODULLER ----------

CREATE TABLE reviews (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id      INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    user_id         INT NOT NULL REFERENCES users(id),
    rating          INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title           VARCHAR(200),
    comment         TEXT,
    photo_urls      TEXT,
    is_approved     BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);

-- ---------- SATIN ALMALAR / ABONELIK ----------

CREATE TABLE subscription_plans (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(200) NOT NULL,
    description         TEXT,
    interval_days       INT NOT NULL,
    duration_months     INT DEFAULT 1,
    price_per_delivery  NUMERIC(10,2) NOT NULL,
    total_price         NUMERIC(10,2) NOT NULL,
    is_active           BOOLEAN DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id                  SERIAL PRIMARY KEY,
    user_id             INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id             INT NOT NULL REFERENCES subscription_plans(id),
    seller_id           INT NOT NULL REFERENCES sellers(id),
    product_id          INT NOT NULL REFERENCES products(id),
    status              VARCHAR(20) DEFAULT 'active',
    start_date          TIMESTAMPTZ NOT NULL,
    end_date            TIMESTAMPTZ,
    next_delivery_date  TIMESTAMPTZ,
    recipient_name      VARCHAR(200),
    recipient_phone     VARCHAR(20),
    delivery_address    TEXT,
    delivery_latitude   NUMERIC(10,7),
    delivery_longitude  NUMERIC(10,7),
    notes               TEXT,
    card_message        TEXT,
    is_gift             BOOLEAN DEFAULT false,
    paused_at           TIMESTAMPTZ,
    cancelled_at        TIMESTAMPTZ,
    cancel_reason       TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

CREATE TABLE subscription_deliveries (
    id                  SERIAL PRIMARY KEY,
    subscription_id     INT NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
    order_id            INT REFERENCES orders(id) ON DELETE SET NULL,
    delivery_number     INT NOT NULL,
    scheduled_date      TIMESTAMPTZ,
    status              VARCHAR(20) DEFAULT 'pending',
    is_gift             BOOLEAN DEFAULT false,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subdeliveries_sub ON subscription_deliveries(subscription_id);

-- ---------- ODEME / FATURA / IADE ----------

CREATE TABLE payments (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id         INT NOT NULL REFERENCES users(id),
    method          VARCHAR(50) NOT NULL,
    amount          NUMERIC(10,2) NOT NULL,
    points_used     INT DEFAULT 0,
    points_earned   INT DEFAULT 0,
    installment     INT DEFAULT 1,
    status          VARCHAR(20) DEFAULT 'pending',
    provider_ref    VARCHAR(200),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_user ON payments(user_id);

CREATE TABLE points_transactions (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id),
    amount          INT NOT NULL,
    type            VARCHAR(50) NOT NULL,
    description     VARCHAR(300),
    order_id        INT REFERENCES orders(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pointstrans_user ON points_transactions(user_id);

CREATE TABLE invoices (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id         INT NOT NULL REFERENCES users(id),
    invoice_no      VARCHAR(50) UNIQUE NOT NULL,
    amount          NUMERIC(10,2) NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending',
    pdf_url         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE refunds (
    id              SERIAL PRIMARY KEY,
    order_id        INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id         INT NOT NULL REFERENCES users(id),
    payment_id      INT REFERENCES payments(id) ON DELETE SET NULL,
    amount          NUMERIC(10,2) NOT NULL,
    reason          TEXT,
    status          VARCHAR(20) DEFAULT 'pending',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------- BILDIRIM ----------

CREATE TABLE notifications (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            VARCHAR(50) NOT NULL,
    title           VARCHAR(200) NOT NULL,
    message         TEXT,
    reference_type  VARCHAR(50),
    reference_id    INT,
    is_read         BOOLEAN DEFAULT false,
    read_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(is_read) WHERE is_read = false;
