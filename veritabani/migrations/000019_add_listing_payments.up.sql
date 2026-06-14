-- ============================================================
-- MIGRATION 000019: Ücretli İlan Sistemi (Listing Payments)
-- ============================================================
-- Emlak ve oto galeri ilanları için ödeme sistemi
-- İlan açma ücreti: emlak 250 TL, oto galeri 250 TL (ayarlanabilir)

-- İlan ücret konfigürasyonu
CREATE TABLE listing_price_config (
    id              SMALLSERIAL PRIMARY KEY,
    domain          VARCHAR(50) NOT NULL UNIQUE, -- realestate, vehicle
    price           NUMERIC(10,2) NOT NULL,
    currency        VARCHAR(5) NOT NULL DEFAULT 'TRY',
    description     VARCHAR(200),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ödeme kayıtları
CREATE TABLE listing_payments (
    id              BIGSERIAL PRIMARY KEY,
    domain          VARCHAR(50) NOT NULL, -- realestate, vehicle
    listing_id      BIGINT NOT NULL, -- property_listings.id veya vehicle_listings.id
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount          NUMERIC(10,2) NOT NULL,
    currency        VARCHAR(5) NOT NULL DEFAULT 'TRY',
    payment_method  VARCHAR(50), -- credit_card, bank_transfer, balance
    payment_ref     VARCHAR(100), -- harici ödeme referansı
    status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, completed, failed, refunded
    paid_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_listing_payments_listing ON listing_payments(listing_id, domain);
CREATE INDEX idx_listing_payments_user ON listing_payments(user_id);
CREATE INDEX idx_listing_payments_status ON listing_payments(status);

-- Varsayılan fiyatlar
INSERT INTO listing_price_config (domain, price, description) VALUES
    ('realestate', 250.00, 'Emlak ilanı açma ücreti'),
    ('vehicle', 250.00, 'Araç ilanı açma ücreti');
