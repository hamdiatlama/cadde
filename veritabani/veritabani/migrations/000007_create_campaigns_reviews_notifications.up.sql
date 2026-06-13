-- ============================================================
-- DOMAIN: KAMPANYA, DEĞERLENDİRME, BİLDİRİM
-- ============================================================

-- ---------- KAMPANYA & İNDİRİM ----------

CREATE TYPE discount_type AS ENUM ('percentage', 'fixed_amount', 'free_shipping');
CREATE TYPE campaign_status AS ENUM ('draft', 'active', 'paused', 'expired');

CREATE TABLE campaigns (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    discount_type   discount_type NOT NULL,
    discount_value  NUMERIC(10,2) NOT NULL,
    min_order_amount NUMERIC(10,2),
    max_discount    NUMERIC(10,2),
    usage_limit     INT,
    used_count      INT NOT NULL DEFAULT 0,
    starts_at       TIMESTAMPTZ NOT NULL,
    ends_at         TIMESTAMPTZ NOT NULL,
    status          campaign_status NOT NULL DEFAULT 'draft',
    created_by      UUID REFERENCES users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_dates ON campaigns(starts_at, ends_at);

-- Kampanya-ürün ilişkisi
CREATE TABLE campaign_products (
    campaign_id     INT NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    PRIMARY KEY (campaign_id, product_id)
);

-- Kampanya-kategori ilişkisi
CREATE TABLE campaign_categories (
    campaign_id     INT NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    category_id     INT NOT NULL REFERENCES product_categories(id) ON DELETE CASCADE,
    PRIMARY KEY (campaign_id, category_id)
);

-- Kuponlar
CREATE TABLE coupons (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(50) UNIQUE NOT NULL,
    campaign_id     INT REFERENCES campaigns(id),
    discount_type   discount_type NOT NULL,
    discount_value  NUMERIC(10,2) NOT NULL,
    min_order_amount NUMERIC(10,2) DEFAULT 0,
    max_usage       INT DEFAULT 1,
    used_count      INT NOT NULL DEFAULT 0,
    max_usage_per_user INT DEFAULT 1,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    valid_from      TIMESTAMPTZ NOT NULL,
    valid_until     TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_coupons_code ON coupons(code);
CREATE INDEX idx_coupons_active ON coupons(is_active) WHERE is_active = true;

-- Kullanılmış kuponlar
CREATE TABLE coupon_usage (
    id              BIGSERIAL PRIMARY KEY,
    coupon_id       INT NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id        UUID REFERENCES orders(id),
    used_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_couponusage_coupon ON coupon_usage(coupon_id);
CREATE INDEX idx_couponusage_user ON coupon_usage(user_id);

-- ---------- DEĞERLENDİRME & YORUM ----------

CREATE TABLE product_reviews (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id        UUID REFERENCES orders(id),
    rating          SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title           VARCHAR(200),
    content         TEXT,
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    is_approved     BOOLEAN NOT NULL DEFAULT false,
    helpful_count   INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (product_id, user_id)
);

CREATE INDEX idx_reviews_product ON product_reviews(product_id);
CREATE INDEX idx_reviews_user ON product_reviews(user_id);
CREATE INDEX idx_reviews_rating ON product_reviews(rating);
CREATE INDEX idx_reviews_approved ON product_reviews(is_approved) WHERE is_approved = true;

-- Yorum görselleri (MinIO)
CREATE TABLE review_images (
    id              BIGSERIAL PRIMARY KEY,
    review_id       BIGINT NOT NULL REFERENCES product_reviews(id) ON DELETE CASCADE,
    file_path       TEXT NOT NULL,
    sort_order      SMALLINT NOT NULL DEFAULT 0
);

-- Yorum "faydalı buldum" oyları
CREATE TABLE review_helpful_votes (
    review_id       BIGINT NOT NULL REFERENCES product_reviews(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_helpful      BOOLEAN NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (review_id, user_id)
);

-- Sürücü değerlendirmeleri
CREATE TABLE driver_reviews (
    id              BIGSERIAL PRIMARY KEY,
    ride_id         UUID UNIQUE NOT NULL REFERENCES rides(id) ON DELETE CASCADE,
    driver_id       UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating          SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_driverreviews_driver ON driver_reviews(driver_id);

-- ---------- BİLDİRİM ----------

CREATE TYPE notification_channel AS ENUM ('push', 'email', 'sms', 'in_app');
CREATE TYPE notification_priority AS ENUM ('low', 'normal', 'high', 'urgent');

CREATE TABLE notification_templates (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(100) UNIQUE NOT NULL,
    title           VARCHAR(200),
    body            TEXT NOT NULL,
    channel         notification_channel NOT NULL DEFAULT 'push',
    variables       JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE notifications (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    template_code   VARCHAR(100) REFERENCES notification_templates(code),
    title           VARCHAR(200) NOT NULL,
    body            TEXT,
    data            JSONB,
    channel         notification_channel NOT NULL DEFAULT 'push',
    priority        notification_priority NOT NULL DEFAULT 'normal',
    is_read         BOOLEAN NOT NULL DEFAULT false,
    is_sent         BOOLEAN NOT NULL DEFAULT false,
    sent_at         TIMESTAMPTZ,
    read_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read) WHERE is_read = false;
CREATE INDEX idx_notifications_sent ON notifications(is_sent) WHERE is_sent = false;

CREATE TABLE notifications_2026_01 PARTITION OF notifications
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE notifications_2026_02 PARTITION OF notifications
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE notifications_2026_03 PARTITION OF notifications
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE notifications_2026_04 PARTITION OF notifications
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE notifications_2026_05 PARTITION OF notifications
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE notifications_2026_06 PARTITION OF notifications
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE notifications_default PARTITION OF notifications DEFAULT;

-- Bildirim gönderme logu (adapter pattern için)
CREATE TABLE notification_logs (
    id              BIGSERIAL PRIMARY KEY,
    notification_id BIGINT NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
    provider        VARCHAR(50) NOT NULL,
    provider_ref    VARCHAR(200),
    status          VARCHAR(20) NOT NULL,
    error_message   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
