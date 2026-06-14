-- ============================================================
-- MIGRATION 000017: Arazi İçeriği (Land Contents)
-- ============================================================
-- Bağ, bahçe, tarla, arsa satışlarında arazide neler var
-- (ağaç, bitki, yapı, kuyu, sulama sistemi, sera, çit vb.)

CREATE TABLE property_land_contents (
    id              BIGSERIAL PRIMARY KEY,
    listing_id      BIGINT NOT NULL REFERENCES property_listings(id) ON DELETE CASCADE,
    content_type    VARCHAR(50) NOT NULL, -- agac, bitki, yapi, kuyu, sulama, sera, cit, havuz, yol
    content_name    VARCHAR(200) NOT NULL, -- örn: Elma Ağacı, Ceviz, Bağ, Sera
    quantity        NUMERIC(10,2), -- adet veya m2
    unit            VARCHAR(20), -- adet, m2, donum, dekars
    description     TEXT,
    sort_order      SMALLINT DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_land_contents_listing ON property_land_contents(listing_id);
