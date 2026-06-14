-- ============================================================
-- MIGRATION 000021: Şirket Sertifikasyon / Vergi Levhası
-- ============================================================
-- Emlak ofisi / oto galeri açmak için belge zorunluluğu

-- listing_documents tablosuna company_id ekle (şirket bazlı belgeler için)
ALTER TABLE listing_documents ADD COLUMN company_id INT REFERENCES contractor_companies(id) ON DELETE CASCADE;
ALTER TABLE listing_documents ADD COLUMN is_company_doc BOOLEAN NOT NULL DEFAULT false;

CREATE INDEX idx_listing_docs_company ON listing_documents(company_id);

-- Şirket doğrulama durumu için ek kolon
ALTER TABLE contractor_companies ADD COLUMN verification_status VARCHAR(20) NOT NULL DEFAULT 'pending';
-- pending: henüz belge yok / beklemede
-- documents_uploaded: belgeler yüklendi, inceleme bekliyor
-- verified: belgeler onaylandı, şirket aktif
-- rejected: belgeler reddedildi

ALTER TABLE contractor_companies ADD COLUMN verification_note TEXT;
ALTER TABLE contractor_companies ADD COLUMN verified_at TIMESTAMPTZ;
ALTER TABLE contractor_companies ADD COLUMN certificate_no VARCHAR(100);
ALTER TABLE contractor_companies ADD COLUMN certificate_expiry DATE;
