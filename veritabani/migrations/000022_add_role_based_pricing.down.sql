-- Bu migration'ı geri almak için:
DELETE FROM listing_price_config WHERE user_role = 'individual';
UPDATE listing_price_config SET price = 250.00, description = 'Emlak ilanı açma ücreti' WHERE domain = 'realestate' AND user_role = 'company';
UPDATE listing_price_config SET price = 250.00, description = 'Araç ilanı açma ücreti' WHERE domain = 'vehicle' AND user_role = 'company';
ALTER TABLE listing_price_config DROP CONSTRAINT IF EXISTS listing_price_config_domain_user_role_key;
ALTER TABLE listing_price_config ADD UNIQUE (domain);
ALTER TABLE listing_price_config DROP COLUMN IF EXISTS user_role;
