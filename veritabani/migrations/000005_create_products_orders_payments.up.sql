-- ============================================================
-- DOMAIN: ÜRÜN KATALOĞU, SEPET, SİPARİŞ, ÖDEME, STOK
-- ============================================================

-- ---------- ÜRÜN KATALOĞU ----------

-- Kategori ağacı (Nested Set / Materialized Path)
CREATE TABLE product_categories (
    id              SERIAL PRIMARY KEY,
    parent_id       INT REFERENCES product_categories(id),
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    description     TEXT,
    image_url       TEXT,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    path            LTREE,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pcat_parent ON product_categories(parent_id);
CREATE INDEX idx_pcat_path ON product_categories USING GIST(path);

-- Ürünler
CREATE TABLE products (
    id              BIGSERIAL PRIMARY KEY,
    category_id     INT NOT NULL REFERENCES product_categories(id),
    seller_id       UUID NOT NULL REFERENCES users(id),
    name            VARCHAR(300) NOT NULL,
    slug            VARCHAR(300) UNIQUE NOT NULL,
    description     TEXT,
    short_description VARCHAR(500),
    brand_name      VARCHAR(200),
    model_name      VARCHAR(200),
    condition       VARCHAR(50),
    sku             VARCHAR(100) UNIQUE,
    barcode         VARCHAR(100),
    unit_type       VARCHAR(50) DEFAULT 'adet',
    weight_kg       NUMERIC(10,3),
    width_cm        NUMERIC(10,2),
    height_cm       NUMERIC(10,2),
    depth_cm        NUMERIC(10,2),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    is_featured     BOOLEAN NOT NULL DEFAULT false,
    sort_order      INT DEFAULT 0,
    seo_title       VARCHAR(200),
    seo_description VARCHAR(500),
    view_count      BIGINT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_seller ON products(seller_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_brand ON products(brand_name);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;

-- Ürün görselleri (MinIO referansı)
CREATE TABLE product_images (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    file_path       TEXT NOT NULL,
    alt_text        VARCHAR(200),
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    is_primary      BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prodimages_product ON product_images(product_id);

-- Ürün varyantları (renk, beden, vb.)
CREATE TABLE product_variants (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    sku             VARCHAR(100) UNIQUE,
    price_adjustment NUMERIC(10,2) NOT NULL DEFAULT 0,
    image_url       TEXT,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prodvariants_product ON product_variants(product_id);

-- Ürün özellik/attribute değerleri
CREATE TABLE product_attributes (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    attribute_name  VARCHAR(100) NOT NULL,
    attribute_value TEXT NOT NULL,
    sort_order      SMALLINT DEFAULT 0
);

CREATE INDEX idx_prodattrs_product ON product_attributes(product_id);

-- ---------- FİYAT & STOK ----------

-- Ürün fiyat geçmişi (her fiyat değişikliği kaydedilir)
CREATE TABLE product_prices (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_id      BIGINT REFERENCES product_variants(id) ON DELETE CASCADE,
    base_price      NUMERIC(12,2) NOT NULL,
    discounted_price NUMERIC(12,2),
    currency        CHAR(3) NOT NULL DEFAULT 'TRY',
    valid_from      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_until     TIMESTAMPTZ,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prodprices_product ON product_prices(product_id);
CREATE INDEX idx_prodprices_active ON product_prices(is_active) WHERE is_active = true;

-- Stok (her ürün/varyant için ayrı satır)
CREATE TABLE product_stock (
    id              BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_id      BIGINT REFERENCES product_variants(id) ON DELETE CASCADE,
    warehouse_id    SMALLINT,
    quantity        INT NOT NULL DEFAULT 0,
    reserved_qty    INT NOT NULL DEFAULT 0,
    min_stock_level INT NOT NULL DEFAULT 0,
    max_stock_level INT,
    version         INT NOT NULL DEFAULT 1,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (product_id, COALESCE(variant_id, 0), COALESCE(warehouse_id, 0))
);

CREATE INDEX idx_stock_product ON product_stock(product_id);

-- ---------- SEPET ----------

CREATE TYPE cart_status AS ENUM ('active', 'abandoned', 'converted', 'expired');

CREATE TABLE carts (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id      VARCHAR(100),
    status          cart_status NOT NULL DEFAULT 'active',
    coupon_code     VARCHAR(50),
    discount_amount NUMERIC(10,2) DEFAULT 0,
    notes           TEXT,
    expires_at      TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '7 days'),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_carts_user ON carts(user_id);
CREATE INDEX idx_carts_session ON carts(session_id);
CREATE INDEX idx_carts_status ON carts(status);

CREATE TABLE cart_items (
    id              BIGSERIAL PRIMARY KEY,
    cart_id         UUID NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id      BIGINT NOT NULL REFERENCES products(id),
    variant_id      BIGINT REFERENCES product_variants(id),
    quantity        INT NOT NULL CHECK (quantity > 0),
    unit_price      NUMERIC(12,2) NOT NULL,
    total_price     NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cartitems_cart ON cart_items(cart_id);
CREATE INDEX idx_cartitems_product ON cart_items(product_id);

-- ---------- SİPARİŞ ----------

CREATE TYPE order_status AS ENUM (
    'pending', 'confirmed', 'processing', 'shipped', 'delivered',
    'cancelled', 'refunded', 'returned'
);

CREATE TYPE payment_status AS ENUM (
    'pending', 'paid', 'failed', 'refunded', 'chargeback'
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_no        VARCHAR(50) UNIQUE NOT NULL,
    user_id         UUID NOT NULL REFERENCES users(id),
    cart_id         UUID REFERENCES carts(id),
    status          order_status NOT NULL DEFAULT 'pending',
    payment_status  payment_status NOT NULL DEFAULT 'pending',
    shipping_address_id UUID REFERENCES user_addresses(id),
    billing_address_id  UUID REFERENCES user_addresses(id),
    subtotal        NUMERIC(12,2) NOT NULL,
    shipping_fee    NUMERIC(10,2) NOT NULL DEFAULT 0,
    discount_amount NUMERIC(10,2) NOT NULL DEFAULT 0,
    tax_amount      NUMERIC(10,2) NOT NULL DEFAULT 0,
    total_amount    NUMERIC(12,2) NOT NULL,
    currency        CHAR(3) NOT NULL DEFAULT 'TRY',
    coupon_code     VARCHAR(50),
    notes           TEXT,
    estimated_delivery TIMESTAMPTZ,
    delivered_at    TIMESTAMPTZ,
    cancelled_at    TIMESTAMPTZ,
    cancellation_reason TEXT,
    version         INT NOT NULL DEFAULT 1,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_no ON orders(order_no);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_payment ON orders(payment_status);

CREATE TABLE orders_2026_01 PARTITION OF orders
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE orders_2026_02 PARTITION OF orders
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE orders_2026_03 PARTITION OF orders
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE orders_2026_04 PARTITION OF orders
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE orders_2026_05 PARTITION OF orders
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE orders_2026_06 PARTITION OF orders
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Sipariş kalemleri
CREATE TABLE order_items (
    id              BIGSERIAL PRIMARY KEY,
    order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id      BIGINT NOT NULL REFERENCES products(id),
    variant_id      BIGINT REFERENCES product_variants(id),
    product_name    VARCHAR(300) NOT NULL,
    quantity        INT NOT NULL CHECK (quantity > 0),
    unit_price      NUMERIC(12,2) NOT NULL,
    total_price     NUMERIC(12,2) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orderitems_order ON order_items(order_id);

-- Sipariş geçmişi (state machine log)
CREATE TABLE order_history (
    id              BIGSERIAL PRIMARY KEY,
    order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    from_status     order_status,
    to_status       order_status NOT NULL,
    changed_by      UUID REFERENCES users(id),
    note            TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orderhist_order ON order_history(order_id);

-- ---------- ÖDEME ----------

CREATE TABLE payments (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id        UUID NOT NULL REFERENCES orders(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    amount          NUMERIC(12,2) NOT NULL,
    currency        CHAR(3) NOT NULL DEFAULT 'TRY',
    provider        VARCHAR(50) NOT NULL,
    provider_ref    VARCHAR(200),
    status          payment_status NOT NULL DEFAULT 'pending',
    payment_method  VARCHAR(50),
    installments    SMALLINT DEFAULT 1,
    gateway_response JSONB,
    paid_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_provider ON payments(provider, provider_ref);
