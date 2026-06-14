ALTER TABLE contractor_companies DROP COLUMN IF EXISTS verification_status;
ALTER TABLE contractor_companies DROP COLUMN IF EXISTS verification_note;
ALTER TABLE contractor_companies DROP COLUMN IF EXISTS verified_at;
ALTER TABLE contractor_companies DROP COLUMN IF EXISTS certificate_no;
ALTER TABLE contractor_companies DROP COLUMN IF EXISTS certificate_expiry;
ALTER TABLE listing_documents DROP COLUMN IF EXISTS company_id;
ALTER TABLE listing_documents DROP COLUMN IF EXISTS is_company_doc;
