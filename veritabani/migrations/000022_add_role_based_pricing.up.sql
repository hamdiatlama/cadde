-- ============================================================
-- MIGRATION 000022: Rol Bazlı İlan Fiyatlandırması
-- ============================================================
-- Bireysel: 25 TL, Şirket/Kurum: 250 TL

-- user_role kolonu ekle
ALTER TABLE listing_price_config ADD COLUMN user_role VARCHAR(20) NOT NULL DEFAULT 'company';
ALTER TABLE listing_price_config DROP CONSTRAINT IF EXISTS listing_price_config_domain_key;
ALTER TABLE listing_price_config ADD UNIQUE (domain, user_role);

-- Mevcut company fiyatlarını güncelle
UPDATE listing_price_config SET user_role = 'company' WHERE user_role = 'company';

-- Bireysel fiyatları ekle
INSERT INTO listing_price_config (domain, user_role, price, description, is_active) VALUES
    ('realestate', 'individual', 25.00, 'Bireysel emlak ilanı açma ücreti', true),
    ('vehicle', 'individual', 25.00, 'Bireysel araç ilanı açma ücreti', true);

-- Şirket fiyatlarını 250 olarak güncelle
UPDATE listing_price_config SET price = 250.00, description = 'Kurumsal emlak ilanı açma ücreti' WHERE domain = 'realestate' AND user_role = 'company';
UPDATE listing_price_config SET price = 250.00, description = 'Kurumsal araç ilanı açma ücreti' WHERE domain = 'vehicle' AND user_role = 'company';
