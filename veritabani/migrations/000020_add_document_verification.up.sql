-- ============================================================
-- MIGRATION 000020: Tapu / Ruhsat Belge Doğrulama Sistemi
-- ============================================================
-- Emlak ilanları için tapu, araç ilanları için ruhsat zorunluluğu

-- Belgeler (tapu, ruhsat, kimlik vb.)
CREATE TABLE listing_documents (
    id              BIGSERIAL PRIMARY KEY,
    domain          VARCHAR(50) NOT NULL, -- realestate, vehicle
    listing_id      BIGINT NOT NULL,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_type   VARCHAR(50) NOT NULL, -- tapu, ruhsat, kimlik, yetki_belgesi
    document_number VARCHAR(100), -- tapu no, plaka, tc kimlik no
    file_path       TEXT NOT NULL,
    file_name       VARCHAR(200),
    file_size       BIGINT,
    mime_type       VARCHAR(50),
    description     TEXT,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, verified, rejected
    rejection_reason TEXT,
    verified_by     UUID REFERENCES users(id),
    verified_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_listing_docs_listing ON listing_documents(listing_id, domain);
CREATE INDEX idx_listing_docs_user ON listing_documents(user_id);
CREATE INDEX idx_listing_docs_status ON listing_documents(status);

-- Doğrulama geçmişi
CREATE TABLE document_verifications (
    id              BIGSERIAL PRIMARY KEY,
    document_id     BIGINT NOT NULL REFERENCES listing_documents(id) ON DELETE CASCADE,
    verified_by     UUID NOT NULL REFERENCES users(id),
    action          VARCHAR(20) NOT NULL, -- verified, rejected
    reason          TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_doc_verifications_doc ON document_verifications(document_id);
